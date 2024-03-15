from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Color, Rectangle, Mesh
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

Config.set("graphics", "fullscreen", "auto")
Builder.load_file("PlayerXLayout.kv")


from kivy.uix.image import Image

from kivy.graphics import Rectangle
from kivy.graphics.context_instructions import Color

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        # เพิ่มพื้นหลังเต็มหน้าจอโดยใช้ Rectangle
        with self.layout.canvas:
            # กำหนดสีพื้นหลัง
            Color(1, 1, 1, 1)  # เปลี่ยนสีตามที่ต้องการ
            # สร้าง Rectangle ที่ครอบคลุมพื้นที่ขนาดเต็มหน้าจอ
            self.background = Rectangle(source='images/BG5.png',size=self.size, pos=self.pos)

        # สร้างปุ่ม "Start"
        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(250, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        start_button.bind(on_press=self.on_start_button_press)

        # เพิ่มปุ่ม "Start" เข้าไปในเลเอาท์
        self.layout.add_widget(start_button)

        # เพิ่มป้ายชื่อสำหรับผู้เล่น 1 และ 2
       

        # เพิ่มช่องกรอกข้อความสำหรับผู้เล่น 1 และ 2

        self.add_widget(self.layout)

    def on_start_button_press(self, instance):
        # ปิดหน้าจอ StartScreen ปัจจุบัน
        app = App.get_running_app()
        app.root.current = "game"

    def on_size(self, *args):
        # อัปเดตขนาดของ Rectangle เมื่อขนาดของหน้าจอเปลี่ยนแปลง
        self.background.size = self.size
        self.background.pos = self.pos


# Class Character
class Item(Label):
    def __init__(self, namee, **kwargs):
        super().__init__(**kwargs)
        self.name = namee
        self.font_size = 10
        self.point = 1
        self.s = 3
        self.m = 3
        self.l = 2  # Quantity of each size

# Custom Button
class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = None
        self.background_normal = "images/Board4.png"
        self.color = (0, 0, 0, 0)

    def addpoint(self, data):
        self.data = data

# Game Main
class TicTacToe(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.buttons = []
        self.X = Item("x")
        self.O = Item("O")

        ############################
        #                          #
        #    [but1, but2, but3]    #
        #    [but4, but5, but6]    #
        #    [but7, but8, but9]    #
        #                          #
        ############################

        self.turn_label = None
        Clock.schedule_interval(self.update_turn_label, 0.1)
        for _ in range(3):
            row = []
            for _ in range(3):
                button = CustomButton(on_press=self.on_button_press)
                row.append(button)
                self.add_widget(button)
            self.buttons.append(row)

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
                instance.addpoint(self.character.point)
                self.checkimg(instance)
                # Check winner
                if self.check_winner():
                    self.show_popup(f"{self.character.name} wins!")
                else:
                    if self.character == self.X:
                        self.character = self.O
                    else:
                        self.character = self.X
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
                    if self.character == self.X:
                        self.character = self.O
                    else:
                        self.character = self.X
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
                    if self.character == self.X:
                        self.character = self.O
                    else:
                        self.character = self.X

    # Add img in field
    def checkimg(self, button):
        if button.text == "x":
            if self.character.point == 1:
                button.background_normal = "images/SX.png"
                button.background_down = "images/put.png"
            elif self.character.point == 2:
                button.background_normal = "images/MX.png"
                button.background_down = "images/put.png"
            else:
                button.background_normal = "images/LX.png"
                button.background_down = "images/put.png"
        else:
            if self.character.point == 1:
                button.background_normal = "images/SO.png"
                button.background_down = "images/put.png"
            elif self.character.point == 2:
                button.background_normal = "images/MO.png"
                button.background_down = "images/put.png"
            else:
                button.background_normal = "images/LO.png"
                button.background_down = "images/put.png"

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
        popup = Popup(
            # title="Game Over",
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
        popup.open()

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

# Status Player X
class StatusXLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StatusXLayout, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.2, "center_y": 0.45}

        self.nameX = Label(
            text="Player X",
            font_size=40,
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "y": 4.5},
        )
        
        self.add_widget(self.nameX)
        
    def update_sizes(self, s, m, l):
        pass
        
# Status Player y
class StatusOLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(StatusOLayout, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {"center_x": 0.8, "center_y": 0.45}

        self.name = Label(
            text="Player O",
            font_size=40,
            size_hint=(None, None),
            pos_hint={"center_x": 0.5, "y": 4.5},
        )
        
        text = Label(text="total size", font_size=40, color=(0, 0, 0), pos_hint={"center_x": 0.8, "y": 3.5})
        
        self.add_widget(self.name)
        self.add_widget(text)
        
        self.textS = Label(text=f"size S = 0", font_size=40, color=(0, 0, 0), pos_hint={"center_x": 0.8, "y": 2.5})
        self.textM = Label(text=f"size M = 0", font_size=40, color=(0, 0, 0), pos_hint={"center_x": 0.8, "y": 2})
        self.textL = Label(text=f"size L = 0", font_size=40, color=(0, 0, 0), pos_hint={"center_x": 0.8, "y": 1.5})
        self.add_widget(self.textS)
        self.add_widget(self.textM)
        self.add_widget(self.textL)

    def update_sizes(self, s, m, l):
        self.textS.text = f"size S = {s}"
        self.textM.text = f"size M = {m}"
        self.textL.text = f"size L = {l}"
    
class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super(BackgroundWidget, self).__init__(**kwargs)

        with self.canvas:
            # Color(1, 1, 0, 1)
            # self.rect = Rectangle(pos=self.pos, size=self.size)
            self.rect = Rectangle(source='images/BG5.png',pos=self.pos, size=self.size)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
# Run Game
from kivy.uix.screenmanager import Screen

class TicTacToeApp(Screen):
    def on_enter(self):
        game = FloatLayout(size_hint=(1, 1))
        
        background = BackgroundWidget()
        game.add_widget(background)

        # title = Label(
        #     text="Tic tac toc",
        #     font_size=40,
        #     pos_hint={"center_x": 0.5, "center_y": 0.9},
        # )

        mapp = TicTacToe(
            size_hint=(None, None),
            size=(500, 500),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        turn = Label(font_size=40, pos_hint={"center_x": 0.5, "center_y": 0.2})

        mapp.turn_label = turn

        sett = BoxLayout(
            size_hint=(None, None),
            size=(500, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.1},
        )
        S = Button(text="S", on_press=lambda instance: mapp.changepoint("S"))
        M = Button(text="M", on_press=lambda instance: mapp.changepoint("M"))
        L = Button(text="L", on_press=lambda instance: mapp.changepoint("L"))
        
        # Create StatusXLayout
        status_x_layout = StatusXLayout()
        # Create StatusOLayout
        status_o_layout = StatusOLayout()

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Add widget
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        sett.add_widget(S)
        sett.add_widget(M)
        sett.add_widget(L)
        # game.add_widget(title)  # Game name
        game.add_widget(mapp)  # Game
        game.add_widget(turn)  # Your Turn
        game.add_widget(sett)  # chang size
        game.add_widget(status_x_layout)  # Status player X
        game.add_widget(status_o_layout)  # Status player O
        # return TicTacToe()
        
        # Store references to status layouts in TicTacToe instance
        mapp.status_x_layout = status_x_layout
        mapp.status_o_layout = status_o_layout

        # Update status labels initially
        mapp.update_status_labels()
        
        self.add_widget(game)


class MyApp(App):
    def build(self):
        # สร้าง ScreenManager เพื่อจัดการหน้าจอ
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(TicTacToeApp(name="game"))
        return sm
    
if __name__ == "__main__":
    MyApp().run()