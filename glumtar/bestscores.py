import os
import pygame
from . import BLACK, BG_SCROLL_SPEED, BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, FPS, FRAMES_SPEED, GO_TO_RECORDS_DELAY, HEIGHT, LIVES, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, SPACE_CADET, TITLE_FONT_SIZE, TITLE_MARGIN, WIDTH
from .entities import LivesCounter, Scoreboard
from tools.timers_and_countdowns import Countdown, ScrollBG
from . data.messages import Reader
from . data.db_manager import DBManager


class BestPlayers:
    font_size_correction = FONT_SIZE - 10
    spacing = FONT_SIZE + 5
    init_text_posY = 300
    row_posY = init_text_posY
    row_posX = WIDTH
    column_X = WIDTH/3
    cell_pos_Y = init_text_posY

    def __init__(self, screen):
        self.screen = screen
        self.kill_game = False
        self.db_file_path = os.path.join(
            'glumtar', 'data', 'best_players.db')

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

        """ self.read_table = Reader('front_messages.txt', FONT, (0, 7))
        self.available_messages = [self.read_table]
        self.read_table.renderize_lines(self.screen)

        self.reader_pointer = 0 """
        self.exit = False
        self.pointer = 0
        # self.records_page_scenes = [self.get_best_scores()]
        self.get_best_scores()
        self.renderize_best_scores(self.screen)

    def mainLoop(self):
        print("Estoy en Best Scores")

        while not self.exit:
            self.screen.fill(SPACE_CADET)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or (event.type == pygame.KEYDOWN and event.key == (pygame.K_q)):
                    self.kill_game = True
                    return self.kill_game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.exit = True
                if event.type == pygame.USEREVENT + 5:
                    self.animate_stars()
            self.screen.fill(SPACE_CADET)
            self.screen.blit(self.bg_front, (self.bg_front_X, self.bg_front_Y))
            self.screen.blit(self.logo, (self.logo_X, self.logo_Y))
            self.draw_ranking()
            self.add_user_choice_message()

            # self.records_page_scenes = [self.get_best_scores()]

            """ self.available_messages[self.reader_pointer].draw_message(
                self.screen) """
            pygame.display.flip()

        return self.exit

    def get_best_scores(self):
        self.db = DBManager(self.db_file_path)
        self.sql = 'SELECT Position, Name, Score FROM glumtar_best_players;'
        self.db.consultSQL(self.sql)
        self.best_players = self.db.consultSQL(self.sql)
        # print(f'La lista de records que tengo es {self.best_players}')

    def renderize_best_scores(self, screen):
        records = self.db.column_names
        self.table_container = {}
        rows_x = 300
        rows_y = 300
        header_spacing = 50
        index = 0
        if index <= len(self.table_container):
            for headers in records:
                rendered_header = self.font_style.render(
                    headers, True, COLUMBIA_BLUE)
                self.screen.blit(rendered_header, (rows_x, rows_y))
                self.table_container[rendered_header] = self.screen.blit(
                    rendered_header, (rows_x, rows_y))
                rows_x += rendered_header.get_width() + header_spacing
            print(f'LOs headers son {self.table_container}')
            print(
                f'Los rects incluidos en table container tienen estas x {self.table_container.items()}')

    def draw_ranking(self):
        for rendered_text, text_rect in self.table_container.items():
            self.screen.blit(rendered_text, (text_rect.x, text_rect.y))
        # text_rect.x += 50

    def animate_stars(self):
        self.bg_front = pygame.image.load(
            self.available_bg[self.bg_controller])

        if self.bg_controller == 0:
            self.bg_controller = 1
        elif self.bg_controller == 1:
            self.bg_controller = 0

    def add_user_choice_message(self):
        escape_message = "Press <ESPACE> to start or Q to quit game"
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        title_render = self.font_style.render(
            escape_message, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - title_render.get_width())/2
        self.pos_Y = HEIGHT - BOTTOM_MARGIN_LIMIT - title_render.get_height()
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))
