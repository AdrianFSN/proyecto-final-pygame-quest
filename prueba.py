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

        print(f'Así ha quedado self play scenes {self.play_scenes}')
        print(
            f'este es el nivel de la primera partida {self.play_scenes[0][0].level} y el de su resolve {self.play_scenes[0][1].level}')
        print(
            f'este es el nivel de la segunda partida {self.play_scenes[1][0].level} y el de su resolve {self.play_scenes[1][1].level}')
