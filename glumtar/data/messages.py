import os
import pygame
from glumtar import COLUMBIA_BLUE, FONT_SIZE, WIDTH


class Reader:
    init_text_posY = 250
    spacing = FONT_SIZE + 5

    def __init__(self, file, font, lines_number=1):
        # self.screen = screen
        self.file_name = file
        self.font = font
        self.number_of_lines = lines_number

        self.font_route = os.path.join(
            'glumtar', 'resources', 'fonts', self.font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)
        self.text_file_path = os.path.join(
            'glumtar', 'data', f'{self.file_name}')
        self.text_posX = WIDTH/2
        self.text_posY = self.init_text_posY
        self.lines_container = {}
        self.activate_pointer = True

    def renderize_lines(self, screen):
        with open(self.text_file_path, mode='r', encoding='UTF-8', newline='\n') as message_file:
            lines = message_file.readlines()
            print(f'Estas son las líneas en lines {lines}')
        pointer = 0
        if pointer <= len(lines):
            for row in lines:
                rendered_line = self.font_style.render(
                    lines[pointer], True, COLUMBIA_BLUE)
                self.lines_container[rendered_line] = screen.blit(
                    rendered_line, ((self.text_posX - rendered_line.get_width())/2, self.text_posY))
                pointer += 1
                self.text_posY += self.spacing
        print(
            f'este es el diccionario de renders y blits {self.lines_container}')

    def draw_message(self, screen):
        for rendered_text, text_rect in self.lines_container.items():
            screen.blit(rendered_text, text_rect.center)


class Instruction:
    def __init__(self, text):
        self.text = text
        self.converted_text = ''

    def turn_into_string(self):
        for line in range(0, len(self.text)):
            self.converted_text += f'{self.text[line]}' + '\n'
            print(
                f'Este es self text {self.text} y este es self converted text {self.converted_text}')

        return self.converted_text
