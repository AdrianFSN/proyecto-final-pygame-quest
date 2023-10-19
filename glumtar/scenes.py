import os

import pygame

from . import BLACK, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, DEFAULT_TIMER, FPS, HEIGHT, LIVES, MARGIN, ROBIN_EGG_BLUE, SPACE_CADET, TIME_UNIT, WIDTH
from .entities import LivesCounter, Meteorite, Ship, Scoreboard
from tools.timers_and_countdowns import CountDown, Timer


class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

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
        self.lives_counter = LivesCounter()

        self.timer = Timer(DEFAULT_TIMER)
        self.set_timer = None

        self.countdown = CountDown(self.clock, self.timer)

        self.player = None
        self.ship = pygame.sprite.GroupSingle()

        self.random_meteorite = None
        self.generated_meteorites = pygame.sprite.Group()

        self.countdown_stop = None

    def mainLoop(self):
        super().mainLoop()
        exit = False
        stop_timer = False
        self.countdown_stop = False
        self.lives_counter.end_game = False
        trigger_ship = False
        while not exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
            self.screen.fill(ROBIN_EGG_BLUE)

            self.paint_background(self.background_posX,
                                  self.background_posY, self.set_timer)
            self.initialize_countdown()
            if not stop_timer:
                self.set_timer -= 1
                if self.set_timer == 0:
                    stop_timer = True

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)

            if self.lives_counter.lives_value in range(1, LIVES+1):
                if not trigger_ship:
                    self.generate_ship()
                    self.ship.update()
                    trigger_ship = False

            self.generate_meteorites()
            self.generated_meteorites.draw(self.screen)
            self.generated_meteorites.update()
            if len(self.generated_meteorites) > 0:
                for meteorite in self.generated_meteorites:
                    if meteorite.rect.right < 0:
                        self.scoreboard.increase_score(meteorite.points)
                        self.generated_meteorites.remove(meteorite)
                        # print("He quitado un meteorito")

            # self.collision = False
            self.killed_ship = False
            self.check_collision()
            self.lives_counter.reduce_lives(self.killed_ship)

            pygame.display.flip()

        return False

    def initialize_countdown(self):
        if not self.countdown_stop:
            self.set_timer = 0
            self.countdown.set_count_down(self.screen)
            if self.countdown.init_value < 0:
                self.countdown_stop = True
                self.set_timer = self.timer.set_timer()

    def generate_ship(self):
        self.player = Ship()
        self.ship.add(self.player)
        self.screen.blit(self.player.image, self.player.rect)

    def generate_meteorites(self):
        if self.set_timer > 0:
            if self.set_timer % TIME_UNIT == 0:
                self.random_meteorite = Meteorite()
                self.generated_meteorites.add(
                    self.random_meteorite)
                self.screen.blit(self.random_meteorite.image,
                                 self.random_meteorite.rect)

    def paint_background(self, posX, posY, timer):
        posX = posX
        posY = posY
        timer = timer
        self.screen.blit(self.background, (posX, posY))
        if self.set_timer != 0:
            self.background_posX -= 1

    def kill_ship(self):
        pygame.sprite.Sprite.kill(self.player)
        self.ship.remove(self.player)
        self.killed_ship = True
        print("Debería haber borrado la nave")
        # pygame.mixer.Sound("algo").play()

    def kill_meteorite(self):
        pygame.sprite.Sprite.kill(self.random_meteorite)
        self.generated_meteorites.remove(self.random_meteorite)
        print("Debería haber borrado el meteorito")

    def check_collision(self):
        # detected_collision = []
        for items in self.generated_meteorites:
            # nave_muerta = pygame.sprite.collide_mask(self.player, items)
            if pygame.sprite.collide_mask(self.player, items):
                self.kill_ship()
                print("He matado la nave")
                print(self.ship)
            if pygame.sprite.collide_mask(items, self.player):
                self.kill_meteorite()
                # detected_collision.append(collision)
                # return self.collision
                self.countdown_stop = False
            return self.countdown_stop, self.initialize_countdown()


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
