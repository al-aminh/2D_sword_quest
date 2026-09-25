"""
# কী করছে: গেম সাময়িক স্থগিত (Pause) রাখার দৃশ্য তৈরি করে যা ব্যাকগ্রাউন্ডকে অক্ষুণ্ণ রাখে।
# কেন লাগছে: গেমপ্লে না মুছে খেলোয়াড়কে বিরতি দেওয়া এবং রিজিউম/রিস্টার্টের সুযোগ দিতে।
# real world-এ এটা কোথায় দেখা যায়: গেম পজ মেনু ও সাব-স্টেট ওভারলে সিস্টেম।
"""

from OpenGL.GL import glBegin, glEnd, glVertex2f, glColor4f, GL_QUADS
from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_DOWN
from src.scenes.base_scene import BaseScene
from src.ui.panel import Panel
from src.ui.button import Button
from src.render.text import draw_stroke_text, get_stroke_text_width
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.app.input import global_input
from src.ui import theme


class PauseScene(BaseScene):
    """
    # কী করছে: চলমান গেমের ওপর সেমি-ট্রান্সপারেন্ট পজ প্যানেল ও বাটন প্রদর্শন করে।
    # কেন লাগছে: খেলা রদবদল না করে ব্যবহারকারীকে পুনরায় চালুর সুবিধা দিতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন মোডাল ডায়ালগ বক্স।
    """

    # কী করছে: পজ সিনের উপাদান এবং ব্যাকগ্রাউন্ড প্লে সিনের রেফারেন্স সংরক্ষণ করে।
    # কেন লাগছে: পূর্বের গেমের অগ্রগতি ধরে রাখতে এবং বাটন সেটআপ করতে।
    # real world-এ এটা কোথায় দেখা যায়: পজ কন্ট্রোলার কনস্ট্রাক্টর।
    def __init__(self, manager, play_scene):
        super().__init__(manager)
        self.play_scene = play_scene

        pw, ph = 380.0, 260.0
        px = (SCREEN_WIDTH - pw) * 0.5
        py = (SCREEN_HEIGHT - ph) * 0.5 - 20.0
        self.panel = Panel(px, py, pw, ph, radius=20.0)

        bw, bh = 240.0, 44.0
        bx = (SCREEN_WIDTH - bw) * 0.5
        self.btn_resume = Button("RESUME", bx, py + 150.0, bw, bh, self._on_resume)
        self.btn_restart = Button("RESTART", bx, py + 95.0, bw, bh, self._on_restart)
        self.btn_quit = Button("QUIT TO MENU", bx, py + 40.0, bw, bh, self._on_quit)

    # কী করছে: গেম স্থগিতাবস্থা তুলে নিয়ে পুনরায় খেলা চালু করে।
    # কেন লাগছে: প্লেয়ার রেজ্যুম টিপলে খেলায় ফিরে যেতে।
    # real world-এ এটা কোথায় দেখা যায়: আনপজ স্টেট ট্রানজিশন।
    def _on_resume(self):
        if self.manager:
            self.manager.switch_to(self.play_scene, with_transition=False)

    # কী করছে: নতুন গেমপ্লে শুরু করার নির্দেশ দেয়।
    # কেন লাগছে: প্রথম থেকে লেভেল রি-স্টার্ট করতে।
    # real world-এ এটা কোথায় দেখা যায়: লেভেল রিলোডার মেকানিজম।
    def _on_restart(self):
        if self.manager:
            from src.scenes.play_scene import PlayScene
            self.manager.switch_to(PlayScene(self.manager), with_transition=True)

    # কী করছে: মূল মেনু স্ক্রিনে ফেরত পাঠায়।
    # কেন লাগছে: বর্তমান খেলা শেষ করে মেইন মেনুতে যেতে।
    # real world-এ এটা কোথায় দেখা যায়: মেনু নেভিগেশন ডিসপ্যাচ।
    def _on_quit(self):
        if self.manager:
            from src.scenes.menu_scene import MenuScene
            self.manager.switch_to(MenuScene(self.manager), with_transition=True)

    # কী করছে: পজ মেনুর বোতামগুলোর হোভার অ্যানিমেশন আপডেট করে।
    # কেন লাগছে: গেমপ্লে না চালিয়েও বাটন ইন্টার‍্যাকশন সচল রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: UI Tick While Paused।
    def update(self, dt: float):
        mx = global_input.mouse_x
        my = global_input.mouse_y
        self.btn_resume.update(dt, mx, my)
        self.btn_restart.update(dt, mx, my)
        self.btn_quit.update(dt, mx, my)

    # কী করছে: মাউস ক্লিক ইভেন্ট প্রসেস করে বাটনে পাঠায়।
    # কেন লাগছে: মাউস ক্লিকে মেনু অ্যাকশন ট্রিগার করতে।
    # real world-এ এটা কোথায় দেখা যায়: মোডাল মাউস ইভেন্ট ক্যাপচার।
    def on_mouse(self, x: float, y: float, button: int = -1, state: int = -1):
        self.btn_resume.update(0.016, x, y)
        self.btn_restart.update(0.016, x, y)
        self.btn_quit.update(0.016, x, y)
        if button == GLUT_LEFT_BUTTON:
            is_down = (state == GLUT_DOWN)
            self.btn_resume.handle_click(x, y, is_down)
            self.btn_restart.handle_click(x, y, is_down)
            self.btn_quit.handle_click(x, y, is_down)

    # কী করছে: ESC চাপলে তৎক্ষণাৎ রেজ্যুম করে খেলায় ফেরে।
    # কেন লাগছে: কীবোর্ডের মাধ্যমে সহজে পজ টগল করতে।
    # real world-এ এটা কোথায় দেখা যায়: কীবোর্ড শর্টকাট একশন হ্যান্ডলার।
    def on_key(self, key: str, is_down: bool):
        if is_down and key == 'escape':
            self._on_resume()

    # কী করছে: ফ্রোজেন গেমপ্লে এবং সেমি-ট্রান্সপারেন্ট ডার্ক ওভারলেসহ পজ মেনু আঁকে।
    # কেন লাগছে: নেপথ্যে গেমটি অপরিবর্তিত রেখে স্পষ্ট পজ ইউআই প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        # পেছনের মূল গেমপ্লে আঁকা
        self.play_scene.draw()

        # ফুল-স্ক্রিন ডার্ক ট্রান্সলুসেন্ট ফেড
        glColor4f(0.04, 0.05, 0.07, 0.72)
        glBegin(GL_QUADS)
        glVertex2f(0.0, 0.0)
        glVertex2f(float(SCREEN_WIDTH), 0.0)
        glVertex2f(float(SCREEN_WIDTH), float(SCREEN_HEIGHT))
        glVertex2f(0.0, float(SCREEN_HEIGHT))
        glEnd()

        self.panel.draw()

        # "PAUSED" শিরোনাম
        title = "PAUSED"
        scale = 0.30
        tw = get_stroke_text_width(title, scale)
        tx = (SCREEN_WIDTH - tw) * 0.5
        ty = self.panel.y + self.panel.h + 15.0
        draw_stroke_text(title, tx, ty, scale=scale, color=theme.ACCENT_PRIMARY, line_width=3.0)

        self.btn_resume.draw()
        self.btn_restart.draw()
        self.btn_quit.draw()
