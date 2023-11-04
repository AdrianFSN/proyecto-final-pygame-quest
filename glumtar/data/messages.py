import os
import pygame
from pygame.locals import *
from glumtar import COLUMBIA_BLUE, DEFAULT_LINES_SPACING


class Reader:

    def __init__(self, file, font, font_size, font_color=COLUMBIA_BLUE, position=(0, 0), lines_number=(0, 2), spacing=DEFAULT_LINES_SPACING):
        self.file_name = file
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.position = position
        self.text_posX = position[0]
        self.text_posY = position[1]
        self.spacing = spacing
        self.line_spacing = 0

        self.start_reading_point = lines_number[0]
        self.stop_reading_point = lines_number[1]
        self.pointer = self.start_reading_point

        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(
            self.font_route, self.font_size)
        self.text_file_path = os.path.join(
            'glumtar', 'data', f'{self.file_name}')

        self.lines_container = {}
        self.activate_pointer = True
        self.rendered_line = None

    def renderize_lines(self, screen):
        with open(self.text_file_path, mode='r', encoding='UTF-8', newline='\n') as message_file:
            lines = message_file.readlines()
            for sentence in range(len(lines)):
                lines[sentence] = lines[sentence][:-1]

        if self.pointer in range(self.start_reading_point, self.stop_reading_point):
            for row in range(self.start_reading_point, self.stop_reading_point):
                self.rendered_line = self.font_style.render(
                    lines[self.pointer], True, self.font_color)
                self.lines_container[self.rendered_line] = screen.blit(
                    self.rendered_line, ((self.text_posX - self.rendered_line.get_width())/2, self.text_posY))
                self.line_spacing = self.rendered_line.get_height() + self.spacing
                self.pointer += 1
                self.text_posY += self.line_spacing
            self.text_posX -= self.rendered_line.get_width()
            self.text_posX = self.text_posX/2

    def draw_message(self, screen):
        for rendered_text, text_rect in self.lines_container.items():
            screen.blit(
                rendered_text, (text_rect.x, text_rect.y))
