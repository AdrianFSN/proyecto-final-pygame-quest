import pygame
from . import ANCHO, ALTO


class Glumtar:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))

    def play(self):
        pass


if __name__ == '__main__':
    print('Arrancamos desde el archivo game.py')
    juego = Glumtar()
    juego.play()
