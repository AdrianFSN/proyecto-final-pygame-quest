import pygame
from . import FPS, HEIGHT, LIVES, WIDTH
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
        self.front_page = FrontPage(self.screen)
        self.records_page = BestPlayers(self.screen)
        self.score_board = Scoreboard(self.screen)
        self.lives_counter = LivesCounter()
        self.available_play_levels = 3
        # self.play_scenes = []

        self.set_a_match = True

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    exit = True
                    break
            if self.set_a_match:
                self.set_up_play()

        pygame.quit()

    def set_up_play(self):
        play_scenes = []
        player = Ship(self.screen)
        for scene in range(1, self.available_play_levels):
            scenario = PlayLevel(self.screen, player,
                                 self.score_board, self.lives_counter, scene)
            resolution = ResolveLevel(scenario.screen, scenario.player,
                                      scenario.scoreboard, scenario.lives_counter, scenario.level)
            play_scenes.append(scenario)
            play_scenes.append(resolution)
            self.set_a_match = False
        """ print(f'Esta es la lista de escenarios disponible {play_scenes}')
        print(
            f'El escenario 1, {play_scenes[0]} es de nivel {play_scenes[0].level}.')
        print(
            f'El escenario 2, {play_scenes[1]} es de nivel {play_scenes[1].level}.')
        print(
            f'El escenario 3, {play_scenes[2]} es de nivel {play_scenes[2].level}.')
        print(
            f'El escenario 4, {play_scenes[3]} es de nivel {play_scenes[3].level}.')
        return self.set_a_match """

    def restart_game(self):
        # Preguntar si quiere continuar
        # Si quiere, setup elements pasa a True
        # Si no quiere, QUIT
        self.set_up_elements = True
        return self.set_up_elements


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    the_game = Glumtar()
    the_game.mainLoop()
