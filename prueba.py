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
