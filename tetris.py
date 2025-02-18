import pygame
import random
import os

class Tetris:
    def __init__(self, screen, width = 10, height = 22, tile_pool = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']):
        self.screen = screen
        self.tetris_board = pygame.image.load(os.path.join('assets', 'sprites', 'BoardWithoutBorder.png'))
        self.width = width
        self.height = height
        self.board = []
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(Tile(j, i))
        self.base_tile_pool = tile_pool
        self.current_tile_pool = self.base_tile_pool
        self.next_tile_pool = self.base_tile_pool
        self.active_piece = None
    
    def draw_board(self):
        x = 200
        y = 50
        num = 0
        for row in reversed(self.board):
            if num < 2:
                num += 1
                continue
            for tile in row:
                tile.draw(self.screen, x, y)
                x += 39
            y += 40
            x = 200
    
    def start_game(self, grav, fast):
        running = True
        random.shuffle(self.current_tile_pool)
        random.shuffle(self.next_tile_pool)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.holding = None
        grav_tick = grav
        fast_drop_tick = fast
        fast_drop = False
        current_tick = 0
        shift_tick = 0
        self.spawn_block()
        defeat = False
        locking = False
        shifting_right = False
        shifting_left = False
        shift_start_tick = 0
        held = False
        while running:
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.draw_board()
            current_tick += 1
            if self.active_piece == None:
                clears = self.line_clear_check()
                if clears:
                    for line in clears:
                        self.clear_line(self.board[line])
                defeat = self.spawn_block()
                held = False
                locking = False
                #if defeat == True:
                #    break
            else:
                if locking:
                    self.active_piece.lock -= 1
                    current_tick = 0
                    if self.active_piece.lock == 0:
                        self.active_piece = None
                elif fast_drop:
                    if current_tick >= fast_drop_tick:
                        current_tick = 0
                        self.active_piece.drop(self.board)
                        locking = self.active_piece.lock_check(self.board)
                else:
                    if current_tick >= grav_tick:
                        current_tick = 0
                        self.active_piece.drop(self.board)
                        locking = self.active_piece.lock_check(self.board)
                
                if shifting_left:
                    shift_start_tick += 1
                    if shift_start_tick == 16:
                        self.active_piece.shift_left(self.board)
                        locking = self.active_piece.lock_check(self.board)
                    elif shift_start_tick > 16:
                        shift_tick += 1
                        if shift_tick == 6:
                            self.active_piece.shift_left(self.board)
                            locking = self.active_piece.lock_check(self.board)
                            shift_tick = 0

                elif shifting_right:
                    shift_start_tick += 1
                    if shift_start_tick == 16:
                        self.active_piece.shift_right(self.board)
                        locking = self.active_piece.lock_check(self.board)
                    elif shift_start_tick > 16:
                        shift_tick += 1
                        if shift_tick == 6:
                            self.active_piece.shift_right(self.board)
                            locking = self.active_piece.lock_check(self.board)
                            shift_tick = 0
            
            #keyUP hold


            events = pygame.event.get()
            for event in events:
                if event == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if self.active_piece:
                            if not locking:
                                self.active_piece.drop(self.board)
                                locking = self.active_piece.lock_check(self.board)
                                fast_drop = True
                    elif event.key == pygame.K_c:
                        if not held:
                            self.hold()
                            held = True
                    elif event.key == pygame.K_LEFT:
                        if self.active_piece:
                            print('attempt Shift')
                            self.active_piece.shift_left(self.board)
                            locking = self.active_piece.lock_check(self.board)
                            shifting_left = True
                    elif event.key == pygame.K_RIGHT:
                        if self.active_piece:
                            print('attempt Shift')
                            self.active_piece.shift_right(self.board)
                            locking = self.active_piece.lock_check(self.board)
                            shifting_right = True
                    elif event.key == pygame.K_SPACE:
                        locking = self.active_piece.lock_check(self.board)
                        while not locking:
                            self.active_piece.drop(self.board)
                            locking = self.active_piece.lock_check(self.board)
                        self.active_piece = None
                    elif event.key == pygame.K_UP:
                        if self.active_piece:
                            self.active_piece.rotate(self.board, 'R')
                            print('Attempted Rotate')
                            locking = self.active_piece.lock_check(self.board)
                    elif event.key == pygame.K_z:
                        if self.active_piece:
                            self.active_piece.rotate(self.board, 'L')
                            print('Attempted Rotate')
                            locking = self.active_piece.lock_check(self.board)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:    
                        fast_drop = False
                    elif event.key == pygame.K_LEFT:
                        if self.active_piece:
                            shifting_left = False
                            shift_tick = 0
                            shift_start_tick = 0
                    elif event.key == pygame.K_RIGHT:
                        if self.active_piece:
                            shifting_right = False
                            shift_tick = 0
                            shift_start_tick = 0

            pygame.display.flip()

    def hold(self):
        if self.holding:
            spawn = self.holding
            self.holding = self.active_piece.piece_type
            for tile in self.active_piece.occupied_tiles:
                tile.unoccupie()
            self.spawn_block(spawn)
        else:
            self.holding = self.active_piece.piece_type
            for tile in self.active_piece.occupied_tiles:
                tile.unoccupie()
            self.spawn_block()

    def clear_line(self, line):
        for tile in line:
            tile.state = ' '

    def line_clear_check(self):
        filled_lines = []
        for i in range(self.height):
            clear = True
            for tile in self.board[i]:
                if tile.state == ' ':
                    clear = False
                    break
            if clear:
                filled_lines.append(i)
        return filled_lines
                
    def generate_next_pool(self):
        self.next_tile_pool = self.base_tile_pool
        random.shuffle(self.next_tile_pool)

    def spawn_block(self, hold = False):
        if hold:
            self.active_piece = Block(hold)
        elif self.current_tile_pool:
            self.active_piece = Block(self.current_tile_pool[-1])
            self.current_tile_pool.pop(-1)
        else:
            self.current_tile_pool = self.next_tile_pool
            self.active_piece = Block(self.current_tile_pool[-1])
            self.current_tile_pool.pop(-1)
        defeat = self.active_piece.spawn_block(self.board)
        return defeat

    def __str__(self):
        return self.board
        
class Block:
    def __init__(self, piece_type):
        self.piece_type = piece_type
        self.lowest_y = 20
        self.occupied_tiles = None
        self.lock = 30
        self.left_side = 0
        self.right_side = 0
        self.center = [0, 0]
        self.ot = 'w'

    def rotate(self, board, type):
        if self.piece_type == 'I':
            if self.ot in {'w', 's'}:
                if board[self.center[1] + 2][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ':
                    for tile in self.occupied_tiles:
                        tile.unoccupie()
                    for i in range(-1, 3):
                        board[self.center[1] + i][self.center[0]].occupie(self)
                        self.ot = 'd'
            else:
                try:
                    if board[self.center[1]][self.center[0] - 2].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        for i in range(-2, 2):
                            board[self.center[1]][self.center[0] + i].occupie(self)
                            self.ot = 'w'
                except:
                    return False
        elif self.piece_type == 'J':
            if self.ot in 'w':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0] + 1].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[1]].occupie(self)
                        self.ot = 'd'
                else:
                    if board[self.center[1] - 1][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        self.ot = 'a'
            elif self.ot in 'd':
                if type == 'R':
                    try:
                        if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0] - 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0] + 1].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[1]].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
            elif self.ot in 's':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0] - 1].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        self.ot = 'a'
                else:
                    if board[self.center[1] - 1][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        self.ot = 'd'
            else:
                if type == 'R':
                    try:
                        if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] + 1][self.center[0] + 1].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[0]].occupie(self)
                            board[self.center[1] + 1][self.center[1]].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1] - 1][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] + 1].occupie(self)
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
        elif self.piece_type == 'L':
            if self.ot == 'w':
                if type == 'R':
                    if board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0] + 1].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0] + 1].occupie(self)
                        self.ot = 'd'
                else:
                    if board[self.center[1] + 1][self.center[0] - 1].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
            elif self.ot == 'd':
                if type == 'R':
                    try:
                        if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] + 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] + 1].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
            elif self.ot == 's':
                if type == 'R':
                    if board[self.center[1] + 1][self.center[0] - 1].state == ' ' and board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
                else:
                    if board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0] + 1].state == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0] + 1].occupie(self)
                        self.ot = 'd'
            else:
                if type == 'R':
                    try:
                        if board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] + 1].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1] - 1][self.center[0]].state == ' ' and board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1]][self.center[0] + 1].state == ' ':
                            for tile in self.occupied_tiles:
                                tile.unoccupie()
                            board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            board[self.center[1]][self.center[0] + 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
        elif self.piece_type == 'T':
            if self.ot == 'w':
                if type == "R":
                    if board[self.center[1] - 1][self.center[0]].state == ' ':
                        board[self.center[1]][self.center[0] - 1].unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'd'
                else:
                    if board[self.center[1] - 1][self.center[0]].state == ' ':
                        board[self.center[1]][self.center[0] + 1].unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
            elif self.ot == 'd':
                if type == "R":
                    try:
                        if board[self.center[1]][self.center[0] - 1].state == ' ':
                            board[self.center[1] + 1][self.center[0]].unoccupie()
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1]][self.center[0] - 1].state == ' ':
                            board[self.center[1] - 1][self.center[0]].unoccupie()
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
            elif self.ot == 's':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0]].state == ' ':
                        board[self.center[1]][self.center[0] + 1].unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
                else:
                    if board[self.center[1] - 1][self.center[0]].state == ' ':
                        board[self.center[1]][self.center[0] - 1].unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'd'
            else:
                if type == 'R':
                    try:
                        if board[self.center[1]][self.center[0] - 1].state == ' ':
                            board[self.center[1] - 1][self.center[0]].unoccupie()
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            self.ot = 'w'
                    except:
                        return False
                else:
                    try:
                        if board[self.center[1]][self.center[0] - 1].state == ' ':
                            board[self.center[1] + 1][self.center[0]].unoccupie()
                            board[self.center[1]][self.center[0] - 1].occupie(self)
                            self.ot = 's'
                    except:
                        return False
        elif self.piece_type == 'S':
            if self.ot in {'w', 's'}:
                try:
                    if board[self.center[1] + 1][self.center[0]].state == ' ' and board[self.center[1] - 1][self.center[0] + 1].state == ' ':
                        board[self.center[1] - 1][self.center[0] - 1].unoccupie()
                        board[self.center[1] - 1][self.center[0]].unoccupie()
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0] + 1].occupie(self)
                        self.ot = 'd'
                except:
                    return False
            else:
                try:
                    if board[self.center[1] - 1][self.center[0] - 1].state == ' ' and board[self.center[1] - 1][self.center[0]].state == ' ':
                        board[self.center[1] + 1][self.center[0]].unoccupie()
                        board[self.center[1] - 1][self.center[0] + 1].unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                except:
                    return False
        elif self.piece_type == 'Z':
            if self.ot == {'w', 's'}:
                try:
                    if board[self.center[1]][self.center[0] + 1].state == ' ' and board[self.center[1] + 1][self.center[0] + 1].state == ' ':
                        board[self.center[1]][self.center[0] - 1].unoccupie()
                        board[self.center[1] - 1][self.center[0] + 1].unoccupie()
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1] + 1][self.center[0] + 1].occupie(self)
                except:
                    return False
            else:
                try:
                    if board[self.center[1]][self.center[0] - 1].state == ' ' and board[self.center[1] - 1][self.center[0] + 1].state == ' ':
                        board[self.center[1]][self.center[0] - 1].occupie()
                        board[self.center[1] - 1][self.center[0] + 1].occupie()
                        board[self.center[1]][self.center[0] + 1].unoccupie(self)
                        board[self.center[1] + 1][self.center[0] + 1].unoccupie(self)
                except:
                    return False

    def shift_left(self, board):
        left = 100
        shift = True
        for tile in self.occupied_tiles:
            if tile.x < left:
                left = tile.x
        if left == 0:
            return False
        else:
            for tile in self.occupied_tiles:
                if board[tile.y][tile.x - 1] not in self.occupied_tiles and board[tile.y][tile.x - 1].state != ' ':
                    shift = False
            if shift:
                self.center[0] -= 1
                new_tiles = []
                for tile in self.occupied_tiles:
                    new_tiles.append(tile)
                for tile in self.occupied_tiles:
                    tile.unoccupie()
                for tile in new_tiles:
                    board[tile.y][tile.x - 1].occupie(self)
    
    def shift_right(self, board):
        right = -100
        shift = True
        for tile in self.occupied_tiles:
            if tile.x > right:
                right = tile.x
        if right == 9:
            return False
        else:
            for tile in self.occupied_tiles:
                if board[tile.y][tile.x + 1] not in self.occupied_tiles and board[tile.y][tile.x + 1].state != ' ':
                    shift = False
            if shift:
                self.center[0] += 1
                print(self.occupied_tiles)
                new_tiles = []
                for tile in self.occupied_tiles:
                    new_tiles.append(tile)
                for tile in self.occupied_tiles:
                    tile.unoccupie()
                for tile in new_tiles:
                    board[tile.y][tile.x + 1].occupie(self)

    def spawn_block(self, board):
        overlap = False
        self.occupied_tiles = []
        if self.piece_type == 'I':
            for i in range(3, 7):
                if board[19][i].occupie(self):
                    overlap = True
            self.center = [5, 19]
        elif self.piece_type == 'J':
            self.center = [4, 18]
            self.lowest_y = 19
            for i in range(3, 6):
                if board[18][i].occupie(self):
                    overlap = True
            if board[19][3].occupie(self):
                overlap = True
        elif self.piece_type == 'L':
            self.center = [4, 18]
            self.lowest_y = 19
            for i in range(3, 6):
                if board[18][i].occupie(self):
                    overlap = True
            if board[19][5].occupie(self):
                overlap = True
        elif self.piece_type == 'O':
            self.center = [4, 18]
            self.lowest_y = 19
            for i in range(4, 6):
                if board[18][i].occupie(self):
                    overlap = True
            for i in range(4, 6):
                if board[19][i].occupie(self):
                    overlap = True
        elif self.piece_type == 'S':
            self.center = [4, 19]
            self.lowest_y = 19
            for i in range(3, 5):
                if board[18][i].occupie(self):
                    overlap = True
            for i in range(4, 6):
                if board[19][i].occupie(self):
                    overlap = True
        elif self.piece_type == 'T':
            self.center = [4, 18]
            self.lowest_y = 19
            for i in range(3, 6):
                if board[18][i].occupie(self):
                    overlap = True
            if board[19][4].occupie(self):
                overlap = True
        elif self.piece_type == 'Z':
            self.center = [4, 19]
            self.lowest_y = 19
            for i in range(3, 5):
                if board[19][i].occupie(self):
                    overlap = True
            for i in range(4, 6):
                if board[18][i].occupie(self):
                    overlap = True
        return overlap
    
    def drop(self, board):
        current_tiles = []
        for tile in self.occupied_tiles:
            current_tiles.append(tile)
        for tile in self.occupied_tiles:
            tile.unoccupie()
        self.occupied_tiles = []
        for tile in current_tiles:
            x, y = tile.x, tile.y
            if y - 1 < self.lowest_y:
                self.lowest_y = y -1
            board[y - 1][x].occupie(self)
        self.center[1] -= 1

    def lock_check(self, board):
        if self.lowest_y == 0:
            return True
        else:
            for tile in self.occupied_tiles:
                if board[tile.y - 1][tile.x].state != ' ':
                    if board[tile.y - 1][tile.x] not in self.occupied_tiles:
                        return True
            return False
            
class Tile:
    def __init__(self, x, y, state = ' '):
        self.state = state
        self.block_in_tile = None
        self.x = x
        self.y = y
        self.red = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileRed.png'))
        self.blue = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileBlue.png'))
        self.cyan = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileCyan.png'))
        self.green = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileGreen.png'))
        self.orange = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileOrange.png'))
        self.purple = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTilePurple.png'))
        self.yellow = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTileYellow.png'))
        self.empty = pygame.image.load(os.path.join('assets', 'sprites', 'SingleTile.png'))
        self.colours = {
            ' ': self.empty,
            'O': self.yellow, 
            'I': self.cyan,
            'T': self.purple, 
            'L': self.orange,
            'J': self.blue,
            'Z': self.red,
            'S': self.green
        }
    
    def occupie(self, block: Block):
        self.block_in_tile = block
        block.occupied_tiles.append(self)
        if self.state != ' ':
            self.state = block.piece_type
            return False
        else:
            self.state = block.piece_type
            return True

    def unoccupie(self):
        self.state = ' '
        self.block_in_tile = None

    def isEmpty(self):
        return self.state == ' '

    def draw(self, screen, x ,y):
        screen.blit(self.colours[self.state], (x, y))

    def __str__(self):
        return self.state
    
    def __repr__(self) -> str:
        return self.__str__()


pygame.init()
screen = pygame.display.set_mode((1600, 900))
game = Tetris(screen)
game.start_game(64, 1)