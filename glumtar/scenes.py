import os

import pygame

from . import BLACK, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FPS, FONT, FONT_SIZE, HEIGHT, LIVES, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, SPACE_CADET, TITLE_FONT_SIZE, TITLE_MARGIN, WIDTH
from .entities import LivesCounter, Meteorite, Ship, Scoreboard
from tools.timers_and_countdowns import Countdown, ScrollBG


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

        self.bg_scroll = ScrollBG(DEFAULT_BG_SCROLL)
        self.set_bg_scroll = DEFAULT_BG_SCROLL

        self.player = Ship()
        # self.ship = pygame.sprite.GroupSingle()

        self.trigger_meteorite = pygame.USEREVENT + 1
        pygame.time.set_timer(self.trigger_meteorite, METEO_FREQUENCY_LEVEL1)

        self.countdown = Countdown(self.screen, 5, 0)
        self.start_a_countdown = pygame.USEREVENT + 2
        pygame.time.set_timer(self.start_a_countdown, COUNTDOWN_TIME)

        self.initial_time = pygame.time.get_ticks()
        self.current_time = None

        self.random_meteorite = None
        self.generated_meteorites = pygame.sprite.Group()

    def mainLoop(self):
        super().mainLoop()
        exit = False
        stop_bg_scroll = False
        self.lives_counter.end_game = False
        # trigger_ship = False
        countdown_active = True

        while not exit:
            self.clock.tick(FPS)
            self.screen.fill(ROBIN_EGG_BLUE)
            self.paint_background(self.background_posX,
                                  self.background_posY, self.set_bg_scroll)
            self.add_glumtar_title()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
                if event.type == self.trigger_meteorite:
                    if not countdown_active:
                        self.generate_meteorites()
                if event.type == self.start_a_countdown:
                    if countdown_active:
                        self.countdown.discount_countdown()

            if not stop_bg_scroll:
                self.set_bg_scroll -= 1
                if self.set_bg_scroll <= 0:
                    stop_bg_scroll = True

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)

            if countdown_active:
                self.countdown.draw_countdown()
                self.countdown.add_countdown_title()
                if self.countdown.counter < self.countdown.stop:
                    countdown_active = False
                    self.countdown.reset_countdown()

            # if self.lives_counter.lives_value in range(1, LIVES+1):
            # if not trigger_ship:
            self.player.update()
            self.screen.blit(self.player.image, self.player.rect)
            # trigger_ship = False

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
            # self.check_collision()
            self.lives_counter.reduce_lives(self.killed_ship)

            pygame.display.flip()

        return False

    def initialize_countdown(self):
        self.countdown = Countdown(self.screen, 5, 0)

    def generate_ship(self):
        self.player = Ship()
        self.player.update()
        # self.ship.add(self.player)
        self.screen.blit(self.player.image, self.player.rect)

    def generate_meteorites(self):
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
        if self.set_bg_scroll != 0:
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
            return self.countdown_stop

    def add_glumtar_title(self):
        self.title = "Glumtar | The Quest"

        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        self.pos_X = (WIDTH - ((len(self.title)*TITLE_FONT_SIZE)))/2
        self.pos_Y = TOP_MARGIN_LIMIT - TITLE_FONT_SIZE

        title_render = self.font_style.render(
            self.title, True, COLUMBIA_BLUE)
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))


class ResolveLevel1(Scene):
    def __init__(self, screen):
        super().__init__(screen)

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            self.clock.tick(FPS)
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
            self.clock.tick(FPS)
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
            self.clock.tick(FPS)
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
