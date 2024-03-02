from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

class Item(Label):
    def __init__(self, namee, **kwargs):
        super().__init__(**kwargs)
        self.name = namee
        self.font_size = 10
        self.point = 1
        self.s = 3 ; self.m = 3 ; self.l = 2  # Quantity of each size
        self.allsize = {'S':self.s,'M':self.m,'L':self.l}


class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.buttons = []
        self.X = Item("x")
        self.O = Item("O")
        for _ in range(3):
            row = []
            for _ in range(3):
                button = Button(text='', font_size=40, on_press=self.on_button_press)
                row.append(button)
                self.add_widget(button)
            self.buttons.append(row)
        self.character = self.X   # Turn Player
        self.winner = None

    def on_button_press(self, instance):
        if instance.text == '':
            instance.text = self.character.name
            if self.check_winner():
                self.show_popup(f"{self.character.name} wins!")
            else:
                self.character = self.O if self.character == self.X else self.X

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
    
    def show_popup(self, text): # Popup if you win
        popup = Popup(title='Game Over', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 200))
        popup.content.add_widget(Button(text=text, size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.5}, on_press=popup.dismiss))
        popup.open()


class TicTacToeApp(App):
    def build(self):
        return TicTacToe()

if __name__ == '__main__':
    TicTacToeApp().run()
