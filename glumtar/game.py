import os
import sys
import pygame
from . import COLUMBIA_BLUE, FONT, FONT_SIZE, FPS, HEIGHT, LIVES, WIDTH, SPACE_CADET
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

        self.kill_game = False
        self.front_page = FrontPage(self.screen)
        self.score_board = Scoreboard(self.screen, COLUMBIA_BLUE)
        self.lives_counter = LivesCounter(COLUMBIA_BLUE, LIVES)
        self.records_page = BestPlayers(
            self.screen, self.score_board)
        self.available_play_levels = 3
        self.play_scenes = []
        self.play_pointer = 0
        self.activate_play_pointer = True
        self.set_a_match = True
        self.music_route = os.path.join(
            'glumtar', 'resources', 'sounds', 'Master _Computer_Games.mp3')

    def mainLoop(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_route)
        pygame.mixer.music.play(loops=-1)
        # pygame.mixer.Sound(boom_route).play()
        exit = False
        while not exit:
            self.clock.tick(FPS)
            self.screen.fill(SPACE_CADET)

            if self.set_a_match:
                self.set_up_play()

            if not self.front_page.exit:
                self.front_page.mainLoop()
                self.kill_game = self.front_page.kill_game
            else:
                if self.play_pointer in range(len(self.play_scenes)) and self.activate_play_pointer:
                    scene = self.play_scenes[self.play_pointer]
                    if not scene.exit:
                        if not scene.execute_game_over:
                            scene.mainLoop()
                            self.kill_game = scene.kill_game
                            if scene.exit:
                                self.play_pointer += 1
                        else:
                            self.activate_play_pointer = False
                            scene.exit = True
                            self.records_page.mainLoop()
                            self.kill_game = self.records_page.kill_game
                    if scene.go_to_frontpage:
                        self.reset_game()
                else:
                    self.activate_play_pointer = False
                    self.records_page.mainLoop()
                    self.kill_game = self.records_page.kill_game
            if self.records_page.exit:
                self.reset_game()
                self.records_page.exit = False
            pygame.display.flip()

            if self.kill_game:
                exit = True
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
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.front_page.exit = False
        self.score_board = Scoreboard(self.screen, COLUMBIA_BLUE)
        self.lives_counter = LivesCounter(COLUMBIA_BLUE, LIVES)
        self.records_page = BestPlayers(
            self.screen, self.score_board)
        self.play_pointer = 0
        self.activate_play_pointer = True
        self.set_a_match = True

        return self.front_page.exit, self.score_board, self.lives_counter, self.play_pointer, self.activate_play_pointer, self.set_a_match


if __name__ == '__main__':
    the_game = Glumtar()
    the_game.mainLoop()
