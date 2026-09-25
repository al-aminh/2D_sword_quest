"""
# কী করছে: প্রধান মেনু সিন তৈরি করে, যাতে অ্যানিমেটেড টাইটেল এবং ইন্টার‍্যাক্টিভ বোতাম রয়েছে।
# কেন লাগছে: গেম শুরুর প্রারম্ভিক আধুনিক ইন্টারফেস এবং ব্যবহারকারীকে খেলা শুরু করার সুযোগ দিতে।
# real world-এ এটা কোথায় দেখা যায়: গেম মেইন মেনু সিস্টেম ও স্টার্ট স্ক্রিন ফ্লো।
"""

import sys
from OpenGL.GLUT import GLUT_DOWN, GLUT_UP, GLUT_LEFT_BUTTON
from src.scenes.base_scene import BaseScene
from src.render.effects import draw_gradient_fill
from src.render.text import draw_stroke_text, get_stroke_text_width
from src.physics.curves import ease_out_cubic, lerp
from src.ui.panel import Panel
from src.ui.button import Button
from src.ui import theme
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.app.input import global_input


class MenuScene(BaseScene):
    """
    # কী করছে: গেমের মেইন মেনুর গ্রাফিক্স, টাইটেল এন্ট্রান্স অ্যানিমেশন ও বাটন ইন্টার‍্যাকশন পরিচালনা করে।
    # কেন লাগছে: প্লেয়ার যাতে মাউস দিয়ে সহজে গেম স্টার্ট বা প্রস্থান করতে পারে।
    # real world-এ এটা কোথায় দেখা যায়: গেম ফ্রন্ট-এন্ড ইউআই আর্কিটেকচার।
    """

    # কী করছে: মেনু সিনের প্যানেল, বাটন ও অ্যানিমেশন টাইমার ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্রাথমিক অবস্থায় বাটন পজিশন ও ট্রানজিশন ক্লক সেট করতে।
    # real world-এ এটা কোথায় দেখা যায়: সিন লাইফসাইকেল কনস্ট্রাক্টর।
    def __init__(self, manager=None):
        super().__init__(manager)
        self.elapsed_time = 0.0
        self.intro_duration = 0.55

        panel_w = 460.0
        panel_h = 240.0
        panel_x = (SCREEN_WIDTH - panel_w) * 0.5
        panel_y = 110.0
        self.panel = Panel(panel_x, panel_y, panel_w, panel_h, radius=20.0)

        btn_w = 280.0
        btn_h = 50.0
        btn_x = (SCREEN_WIDTH - btn_w) * 0.5

        self.btn_play = Button("PLAY GAME", btn_x, panel_y + 130.0, btn_w, btn_h, self._on_play_click)
        self.btn_quit = Button("QUIT", btn_x, panel_y + 50.0, btn_w, btn_h, self._on_quit_click)

    # কী করছে: প্লে বাটনে ক্লিক হলে প্লেয়িং সিনে যাওয়ার নির্দেশ দেয়।
    # কেন লাগছে: খেলা শুরু করার জন্য সিন ট্রানজিশন ট্রিগার করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যাকশন ইভেন্ট ডিসপ্যাচ ও স্টেট নেভিগেশন।
    def _on_play_click(self):
        if self.manager:
            from src.scenes.play_scene import PlayScene
            self.manager.switch_to(PlayScene(self.manager), with_transition=True)

    # কী করছে: ক্যুইট বাটনে ক্লিক হলে ওপেনজিএল উইন্ডো ও অ্যাপ্লিকেশন বন্ধ করে।
    # কেন লাগছে: গ্লুট মেইনলুপের ভেতর থেকে কোনো এক্সেপশন ক্র্যাশ ছাড়াই অ্যাপ্লিকেশন বন্ধ করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যাপ্লিকেশন লাইফসাইকেল টার্মিনেশন।
    def _on_quit_click(self):
        try:
            from OpenGL.GLUT import glutLeaveMainLoop
            glutLeaveMainLoop()
        except Exception:
            pass
        import os
        os._exit(0)

    # কী করছে: টাইটেল ও বাটনের হোভার অ্যানিমেশন প্রতি ফ্রেমে আপডেট করে।
    # কেন লাগছে: মাউসের অবস্থানের সাথে বাটনের মসৃণ প্রতিক্রিয়া নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: UI Tick ও অ্যানিমেশন লুপ।
    def update(self, dt: float):
        self.elapsed_time += dt
        mx = global_input.mouse_x
        my = global_input.mouse_y
        self.btn_play.update(dt, mx, my)
        self.btn_quit.update(dt, mx, my)

    # কী করছে: মাউস ক্লিক ও মুভমেন্ট ইভেন্ট বাটনে পাঠায়।
    # কেন লাগছে: মাউসের বোতাম টিপলে বা কার্সার সরালে বাটন স্টেট পরিবর্তন করতে।
    # real world-এ এটা কোথায় দেখা যায়: মাউস ইভেন্ট লিসেনার প্রপাগেশন।
    def on_mouse(self, x: float, y: float, button: int = -1, state: int = -1):
        self.btn_play.update(0.016, x, y)
        self.btn_quit.update(0.016, x, y)
        if button == GLUT_LEFT_BUTTON:
            is_down = (state == GLUT_DOWN)
            self.btn_play.handle_click(x, y, is_down)
            self.btn_quit.handle_click(x, y, is_down)

    # কী করছে: মেনু সিনের সমস্ত উপাদান (ব্যাকগ্রাউন্ড, প্যানেল, টাইটেল, বাটন) স্ক্রিনে আঁকে।
    # কেন লাগছে: আধুনিক ডার্ক থিমের স্টার্ট স্ক্রিন ব্যবহারকারীকে প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        draw_gradient_fill(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, theme.COLOR_SKY_TOP, theme.COLOR_SKY_BOTTOM)
        self.panel.draw()

        # অ্যানিমেটেড টাইটেল ইজিং
        progress = min(1.0, self.elapsed_time / self.intro_duration)
        eased_p = ease_out_cubic(progress)
        title_y = lerp(SCREEN_HEIGHT - 60.0, SCREEN_HEIGHT - 130.0, eased_p)
        title_alpha = eased_p

        title_text = "SWORD QUEST"
        t_scale = 0.38
        t_w = get_stroke_text_width(title_text, t_scale)
        tx = (SCREEN_WIDTH - t_w) * 0.5
        t_color = (theme.ACCENT_PRIMARY[0], theme.ACCENT_PRIMARY[1], theme.ACCENT_PRIMARY[2], title_alpha)
        draw_stroke_text(title_text, tx, title_y, scale=t_scale, color=t_color, line_width=3.5)

        # সাব-হেডিং
        sub_text = "2D MELEE PLATFORMER"
        sub_scale = 0.13
        sub_w = get_stroke_text_width(sub_text, sub_scale)
        sx = (SCREEN_WIDTH - sub_w) * 0.5
        s_color = (theme.COLOR_TEXT_MUTED[0], theme.COLOR_TEXT_MUTED[1], theme.COLOR_TEXT_MUTED[2], title_alpha * 0.9)
        draw_stroke_text(sub_text, sx, title_y - 32.0, scale=sub_scale, color=s_color, line_width=1.8)

        self.btn_play.draw()
        self.btn_quit.draw()
