import pygame
from . import FPS, HEIGHT, WIDTH
from .playlevel import PlayLevel
from .entities import LivesCounter, Scoreboard, Ship


class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.player = Ship(self.screen)
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()

        self.info_scenes = []
        self.play_scenes = [PlayLevel(self.screen, self.player,
                                      self.scoreboard, self.lives_counter)]
        # for info in range(2):

        """ self.scenes = [FrontPage(self.screen),
                       PlayLevel(self.screen, self.player,
                                 self.scoreboard, self.lives_counter),
                       ResolveLevel(self.screen, self.player,
                                    self.scoreboard, self.lives_counter),
                       MatchLevel2(self.screen),
                       ResolveLevel2(self.screen),
                       BestPlayers(self.screen),
                       ] """

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            # bucle principal (o main loop)

            # Bloque 1: captura de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    exit = True
                    break

            # Bloque 2: renderizar nuestros objetos (aunque no se enseñan todavía)

            # Bloque 3: mostrar los cambios en la pantalla
            pygame.display.flip()

        pygame.quit()

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
