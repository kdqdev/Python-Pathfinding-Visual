import pygame
from menu import *


game_width = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

# controls whether menu should be displayed
class MenuController:
    def __init__(self):
        pygame.init()
        self.UP, self.DOWN, self.START, self.BACK = False, False, False, False # keys that are pressed
        self.run_status, self.play_status = True, True
        self.d_width, self.d_height = game_width, game_width
        self.display = pygame.Surface((self.d_width, self.d_height))
        self.window = pygame.display.set_mode((self.d_width, self.d_height))
        self.astar = False
        self.bfs = False
        self.main_page = MainPage(self)
        self.menu = self.main_page


    def loop(self):
        while self.play_status:
            self.event_check()
            if self.START:
                self.play_status = False
            self.display.fill(BLACK)
            self.screen_text("End", 20, (self.d_width/2), (self.d_height/2))
            # puts images on screen instead of pygame inbuilt function like drawcircle., block image transfer.
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_events


    # checks if any input was receive from user
    def event_check(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.run_status, self.play_status = False, False
                self.menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK = True
                if event.key == pygame.K_DOWN:
                    self.DOWN = True
                if event.key == pygame.K_UP:
                    self.UP = True

    def reset_events(self):
        self.UP, self.DOWN, self.START, self.BACK = False, False, False, False

    def screen_text(self, text, size, x, y):
        if size == 25:
            font = pygame.font.Font("atarianfont.ttf", size)
            text_render = font.render(text, True, ORANGE)
            text_pos = text_render.get_rect()
            text_pos.center = (x, y)
            self.display.blit(text_render, text_pos)
        else:
            font = pygame.font.Font("arcadefont.ttf", size)
            text_render = font.render(text, True, WHITE)
            text_pos = text_render.get_rect()
            text_pos.center = (x, y)
            self.display.blit(text_render, text_pos)

# new commit test 3