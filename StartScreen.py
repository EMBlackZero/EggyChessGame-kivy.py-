from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput



class StartScreen(App):
    def build(self):
        layout = FloatLayout()

        # สร้างปุ่ม "start" และกำหนดตำแหน่ง
        start_button = Button(
            text="Start",
            size_hint=(None, None),
            size=(250, 80),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
        )
        start_button.bind(on_press=self.on_start_button_press)

        # เพิ่มปุ่ม "start" ลงในเลย์เอาต์
        layout.add_widget(start_button)

        # เพิ่มป้ายชื่อ Player 1 และ Player 2
        player1_label = Label(
            text="Player 1",
            size_hint=(None, None),
            size=(100, 30),
            pos_hint={"right": 0.2, "center_y": 0.9},
        )
        player2_label = Label(
            text="Player 2",
            size_hint=(None, None),
            size=(100, 30),
            pos_hint={"right": 0.9, "center_y": 0.9},
        )
        layout.add_widget(player1_label)
        layout.add_widget(player2_label)

        # เพิ่มช่องกรอกชื่อ Player 1 และ Player 2
        player1_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 30),
                                  pos_hint={'right': 0.25, 'center_y': 0.8})
        player2_input = TextInput(multiline=False, size_hint=(None, None), size=(200, 30),
                                  pos_hint={'right': 0.95, 'center_y': 0.8})
        layout.add_widget(player1_input)
        layout.add_widget(player2_input)

        return layout

    def on_start_button_press(self, instance):
        # ฟังก์ชันนี้จะถูกเรียกเมื่อปุ่ม "start" ถูกกด
        print("Start button pressed")


if __name__ == "__main__":
    StartScreen().run()
