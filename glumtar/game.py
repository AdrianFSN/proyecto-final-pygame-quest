import pygame
from . import HEIGHT, WIDTH
from .scenes import FrontPage, MatchLevel1, MatchLevel2, ResolveLevel1, ResolveLevel2, BestPlayers


class Glumtar:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")

        self.scenes = [FrontPage(self.pantalla),
                       MatchLevel1(self.pantalla),
                       ResolveLevel1(self.pantalla),
                       MatchLevel2(self.pantalla),
                       ResolveLevel2(self.pantalla),
                       BestPlayers(self.pantalla),
                       ]

    def play(self):
        for scene in self.scenes:
            quit_game = scene.mainLoop()
            if quit_game:
                print("Alguien ha decidido salir de la aplicación por la X")
                break

        pygame.quit()


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Glumtar()
    juego.play()
