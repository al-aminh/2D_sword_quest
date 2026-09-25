"""
# কী করছে: গেম সমাপ্তির সারাংশ দৃশ্য (জয় অথবা পরাজয়) এবং স্কোরবোর্ড পরিচালনা করে।
# কেন লাগছে: খেলার ফলাফল প্রদর্শন এবং পুনরায় খেলার বোতাম প্রদান করতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ওভার / ভিক্টরি স্ক্রিন ও রেজাল্ট ডিসপ্লে।
"""

from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_DOWN
from src.scenes.base_scene import BaseScene
from src.ui.panel import Panel
from src.ui.button import Button
from src.render.effects import draw_gradient_fill
from src.render.text import draw_stroke_text, draw_bitmap_text, get_stroke_text_width
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.app.input import global_input
from src.ui import theme


class EndScene(BaseScene):
    """
    # কী করছে: জয় কিংবা পরাজয়ের সারাংশ, পরিসংখ্যান এবং পুনরায় খেলার সুযোগ উপস্থাপন করে।
    # কেন লাগছে: গেমের পরিসমাপ্তিতে স্পষ্ট প্রতিক্রিয়া প্রদান করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম রেজাল্ট স্ক্রিন ক্লাস।
    """

    # কী করছে: এন্ড সিনের ডাটা, স্কোর ও বাটন ইনিশিয়ালাইজ করে।
    # কেন লাগছে: ফলাফল সংক্রান্ত মান সংরক্ষণ ও বোতাম প্রস্তুত করতে।
    # real world-এ এটা কোথায় দেখা যায়: এন্ড-গেম কন্ট্রোলার ইনিশিয়ালাইজেশন।
    def __init__(self, manager, is_win: bool, score: int, elapsed_time: float):
        super().__init__(manager)
        self.is_win = is_win
        self.score = score
        self.elapsed_time = elapsed_time

        pw, ph = 460.0, 300.0
        px = (SCREEN_WIDTH - pw) * 0.5
        py = 80.0
        self.panel = Panel(px, py, pw, ph, radius=22.0)

        bw, bh = 260.0, 48.0
        bx = (SCREEN_WIDTH - bw) * 0.5
        self.btn_replay = Button("PLAY AGAIN", bx, py + 95.0, bw, bh, self._on_replay)
        self.btn_menu = Button("MAIN MENU", bx, py + 35.0, bw, bh, self._on_menu)

    # কী করছে: পুনরায় নতুন গেমপ্লে আরম্ভ করে।
    # কেন লাগছে: খেলোয়াড় আবার সাথে সাথে খেলতে চাইলে তা চালু করতে।
    # real world-এ এটা কোথায় দেখা যায়: কুইক রিস্টার্ট ফ্লো।
    def _on_replay(self):
        if self.manager:
            from src.scenes.play_scene import PlayScene
            self.manager.switch_to(PlayScene(self.manager), with_transition=True)

    # কী করছে: প্রধান মেনু সিনে ফেরত নিয়ে যায়।
    # কেন লাগছে: মেইন মেনু নেভিগেশন সচল রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: ব্যাক টু টাইটেল স্ক্রিন অ্যাকশন।
    def _on_menu(self):
        if self.manager:
            from src.scenes.menu_scene import MenuScene
            self.manager.switch_to(MenuScene(self.manager), with_transition=True)

    # কী করছে: বোতামগুলোর হোভার অ্যানিমেশন আপডেট করে।
    # কেন লাগছে: মাউসের অবস্থানের সাথে বোতামের ভিজ্যুয়াল রেসপন্স দিতে।
    # real world-এ এটা কোথায় দেখা যায়: UI Tick Update।
    def update(self, dt: float):
        mx = global_input.mouse_x
        my = global_input.mouse_y
        self.btn_replay.update(dt, mx, my)
        self.btn_menu.update(dt, mx, my)

    # কী করছে: মাউস ক্লিক ইভেন্ট প্রক্রিয়া করে।
    # কেন লাগছে: বাটন ক্লিকে প্রতিক্রিয়া জানাতে।
    # real world-এ এটা কোথায় দেখা যায়: মাউস ইভেন্ট লিসেনার।
    def on_mouse(self, x: float, y: float, button: int = -1, state: int = -1):
        self.btn_replay.update(0.016, x, y)
        self.btn_menu.update(0.016, x, y)
        if button == GLUT_LEFT_BUTTON:
            is_down = (state == GLUT_DOWN)
            self.btn_replay.handle_click(x, y, is_down)
            self.btn_menu.handle_click(x, y, is_down)

    # কী করছে: স্কোর এবং সমাপ্তি সময় তথ্য টেক্সট আকারে আঁকে।
    # কেন লাগছে: খেলোয়াড়কে তার সাফল্য ও পরিসংখ্যান অবগত করতে।
    # real world-এ এটা কোথায় দেখা যায়: স্কোরবোর্ড সামারি রেন্ডারিং।
    def _draw_summary_info(self):
        center_x = SCREEN_WIDTH * 0.5
        # স্কোর
        sc_txt = f"FINAL SCORE: {self.score}"
        tw = get_stroke_text_width(sc_txt, 0.16)
        draw_stroke_text(sc_txt, center_x - tw * 0.5, self.panel.y + 220.0, scale=0.16, color=theme.ACCENT_GOLD)

        # সময়
        tm_txt = f"TIME: {self.elapsed_time:.1f} SECONDS"
        tw2 = get_stroke_text_width(tm_txt, 0.13)
        draw_stroke_text(tm_txt, center_x - tw2 * 0.5, self.panel.y + 175.0, scale=0.13, color=theme.COLOR_TEXT_BODY)

    # কী করছে: এন্ড স্ক্রিনের টাইটেল, প্যানেল ও বোতাম স্ক্রিনে আঁকে।
    # কেন লাগছে: মার্জিত থিমে খেলার ফলাফল প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        draw_gradient_fill(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, theme.COLOR_SKY_TOP, theme.COLOR_SKY_BOTTOM)
        self.panel.draw()

        # শিরোনাম
        title = "VICTORY!" if self.is_win else "GAME OVER"
        t_col = theme.ACCENT_GOLD if self.is_win else theme.COLOR_ENEMY
        scale = 0.40
        tw = get_stroke_text_width(title, scale)
        tx = (SCREEN_WIDTH - tw) * 0.5
        draw_stroke_text(title, tx, SCREEN_HEIGHT - 110.0, scale=scale, color=t_col, line_width=4.0)

        self._draw_summary_info()
        self.btn_replay.draw()
        self.btn_menu.draw()
