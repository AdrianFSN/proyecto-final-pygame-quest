import os
import pygame
from . import BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, DEFAULT_POS_Y, FONT, FONT_SIZE, FPS, HEIGHT, TOP_MARGIN_LIMIT, SPACE_CADET, TITLE_FONT_SIZE, WIDTH
from .data.messages import Reader


class FrontPage:
    read_more_bottom_margin = 130
    INSTRUCTION_LINES_FONT_SIZE = FONT_SIZE - 10

    def __init__(self, screen):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.kill_game = False
        self.available_bg = []

        self.bg_controller = 0
        for bg in range(1, 3):
            self.bg_front_route = os.path.join(
                'glumtar', 'resources', 'images', f'BG_front_page{bg}.jpg')
            self.available_bg.append(self.bg_front_route)

        self.bg_front = pygame.image.load(
            self.available_bg[self.bg_controller])
        self.bg_front_X = 0
        self.bg_front_Y = 0

        logo_route = os.path.join(
            'glumtar', 'resources', 'images', 'glumtar_logo2.png')
        self.logo = pygame.image.load(logo_route)
        self.logo_X = (WIDTH - self.logo.get_width())/2
        self.logo_Y = TOP_MARGIN_LIMIT

        self.activate_stars = pygame.USEREVENT + 5
        pygame.time.set_timer(self.activate_stars, 1500)

        self.font = FONT
        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)

        self.paragraph1 = Reader(
            'front_messages.txt', FONT, self.INSTRUCTION_LINES_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, DEFAULT_POS_Y), (0, 7))
        self.paragraph2 = Reader(
            'front_messages.txt', FONT, self.INSTRUCTION_LINES_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, DEFAULT_POS_Y), (7, 12))
        self.paragraph3 = Reader(
            'front_messages.txt', FONT, self.INSTRUCTION_LINES_FONT_SIZE, COLUMBIA_BLUE, (WIDTH, DEFAULT_POS_Y), (12, 16))
        self.available_messages = [self.paragraph1,
                                   self.paragraph2, self.paragraph3]
        self.paragraph1.render_lines(self.screen)
        self.paragraph2.render_lines(self.screen)
        self.paragraph3.render_lines(self.screen)

        self.reader_pointer = 0
        self.exit = False
        self.go_to_frontpage = False

    def mainLoop(self):
        while not self.exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    self.kill_game = True
                    return self.kill_game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reader_pointer = 0
                    self.exit = True
                    return self.exit
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
            self.add_escape_message()
            self.available_messages[self.reader_pointer].draw_message(
                self.screen)
            if self.reader_pointer == 2:
                self.add_meteo_list()
            self.add_read_more_message()

            pygame.display.flip()

    def animate_stars(self):
        self.bg_front = pygame.image.load(
            self.available_bg[self.bg_controller])

        if self.bg_controller == 0:
            self.bg_controller = 1
        elif self.bg_controller == 1:
            self.bg_controller = 0

    def add_escape_message(self):
        escape_message = "Press SPACE to start"
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        title_render = self.font_style.render(
            escape_message, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - title_render.get_width())/2
        self.pos_Y = HEIGHT - BOTTOM_MARGIN_LIMIT - title_render.get_height()
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))

    def add_read_more_message(self):
        read_more_title = "Press arrow keys < > to read more"
        self.font_style = pygame.font.Font(
            self.font_route, self.INSTRUCTION_LINES_FONT_SIZE)
        read_more_render = self.font_style.render(
            read_more_title, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - read_more_render.get_width())/2
        self.pos_Y = HEIGHT - self.read_more_bottom_margin - read_more_render.get_height()
        self.screen.blit(
            read_more_render, (self.pos_X, self.pos_Y))

    def add_meteo_list(self):
        meteo_list_route = os.path.join(
            'glumtar', 'resources', 'images', f'meteo_list.png')
        meteo_list = pygame.image.load(meteo_list_route)
        pos_X = 0
        pos_Y = 0
        self.screen.blit(meteo_list, (pos_X, pos_Y))
