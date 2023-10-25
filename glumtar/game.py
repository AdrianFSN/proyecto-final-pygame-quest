import pygame
from . import HEIGHT, WIDTH
from .scenes import FrontPage, MatchLevel1, MatchLevel2, ResolveLevel2, BestPlayers
from .entities import LivesCounter, Scoreboard, Ship


class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.player = Ship()
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()

        self.scenes = [FrontPage(self.screen),
                       MatchLevel1(self.screen, self.player,
                                   self.scoreboard, self.lives_counter),

                       MatchLevel2(self.screen),
                       ResolveLevel2(self.screen),
                       BestPlayers(self.screen),
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
