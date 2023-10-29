import os
import pygame
from . import BLACK, BG_SCROLL_SPEED, BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, FPS, FRAMES_SPEED, GO_TO_RECORDS_DELAY, HEIGHT, LIVES, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, SPACE_CADET, TITLE_FONT_SIZE, TITLE_MARGIN, WIDTH
from .entities import LivesCounter, Scoreboard
from tools.timers_and_countdowns import Countdown, ScrollBG
from .data.messages import Reader


class BestPlayers:
    def __init__(self, screen):
        self.screen = screen
        self.exit = False

    def mainLoop(self):
        print("Estoy en Best Scores")

        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.exit = True
            self.screen.fill(CORAL_PINK)
            pygame.display.flip()

        return self.exit
