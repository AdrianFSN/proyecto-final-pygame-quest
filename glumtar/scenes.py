import os

import pygame

from . import BLACK, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, DEFAULT_TIMER, FPS, HEIGHT, MARGIN, ROBIN_EGG_BLUE, SPACE_CADET, TIME_UNIT, WIDTH
from .entities import Meteorite, Ship, Scoreboard
from tools.timers_and_countdowns import Timer


class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.reloj = pygame.time.Clock()

    def mainLoop(self):
        print("Empty method for Scene's main loop")


class FrontPage(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(SPACE_CADET)
            pygame.display.flip()

        return False


class MatchLevel1(Scene):

    def __init__(self, screen):
        super().__init__(screen)
        bg_route = os.path.join('glumtar', 'resources',
                                'images', 'BG_level1.jpg')
        self.background = pygame.image.load(bg_route)
        self.background_posX = 0
        self.background_posY = 0

        self.scoreboard = Scoreboard()

        self.player = Ship()
        self.timer = Timer(DEFAULT_TIMER)
        self.set_timer = self.timer.set_timer()
        self.random_meteorite = None
        self.generated_meteorites = pygame.sprite.Group()

    def mainLoop(self):
        super().mainLoop()
        exit = False
        stop_timer = False
        while not exit:
            self.reloj.tick(FPS)
            if not stop_timer:
                self.set_timer -= 1
                if self.set_timer == 0:
                    stop_timer = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(ROBIN_EGG_BLUE)
            self.paint_background(self.background_posX,
                                  self.background_posY, self.set_timer)

            self.scoreboard.show_scoreboard(self.screen)

            self.player.update()
            self.screen.blit(self.player.img_new_size, self.player.rect)

            self.generate_meteorites()
            self.generated_meteorites.draw(self.screen)
            self.generated_meteorites.update()
            if len(self.generated_meteorites) > 0:
                for meteorite in self.generated_meteorites:
                    if meteorite.rect.right < 0:
                        self.scoreboard.increase_score(meteorite.points)
                        self.generated_meteorites.remove(meteorite)

            pygame.display.flip()

        return False

    def generate_meteorites(self):
        if self.set_timer > 0:
            if self.set_timer % TIME_UNIT == 0:
                self.random_meteorite = Meteorite()
                self.generated_meteorites.add(
                    self.random_meteorite)

    def paint_background(self, posX, posY, timer):
        posX = posX
        posY = posY
        timer = timer
        self.screen.blit(self.background, (posX, posY))
        if self.set_timer != 0:
            self.background_posX -= 1


class ResolveLevel1(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            self.reloj.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(CORAL_PINK)
            pygame.display.flip()

        return False


class MatchLevel2(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            self.reloj.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(CORNELL_RED)
            pygame.display.flip()

        return False


class ResolveLevel2(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            self.reloj.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(COLUMBIA_BLUE)
            pygame.display.flip()

        return False


class BestPlayers(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(BLACK)
            pygame.display.flip()

        return False
