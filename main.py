import pygame
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        self.main_menu_sprite = pygame.image.load(os.path.join("assets", "sprites", "Start Menu.png"))
        self.main_menu_sprite = pygame.transform.scale(self.main_menu_sprite, (1600, 900))
        self.start_game_rect = pygame.Rect(987, 134, 390, 135)
    
    def main_menu(self):
        running = True
        start_game = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.main_menu_sprite, (0, 0))
            
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            for event in events:
                if event == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (event.mod & pygame.KMOD_ALT):
                    running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.start_game_rect.collidepoint(mouse_pos):
                        running = False
                        start_game = True
            
            pygame.display.flip()
        
        if start_game:
            self.tetris_game

    def tetris_game(self):
        running = True
        
game = Game()
game.main_menu()