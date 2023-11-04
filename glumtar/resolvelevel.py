import os
import pygame
from . import AVAILABLE_BG, COLUMBIA_BLUE, CORAL_PINK, DEFAULT_POS_Y, FONT, FONT_SIZE, FPS, SPACE_CADET, TOP_MARGIN_LIMIT, TITLE_FONT_SIZE, WIDTH
from .playlevel import PlayLevel
from .data.messages import Reader


class ResolveLevel(PlayLevel):
    alpha = 0
    fade_in_speed = 7
    PLANET_AHEAD_Y = DEFAULT_POS_Y - 150
    PLANET_NAME_Y = PLANET_AHEAD_Y + 50
    PLANETS_ALERTS_FONT_SIZE = FONT_SIZE - 10

    def __init__(self, screen, player, scoreboard, livescounter, level):
        super().__init__(screen, scoreboard, livescounter, level)
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.kill_game = False
        self.player = player
        self.scoreboard = scoreboard
        self.lives_counter = livescounter
        self.level = level
        self.texts_font_color = COLUMBIA_BLUE

        self.available_bg = []
        self.selected_bg = []
        self.bg_controller = self.level - 1
        self.bg_resolve_route_A = None
        self.bg_resolve_route_B = None
        for bg in range(1, AVAILABLE_BG):
            if not bg % 2 == 0:
                self.bg_resolve_route_A = os.path.join(
                    'glumtar', 'resources', 'images', f'BG_planet{bg}.jpg')
            else:
                self.bg_resolve_route_B = os.path.join(
                    'glumtar', 'resources', 'images', f'BG_planet{bg}.jpg')
                self.available_bg.append(
                    (self.bg_resolve_route_A, self.bg_resolve_route_B))
        for bg_pairs in range(len(self.available_bg)):
            self.selected_bg.append(self.available_bg[bg_pairs])

        self.background_A = pygame.image.load(
            self.available_bg[self.bg_controller][0])
        self.background_B = pygame.image.load(
            self.available_bg[self.bg_controller][1])
        self.background_B.set_alpha(self.alpha)

        self.bg_fade_in = pygame.USEREVENT + 6
        pygame.time.set_timer(self.bg_fade_in, 100)

        self.advance_level = pygame.USEREVENT + 7
        pygame.time.set_timer(self.advance_level, 6000)

        self.background_posX = 0
        self.background_posY = 0

        self.landing_ahead_message = Reader(
            'levels.txt', FONT, self.PLANETS_ALERTS_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, self.PLANET_AHEAD_Y), (0, 1))
        self.planet_level_1 = Reader(
            'levels.txt', FONT, self.PLANETS_ALERTS_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, self.PLANET_NAME_Y), (1, 2))
        self.planet_level_2 = Reader(
            'levels.txt', FONT, self.PLANETS_ALERTS_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, self.PLANET_NAME_Y), (2, 5))
        self.available_planets_texts = [
            self.planet_level_1, self.planet_level_2]

        self.landing_ahead_message.render_lines(self.screen)
        self.planet_level_1.render_lines(self.screen)
        self.planet_level_2.render_lines(self.screen)
        self.go_to_exit = False
        self.exit = False

    def mainLoop(self):
        while not self.exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    self.kill_game = True
                    return self.kill_game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.exit = True
                if event.type == self.bg_fade_in:
                    if self.player.rect.center[0] <= WIDTH/2 and self.alpha < 255:
                        self.alpha += self.fade_in_speed
                    elif self.alpha > 255:
                        self.alpha = 255
                if event.type == self.advance_level:
                    if self.player.rect.bottom >= self.player.stop_landing:
                        self.go_to_exit = True

            self.screen.fill(CORAL_PINK)
            self.screen.blit(
                self.background_A, (self.background_posX, self.background_posY))
            self.screen.blit(
                self.background_B, (self.background_posX, self.background_posY))
            self.background_B.set_alpha(self.alpha)
            self.add_level_title()
            self.landing_ahead_message.draw_message(self.screen)

            if self.alpha == 255:
                if self.level == 1:
                    self.planet_level_1.draw_message(self.screen)
                elif self.level == 2:
                    self.planet_level_2.draw_message(self.screen)

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)

            self.player.land = True
            self.player.update()
            if not self.player.request_draw_rotation:
                self.screen.blit(self.player.image, self.player.rect)
            if self.go_to_exit:
                self.exit = True

            pygame.display.flip()

        return self.exit

    def add_level_title(self):
        self.title = f"Level {self.level}"
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        self.pos_X = (WIDTH - ((len(self.title)*TITLE_FONT_SIZE)))/2
        self.pos_Y = TOP_MARGIN_LIMIT - TITLE_FONT_SIZE

        title_render = self.font_style.render(
            self.title, True, self.texts_font_color)
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))
