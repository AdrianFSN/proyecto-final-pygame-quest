import os
import pygame
from . import BLACK, BG_SCROLL_SPEED, BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, FPS, FRAMES_SPEED, GO_TO_RECORDS_DELAY, HEIGHT, LIVES, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, SPACE_CADET, TITLE_FONT_SIZE, TITLE_MARGIN, WIDTH
from .entities import LivesCounter, Meteorite, Ship, Scoreboard
from tools.timers_and_countdowns import Countdown, ScrollBG
from .data.messages import Reader


class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def mainLoop(self):
        print("Empty method for Scene's main loop")


class FrontPage(Scene):
    read_more_bottom_margin = 150
    font_size_correction = FONT_SIZE - 10

    def __init__(self, screen):
        super().__init__(screen)
        self.available_bg = []
        self.bg_index = 1
        self.bg_controller = 0
        for bg in range(1, 3):
            self.bg_front_route = os.path.join(
                'glumtar', 'resources', 'images', f'BG_front_page{self.bg_index}.jpg')
            self.available_bg.append(self.bg_front_route)
            self.bg_index += 1

        self.bg_front = pygame.image.load(
            self.available_bg[self.bg_controller])
        self.bg_front_X = 0
        self.bg_front_Y = 0

        logo_route = os.path.join(
            'glumtar', 'resources', 'images', 'glumtar_logo.png')
        self.logo = pygame.image.load(logo_route)
        self.logo_X = (WIDTH - self.logo.get_width())/2
        self.logo_Y = TOP_MARGIN_LIMIT

        self.activate_stars = pygame.USEREVENT + 5
        pygame.time.set_timer(self.activate_stars, 1500)

        self.font = FONT
        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)

        self.paragraph1 = Reader('messages.txt', FONT, (0, 7))
        self.paragraph2 = Reader('messages.txt', FONT, (7, 12))
        self.paragraph3 = Reader('messages.txt', FONT, (12, 16))
        self.available_messages = [self.paragraph1,
                                   self.paragraph2, self.paragraph3]
        self.paragraph1.renderize_lines(self.screen)
        self.paragraph2.renderize_lines(self.screen)
        self.paragraph3.renderize_lines(self.screen)

        self.reader_pointer = 0

    def mainLoop(self):
        super().mainLoop()
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit = True
                if event.type == pygame.USEREVENT + 5:
                    self.animate_stars()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    if self.reader_pointer < len(self.available_messages) - 1:
                        self.reader_pointer += 1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if self.reader_pointer <= len(self.available_messages)-1 and self.reader_pointer > 0:
                        self.reader_pointer -= 1

            self.screen.fill(SPACE_CADET)
            self.screen.blit(self.bg_front, (self.bg_front_X, self.bg_front_Y))
            self.screen.blit(self.logo, (self.logo_X, self.logo_Y))
            # self.paragraph3.draw_message(self.screen)
            self.add_escape_message()
            self.available_messages[self.reader_pointer].draw_message(
                self.screen)
            self.add_read_more_message()

            pygame.display.flip()

        return False

    def animate_stars(self):
        self.bg_front = pygame.image.load(
            self.available_bg[self.bg_controller])

        if self.bg_controller == 0:
            self.bg_controller = 1
        elif self.bg_controller == 1:
            self.bg_controller = 0

    def add_escape_message(self):
        escape_message = "Press <ESPACE> to start"
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        title_render = self.font_style.render(
            escape_message, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - title_render.get_width())/2
        self.pos_Y = HEIGHT - BOTTOM_MARGIN_LIMIT - title_render.get_height()
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))

    def add_read_more_message(self):
        read_more_title = "Press L or R to read more"
        self.font_style = pygame.font.Font(
            self.font_route, self.font_size_correction)
        read_more_render = self.font_style.render(
            read_more_title, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - read_more_render.get_width())/2
        self.pos_Y = HEIGHT - self.read_more_bottom_margin - read_more_render.get_height()
        self.screen.blit(
            read_more_render, (self.pos_X, self.pos_Y))


class MatchLevel1(Scene):
    def __init__(self, screen, player, scoreboard, livescounter):
        super().__init__(screen)
        bg_route = os.path.join('glumtar', 'resources',
                                'images', 'BG_level1.jpg')
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
        # self.end_game = False

    def mainLoop(self):
        super().mainLoop()
        exit = False
        # stop_bg_scroll = False
        countdown_active = True
        end_game = False
        activate_explosion = False
        initialize_ship_costume = False

        while not exit:
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
                    if end_game:
                        self.go_to_records()
                        break

            if not self.stop_bg_scroll:
                self.set_bg_scroll -= BG_SCROLL_SPEED
                if self.set_bg_scroll <= 0:
                    self.stop_bg_scroll = True
                    print(f'Este esl scroll stop {self.stop_bg_scroll}')
                    exit = True
                elif end_game:
                    self.stop_bg_scroll = True
                    print(
                        f'Este esl scroll stop desde end game {self.stop_bg_scroll}')

            end_game = self.execute_game_over

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)
            # print(f"End game está en {end_game}")

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

        return False

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
        return self.execute_game_over

    def go_to_records(self):
        return
        go_to_scene = MatchLevel2(self.screen)

        return go_to_scene.mainLoop()


class ResolveLevel1(Scene):

    def __init__(self, screen, player, scoreboard, livescounter):
        super().__init__(screen)
        bg_route = os.path.join('glumtar', 'resources',
                                'images', 'planet1.jpg')
        self.background = pygame.image.load(bg_route)
        self.background_posX = 0
        self.background_posY = 0

        self.player = player
        self.scoreboard = scoreboard
        self.lives_counter = livescounter

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
            self.screen.blit(
                self.background, (self.background_posX, self.background_posY))
            self.add_level_title()

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)

            self.player.land = True
            self.player.update()
            if not self.player.request_draw_rotation:
                self.screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()

        return False

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
