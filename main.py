import os
import ssl
import urllib.request
import webbrowser

# SSL Bypass to prevent download errors on Android
ssl._create_default_https_context = ssl._create_unverified_context

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# Deep cosmic blue/black background
Window.clearcolor = get_color_from_hex('#050814')

# 1. Download Helper for White Outline Icons
def fetch_icon(url, filename):
    cache_dir = "neon_icons"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    filepath = os.path.join(cache_dir, filename)
    
    if not os.path.exists(filepath):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            
    return filepath

# 2. Glassmorphic Neon Button
class NeonGlassButton(ButtonBehavior, BoxLayout):
    def __init__(self, theme_color_hex, text, icon_path, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = [15, 15, 15, 15] 
        self.spacing = 15 
        
        self.theme_color = get_color_from_hex(theme_color_hex)
        
        with self.canvas.before:
            # Semi-transparent glass background
            Color(rgba=(0.05, 0.08, 0.15, 0.6))
            self.bg_rect = RoundedRectangle(radius=[15])
            
            # Glowing Neon Border
            Color(rgba=self.theme_color)
            self.border = Line(width=1.2, rounded_rectangle=[self.x, self.y, self.width, self.height, 15])
            
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        
        # Tint the white outline icon to match the neon border color
        self.icon = Image(source=icon_path, fit_mode="contain", color=self.theme_color, size_hint=(0.35, 1))
        self.add_widget(self.icon)
        
        self.text_lbl = Label(
            text=text, bold=True, font_size='14sp', 
            color=(0.9, 0.9, 0.9, 1), halign='left', valign='middle'
        )
        self.text_lbl.bind(size=self.text_lbl.setter('text_size'))
        self.add_widget(self.text_lbl)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, 15]

# 3. Animated Footer
class RainbowLabel(Label):
    def __init__(self, base_text, **kwargs):
        super().__init__(**kwargs)
        self.base_text = base_text
        self.markup = True
        self.colors = ['#FF0055', '#FFaa00', '#00FFaa', '#00aaff', '#aa00ff']
        self.offset = 0
        Clock.schedule_interval(self.update_colors, 0.2)
        
    def update_colors(self, dt):
        colored_text = "[i]"
        for i, char in enumerate(self.base_text):
            if char == " ":
                colored_text += " "
                continue
            color = self.colors[(i + self.offset) % len(self.colors)]
            colored_text += f"[color={color}]{char}[/color]"
        colored_text += "[/i]"
        self.text = colored_text
        self.offset += 1

class DocumentCheckerApp(App):
    def build(self):
        root_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        main_layout = BoxLayout(orientation='vertical', padding=25, spacing=20, size_hint=(1, 1))
        
        # Header
        header = BoxLayout(orientation='vertical', size_hint=(1, 0.15))
        title = Label(
            text="[b]DOCUMENT CHECKER[/b]", 
            markup=True, font_size='22sp', color=get_color_from_hex('#00FFFF'),
            halign='center', valign='middle'
        )
        title.bind(size=title.setter('text_size')) 
        header.add_widget(title)
        main_layout.add_widget(header)

        # Main Grid
        grid = GridLayout(cols=2, spacing=15, size_hint=(1, 0.65))
        
        # Icons
        aadhaar_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/fingerprint.png", "aadhaar_out.png")
        validity_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/user-shield.png", "validity_out.png")
        birth_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/certificate.png", "birth_out.png")
        ration_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/wheat.png", "ration_out.png")
        pan_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/bank-cards.png", "pan_out.png")
        update_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/synchronize.png", "update_out.png")
        dl_img = fetch_icon("https://img.icons8.com/ios/100/ffffff/download-from-cloud.png", "dl_out.png")

        features = [
            ("AADHAR\nDOWNLOAD", "https://myaadhaar.uidai.gov.in/genricDownloadAadhaar/en", "#FF3366", aadhaar_img),
            ("AADHAR\nVALIDITY", "https://myaadhaar.uidai.gov.in/check-aadhaar-validity/en", "#00FFCC", validity_img),
            ("BIRTH\nCERTIFICATE", "https://janma-mrityutathya.wb.gov.in/verifycertificate", "#9966FF", birth_img),
            ("RATION CARD\nCHECK", "https://wbpds.wb.gov.in/(S(0l5dlttphtqhmbabibdwkusp))/CheckRationCDetails.aspx", "#FF9933", ration_img),
            ("PAN CARD\nCHECK", "https://eportal.incometax.gov.in/iec/foservices/#/pre-login/verifyYourPAN/1", "#FF3399", pan_img),
            ("UPDATE\nSTATUS", "https://myaadhaar.uidai.gov.in/CheckAadhaarStatus/en", "#FFCC00", update_img),
        ]

        for text, link, color, icon_path in features:
            btn = NeonGlassButton(theme_color_hex=color, text=text, icon_path=icon_path)
            btn.bind(on_press=lambda instance, u=link: webbrowser.open(u))
            grid.add_widget(btn)
            
        main_layout.add_widget(grid)
        
        # Bottom Button
        bottom_btn = NeonGlassButton(
            theme_color_hex="#33CCFF", text="RATION CARD DOWNLOAD", icon_path=dl_img, size_hint=(1, 0.15)
        )
        bottom_btn.bind(on_press=lambda instance: webbrowser.open("https://food.wb.gov.in/")) 
        main_layout.add_widget(bottom_btn)
        
        # Footer
        footer = RainbowLabel(
            base_text="Developed by NITU", 
            size_hint=(1, 0.05), font_size='12sp', halign='right', valign='bottom'
        )
        footer.bind(size=footer.setter('text_size'))
        main_layout.add_widget(footer)

        root_anchor.add_widget(main_layout)
        return root_anchor


if __name__ == '__main__':
    DocumentCheckerApp().run()
