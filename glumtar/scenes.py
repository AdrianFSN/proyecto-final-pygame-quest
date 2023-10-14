import pygame

from . import BLACK, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, FPS, HEIGHT, ROBIN_EGG_BLUE, SPACE_CADET, WIDTH
from .entities import Meteorite, Ship


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
        self.player = Ship()
        self.meteorite = Meteorite(20)

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
            self.screen.fill(ROBIN_EGG_BLUE)

            self.player.update()
            self.screen.blit(self.player.img_new_size, self.player.rect)
            self.meteorite.update()
            self.screen.blit(self.meteorite.img_new_size, self.meteorite.rect)

            pygame.display.flip()

        return False


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
