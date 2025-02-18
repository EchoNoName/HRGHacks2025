import pygame
import random

class Tetris:
    def __init__(self, screen, width = 10, height = 22, tile_pool = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']):
        self.screen = screen
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
    
    def start_game(self, grav, fast):
        running = True
        random.shuffle(self.current_tile_pool)
        random.shuffle(self.next_tile_pool)
        pygame.init()
        self.clock = pygame.time.Clock()
        holding = None
        grav_tick = grav
        fast_drop_tick = fast
        fast_drop = False
        current_tick = 0
        self.spawn_block()
        defeat = False
        locking = False
        while running:
            self.clock.tick(60)
            current_tick += 1
            if self.active_piece == None:
                clears = self.line_clear_check()
                if clears:
                    for line in clears:
                        self.clear_line(self.board[line])
                defeat = self.spawn_block()
                if defeat == True:
                    break
            else:
                if locking:
                    self.active_piece.lock -= 1
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
                        

    def clear_line(self, line):
        for tile in line:
            tile.state = ' '

    def line_clear_check(self):
        filled_lines = []
        for i in range(self.height):
            clear = True
            for tile in self.baord[i]:
                if tile.state == ' ':
                    clear = False
                    break
            if clear:
                filled_lines.append(i)
        return filled_lines
                
    def generate_next_pool(self):
        self.next_tile_pool = self.base_tile_pool
        random.shuffle(self.next_tile_pool)

    def spawn_block(self):
        if self.current_tile_pool:
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
        self.center = [0, 0]
        self.ot = 'w'

    def rotate(self, board, type):
        if self.piece_type == 'I':
            if self.ot in {'w', 's'}:
                if board[self.center[1] + 2][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ':
                    for tile in self.occupied_tiles:
                        tile.unoccupie()
                    for i in range(-1, 3):
                        board[self.center[1] + i][self.center[0]].occupie(self)
                        self.ot = 'd'
            else:
                try:
                    if board[self.center[1]][self.center[0] - 2] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ':
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
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0] + 1] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[1]].occupie(self)
                        self.ot = 'd'
                else:
                    if board[self.center[1] - 1][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        self.ot = 'a'
            elif self.ot in 'd':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0] - 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        self.ot = 's'
                else:
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0] + 1] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[1]].occupie(self)
                        self.ot = 'w'
            elif self.ot in 's':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0] - 1] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        self.ot = 'a'
                else:
                    if board[self.center[1] - 1][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        self.ot = 'd'
            else:
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] + 1][self.center[0] + 1] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] + 1][self.center[1]].occupie(self)
                        self.ot = 'w'
                else:
                    if board[self.center[1] - 1][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        self.ot = 's'
        elif self.piece_type == 'L':
            if self.ot == 'w':
                if type == 'R':
                    if board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0] + 1].occupie(self)
                        self.ot = 'd'
                else:
                    if board[self.center[1] + 1][self.center[0] - 1] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
            elif self.ot == 'd':
                if type == 'R':
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        self.ot = 's'
                else:
                    if board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        self.ot = 'w'
            elif self.ot == 's':
                if type == 'R':
                    if board[self.center[1] + 1][self.center[0] - 1] == ' ' and board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        self.ot = 'a'
                else:
                    if board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1] - 1][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0]].occupie(self)
                        board[self.center[1] - 1][self.center[0] + 1].occupie(self)
                        self.ot = 'd'
            else:
                if type == 'R':
                    if board[self.center[1] + 1][self.center[0]] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] + 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        self.ot = 'w'
                else:
                    if board[self.center[1] - 1][self.center[0]] == ' ' and board[self.center[1]][self.center[0] - 1] == ' ' and board[self.center[1]][self.center[0] + 1] == ' ':
                        for tile in self.occupied_tiles:
                            tile.unoccupie()
                        board[self.center[1] - 1][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] - 1].occupie(self)
                        board[self.center[1]][self.center[0] + 1].occupie(self)
                        self.ot = 's'
        elif 


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
        current_tiles = self.occupied_tiles
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
        if self.lowest_y == 1:
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
    
    def occupie(self, block: Block):
        self.block_in_tile = block
        block.occupied_tiles.append(self)
        if self.state != ' ':
            self.state = block.piece_type
            return True
        else:
            self.state = block.piece_type
            return False

    def unoccupie(self):
        self.state = ' '

    def isEmpty(self):
        return self.state == ' '

    def draw(self):
        if self.state != ' ':
            return True

    def __str__(self):
        return self.state

    def __repr__(self):
        return self.__str__()
    
game = Tetris()
game.start_game(64, 1)