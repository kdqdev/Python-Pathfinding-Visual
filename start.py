from mainmenu import MenuController
from visualizer import *

g = MenuController()
a = Algorithm()
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

while g.run_status:
    if not g.astar or g.bfs:
        g.menu.main_display()
        g.loop()
    if g.astar or g.bfs:
        if g.astar:
            alg = True
        else:
            alg = False
        found_path = a.main(WIN, WIDTH, alg)
        g.run_status, g.play_status = True, True
        g.menu.run_display = True
        g.astar = found_path
        g.astar = False
        g.bfs = False
        g.run_status, g.play_status = True, True