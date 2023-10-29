import pygame
from . import FPS, HEIGHT, WIDTH
from . playlevel import PlayLevel
from . resolvelevel import ResolveLevel
from . frontpage import FrontPage
from . bestscores import BestPlayers
from . entities import LivesCounter, Scoreboard, Ship


class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.player = Ship(self.screen)
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()
        self.front_page = FrontPage(self.screen)
        self.records_page = BestPlayers(self.screen)
        self.info_scenes = [self.front_page, self.records_page]
        self.available_play_levels = 3
        self.play = None
        self.resolve = None
        self.level = 1
        self.play_scenes = []
        for levels in range(self.level, self.available_play_levels):
            # print(f'Levels es {levels}')
            self.play = PlayLevel(
                self.screen, self.player, self.scoreboard, self.lives_counter, levels)
            self.resolve = ResolveLevel(
                self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
            self.play_scenes.append((self.play, self.resolve))
        print(f'Así ha quedado self play scenes {self.play_scenes}')
        print(
            f'este es el nivel de la primera partida {self.play_scenes[0][0].level} y el de su resolve {self.play_scenes[0][1].level}')
        print(
            f'este es el nivel de la segunda partida {self.play_scenes[1][0].level} y el de su resolve {self.play_scenes[1][1].level}')

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


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Glumtar()
    juego.play()
