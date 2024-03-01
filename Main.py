from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super(TicTacToe, self).__init__(**kwargs)
        self.cols = 3
        self.buttons = []
        self.current_player = 'X'
        for _ in range(3):
            row = []
            for _ in range(3):
                button = Button(text='', font_size=40, on_press=self.on_button_press)
                row.append(button)
                self.add_widget(button)
            self.buttons.append(row)

    def on_button_press(self, instance):
        if instance.text == '':
            instance.text = self.current_player
            if self.check_winner():
                self.ids.status.text = f'Player {self.current_player} wins!'
            elif self.check_draw():
                self.ids.status.text = 'Draw!'
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(3):
            # Check rows
            if self.buttons[i][0].text == self.buttons[i][1].text == self.buttons[i][2].text != '':
                return True
            # Check columns
            if self.buttons[0][i].text == self.buttons[1][i].text == self.buttons[2][i].text != '':
                return True
        # Check diagonals
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text != '':
            return True
        if self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text != '':
            return True
        return False

    def check_draw(self):
        for row in self.buttons:
            for button in row:
                if button.text == '':
                    return False
        return True

class TicTacToeApp(App):
    def build(self):
        return TicTacToe()

if __name__ == '__main__':
    TicTacToeApp().run()
