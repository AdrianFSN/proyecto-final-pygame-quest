import os
import pygame
from glumtar import COLUMBIA_BLUE, FONT_SIZE, WIDTH


class Reader:
    init_text_posY = 300
    font_size_correction = FONT_SIZE - 10
    spacing = FONT_SIZE + 5

    def __init__(self, file, font, lines_number=(0, 2)):
        # self.screen = screen
        self.file_name = file
        self.font = font
        self.start_reading_point = lines_number[0]
        self.stop_reading_point = lines_number[1]
        self.pointer = self.start_reading_point

        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(
            self.font_route, self.font_size_correction)
        self.text_file_path = os.path.join(
            'glumtar', 'data', f'{self.file_name}')
        self.text_posX = WIDTH
        self.text_posY = self.init_text_posY
        self.lines_container = {}
        self.activate_pointer = True
        self.rendered_line = None

    def renderize_lines(self, screen):
        with open(self.text_file_path, mode='r', encoding='UTF-8', newline='\n') as message_file:
            lines = message_file.readlines()
            for sentence in range(len(lines)):
                lines[sentence] = lines[sentence][:-1]
        if self.pointer <= len(lines):
            for row in range(self.start_reading_point, self.stop_reading_point):
                self.rendered_line = self.font_style.render(
                    lines[self.pointer], True, COLUMBIA_BLUE)
                self.lines_container[self.rendered_line] = screen.blit(
                    self.rendered_line, ((self.text_posX - self.rendered_line.get_width())/2, self.text_posY))
                self.pointer += 1
                self.text_posY += self.spacing

    def draw_message(self, screen):
        for rendered_text, text_rect in self.lines_container.items():
            screen.blit(
                rendered_text, (text_rect.x, text_rect.y))
