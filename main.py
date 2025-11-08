
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class MainApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=40)
        
        label = MDLabel(
            text="Welcome to Real Estate App",
            halign="center"
        )
        
        button = MDRaisedButton(
            text="Login",
            pos_hint={"center_x": 0.5}
        )
        
        layout.add_widget(label)
        layout.add_widget(button)
        
        return layout

if __name__ == "__main__":
    MainApp().run()
