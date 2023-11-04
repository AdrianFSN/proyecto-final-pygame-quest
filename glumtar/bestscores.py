import os
import pygame
from pygame.locals import *
from . import BOTTOM_MARGIN_LIMIT, COLUMBIA_BLUE, DEFAULT_POS_Y, FONT, FONT_SIZE, FPS, HEIGHT, TOP_MARGIN_LIMIT, SPACE_CADET, TITLE_FONT_SIZE, WIDTH
from . data.messages import Reader
from . data.db_manager import DBManager


class BestPlayers:
    MAX_RECORDS_IN_LIST = 5
    PRESS_ENTER_Y = 450
    RECORD_TABLE_X = WIDTH/2
    RECORD_TABLE_Y = 350
    CELL_HEIGHT = FONT_SIZE + 20
    BEST_SC_ALIGNMENT_LEFT = RECORD_TABLE_X - len('Name') * FONT_SIZE
    BEST_SC_ALIGNMENT_RIGHT = RECORD_TABLE_X + len('Score') * FONT_SIZE
    ROWS_Y = 300
    RECORDS_LENGTH = 5
    TITLE_Y = DEFAULT_POS_Y - CELL_HEIGHT

    def __init__(self, screen, scoreboard):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.score_board = scoreboard
        self.kill_game = False
        self.db_file_path = os.path.join(
            'glumtar', 'data', 'best_players.db')

        self.available_bg = []
        self.bg_controller = 0
        for bg in range(1, 3):
            self.bg_front_route = os.path.join(
                'glumtar', 'resources', 'images', f'BG_records{bg}.jpg')
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
        self.activate_cursor = pygame.USEREVENT + 8
        pygame.time.set_timer(self.activate_cursor, 500)

        self.font = FONT
        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)

        self.exit = False
        self.pointer = 0
        self.new_name = ''
        self.new_record = 0
        self.activate_insert_record = False
        self.db = DBManager(self.db_file_path)
        self.table_container = {}
        self.new_record_insert_container = {}
        self.activate_box_cursor = False
        self.render_new_record = False
        self.draw_no_ranking = False
        self.redraw_ranking = False
        self.start_rendering = True
        self.good_news = Reader(
            'records_messages.txt', FONT, FONT_SIZE, COLUMBIA_BLUE, (WIDTH, DEFAULT_POS_Y), (1, 2))
        self.press_enter = Reader(
            'records_messages.txt', FONT, FONT_SIZE, COLUMBIA_BLUE, (WIDTH, self.PRESS_ENTER_Y), (2, 3))
        self.best_records_title = Reader(
            'records_messages.txt', FONT, FONT_SIZE, COLUMBIA_BLUE, (WIDTH, self.TITLE_Y), (3, 4))
        self.get_best_scores()

    def mainLoop(self):
        self.new_record = self.score_board.scoreboard_value
        catch_record = True
        while not self.exit:
            self.clock.tick(FPS)
            self.screen.fill(SPACE_CADET)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or (event.type == pygame.KEYDOWN and event.key == (pygame.K_0)) or (event.type == pygame.KEYDOWN and event.key == (pygame.K_KP0)):
                    self.kill_game = True
                    return self.kill_game

                if self.activate_insert_record:
                    self.write_name(event)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.exit = True
                if event.type == pygame.USEREVENT + 5:
                    self.animate_stars()
                if event.type == pygame.USEREVENT + 8:
                    if not self.activate_box_cursor:
                        self.activate_box_cursor = True
                    elif self.activate_box_cursor:
                        self.activate_box_cursor = False
            self.screen.fill(SPACE_CADET)
            self.screen.blit(self.bg_front, (self.bg_front_X, self.bg_front_Y))
            self.screen.blit(self.logo, (self.logo_X, self.logo_Y))
            self.score_board.show_scoreboard(self.screen)

            if catch_record:
                if self.confirm_new_record():
                    self.draw_no_ranking = True
                    self.render_new_record = True
                    self.start_rendering = False
                    catch_record = False

            if self.render_new_record:
                self.render_name_and_score()

            if self.redraw_ranking:
                self.get_best_scores()
                self.draw_no_ranking = False

            if not self.draw_no_ranking:
                self.render_best_scores(self.screen)
                self.draw_ranking()

            self.add_user_choice_message()
            pygame.display.flip()

        return self.exit

    def get_best_scores(self):
        self.sql = 'SELECT Name, Score FROM glumtar_best_players ORDER BY Score DESC LIMIT 5;'
        self.best_players = self.db.consultSQL(self.sql)

    def render_best_scores(self, screen):
        headers_records = self.db.column_names
        data_records = self.best_players
        self.table_container = {}
        rows_y = self.ROWS_Y
        data_index = 0
        header_index = 0
        alignment_left = self.best_records_title.text_posX

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
                    rendered_header, (self.BEST_SC_ALIGNMENT_RIGHT, rows_y))
                self.table_container[rendered_header] = rendered_header_rect
        if data_index < self.RECORDS_LENGTH:
            for name, score in data_records:
                player = data_records[data_index].get(name)
                points = str(self.best_players[data_index].get(score))
                rendered_player = self.font_style.render(
                    player, True, COLUMBIA_BLUE)
                player_rect = self.screen.blit(
                    rendered_player, (alignment_left, rows_y + self.CELL_HEIGHT))

                rendered_points = self.font_style.render(
                    points, True, COLUMBIA_BLUE)
                points_rect = self.screen.blit(
                    rendered_points, (self.BEST_SC_ALIGNMENT_RIGHT, rows_y + self.CELL_HEIGHT))

                self.table_container[rendered_player] = player_rect
                self.table_container[rendered_points] = points_rect
                data_index += 1
                rows_y += self.CELL_HEIGHT
        self.best_records_title.render_lines(self.screen)

    def confirm_new_record(self):
        confirmation_list = []
        pointer = 0
        if pointer < self.MAX_RECORDS_IN_LIST:
            for scores in self.best_players:
                registered_scores = self.best_players[pointer].get('Score')
                confirmation_list.append(registered_scores)
                pointer += 1
        minor_record = min(confirmation_list)
        if self.new_record > minor_record:
            print(f'Tenemos nuevo record = {self.new_record}')
            self.activate_insert_record = True
            return True, self.activate_insert_record
        else:
            return False

    def write_name(self, event):
        text_length = 3
        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                self.insert_new_record()
                self.activate_insert_record = False
                self.render_new_record = False
                self.redraw_ranking = True
                return True, self.activate_insert_record, self.render_new_record, self.redraw_ranking
            else:
                if event.unicode.isalpha() and len(self.new_name) < text_length:
                    self.new_name += event.unicode
                    print(f'Esta es la len de self new name {self.new_name}')
                if event.key == K_BACKSPACE:
                    self.new_name = self.new_name[:-1]
                    # return False

    def render_name_and_score(self):
        posy = self.RECORD_TABLE_Y
        height_even = posy
        height_odd = posy

        list_of_requests = ['Your name', 'New record', self.new_name.upper(), str(
            self.new_record)]
        alignment_left = self.RECORD_TABLE_X - \
            len(list_of_requests[0]) * FONT_SIZE
        alignment_right = alignment_left + \
            len(list_of_requests[0]) * FONT_SIZE
        cursor_box_alignmentL = alignment_left
        cursor_box_alignmentY = posy - 5

        self.illuminate_box_cursor(
            self.CELL_HEIGHT, cursor_box_alignmentL, cursor_box_alignmentY)

        for index in range(len(list_of_requests)):
            render = self.font_style.render(
                list_of_requests[index], True, COLUMBIA_BLUE)
            if index % 2 == 0:
                render_rect = self.screen.blit(render, (
                    alignment_left, height_even))
                height_even += self.CELL_HEIGHT
            elif index % 2 != 0:
                render_rect = self.screen.blit(render, (
                    alignment_right, height_odd))
                height_odd += self.CELL_HEIGHT
            index += 1
            self.new_record_insert_container[render] = render_rect

        self.good_news.render_lines(self.screen)
        self.press_enter.render_lines(self.screen)
        self.good_news.draw_message(self.screen)
        self.press_enter.draw_message(self.screen)

    def illuminate_box_cursor(self, cell_height, cursor_box_alignmentL, cursor_box_alignmentY):
        if self.activate_box_cursor:
            text_box_rect1 = pygame.Rect(
                cursor_box_alignmentL, cursor_box_alignmentY + cell_height, FONT_SIZE, FONT_SIZE)
            text_box_rect2 = pygame.Rect(
                cursor_box_alignmentL + FONT_SIZE, cursor_box_alignmentY + cell_height, FONT_SIZE, FONT_SIZE)
            text_box_rect3 = pygame.Rect(
                cursor_box_alignmentL + FONT_SIZE*2, cursor_box_alignmentY + cell_height, FONT_SIZE, FONT_SIZE)

            if len(self.new_name) == 0:
                pygame.draw.rect(self.screen, COLUMBIA_BLUE, text_box_rect1)
            elif len(self.new_name) == 1:
                pygame.draw.rect(self.screen, COLUMBIA_BLUE, text_box_rect2)
            elif len(self.new_name) == 2:
                pygame.draw.rect(self.screen, COLUMBIA_BLUE, text_box_rect3)

    def insert_new_record(self):
        self.sql = 'INSERT INTO glumtar_best_players (Name, Score) VALUES (?, ?);'
        values = (self.new_name.upper(), self.new_record)
        self.insertion = self.db.insertSQL(self.sql, values)
        return f'He pasado por la función de insertar de best players'

    def draw_ranking(self):
        self.best_records_title.draw_message(self.screen)
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
        escape_message = "Press <ESPACE> to start or 0 to quit game"
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        title_render = self.font_style.render(
            escape_message, True, COLUMBIA_BLUE)
        self.pos_X = (WIDTH - title_render.get_width())/2
        self.pos_Y = HEIGHT - BOTTOM_MARGIN_LIMIT - title_render.get_height()
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))
