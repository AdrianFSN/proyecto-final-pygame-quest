import pygame
from . import FPS, GO_TO_RECORDS_DELAY, HEIGHT, WIDTH
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

        self.request_go_to_records = pygame.USEREVENT + 3
        pygame.time.set_timer(self.request_go_to_records, GO_TO_RECORDS_DELAY)

        self.play_scenes = []
        for levels in range(self.level, self.available_play_levels):
            # print(f'Levels es {levels}')
            self.play = PlayLevel(
                self.screen, self.player, self.scoreboard, self.lives_counter, levels)
            self.resolve = ResolveLevel(
                self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
            self.play_scenes.append([self.play, self.resolve])

        self.info_switches_list = []
        self.info_scene_switch = None
        for switch in range(len(self.info_scenes)):
            self.info_scene_switch = switch
            self.info_switches_list.append([self.info_scene_switch, False])

        self.play_switches_list = []
        self.play_scene_switch = None
        for switch in range(len(self.play_scenes)):
            self.play_scene_switch = switch
            self.play_switches_list.append([self.play_scene_switch, False])
        print(f'Esta es la lista de switches {self.play_switches_list}')

        self.info_switches_list[0][1] = True
        # print(f'Esta es la lista de switches {self.info_switches_list}')
        self.game_over = False

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            # bucle principal (o main loop)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    exit = True
                    break
                """ if event.type == self.request_go_to_records:
                    if self.game_over:
                        self.records_page.mainLoop()
                        print(f'He intentado ir a front page') """
            if self.info_switches_list[0]:
                self.front_page.mainLoop()
                print(f'Así ha quedado self play scenes {self.play_scenes}')

                if self.front_page.exit:
                    if not self.play_switches_list[0][1]:
                        self.play_scenes[0][0].mainLoop()
                        if not self.play_scenes[0][0].execute_game_over:
                            if self.play_scenes[0][0].exit:
                                self.play_scenes[0][1].mainLoop()
                        else:
                            print(
                                f'El execute G Over está en {self.play_scenes[0][0].execute_game_over}')
                            self.game_over = True
                            self.play_switches_list[0][1] = True
                            print(f'Game over está en {self.game_over}')
                            self.records_page.mainLoop()
                            print(f'He intentado ir a front page')

            # Bloque 1: captura de eventos

            # Bloque 2: renderizar nuestros objetos (aunque no se enseñan todavía)

            # Bloque 3: mostrar los cambios en la pantalla
            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Glumtar()
    juego.play()
