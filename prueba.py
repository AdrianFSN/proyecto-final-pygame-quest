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

 import pygame
from . import FPS, GO_TO_RECORDS_DELAY, HEIGHT, WIDTH
from . playlevel import PlayLevel
from . resolvelevel import ResolveLevel
from . frontpage import FrontPage
from . bestscores import BestPlayers
from . entities import LivesCounter, Scoreboard, Ship


class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.player = Ship(self.screen)
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()
        # self.front_page_exit = False
        self.front_page = FrontPage(self.screen)
        self.records_page = BestPlayers(self.screen)
        self.info_scenes = [self.front_page, self.records_page]
        self.available_play_levels = 3
        self.play = None
        self.resolve = None
        self.level = 1

        self.play_scenes = []
        for levels in range(self.level, self.available_play_levels):
            self.play = PlayLevel(
                self.screen, self.player, self.scoreboard, self.lives_counter, levels)
            self.resolve = ResolveLevel(
                self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
            self.play_scenes.append([self.play, self.resolve])

        self.info_switches_list = []
        self.info_scene_switch = None
        for switch in range(len(self.info_scenes)):
            self.info_scene_switch = switch
            self.info_switches_list.append([self.info_scene_switch, False])

        self.play_switches_list = []
        self.play_scene_switch = None
        for switch in range(len(self.play_scenes)):
            self.play_scene_switch = switch
            self.play_switches_list.append([self.play_scene_switch, False])

        self.info_switches_list[0][1] = True
        # print(f'Esta es la lista de switches {self.info_switches_list}')
        self.game_over = False

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            # bucle principal (o main loop)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    exit = True
                    break

            if self.info_switches_list[0][1]:
                self.front_page.mainLoop()

                if self.front_page.exit:
                    if not self.play_switches_list[0][1]:
                        self.play_scenes[0][0].mainLoop()
                        if not self.play_scenes[0][0].execute_game_over:
                            if self.play_scenes[0][0].exit:
                                self.play_scenes[0][1].mainLoop()
                        else:
                            self.game_over = True
                            self.play_switches_list[0][1] = True
                            self.records_page.mainLoop()
                            if self.records_page.exit:
                                self.info_switches_list[0][1] = True
                                self.front_page.exit = False

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Glumtar()
    juego.play()



    class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.player = Ship(self.screen)
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()
        # self.front_page_exit = False
        self.front_page = FrontPage(self.screen)
        self.records_page = BestPlayers(self.screen)
        self.info_scenes = [self.front_page, self.records_page]
        self.available_play_levels = 3
        self.play = None
        self.resolve = None
        self.level = 1

        self.play_scenes = []
        for levels in range(self.level, self.available_play_levels):
            self.play = PlayLevel(
                self.screen, self.player, self.scoreboard, self.lives_counter, levels)
            self.resolve = ResolveLevel(
                self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
            self.play_scenes.append([self.play, self.resolve])

        self.info_switches_list = []
        self.info_scene_switch = None
        for switch in range(len(self.info_scenes)):
            self.info_scene_switch = switch
            self.info_switches_list.append([self.info_scene_switch, False])

        self.play_switches_list = []
        self.play_scene_switch = None
        for switch in range(len(self.play_scenes)):
            self.play_scene_switch = switch
            self.play_switches_list.append([self.play_scene_switch, False])

        self.info_switches_list[0][1] = True
        self.game_over = False

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            # bucle principal (o main loop)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    print("Alguien ha decidido salir de la aplicación por la X")
                    exit = True
                    break

            if self.info_switches_list[0][1]:
                self.front_page.mainLoop()

                if self.front_page.exit:
                    if not self.play_switches_list[0][1]:
                        self.play_scenes[0][0].mainLoop()
                        if not self.play_scenes[0][0].execute_game_over:
                            if self.play_scenes[0][0].exit:
                                self.play_scenes[0][1].mainLoop()
                        else:
                            self.game_over = True
                            self.play_switches_list[0][1] = True
                            self.records_page.mainLoop()
                            if self.records_page.exit:
                                self.info_switches_list[0][1] = True
                                self.game_over = False
                                self.restart_game()

            pygame.display.flip()

        pygame.quit()

    def restart_game(self):
        self.info_scenes = []
        self.front_page = FrontPage(self.screen)
        self.info_scenes = [self.front_page, self.records_page]

        self.play_scenes = []
        for levels in range(self.level, self.available_play_levels):
            self.play = PlayLevel(
                self.screen, self.player, self.scoreboard, self.lives_counter, levels)
            self.resolve = ResolveLevel(
                self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
            self.play_scenes.append([self.play, self.resolve])

        self.info_switches_list = []
        self.info_scene_switch = None
        for switch in range(len(self.info_scenes)):
            self.info_scene_switch = switch
            self.info_switches_list.append([self.info_scene_switch, False])

        self.play_switches_list = []
        self.play_scene_switch = None
        for switch in range(len(self.play_scenes)):
            self.play_scene_switch = switch
            self.play_switches_list.append([self.play_scene_switch, False])



            class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.player = Ship(self.screen)
        self.scoreboard = Scoreboard()
        self.lives_counter = LivesCounter()
        self.records_page = BestPlayers(self.screen)
        # self.info_scenes = [self.front_page, self.records_page]
        self.front_page = None
        self.available_play_levels = 3
        self.play_scenes = []
        self.play = None
        self.resolve = None
        self.level = 1

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    exit = True
                    break
            self.front_page = FrontPage(self.screen)
            if not self.front_page.exit:
                self.front_page.mainLoop()

            if self.front_page.exit:
                self.play_scenes = []
                for levels in range(self.level, self.available_play_levels):
                    self.play = PlayLevel(self.screen, self.player,
                                          self.scoreboard, self.lives_counter, levels)
                    self.resolve = ResolveLevel(
                        self.play.screen, self.play.player, self.play.scoreboard, self.play.lives_counter, self.play.level)
                    self.play_scenes.append([self.play, self.resolve])

                for self.play, self.resolve in self.play_scenes:
                    self.play.mainLoop()
                    if not self.play.execute_game_over:
                        if self.play.exit:
                            self.resolve.mainLoop()
                    else:
                        self.records_page.mainLoop()
                        self.front_page.exit = False


class Glumtar:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Glumtar | The Quest")
        self.clock = pygame.time.Clock()
        self.records_page = BestPlayers(self.screen)
        self.available_play_levels = 3
        self.play_scenes = []
        self.play = None
        self.resolve = None
        self.level = 1

        self.set_up_elements = True

    def mainLoop(self):
        exit = False
        while not exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    exit = True
                    break
            if self.set_up_elements:
                scoreboard = Scoreboard(self.screen)
                player = Ship(self.screen)
                lives_counter = LivesCounter()
                front_page = FrontPage(self.screen)
                play_level1 = PlayLevel(
                    self.screen, player, scoreboard, lives_counter, 1)
                resolve_level1 = ResolveLevel(
                    self.screen, play_level1.player, play_level1.scoreboard, play_level1.lives_counter, 1)
                play_level2 = PlayLevel(
                    self.screen, player, scoreboard, lives_counter, 1)
                resolve_level2 = ResolveLevel(
                    self.screen, play_level2.player, play_level2.scoreboard, play_level2.lives_counter, 2)
                scenes_list = [front_page, play_level1, resolve_level1,
                               play_level2, resolve_level2, self.records_page]
                self.set_up_elements = False

            for stage in scenes_list:
                if not front_page.exit:
                    front_page.mainLoop()
                    if front_page.exit:
                        if play_level1.execute_game_over:
                            self.records_page.mainLoop()
                            if self.records_page.exit:
                                self.restart_game()
                        else:
                            play_level1.mainLoop()
                            if play_level1.exit:
                                resolve_level1.mainLoop()
                                if resolve_level1.exit:
                                    if play_level2.execute_game_over:
                                        self.records_page.mainLoop()
                                        if self.records_page.exit:
                                            self.restart_game()
                                        else:
                                            play_level2.mainLoop()
                                            if play_level2.exit:
                                                resolve_level2.mainLoop()
                                                if resolve_level1.exit:
                                                    self.records_page.mainLoop()
                                                    if self.records_page.exit:
                                                        self.restart_game()

        pygame.quit()

    def restart_game(self):
        # Preguntar si quiere continuar
        # Si quiere, setup elements pasa a True
        # Si no quiere, QUIT
        self.set_up_elements = True
        return self.set_up_elements
    
############################ Esta es la clase scoreboard con ls modificaciones ##############

class Scoreboard:
    margin_title = 50
    font_title_adjust = 20

    def __init__(self, screen, points=0):
        self.screen = screen
        self.scoreboard_value = points
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, FONT_SIZE)

    def increase_score(self, score_up):
        self.scoreboard_value += score_up

    def show_scoreboard(self, screen):
        score_string = str(self.scoreboard_value)
        scoreboard_text = self.font_style.render(
            score_string, True, COLUMBIA_BLUE)
        pointsX = SCOREBOARD_MARGIN
        pointsY = TOP_MARGIN_LIMIT - FONT_SIZE
        screen.blit(scoreboard_text, (pointsX, pointsY))

if not scene.execute_game_over:
                            scene.mainLoop()
                        else:
                            print("Ha habido un game over")
                            self.activate_play_pointer = False
                            self.scene.exit = True
                            self.play_pointer += 1
