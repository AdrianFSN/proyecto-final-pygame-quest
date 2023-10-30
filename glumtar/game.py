import os
import pygame
from . import FONT, FONT_SIZE, FPS, HEIGHT, LIVES, WIDTH, SPACE_CADET
from . playlevel import PlayLevel
from . resolvelevel import ResolveLevel
from . frontpage import FrontPage
from . bestscores import BestPlayers
from . entities import LivesCounter, Scoreboard, Ship


class Glumtar:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = FONT
        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()

        self.front_page = FrontPage(self.screen)
        self.records_page = BestPlayers(
            self.screen)
        self.score_board = Scoreboard(self.screen)
        self.lives_counter = LivesCounter(LIVES)
        self.available_play_levels = 3
        self.play_scenes = []
        self.play_pointer = 0
        self.activate_play_pointer = True

        self.set_a_match = True

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            self.screen.fill(SPACE_CADET)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    self.activate_play_pointer = False
                    self.set_a_match = False
                    exit = True
                    break
            if self.set_a_match:
                self.set_up_play()

            if not self.front_page.exit:
                self.front_page.mainLoop()
            else:
                if self.play_pointer in range(len(self.play_scenes)) and self.activate_play_pointer:
                    scene = self.play_scenes[self.play_pointer]
                    if not scene.exit:
                        if not scene.execute_game_over:
                            scene.mainLoop()
                            if scene.exit:
                                self.play_pointer += 1
                        else:
                            self.activate_play_pointer = False
                            scene.exit = True
                            self.records_page.mainLoop()
                else:
                    self.activate_play_pointer = False
                    self.records_page.mainLoop()
            if self.records_page.exit:
                self.reset_game()
                self.records_page.exit = False

            pygame.display.flip()

        pygame.quit()

    def set_up_play(self):
        self.play_scenes = []
        for scene in range(1, self.available_play_levels):
            scenario = PlayLevel(self.screen,
                                 self.score_board, self.lives_counter, scene)
            resolution = ResolveLevel(scenario.screen, scenario.player,
                                      scenario.scoreboard, scenario.lives_counter, scenario.level)
            self.play_scenes.append(scenario)
            self.play_scenes.append(resolution)
            self.set_a_match = False

        return self.set_a_match, self.play_scenes

    def reset_game(self):
        pygame.font.init()
        """ self.font = FONT
        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font) """
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.front_page.exit = False
        self.score_board = Scoreboard(self.screen)
        self.lives_counter = LivesCounter(LIVES)
        self.play_pointer = 0
        self.activate_play_pointer = True
        self.set_a_match = True

        return self.front_page.exit, self.score_board, self.lives_counter, self.play_pointer, self.activate_play_pointer, self.set_a_match


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    the_game = Glumtar()
    the_game.mainLoop()
