trozos de instructions

        """self.instructions_filename = 'messages.txt'
        self.instructions_file_path = os.path.join(
            'glumtar', 'data', 'messages.txt') """
        # self.cursor = 0
        # self.writer = 0
        # self.read_instructions()
        # self.instructions_texts = self.read_instructions()

            # if self.writer < len(self.reader_surfaces):
            #    self.screen.blit(self.reader_surfaces[self.writer], ((
            #        self.instructions_posX - self.instructions_render.get_width())/2, self.instructions_posY))
            # self.show_instructions()
            # self.draw_instructions(self.instructions_texts[0])
            # self.screen.blit(self.instructions_render, ((
            #    self.instructions_posX - self.instructions_render.get_width())/2, self.instructions_posY))

""" def read_instructions(self):
        with open(self.instructions_file_path, mode='r', encoding='UTF-8', newline='\n') as instructions_file:
            reader = instructions_file.readlines()

        for lines in reader:
            # if self.cursor < len(reader):
            self.instructions_render = self.font_style.render(
                reader[self.cursor], True, COLUMBIA_BLUE)
            self.reader_surfaces.append(self.instructions_render)
            print(f"Este es el reader surfaces {self.reader_surfaces}")
            self.cursor += 1
            print(f"Este es el reader_text {lines}")

        return len(self.reader_surfaces) """

    """ def show_instructions(self):
        self.screen.blit(self.reader_surfaces[0], ((
            self.instructions_posX - self.instructions_render.get_width())/2, self.instructions_posY))
        print(f"Surface es {self.reader_surfaces[0]}")
        position_2 = self.instructions_posY + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[1], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_2))
        position_3 = position_2 + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[2], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_3))
        position_4 = position_3 + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[3], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_4))
        position_5 = position_4 + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[4], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_5))
        position_6 = position_5 + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[5], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_6))
        position_7 = position_6 + self.instructions_render.get_height()
        self.screen.blit(self.reader_surfaces[6], ((
            self.instructions_posX - self.instructions_render.get_width())/2, position_7)) """
"""     instructions_posX = WIDTH
    init_instructions_posY = 250
    instructions_posY = init_instructions_posY """
    """ paragraph1 = []
    paragraph2 = []
    render_paragraph1 = None
    render_paragraph2 = None
    rendered_paragraph1 = []
    rendered_paragraph2 = []

    reader_surfaces = []
    lines_writer = 6
    spacing = FONT_SIZE
    visible_instruction = None
    reader = None

    instructions_render = None """