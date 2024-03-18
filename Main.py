from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics.context_instructions import Color
from kivy.uix.image import Image, AsyncImage
from kivy.core.audio import SoundLoader


# Config.set("graphics", "fullscreen", "auto")
Builder.load_file("PlayerXLayout.kv")

# X = White
# O = Black

# Start
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # Add bg full srceen with Rectangle
        with self.layout.canvas:
            Color(1, 1, 1, 1) 
            self.background = Rectangle(
                source="images/BG6.png", size=self.size, pos=self.pos
            )

        # สร้างปุ่ม "Start"
        start_button = Button(
            size_hint=(None, None),
            size=(250, 60),
            pos_hint={"center_x": 0.5, "center_y": 0.28},
            background_normal="images/startbutton.png",  # Set background image
        )
        start_button.bind(on_press=self.on_start_button_press)

        # Add "Start" button in layout
        self.layout.add_widget(start_button)

        self.add_widget(self.layout)

    # close startscreen 
    def on_start_button_press(self, instance):
        instance.background_down = "images/startbutton.png"
        app = App.get_running_app()
        app.root.current = "game"
        win_sound = SoundLoader.load('images/Sound/Teleport.mp3')
        win_sound.play()

    def on_size(self, *args):
        self.background.size = self.size
        self.background.pos = self.pos
    win_sound = SoundLoader.load('images/Sound/backgroundmusic.mp3')
    win_sound.play()
        
# Class Character
class Item(Label):
    def __init__(self, namee, **kwargs):
        super().__init__(**kwargs)
        self.name = namee
        self.font_size = 10
        self.point = 1
        # Quantity of each size
        self.s = 3  # 1 point
        self.m = 3  # 2 point
        self.l = 2  # 3 point
        self.total = 0

# Custom Button
class CustomButton(Button):
    def __init__(self, img, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.background_normal = img
        self.color = (0, 0, 0, 0)

    def addpoint(self, data):
        self.data = data

# Custom Button size
class CustomButtonSize(Button):
    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        if size == "s":
            self.background_normal = "images/iconS.png"
            self.background_down = "images/iconS.png"
        elif size == "m":
            self.background_normal = "images/iconM.png"
            self.background_down = "images/iconM.png"
        elif size == "l":
            self.background_normal = "images/iconL.png"
            self.background_down = "images/iconL.png"
    
# Custom Button Reset 
class CustomResetButton(Button):
    def __init__(self, image_size=(110, 110), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = "images/reset.png"
        self.background_down = "images/reset.png"
        self.size_hint = (None, None)
        self.size = image_size
        self.pos_hint = {"right": 0.99, "top": 0.98}

# Custom Challenge Reset 
class CustomChallengeButton(Button):
    def __init__(self, image_size=(110, 110), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = "images/challenge.png"
        self.background_down = "images/challenge.png"
        self.size_hint = (None, None)
        self.size = image_size
        self.pos_hint = {"right": 0.94, "top": 0.98} #right": 0.945
                   
# Game Main
class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.buttons = []
        self.X = Item("x")
        self.O = Item("O")

        #############################
        #                           #
        #    [but1, but2, but3],    #
        #    [but4, but5, but6],    #
        #    [but7, but8, but9],    #
        #                           #
        #############################

        self.turn_label = None
        self.timelimit_label = None
        self.timelimit = 10
        Clock.schedule_interval(self.update_turn_label, 0.1)
        Clock.schedule_interval(self.timer, 1)
        for _ in range(3):
            row = []
            for _ in range(3):
                button = CustomButton("images/Board4.png" ,on_press=self.on_button_press)
                row.append(button)
                self.add_widget(button)
            self.buttons.append(row)
        # print(str(self.buttons

        self.character = self.X  # Turn Player
        self.winner = None

    # Change Size
    def changepoint(self, button):
        # self.X.point = 2
        if button == "S" and self.character.s > 0:
            self.character.point = 1
        elif button == "M" and self.character.m > 0:
            self.character.point = 2
        elif button == "L" and self.character.l > 0:
            self.character.point = 3
        else:
            self.show_popup("button size emty")

    # If tuch button
    def on_button_press(self, instance):  # instance = button
        # Button = empty
        if instance.text == "" and not self.winner:
            if self.checksize():
                self.delet()
                instance.text = self.character.name
                # print(self.character.name)
                instance.addpoint(self.character.point)
                self.checkimg(instance)
                # Check winner
                if self.check_winner():
                    self.show_popup(f"{self.character.name} wins!")
                else:
                    self.character = self.O if self.character == self.X else self.X
                    self.timelimit = 10
            else:
                # Automatically change the point (assuming it's related to grid size)
                self.autochangepoint()
                self.delet()
                instance.text = self.character.name
                instance.addpoint(self.character.point)
                self.checkimg(instance)
                if self.check_winner():
                    self.show_popup(f"{self.character.name} wins!")
                else:
                    self.character = self.O if self.character == self.X else self.X
                    self.timelimit = 10
        # Button != empty
        elif (
            instance.text != ""
            and not self.winner
            and instance.text != self.character.name
        ):
            if instance.data < self.character.point:
                self.delet()
                instance.text = self.character.name
                instance.data = self.character.point
                self.checkimg(instance)
                if self.check_winner():
                    self.show_popup(f"{self.character.name} wins!")
                else:
                    self.character = self.O if self.character == self.X else self.X
                    self.timelimit = 10

    # Add img in field
    def checkimg(self, button):
        if button.text == "x":
            if self.character.point == 1:
                button.background_normal = "images/New/SX.png"
                button.background_down = "images/New/put.png"
            elif self.character.point == 2:
                button.background_normal = "images/New/MX.png"
                button.background_down = "images/New/put.png"
            else:
                button.background_normal = "images/New/LX.png"
                button.background_down = "images/New/put.png"
        else:
            if self.character.point == 1:
                button.background_normal = "images/New/SO.png"
                button.background_down = "images/New/put.png"
            elif self.character.point == 2:
                button.background_normal = "images/New/MO.png"
                button.background_down = "images/New/put.png"
            else:
                button.background_normal = "images/New/LO.png"
                button.background_down = "images/New/put.png"
        win_sound = SoundLoader.load('images/Sound/Teleport.mp3')
        win_sound.play()

    # Check size character s m l
    def checksize(self):
        if self.character.point == 1:
            if self.character.s > 0:
                return True
        elif self.character.point == 2:
            if self.character.m > 0:
                return True
        elif self.character.point == 3:
            if self.character.l > 0:
                return True
        return False

    # Update status size player
    def update_status_labels(self):
        # Update StatusXLayout
        self.status_x_layout.update_sizes(self.X.s, self.X.m, self.X.l)
        # Update StatusOLayout
        self.status_o_layout.update_sizes(self.O.s, self.O.m, self.O.l)

    # Delete amount
    def delet(self):
        print(self.character.name)
        if self.character.point == 1:
            self.character.s -= 1
        elif self.character.point == 2:
            self.character.m -= 1
        elif self.character.point == 3:
            self.character.l -= 1

        print("s", self.character.s)
        print("m", self.character.m)
        print("l", self.character.l)

        # Update status labels
        self.update_status_labels()

    # Check winner
    def check_winner(self):
        # Check rows
        for row in self.buttons:
            if row[0].text == row[1].text == row[2].text != "":
                return True

        # Check columns
        for col in range(3):
            if (
                self.buttons[0][col].text
                == self.buttons[1][col].text
                == self.buttons[2][col].text
                != ""
            ):
                return True

        # Check diagonals
        if (
            self.buttons[0][0].text
            == self.buttons[1][1].text
            == self.buttons[2][2].text
            != ""
        ):
            return True
        if (
            self.buttons[0][2].text
            == self.buttons[1][1].text
            == self.buttons[2][0].text
            != ""
        ):
            return True

        return False

    # Popup if you win
    def show_popup(self, text):
        print(text)
        popup = Popup(
            title="Finish Game ",
            content=BoxLayout(orientation="vertical"),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.content.add_widget(
            Button(
                text=text,
                size_hint=(None, None),
                size=(200, 50),
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_press=popup.dismiss,
            )
        )
        if popup != popup.dismiss and text != "button size emty":
           self.reset_game()
        if text == "x wins!" and text !='button size emty':
            win_sound = SoundLoader.load('images/Sound/winX.mp3')
            win_sound.play()
        elif text == "O wins!"and text !='button size emty':
            win_sound = SoundLoader.load('images/Sound/winO.mp3')
            win_sound.play()
        elif  text =='button size emty':
            win_sound = SoundLoader.load('images/Sound/buttonsizeemty.mp3')
            win_sound.play()
        popup.open()
    
    # If you cann't play (Draw)
    def draw_game(self):
        for row in self.buttons:
            for i in range (0,3):
                if row[i].text == "x":
                    self.X.total += row[i].data
                elif row[i].text == "O":
                    self.O.total += row[i].data
        if self.X.total > self.O.total:
            print(str(f"{self.X.total} {self.O.total}"))
            self.show_popup(f"x wins!")
        elif self.X.total < self.O.total :
            self.show_popup(f"o wins!")
        elif self.X.total == self.O.total :
             self.show_popup(f"draw")
    
    # Restart game
    def reset_game(self):
        # Clear the text and point data of all buttons
        for row in self.buttons:
            for button in row:
                button.text = ""
                button.data = None
                button.background_normal = "images/Board4.png"

        # Reset player X and O data
        self.X.s = 3
        self.X.m = 3
        self.X.l = 2
        self.X.total = 0
        self.O.s = 3
        self.O.m = 3
        self.O.l = 2
        self.O.total = 0
        self.timelimit = 10
       
        # Reset the turn to player X
        self.character = self.X
        self.character.point = 1
        # Update status labels
        self.update_status_labels()

        # Reset winner status
        self.winner = None

        # Close any open popups
        for child in self.parent.children:
            if isinstance(child, Popup):
                child.dismiss()
        
    # Timer Turn
    def timer(self, dt):
        if self.timelimit == 0:
            self.character = self.O if self.character == self.X else self.X
            self.timelimit = 10
        else:
            self.timelimit -= 1
        
        self.timelimit_label.text = f"{self.timelimit}"
            
    # Update Yourturn
    def update_turn_label(self, dt):
        if self.turn_label and self.character:
            size = ""
            if self.character.point == 1:
                size = "S"
            elif self.character.point == 2:
                size = "M"
            elif self.character.point == 3:
                size = "L"

            self.turn_label.text = f"Is turn: {self.character.name} Size: {size}"

    # Auto change size if size = 0
    def autochangepoint(self):
        # Adjust the point size based on the available sizes
        if self.X.s > 0:
            self.character.point = 1
        elif self.X.m > 0:
            self.character.point = 2
        elif self.X.l > 0:
            self.character.point = 3

# Status Player X White
class StatusXLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StatusXLayout, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.2, "center_y": 0.45}
        self.nameX = Label(text=f"Player X", font_size=40, color=(1, 1, 1, 1), pos_hint={"center_x": 0.001, "y": 0.6},)
        self.add_widget(self.nameX)
    
        # Add circle 
        with self.canvas:
            Color(1, 1, 1, 1)
            self.circle1 = Ellipse(pos=(170, 330), size=(50, 50))
            self.circle2 = Ellipse(pos=(330, 330), size=(50, 50))
            self.circle3 = Ellipse(pos=(490, 335), size=(50, 50))
        
        self.textS = Label(text=f"0", font_size=30, color=(0, 0, 0, 1), pos=(466, 306))
        self.textM = Label(text=f"0", font_size=30, color=(0, 0, 0, 1), pos=(306, 306))
        self.textL = Label(text=f"0", font_size=30, color=(0, 0, 0, 1), pos=(146, 305))
        self.add_widget(self.textS)
        self.add_widget(self.textM)
        self.add_widget(self.textL)

    def update_sizes(self, s, m, l):
        self.textS.text = f"{s}"
        self.textM.text = f"{m}"
        self.textL.text = f"{l}"

# Status Player O Black
class StatusOLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StatusOLayout, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.8, "center_y": 0.45}
        self.name = Label(text=f"Player O", font_size=40, color=(0, 0, 0, 1), pos_hint={"center_x": 1.2, "y": 0.6},)
        self.add_widget(self.name)

        # Add circle 
        with self.canvas:
            Color(0, 0, 0)
            self.circle1 = Ellipse(pos=(1470, 330), size=(50, 50))
            self.circle2 = Ellipse(pos=(1640, 330), size=(50, 50))
            self.circle3 = Ellipse(pos=(1780, 335), size=(50, 50))
        
        self.textS = Label(text=f"0", font_size=30, color=(1, 1, 1, 1), pos=(1756, 308))
        self.textM = Label(text=f"0", font_size=30, color=(1, 1, 1, 1), pos=(1616, 305))
        self.textL = Label(text=f"0", font_size=30, color=(1, 1, 1, 1), pos=(1446, 305))
        self.add_widget(self.textS)
        self.add_widget(self.textM)
        self.add_widget(self.textL)

    def update_sizes(self, s, m, l):
        self.textS.text = f"{s}"
        self.textM.text = f"{m}"
        self.textL.text = f"{l}"

# Bg Game main
class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super(BackgroundWidget, self).__init__(**kwargs)

        with self.canvas:
            # Color(1, 1, 0, 1)
            # self.rect = Rectangle(pos=self.pos, size=self.size)
            self.rect = Rectangle(source="images/BG5.png", pos=self.pos, size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# Run Game
class TicTacToeApp(Screen):
    def on_enter(self):
        game = FloatLayout(size_hint=(1, 1))

        background = BackgroundWidget()
        game.add_widget(background)

        mapp = TicTacToe(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        turn = Label(font_size=40, pos_hint={"center_x": 0.5, "center_y": 0.8})
        mapp.turn_label = turn
        
        time = Label(font_size=40, pos_hint={'center_x': 0.5, 'center_y': 0.89}, color=(0, 0, 0, 1))
        mapp.timelimit_label = time

        sett = BoxLayout(
            size_hint=(None, None),
            size=(870, 290),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
        )
        
        S = CustomButtonSize("s", on_press=lambda instance: mapp.changepoint("S"))
        M = CustomButtonSize("m", on_press=lambda instance: mapp.changepoint("M"))
        L = CustomButtonSize("l", on_press=lambda instance: mapp.changepoint("L"))

        # Create StatusXLayout
        status_x_layout = StatusXLayout()
        # Create StatusOLayout
        status_o_layout = StatusOLayout()

        reset_button = CustomResetButton()
        reset_button.bind(on_press=lambda instance: mapp.reset_game())
        game.add_widget(reset_button)
        
        challenge_button = CustomChallengeButton()
        challenge_button.bind(on_press=lambda instance: mapp.draw_game())
        game.add_widget(challenge_button)

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Add widget
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        sett.add_widget(L)
        sett.add_widget(M)
        sett.add_widget(S)
        game.add_widget(mapp)  # Game
        game.add_widget(turn)  # Your Turn
        game.add_widget(time)  # Time
        game.add_widget(sett)  # chang size
        game.add_widget(status_x_layout)  # Status player X
        game.add_widget(status_o_layout)  # Status player O

        # Store references to status layouts in TicTacToe instance
        mapp.status_x_layout = status_x_layout
        mapp.status_o_layout = status_o_layout

        # Update status labels initially
        mapp.update_status_labels()

        self.add_widget(game)

# First page game
class MyApp(App):
    def build(self):
        # สร้าง ScreenManager เพื่อจัดการหน้าจอ
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(TicTacToeApp(name="game"))
        
        return sm

if __name__ == "__main__":
    MyApp().run()