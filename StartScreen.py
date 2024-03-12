from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class StartScreen(App):
    def build(self):
        layout = FloatLayout()
        
        # สร้างปุ่ม "start" และกำหนดตำแหน่ง
        start_button = Button(text='Start', size_hint=(None, None), size=(200, 50),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        start_button.bind(on_press=self.on_start_button_press)
        
        # เพิ่มปุ่ม "start" ลงในเลย์เอาต์
        layout.add_widget(start_button)
        
        return layout
    
    def on_start_button_press(self, instance):
        # ฟังก์ชันนี้จะถูกเรียกเมื่อปุ่ม "start" ถูกกด
        print("Start button pressed")

if __name__ == '__main__':
    StartScreen().run()
