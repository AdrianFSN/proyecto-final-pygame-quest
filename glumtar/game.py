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
        self.records_page = BestPlayers(self.screen)
        self.available_play_levels = 3
        self.play_scenes = []
        self.play = None
        self.resolve = None
        self.level = 1

        self.set_up_elements = True

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    exit = True
                    break
            if self.set_up_elements:
                scoreboard = Scoreboard(self.screen)
                player = Ship(self.screen)
                lives_counter = LivesCounter()
                front_page = FrontPage(self.screen)
                play_level1 = PlayLevel(
                    self.screen, player, scoreboard, lives_counter, 1)
                resolve_level1 = ResolveLevel(
                    self.screen, play_level1.player, play_level1.scoreboard, play_level1.lives_counter, 1)
                play_level2 = PlayLevel(
                    self.screen, player, scoreboard, lives_counter, 1)
                resolve_level2 = ResolveLevel(
                    self.screen, play_level2.player, play_level2.scoreboard, play_level2.lives_counter, 2)
                scenes_list = [front_page, play_level1, resolve_level1,
                               play_level2, resolve_level2, self.records_page]
                self.set_up_elements = False

            for stage in scenes_list:
                if not front_page.exit:
                    front_page.mainLoop()
                    if front_page.exit:
                        if play_level1.execute_game_over:
                            self.records_page.mainLoop()
                            if self.records_page.exit:
                                self.restart_game()
                        else:
                            play_level1.mainLoop()
                            if play_level1.exit:
                                resolve_level1.mainLoop()
                                if resolve_level1.exit:
                                    if play_level2.execute_game_over:
                                        self.records_page.mainLoop()
                                        if self.records_page.exit:
                                            self.restart_game()
                                        else:
                                            play_level2.mainLoop()
                                            if play_level2.exit:
                                                resolve_level2.mainLoop()
                                                if resolve_level1.exit:
                                                    self.records_page.mainLoop()
                                                    if self.records_page.exit:
                                                        self.restart_game()

        pygame.quit()

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
