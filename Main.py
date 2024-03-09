from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image, AsyncImage

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
        self.turn_label = None
        Clock.schedule_interval(self.update_turn_label, 0.1)
        for _ in range(3):
            row = []
            for _ in range(3):
                button = Button(text='', font_size=40, on_press=self.on_button_press)
                row.append(button)
                self.add_widget(button)
            self.buttons.append(row)
        self.character = self.X   # Turn Player
        self.winner = None
    
    
    def changepoint(self, button):
        #self.X.point = 2
        if button == "S":
            self.character.point = 1
        elif button == "M" and self.character.m > 0:
            self.character.point = 2
        else:
            self.character.point = 3
        print(self.character.point)

    def on_button_press(self, instance):    # if tuch button
        if instance.text == '':
            instance.text = self.character.name
            if self.check_winner():
                self.show_popup(f"{self.character.name} wins!")
            else:
                self.character = self.O if self.character == self.X else self.X

    def check_winner(self): # Check winner
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
        
    def update_turn_label(self, dt):    #Update Yourturn
        if self.turn_label:
            self.turn_label.text = f"Is turn : {self.character.name}"

class TicTacToeApp(App):
    def build(self):
        game = FloatLayout()
        title = Label(text="Tic tac toc", font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.9})
        mapp = TicTacToe(size_hint=(None, None), size=(500, 500), pos_hint={'center_x': 0.5, 'center_y': 0.6})
        
        turn = Label(font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.3})
        mapp.turn_label = turn

        
        sett = BoxLayout(size_hint=(None, None), size=(500, 100), pos_hint={'center_x': 0.5, 'center_y': 0.1})
        
        S = Button(text="S", on_press=lambda instance: mapp.changepoint("S"))
        M = Button(text="M", on_press=lambda instance: mapp.changepoint("M"))
        L = Button(text="L", on_press=lambda instance: mapp.changepoint("L"))
        sett.add_widget(S)
        sett.add_widget(M)
        sett.add_widget(L)
        
        game.add_widget(title)  # Game name
        game.add_widget(mapp)   # Game
        game.add_widget(turn)   # Your Turn
        game.add_widget(sett)   # chang size

        
        # return TicTacToe()
        return game

if __name__ == '__main__':
    TicTacToeApp().run()
