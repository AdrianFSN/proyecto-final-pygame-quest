import os
import pygame
from . import BLACK, BG_SCROLL_SPEED, BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, CORAL_PINK, CORNELL_RED, COUNTDOWN_TIME, DEFAULT_BG_SCROLL, FONT, FONT_SIZE, FONT_SIZE_CONTROLLER, FPS, FRAMES_SPEED, GO_TO_RECORDS_DELAY, HEIGHT, LIVES, TOP_MARGIN_LIMIT, METEO_FREQUENCY_LEVEL1, ROBIN_EGG_BLUE, SPACE_CADET, TITLE_FONT_SIZE, TITLE_MARGIN, WIDTH
from .entities import LivesCounter, Scoreboard
from tools.timers_and_countdowns import Countdown, ScrollBG
from . data.messages import Reader
from . data.db_manager import DBManager


class BestPlayers:
    MAX_RECORDS_IN_LIST = 10

    def __init__(self, screen, scoreboard):
        self.screen = screen
        self.score_board = scoreboard
        self.kill_game = False
        self.db_file_path = os.path.join(
            'glumtar', 'data', 'best_players.db')

        self.available_bg = []
        self.bg_controller = 0
        for bg in range(1, 3):
            self.bg_front_route = os.path.join(
                'glumtar', 'resources', 'images', f'BG_front_page{bg}.jpg')
            self.available_bg.append(self.bg_front_route)
            bg += 1

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

        self.exit = False
        self.pointer = 0
        self.new_name = 'EXITO'
        self.new_record = 0
        self.activate_insert_record = False
        self.db = DBManager(self.db_file_path)

        self.table_container = {}
        self.get_best_scores()
        self.renderize_best_scores(self.screen)

    def mainLoop(self):
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
            self.score_board.show_scoreboard(self.screen)
            self.new_record = self.score_board.scoreboard_value
            # print(f'self new record es {self.new_record}')
            # print(
            # f'activate insert new record está en {self.activate_insert_record}')

            if not self.activate_insert_record:
                self.draw_ranking()
            else:
                self.insert_new_record()
                print(f'He pasado por la peticion de insertar record')

            self.add_user_choice_message()
            self.confirm_new_record()
            self.insert_new_record()

            pygame.display.flip()

        return self.exit

    def get_best_scores(self):
        # self.db = DBManager(self.db_file_path)
        self.sql = 'SELECT Name, Score FROM glumtar_best_players ORDER BY Score DESC LIMIT 5;'
        self.best_players = self.db.consultSQL(self.sql)

    def renderize_best_scores(self, screen):
        headers_records = self.db.column_names
        # print(f'self.db column names es {self.db.column_names} ')
        data_records = self.best_players
        self.table_container = {}
        rows_y = 300
        alignment_right = 850
        alignment_left = 450
        cell_height = FONT_SIZE + 20
        data_index = 0
        header_index = 0
        records_length = 5

        for headers in headers_records:
            if header_index == 0:
                rendered_header = self.font_style.render(
                    headers, True, COLUMBIA_BLUE)
                self.table_container[rendered_header] = self.screen.blit(
                    rendered_header, (alignment_left, rows_y))
                header_index += 1
            else:
                rendered_header = self.font_style.render(
                    headers, True, COLUMBIA_BLUE)
                rendered_header_rect = self.screen.blit(
                    rendered_header, (alignment_left, rows_y))
                rendered_header_rect.right = alignment_right
                self.table_container[rendered_header] = rendered_header_rect

        if data_index < records_length:
            for name, score in data_records:
                player = data_records[data_index].get(name)
                points = str(self.best_players[data_index].get(score))
                rendered_player = self.font_style.render(
                    player, True, COLUMBIA_BLUE)
                player_rect = self.screen.blit(
                    rendered_player, (alignment_left, rows_y + cell_height))
                player_rect.left = alignment_left

                rendered_points = self.font_style.render(
                    points, True, COLUMBIA_BLUE)
                points_rect = self.screen.blit(
                    rendered_points, (alignment_left, rows_y + cell_height))
                points_rect.right = alignment_right

                self.table_container[rendered_player] = player_rect
                self.table_container[rendered_points] = points_rect
                data_index += 1
                rows_y += cell_height

    def confirm_new_record(self):
        confirmation_list = []
        pointer = 0
        if pointer < self.MAX_RECORDS_IN_LIST:
            for scores in self.best_players:
                registered_scores = self.best_players[pointer].get('Score')
                confirmation_list.append(registered_scores)
                pointer += 1
        # print(f'confirmation list es {confirmation_list}')
        minor_record = min(confirmation_list)
        # print(f'Minor record es {minor_record}')
        if self.new_record > minor_record:
            print(f'Tenemos nuevo record = {self.new_record}')
            self.activate_insert_record = True
            return self.activate_insert_record

    def insert_new_record(self):
        self.sql = 'INSERT INTO glumtar_best_players (Name, Score) VALUES (?, ?);'
        values = (self.new_name, self.new_record)
        self.insertion = self.db.insertSQL(self.sql, values)
        self.new_record = 0
        self.activate_insert_record = False
        return self.activate_insert_record

    def draw_ranking(self):
        for rendered_text, text_rect in self.table_container.items():
            self.screen.blit(rendered_text, (text_rect.x, text_rect.y))

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
