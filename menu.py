import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# controls of the Menu acts(cursor, input, etc)
class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = (self.game.d_width / 2), (self.game.d_height / 2)
        self.run_display = True
        self.cursor_box = pygame.Rect(0, 0, 50, 50)
        self.offset = -100


    def draw_cursor(self):
        self.game.screen_text('>', 80, self.cursor_box.x, self.cursor_box.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_events()

class MainPage(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "A* Algorithm"
        self.startx, self.starty = self.mid_w - 200, self.mid_h
        self.optionx, self.optiony = self.mid_w - 200, self.mid_h + 100
        self.creditx, self.credity = self.mid_w - 200, self.mid_h + 200
        self.cursor_box.midtop = (self.startx + self.offset, self.starty)

    def main_display(self):
        self.run_display = True
        while self.run_display:
            self.game.event_check()
            self.check_input()
            self.game.display.fill(BLACK)
            self.game.screen_text('Sorting Algorithm Visual', 65, self.game.d_width / 2, self.game.d_height / 2 - 200)
            self.game.screen_text('Choose algorithm to sort with: ', 25, (self.game.d_width /2) - 140, self.game.d_height / 2 - 100)
            self.game.screen_text("A* Algorithm", 40, self.startx + 35, self.starty)
            self.game.screen_text("Breadth-First Search", 40, self.optionx + 115, self.optiony)
            self.game.screen_text("Exit", 40, self.creditx - 42, self.credity)
            self.draw_cursor()
            self.blit_screen()



    def move_cursor(self):
        if self.game.DOWN:
            if self.state == 'A* Algorithm':
                self.cursor_box.midtop = (self.optionx + self.offset, self.optiony)
                self.state = 'BFS'
            elif self.state == 'BFS':
                self.cursor_box.midtop = (self.creditx + self.offset, self.credity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_box.midtop = (self.startx + self.offset, self.starty)
                self.state = 'A* Algorithm'
        elif self.game.UP:
            if self.state == 'A* Algorithm':
                self.cursor_box.midtop = (self.creditx + self.offset, self.credity)
                self.state = 'Exit'
            elif self.state == 'BFS':
                self.cursor_box.midtop = (self.startx + self.offset, self.starty)
                self.state = 'A* Algorithm'
            elif self.state == 'Exit':
                self.cursor_box.midtop = (self.optionx + self.offset, self.optiony)
                self.state = 'BFS'

    def check_input(self):
        self.move_cursor()
        if self.game.START:
            if self.state == 'A* Algorithm':
                self.game.astar = True
                self.game.run_status, self.game.play_status = False, False
                self.game.menu.run_display = False
            elif self.state == 'BFS':
                self.game.bfs = True
                self.game.run_status, self.game.play_status = False, False
                self.game.menu.run_display = False
            elif self.state == 'Exit':
                self.game.run_status, self.game.play_status = False, False
                self.game.menu.run_display = False
            self.run_display = False

