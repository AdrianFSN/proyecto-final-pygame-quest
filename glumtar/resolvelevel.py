import os
import pygame
from . import COLUMBIA_BLUE, CORAL_PINK, FONT, FPS, TOP_MARGIN_LIMIT, TITLE_FONT_SIZE, WIDTH
from .playlevel import PlayLevel


class ResolveLevel(PlayLevel):
    alpha = 0
    fade_in_speed = 7

    def __init__(self, screen, player, scoreboard, livescounter, level):
        super().__init__(screen, player, scoreboard, livescounter, level)
        self.available_bg = []
        self.bg_A_controller = 2
        self.bg_B_controller = 3
        for bg in range(1, 5):
            self.bg_resolve_route = os.path.join(
                'glumtar', 'resources', 'images', f'BG_planet{bg}.jpg')
            self.available_bg.append(self.bg_resolve_route)
            # print(f'Estos son los fondos disponibles {self.available_bg}')

        self.background_A = pygame.image.load(
            self.available_bg[self.bg_A_controller])
        self.background_B = pygame.image.load(
            self.available_bg[self.bg_B_controller])
        self.background_B.set_alpha(self.alpha)

        self.bg_fade_in = pygame.USEREVENT + 6
        pygame.time.set_timer(self.bg_fade_in, 100)

        self.background_posX = 0
        self.background_posY = 0

        self.player = player
        self.scoreboard = scoreboard
        self.lives_counter = livescounter
        self.exit = False

    def mainLoop(self):
        while not self.exit:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.exit = True
                if event.type == self.bg_fade_in:
                    if self.player.rect.center[0] <= WIDTH/2 and self.alpha < 255:
                        self.alpha += self.fade_in_speed
                    elif self.alpha > 255:
                        self.alpha = 255

            self.screen.fill(CORAL_PINK)
            self.screen.blit(
                self.background_A, (self.background_posX, self.background_posY))
            self.screen.blit(
                self.background_B, (self.background_posX, self.background_posY))
            self.background_B.set_alpha(self.alpha)

            self.add_level_title()

            self.scoreboard.show_scoreboard(self.screen)
            self.lives_counter.show_lives(self.screen)

            self.player.land = True
            self.player.update()
            if not self.player.request_draw_rotation:
                self.screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()

        return self.exit

    def add_level_title(self):
        self.title = "Level 1"
        font = FONT
        self.font_route = os.path.join('glumtar', 'resources', 'fonts', font)
        self.font_style = pygame.font.Font(self.font_route, TITLE_FONT_SIZE)
        self.pos_X = (WIDTH - ((len(self.title)*TITLE_FONT_SIZE)))/2
        self.pos_Y = TOP_MARGIN_LIMIT - TITLE_FONT_SIZE

        title_render = self.font_style.render(
            self.title, True, COLUMBIA_BLUE)
        self.screen.blit(
            title_render, (self.pos_X, self.pos_Y))
