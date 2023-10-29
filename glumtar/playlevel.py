import os
import pygame
from . import BG_SCROLL_SPEED, COLUMBIA_BLUE, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, FPS, FRAMES_SPEED, GO_TO_RECORDS_DELAY, HEIGHT, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, TITLE_FONT_SIZE, WIDTH
from .entities import Meteorite
from tools.timers_and_countdowns import Countdown, ScrollBG
# from .data.messages import Reader
# from .game import Glumtar


class PlayLevel:
    def __init__(self, screen, player, scoreboard, livescounter, level):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.level = level
        bg_route = os.path.join('glumtar', 'resources',
                                'images', 'BG_level2.jpg')
        self.background = pygame.image.load(bg_route)
        self.background_posX = 0
        self.background_posY = 0

        self.scoreboard = scoreboard
        self.lives_counter = livescounter

        self.bg_scroll = ScrollBG(DEFAULT_BG_SCROLL)
        self.set_bg_scroll = DEFAULT_BG_SCROLL
        self.player = player

        self.trigger_meteorite = pygame.USEREVENT + 1
        pygame.time.set_timer(self.trigger_meteorite, METEO_FREQUENCY_LEVEL1)

        self.countdown = Countdown(self.screen, 5, 0)
        self.start_a_countdown = pygame.USEREVENT + 2
        pygame.time.set_timer(self.start_a_countdown, COUNTDOWN_TIME)

        self.request_go_to_records = pygame.USEREVENT + 3
        pygame.time.set_timer(self.request_go_to_records, GO_TO_RECORDS_DELAY)

        self.activate_explosion_frames = pygame.USEREVENT + 4
        pygame.time.set_timer(self.activate_explosion_frames, 5)
        self.frames_speed = FRAMES_SPEED

        self.initial_time = pygame.time.get_ticks()
        self.current_time = None

        self.random_meteorite = None
        self.generated_meteorites = pygame.sprite.Group()
        self.collision_detected = False
        self.allow_collisions = False
        self.allow_points = True
        self.execute_game_over = False
        self.stop_bg_scroll = False
        self.exit = False
        # self.end_game = False

    def mainLoop(self):
        countdown_active = True
        activate_explosion = False
        # initialize_ship_costume = False

        while not self.exit:
            self.clock.tick(FPS)
            self.screen.fill(ROBIN_EGG_BLUE)
            self.paint_background(self.background_posX,
                                  self.background_posY, self.set_bg_scroll)
            self.add_level_title()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == self.trigger_meteorite:
                    if not countdown_active:
                        self.generate_meteorites()
                if event.type == self.start_a_countdown:
                    if countdown_active:
                        self.countdown.discount_countdown()
                if event.type == self.activate_explosion_frames:
                    if activate_explosion:
                        self.player.explode_the_ship(self.frames_speed)
                        if self.frames_speed <= len(self.player.explosion_frames):
                            self.frames_speed += 1
                        else:
                            activate_explosion = False
                            self.frames_speed = FRAMES_SPEED
                            self.player.reset_ship_costume()
                            if self.lives_counter.lives_value > 0:
                                countdown_active = True

                if event.type == self.request_go_to_records:
                    if self.execute_game_over:
                        return self.execute_game_over

            if not self.stop_bg_scroll:
                self.set_bg_scroll -= BG_SCROLL_SPEED
                if self.set_bg_scroll <= 0:
                    self.stop_bg_scroll = True
                    print(f'Este esl scroll stop {self.stop_bg_scroll}')
                    self.exit = True
                """ elif self.end_game:
                    self.stop_bg_scroll = True
                    print(
                        f'Este esl scroll stop desde end game {self.stop_bg_scroll}') """

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)
            print(f"Execute game over está en {self.execute_game_over}")

            if countdown_active:
                self.countdown.draw_countdown()
                self.countdown.add_countdown_title()
                self.allow_collisions = False
                self.allow_points = False
                self.player.reset_ship_costume()

                if self.countdown.counter < self.countdown.stop:
                    countdown_active = False
                    self.countdown.reset_countdown()
                    self.allow_collisions = True
                    self.allow_points = True
                    self.screen.blit(self.player.image, self.player.rect)

            self.player.update()
            self.screen.blit(self.player.image, self.player.rect)

            self.generated_meteorites.draw(self.screen)
            self.generated_meteorites.update()

            if self.allow_collisions == True:
                if self.check_collision():
                    activate_explosion = True
                    self.collision_detected = True
                    self.play_ship_explosion_sound()
                    self.lives_counter.reduce_lives(
                        self.collision_detected)

            if self.lives_counter.lives_value == 0:
                self.show_game_over()
                self.allow_collisions = False
                countdown_active = False
                self.allow_points = False

            for meteorite in self.generated_meteorites:
                if meteorite.rect.right < 0:
                    self.generated_meteorites.remove(meteorite)
                    if self.allow_points:
                        self.scoreboard.increase_score(meteorite.points)

            pygame.display.flip()

        return self.exit, self.execute_game_over

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
        if self.set_bg_scroll != 0:  # Esto es lo que realmente para el scroll.
            self.background_posX -= 1

    def check_collision(self):
        if pygame.sprite.spritecollide(
                self.player, self.generated_meteorites, True, pygame.sprite.collide_mask):
            return True

    def play_ship_explosion_sound(self):
        boom_route = os.path.join(
            'glumtar', 'resources', 'sounds', 'Boom1.wav')
        pygame.mixer.init()
        pygame.mixer.Sound(boom_route).play()

    def add_level_title(self):
        self.title = "Level 1"
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        self.pos_X = (WIDTH - ((len(self.title)*TITLE_FONT_SIZE)))/2
        self.pos_Y = TOP_MARGIN_LIMIT - TITLE_FONT_SIZE

        title_render = self.font_style.render(
            self.title, True, COLUMBIA_BLUE)
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))

    def show_game_over(self):
        game_over_title = "Game Over"
        font = FONT
        self.execute_game_over = True
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(
            self.font_route, FONT_SIZE + FONT_SIZE_CONTROLLER)
        self.pos_X = (WIDTH - ((len(game_over_title)*FONT_SIZE)))/2
        self.pos_Y = (HEIGHT - FONT_SIZE)/2

        game_over_title_render = self.font_style.render(
            game_over_title, True, COLUMBIA_BLUE)
        self.screen.blit(
            game_over_title_render, (self.pos_X, self.pos_Y))

        # return self.execute_game_over
