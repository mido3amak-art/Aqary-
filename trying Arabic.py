from kivy.core.text import LabelBase
import arabic_reshaper

# تسجيل الخط العربي اللي عندك
LabelBase.register(name="ArabicFont", fn_regular="/storage/emulated/0/Pydroid3/MyProjects/Cairo-Regular.ttf")

# دالة لتصحيح الحروف العربية
def fix_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return reshaped_text[::-1]  # نعكس الاتجاه

import arabic_reshaper

def fix_arabic_text(text):
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return reshaped_text[::-1]  # نعكس النص عشان يظهر مضبوط
    except Exception:
        return text
        
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.text import LabelBase

# تحديد المسار الكامل يدويًا بدون الاعتماد على __file__
font_path = "/storage/emulated/0/Pydroid3/MyProjects/NotoNaskhArabic-Regular.ttf"

try:
    LabelBase.register(name="ArabicFont", fn_regular=font_path)
    print("✅ Arabic font registered successfully!")
except Exception as e:
    print(f"⚠️ Font registration failed: {e}")
    
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserIconView
import os
import json

Window.clearcolor = (1, 1, 1, 1)


# ---- BEGIN INJECTED HELPERS (added by assistant) ----
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image as KVImage
from kivy.animation import Animation
from kivy.uix.settings import SettingsWithSidebar

APP_ICON_PATH = "app_icon.png"
AUTOSAVE_FILE = "autosave_vehsh.json"

def set_gradient_background(widget, color_top=(0.7,0.9,1,1), color_bottom=(0.95,0.85,0.75,1)):
    widget.canvas.before.clear()
    with widget.canvas.before:
        Color(*color_bottom)
        Rectangle(pos=widget.pos, size=widget.size)
    # bind to size/pos to redraw (simple solid bottom color; full gradient requires texture work)
    def _update(instance, *a):
        widget.canvas.before.clear()
        with widget.canvas.before:
            Color(*color_bottom)
            Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=_update, size=_update)

def add_settings_button_to_screen(screen, app):
    try:
        root = None
        # if screen has children and first child is a layout, use it
        if hasattr(screen, 'children') and screen.children:
            root = screen.children[0]
        if root is None or not hasattr(root, 'add_widget'):
            return
        # add small settings button at top-right using FloatLayout wrapper
        float_wrapper = FloatLayout(size=root.size, size_hint=root.size_hint)
        # move existing widgets into float_wrapper
        while root.children:
            w = root.children[-1]
            root.remove_widget(w)
            float_wrapper.add_widget(w)
        # settings button
        btn = Button(text='⚙', size_hint=(None,None), size=(48,48), pos_hint={'right':0.98,'top':0.98})
        def _open_settings(inst):
            app.open_settings_popup()
        btn.bind(on_release=_open_settings)
        float_wrapper.add_widget(btn)
        # replace in screen
        screen.clear_widgets()
        screen.add_widget(float_wrapper)
        # apply background
        set_gradient_background(float_wrapper)
    except Exception as e:
        print("add_settings_button error:", e)

def autosave_textinputs_in_screen(screen, app):
    # find TextInput widgets and bind on_text to save
    try:
        tinputs = []
        def _gather(widget):
            from kivy.uix.textinput import TextInput
            if isinstance(widget, TextInput):
                tinputs.append(widget)
            if hasattr(widget,'children'):
                for c in widget.children:
                    _gather(c)
        _gather(screen)
        def save(*a):
            data = {'screen': screen.name, 'values': {}}
            for t in tinputs:
                key = t.hint_text or t.id or str(id(t))
                data['values'][key] = t.text
            try:
                import json
                with open(AUTOSAVE_FILE,'w') as f:
                    json.dump(data, f)
            except Exception as e:
                print("autosave write error:", e)
        for t in tinputs:
            t.bind(text=lambda *a: save())
    except Exception as e:
        print("autosave hook error:", e)

# small image viewer util
def open_image_viewer(app, image_path):
    try:
        from kivy.uix.image import Image
        box = BoxLayout(orientation='vertical')
        img = Image(source=image_path, allow_stretch=True)
        box.add_widget(img)
        btn = Button(text='Close', size_hint=(1,0.12))
        popup = Popup(title='Image Viewer', content=box, size_hint=(0.95,0.95))
        btn.bind(on_release=popup.dismiss)
        box.add_widget(btn)
        popup.open()
    except Exception as e:
        print("image viewer error:", e)

# After ScreenManager is created, call this to enhance existing screens
def enhance_screens(sm, app):
    for s in sm.screens:
        try:
            add_settings_button_to_screen(s, app)
            autosave_textinputs_in_screen(s, app)
        except Exception as e:
            print("enhance_screens error for", s.name, e)
# ---- END INJECTED HELPERS ----



users = {}
current_user = None
properties = [
    {"area": "Downtown", "district": "A", "info": "2 rooms, 100 sqm", "views": 0, "images": []},
    {"area": "Downtown", "district": "B", "info": "3 rooms, 150 sqm", "views": 0, "images": []},
    {"area": "Suburbs", "district": "C", "info": "Villa, 300 sqm", "views": 0, "images": []},
]

PAYMENT_PHONE = "+201063386820"

def exit_app(*a):
    App.get_running_app().stop()

def validate_password(password):
    if len(password) < 8:
        return False
    has_digit = any(ch.isdigit() for ch in password)
    has_alpha = any(ch.isalpha() for ch in password)
    return has_digit and has_alpha

def add_top_exit(layout):
    btn = Button(text="Exit", size_hint=(0.1,0.01), height=dp(44))
    btn.bind(on_release=exit_app)
    layout.add_widget(btn)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[2,50,1,50])
        add_top_exit(layout)

        layout.add_widget(Label(text="Are you Buyer or Seller?", font_size=22, size_hint=(1,0.1)))

        btn_buyer = Button(text="Buyer", size_hint=(1,0.02), height=dp(50))
        btn_buyer.bind(on_release=lambda x: setattr(self.manager, "current", "buyer"))
        layout.add_widget(btn_buyer)

        btn_seller = Button(text="Seller", size_hint=(1,0.02), height=dp(50))
        btn_seller.bind(on_release=lambda x: setattr(self.manager, "current", "seller_choice"))
        layout.add_widget(btn_seller)

        self.add_widget(layout)

class SellerChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[20,30,20,30])
        add_top_exit(layout)
        layout.add_widget(Label(text="Seller Options", font_size=22, size_hint=(1, 0.12)))

        btn_new = Button(text="New Account", size_hint=(1, 0.05), height=dp(50))
        btn_new.bind(on_release=lambda x: setattr(self.manager, "current", "seller_register"))
        layout.add_widget(btn_new)

        btn_existing = Button(text="Existing Account", size_hint=(1, 0.05), height=dp(50))
        btn_existing.bind(on_release=lambda x: setattr(self.manager, "current", "seller_login"))
        layout.add_widget(btn_existing)

        btn_back = Button(text="Back", size_hint=(1, 0.05), height=dp(50))
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        layout.add_widget(btn_back)

        btn_home = Button(text="Home", size_hint=(1, 0.05), height=dp(50))
        btn_home.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        layout.add_widget(btn_home)

        self.add_widget(layout)

class SellerRegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[20,20,20,20])
        add_top_exit(layout)
        layout.add_widget(Label(text="Register New Seller", font_size=22, size_hint=(1,0.12)))

        self.username = TextInput(
    hint_text=fix_arabic_text("اسم المستخدم"),
    font_name="ArabicFont"
)

        
        self.password = TextInput(hint_text="New Password", multiline=False, password=True, font_size=22, size_hint=(1,0.1))
        self.msg_label = Label(text="", font_size=30, size_hint=(1,0.08), color=(1,0,0,1))

        pass_row = BoxLayout(orientation="horizontal", size_hint=(1, 1), spacing=8)
        pass_row.add_widget(self.password)
        self.reg_toggle_btn = Button(text="Show", size_hint=(0.3, 0.1), height=dp(48), font_size=22)
        self.reg_toggle_btn.bind(on_release=self.toggle_password_register)
        pass_row.add_widget(self.reg_toggle_btn)

        layout.add_widget(self.username)
        layout.add_widget(pass_row)
        layout.add_widget(self.msg_label)

        btn_register = Button(text="Register", size_hint=(1,0.1), height=dp(50))
        btn_register.bind(on_release=self.register_user)
        layout.add_widget(btn_register)

        bottom = BoxLayout(size_hint=(1,0.14), spacing=8)
        btn_back = Button(text="Back", size_hint=(0.32,1), height=dp(50))
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "seller_choice"))
        btn_home = Button(text="Home", size_hint=(0.32,1), height=dp(50))
        btn_home.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        btn_exit = Button(text="Exit", size_hint=(0.32,1), height=dp(50))
        btn_exit.bind(on_release=exit_app)
        bottom.add_widget(btn_back); bottom.add_widget(btn_home); bottom.add_widget(btn_exit)
        layout.add_widget(bottom)

        self.add_widget(layout)

    def toggle_password_register(self, instance):
        self.password.password = not self.password.password
        instance.text = "Hide" if not self.password.password else "Show"

    def register_user(self, instance):
        global users, current_user
        uname = self.username.text.strip()
        pwd = self.password.text.strip()

        if not uname or not pwd:
            self.msg_label.text = "Please fill all fields"
            return
        if uname in users:
            self.msg_label.text = "Username already exists!"
            return
        if not validate_password(pwd):
            self.msg_label.text = "Password must be 8+ chars with letters and numbers"
            return

        users[uname] = pwd
        current_user = uname
        popup = Popup(title="Welcome", content=Label(text=f"Welcome {uname}!"), size_hint=(0.8,0.4))
        popup.bind(on_dismiss=lambda *a: setattr(self.manager, "current", "seller_home"))
        popup.open()

class SellerLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[20,20,20,20])
        add_top_exit(layout)
        layout.add_widget(Label(text="Seller Login", font_size=22, size_hint=(1,0.12)))

        self.username = TextInput(hint_text="Username", multiline=False, font_size=22, size_hint=(1,0.1))
        self.password = TextInput(hint_text="Password", multiline=False, password=True, font_size=22, size_hint=(1,0.1))

        pass_row = BoxLayout(orientation="horizontal", size_hint=(1, 0.8), spacing=8)
        pass_row.add_widget(self.password)
        self.login_toggle_btn = Button(text="Show", size_hint=(0.3, 0.1), height=dp(48), font_size=22)
        self.login_toggle_btn.bind(on_release=self.toggle_password_login)
        pass_row.add_widget(self.login_toggle_btn)

        self.msg_label = Label(text="", font_size=24, size_hint=(1,0.08), color=(1,0,0,1))

        layout.add_widget(self.username)
        layout.add_widget(pass_row)
        layout.add_widget(self.msg_label)

        btn_login = Button(text="Login", size_hint=(1,0.1), height=dp(50))
        btn_login.bind(on_release=self.login)
        layout.add_widget(btn_login)

        bottom = BoxLayout(size_hint=(1,0.14), spacing=8)
        btn_back = Button(text="Back", size_hint=(0.32,1), height=dp(50))
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "seller_choice"))
        btn_home = Button(text="Home", size_hint=(0.32,1), height=dp(50))
        btn_home.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        btn_exit = Button(text="Exit", size_hint=(0.32,1), height=dp(50))
        btn_exit.bind(on_release=exit_app)
        bottom.add_widget(btn_back); bottom.add_widget(btn_home); bottom.add_widget(btn_exit)
        layout.add_widget(bottom)

        self.add_widget(layout)

    def toggle_password_login(self, instance):
        self.password.password = not self.password.password
        instance.text = "Hide" if not self.password.password else "Show"

    def login(self, instance):
        global users, current_user
        uname = self.username.text.strip()
        pwd = self.password.text.strip()
        if uname in users and users[uname] == pwd:
            current_user = uname
            popup = Popup(title="Welcome", content=Label(text=f"Welcome {uname}!"), size_hint=(0.8,0.4))
            popup.bind(on_dismiss=lambda *a: setattr(self.manager, "current", "seller_home"))
            popup.open()
        else:
            self.msg_label.text = "Wrong username or password!"

class SellerHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[12,12,12,12])
        add_top_exit(layout)
        self.welcome_label = Label(text="", font_size=28, size_hint=(1,0.10))
        layout.add_widget(self.welcome_label)
        self.title_input = TextInput(hint_text="Property Title", multiline=False, font_size=22, size_hint=(1,0.1))
        self.price_input = TextInput(hint_text="Price", multiline=False, font_size=30, size_hint=(1,0.1))
        self.desc_input = TextInput(hint_text="Description", multiline=True, font_size=22, size_hint=(1,0.25))
        layout.add_widget(self.title_input)
        layout.add_widget(self.price_input)
        layout.add_widget(self.desc_input)
        self.image_paths = []
        self.max_images = 8
        self.add_images_btn = Button(text="Add Images", size_hint=(1,0.1), height=dp(48))
        self.add_images_btn.bind(on_release=self.open_image_chooser)
        layout.add_widget(self.add_images_btn)
        self.images_grid = GridLayout(cols=4, spacing=8, size_hint_y=None)
        self.images_grid.bind(minimum_height=self.images_grid.setter('height'))
        layout.add_widget(self.images_grid)
        save_btn = Button(text="Save Property", size_hint=(1,0.1), height=dp(48))
        save_btn.bind(on_release=self.initiate_save_with_payment)
        layout.add_widget(save_btn)
        delete_account_btn = Button(text="Delete Account", size_hint=(1,0.1), height=dp(48), background_color=(0.9,0.2,0.2,1))
        delete_account_btn.bind(on_release=self.confirm_delete_account)
        layout.add_widget(delete_account_btn)
        bottom = BoxLayout(size_hint=(1,0.12), spacing=8)
        btn_back = Button(text="Back", size_hint=(0.32,1))
        btn_home = Button(text="Home", size_hint=(0.32,1))
        btn_exit = Button(text="Exit", size_hint=(0.32,1))
        btn_back.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        btn_home.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        btn_exit.bind(on_release=exit_app)
        bottom.add_widget(btn_back); bottom.add_widget(btn_home); bottom.add_widget(btn_exit)
        layout.add_widget(bottom)
        self.add_widget(layout)

    def on_pre_enter(self, *a):
        global current_user
        if current_user:
            self.welcome_label.text = f"Welcome {current_user}!"
        self.refresh_images_grid()

    def open_image_chooser(self, instance):
        if len(self.image_paths) >= self.max_images:
            p = Popup(title="Alert", content=Label(text=f"Max {self.max_images} images allowed"), size_hint=(0.7,0.3))
            p.open()
            return
        chooser = FileChooserIconView(path='/storage/emulated/0/', filters=['*.png', '*.jpg', '*.jpeg'])
        chooser.multiselect = True
        chooser.size_hint = (1, 0.6)
        info_label = Label(text=f"Selected: 0 / {self.max_images}", size_hint=(1,0.08))
        preview_grid = GridLayout(cols=4, spacing=6, size_hint_y=None)
        preview_grid.bind(minimum_height=preview_grid.setter('height'))
        scroll = ScrollView(size_hint=(1, 0.3))
        scroll.add_widget(preview_grid)
        def update_preview(instance, selection):
            preview_grid.clear_widgets()
            sel = selection or []
            count = len(sel)
            info_label.text = f"Selected: {count} / {self.max_images}"
            for p in sel:
                if os.path.isfile(p):
                    try:
                        thumb = Image(source=p, size_hint_y=None, height=dp(80))
                        preview_grid.add_widget(thumb)
                    except Exception:
                        preview_grid.add_widget(Label(text="Can't load", size_hint_y=None, height=dp(80)))
        chooser.bind(selection=update_preview)
        box = BoxLayout(orientation='vertical', spacing=8, padding=8)
        box.add_widget(chooser)
        box.add_widget(info_label)
        box.add_widget(scroll)
        def confirm_selection(btn):
            sel = chooser.selection or []
            total_after = len(self.image_paths) + len(sel)
            if total_after > self.max_images:
                p = Popup(title="Alert", content=Label(text=f"You can select up to {self.max_images} images only!"), size_hint=(0.7,0.3))
                p.open()
                return
            for s in sel:
                if s not in self.image_paths:
                    self.image_paths.append(s)
            popup.dismiss()
            self.refresh_images_grid()
        confirm_btn = Button(text="Confirm Selection", size_hint=(1,0.1), height=dp(44))
        confirm_btn.bind(on_release=confirm_selection)
        cancel_btn = Button(text="Cancel", size_hint=(1,0.1), height=dp(44))
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        box.add_widget(confirm_btn)
        box.add_widget(cancel_btn)
        popup = Popup(title="Choose Images (thumbnails) - max 8", content=box, size_hint=(0.95,0.95))
        popup.open()

    def refresh_images_grid(self):
        self.images_grid.clear_widgets()
        rows = 2
        self.images_grid.height = dp(110 * rows)
        for idx, path in enumerate(self.image_paths):
            cell = BoxLayout(orientation='vertical', spacing=4, padding=4, size_hint_y=None, height=dp(110))
            if os.path.isfile(path):
                try:
                    img = Image(source=path, allow_stretch=True, keep_ratio=True)
                    img.size_hint = (1,0.78)
                except Exception:
                    img = Label(text="Cannot load", size_hint=(1,0.78))
            else:
                img = Label(text="Missing", size_hint=(1,0.78))
            cell.add_widget(img)
            del_btn = Button(text="Delete", size_hint=(1,0.22), height=dp(36))
            def make_delete(i):
                return lambda btn: self.delete_image_at(i)
            del_btn.bind(on_release=make_delete(idx))
            cell.add_widget(del_btn)
            self.images_grid.add_widget(cell)
        for _ in range(self.max_images - len(self.image_paths)):
            placeholder = BoxLayout(size_hint_y=None, height=dp(110))
            self.images_grid.add_widget(placeholder)

    def delete_image_at(self, index):
        if 0 <= index < len(self.image_paths):
            self.image_paths.pop(index)
            self.refresh_images_grid()

    def confirm_delete_account(self, instance):
        box = BoxLayout(orientation='vertical', spacing=8, padding=8)
        box.add_widget(Label(text="Are you sure you want to delete your account?", font_size=28))
        btns = BoxLayout(size_hint=(1, 0.3), spacing=8)
        yes = Button(text="Confirm", size_hint=(0.5,1))
        no = Button(text="Cancel", size_hint=(0.5,1))
        btns.add_widget(yes); btns.add_widget(no)
        box.add_widget(btns)
        popup = Popup(title="Confirm Delete Account", content=box, size_hint=(0.8,0.4))
        yes.bind(on_release=lambda x: self.delete_account(popup))
        no.bind(on_release=lambda x: popup.dismiss())
        popup.open()

    def delete_account(self, popup):
        global users, current_user
        popup.dismiss()
        if current_user and current_user in users:
            users.pop(current_user, None)
        current_user = None
        p = Popup(title="Deleted", content=Label(text="Account deleted."), size_hint=(0.7,0.3))
        p.bind(on_dismiss=lambda *a: setattr(self.manager, "current", "start"))
        p.open()

    def initiate_save_with_payment(self, instance):
        title = self.title_input.text.strip()
        price = self.price_input.text.strip()
        desc = self.desc_input.text.strip()
        if not title:
            p = Popup(title="Error", content=Label(text="Please enter a title"), size_hint=(0.7,0.3))
            p.open()
            return
        if not self.image_paths:
            p = Popup(title="Error", content=Label(text="Please add at least one image"), size_hint=(0.7,0.3))
            p.open()
            return
        box = BoxLayout(orientation='vertical', spacing=8, padding=8)
        box.add_widget(Label(text=f"To save, please pay to: {PAYMENT_PHONE}", font_size=30))
        box.add_widget(Label(text="After you transfer the fee, press 'I Paid'. (This app simulates verification.)", font_size=28))
        btns = BoxLayout(size_hint=(1,0.25), spacing=8)
        paid_btn = Button(text="I Paid", size_hint=(0.5,1))
        cancel_btn = Button(text="Cancel", size_hint=(0.5,1))
        btns.add_widget(paid_btn); btns.add_widget(cancel_btn)
        box.add_widget(btns)
        popup = Popup(title="Payment Required", content=box, size_hint=(0.8,0.5))
        cancel_btn.bind(on_release=lambda x: popup.dismiss())
        def on_paid(btn):
            popup.dismiss()
            self.save_property_after_payment(title, price, desc)
        paid_btn.bind(on_release=on_paid)
        popup.open()

    def save_property_after_payment(self, title, price, desc):
        new_prop = {
            "area": title,
            "district": price,
            "info": desc,
            "views": 0,
            "images": list(self.image_paths)
        }
        properties.append(new_prop)
        p = Popup(title="Saved", content=Label(text="Payment Confirmed - Property Saved"), size_hint=(0.7,0.3))
        p.open()
        self.title_input.text = ""
        self.price_input.text = ""
        self.desc_input.text = ""
        self.image_paths = []
        self.refresh_images_grid()
        # placeholder for future DB sync:
        # save to a local file as staging (for now)
        try:
            with open("local_props_staging.json", "w", encoding="utf-8") as f:
                json.dump(properties, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

class BuyerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=12, padding=[12,12,12,12])
        add_top_exit(layout)
        layout.add_widget(Label(text="Properties List", font_size=22, size_hint=(1,0.1)))
        self.filter_btn = Button(text="Filter", size_hint=(1,0.1), height=dp(48))
        self.viewed_btn = Button(text="Most Viewed", size_hint=(1,0.1), height=dp(48))
        self.filter_btn.bind(on_release=lambda x: setattr(self.manager, "current", "filter"))
        self.viewed_btn.bind(on_release=self.show_most_viewed)
        layout.add_widget(self.filter_btn)
        layout.add_widget(self.viewed_btn)
        self.show_area = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.show_area.bind(minimum_height=self.show_area.setter('height'))
        scroll = ScrollView(size_hint=(1,0.6))
        scroll.add_widget(self.show_area)
        layout.add_widget(scroll)
        bottom = BoxLayout(size_hint=(1,0.12), spacing=8)
        back_btn = Button(text="Back", size_hint=(0.32,1))
        home_btn = Button(text="Home", size_hint=(0.32,1))
        exit_btn = Button(text="Exit", size_hint=(0.32,1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        home_btn.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        exit_btn.bind(on_release=exit_app)
        bottom.add_widget(back_btn); bottom.add_widget(home_btn); bottom.add_widget(exit_btn)
        layout.add_widget(bottom)
        self.add_widget(layout)

    def on_pre_enter(self, *a):
        self.show_all_properties()

    def show_all_properties(self):
        self.show_area.clear_widgets()
        sorted_props = sorted(properties, key=lambda p: (p['area'].lower(), p['district'].lower()))
        for p in sorted_props:
            info = f"{p['area']} - {p['district']} | {p['info']} | Views: {p.get('views',0)}"
            btn = Button(text=info, size_hint_y=None, height=dp(48))
            btn.bind(on_release=lambda b, prop=p: self.open_property_detail(prop))
            self.show_area.add_widget(btn)

    def open_property_detail(self, prop):
        prop['views'] = prop.get('views', 0) + 1
        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        content.add_widget(Label(text=f"{prop['area']} - {prop['district']}", font_size=24))
        content.add_widget(Label(text=prop.get('info',''), font_size=18))
        content.add_widget(Label(text=f"Views: {prop.get('views',0)}", font_size=24))
        if prop.get('images'):
            imgs_row = GridLayout(cols=4, spacing=6, size_hint_y=None)
            imgs_row.bind(minimum_height=imgs_row.setter('height'))
            for path in prop.get('images'):
                if os.path.isfile(path):
                    try:
                        thumb = Image(source=path, size_hint_y=None, height=dp(80))
                    except Exception:
                        thumb = Label(text="Can't load", size_hint_y=None, height=dp(80))
                else:
                    thumb = Label(text="Missing", size_hint_y=None, height=dp(80))
                imgs_row.add_widget(thumb)
            content.add_widget(imgs_row)
        popup = Popup(title="Property Detail", content=content, size_hint=(0.9,0.8))
        close = Button(text="Close", size_hint=(1,0.14))
        close.bind(on_release=popup.dismiss)
        content.add_widget(close)
        popup.open()

    def show_most_viewed(self, instance):
        app = App.get_running_app()
        app.filtered_props = sorted(properties, key=lambda p: p.get('views',0), reverse=True)
        setattr(self.manager, "current", "results")

class FilterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer = BoxLayout(orientation='vertical', spacing=8, padding=12)
        add_top_exit(outer)
        outer.add_widget(Label(text="Filter Properties", font_size=20, size_hint=(1,0.12)))
        self.area_input = TextInput(hint_text="Enter area (partial or full)", size_hint=(1, 0.08))
        self.district_input = TextInput(hint_text="Enter district (partial or full)", size_hint=(1, 0.08))
        outer.add_widget(self.area_input); outer.add_widget(self.district_input)
        apply = Button(text="Apply Filter", size_hint=(1, 0.1))
        apply.bind(on_release=self.apply_filter)
        outer.add_widget(apply)
        bottom = BoxLayout(size_hint=(1, 0.14), spacing=8)
        back_btn = Button(text="Back", size_hint=(0.32,1))
        home_btn = Button(text="Home", size_hint=(0.32,1))
        exit_btn = Button(text="Exit", size_hint=(0.32,1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "buyer"))
        home_btn.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        exit_btn.bind(on_release=exit_app)
        bottom.add_widget(back_btn); bottom.add_widget(home_btn); bottom.add_widget(exit_btn)
        outer.add_widget(bottom)
        self.add_widget(outer)

    def apply_filter(self, instance):
        area = self.area_input.text.strip().lower()
        district = self.district_input.text.strip().lower()
        filtered = []
        for p in properties:
            if (area == "" or area in p['area'].lower()) and (district == "" or district in p['district'].lower()):
                filtered.append(p)
        app = App.get_running_app()
        app.filtered_props = filtered
        self.manager.current = 'results'

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer = BoxLayout(orientation='vertical', spacing=8, padding=12)
        add_top_exit(outer)
        outer.add_widget(Label(text="Results", font_size=20, size_hint=(1,0.12)))
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        outer.add_widget(self.scroll)
        bottom = BoxLayout(size_hint=(1, 0.12), spacing=8)
        back_btn = Button(text="Back (to Filter)", size_hint=(0.32,1))
        home_btn = Button(text="Home", size_hint=(0.32,1))
        exit_btn = Button(text="Exit", size_hint=(0.32,1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "filter"))
        home_btn.bind(on_release=lambda x: setattr(self.manager, "current", "start"))
        exit_btn.bind(on_release=exit_app)
        bottom.add_widget(back_btn); bottom.add_widget(home_btn); bottom.add_widget(exit_btn)
        outer.add_widget(bottom)
        self.add_widget(outer)

    def on_pre_enter(self, *args):
        self.grid.clear_widgets()
        app = App.get_running_app()
        results = getattr(app, 'filtered_props', None)
        if not results:
            self.grid.add_widget(Label(text="No results. Try changing the filter.", font_size=28, size_hint_y=None, height=dp(60)))
            return
        for p in results:
            text = f"{p['area']} - {p['district']} | {p.get('info','')} | Views: {p.get('views',0)}"
            btn = Button(text=text, size_hint_y=None, height=dp(56))
            btn.bind(on_release=lambda b, prop=p: self.open_detail(prop))
            self.grid.add_widget(btn)

    def open_detail(self, prop):
        prop['views'] = prop.get('views',0) + 1
        content = BoxLayout(orientation='vertical', spacing=8, padding=8)
        content.add_widget(Label(text=f"{prop['area']} - {prop['district']}", font_size=20))
        content.add_widget(Label(text=prop.get('info',''), font_size=24))
        content.add_widget(Label(text=f"Views: {prop.get('views',0)}", font_size=24))
        if prop.get('images'):
            imgs = GridLayout(cols=4, spacing=6, size_hint_y=None)
            imgs.bind(minimum_height=imgs.setter('height'))
            for path in prop.get('images'):
                if os.path.isfile(path):
                    try:
                        thumb = Image(source=path, size_hint_y=None, height=dp(80))
                    except Exception:
                        thumb = Label(text="Can't load", size_hint_y=None, height=dp(80))
                else:
                    thumb = Label(text="Missing", size_hint_y=None, height=dp(80))
                imgs.add_widget(thumb)
            content.add_widget(imgs)
        popup = Popup(title="Property Detail", content=content, size_hint=(0.9,0.8))
        close = Button(text="Close", size_hint=(1,0.14))
        close.bind(on_release=popup.dismiss)
        content.add_widget(close)
        popup.open()

class RealEstateApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(SellerChoiceScreen(name="seller_choice"))
        sm.add_widget(SellerRegisterScreen(name="seller_register"))
        sm.add_widget(SellerLoginScreen(name="seller_login"))
        sm.add_widget(SellerHomeScreen(name="seller_home"))
        sm.add_widget(BuyerScreen(name="buyer"))
        sm.add_widget(FilterScreen(name="filter"))
        sm.add_widget(ResultsScreen(name="results"))
        self.filtered_props = []
        return sm

if __name__ == "__main__":
    RealEstateApp().run()