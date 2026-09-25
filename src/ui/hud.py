"""
# কী করছে: গেমের হেডস-আপ ডিসপ্লে (HUD) যা স্কোর, জীবন ও অতিবাহিত সময় প্রদর্শন করে।
# কেন লাগছে: গেমপ্লে চলাকালীন খেলোয়াড়কে রিয়েল-টাইম স্ট্যাটাস সহজে অবগত করতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন ইউজার ইন্টারফেস ও ওএসডি ইনফো প্যানেল।
"""

from src.render.primitives import draw_rounded_rect, draw_circle
from src.render.text import draw_stroke_text, draw_bitmap_text
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui import theme


class HUD:
    """
    # কী করছে: ইন-গেম স্কোরবোর্ড, হার্টস ও টাইম কাউন্টার প্যানেল রেন্ডার করে।
    # কেন লাগছে: পরিষ্কার ও মার্জিত ডিজাইনে গেমের গুরুত্বপূর্ণ তথ্য উপস্থাপন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ডেক্সটপ উইজেট ও ড্যাশবোর্ড স্ট্যাটাস বার।
    """

    # কী করছে: হাড উইজেটের প্রারম্ভিক প্যানেল সাইজ ও স্থানাঙ্ক নির্ধারণ করে।
    # কেন লাগছে: স্ক্রিনের উপরের বাম কোণে প্যানেলটি নির্দিষ্ট স্থানে বসাতে।
    # real world-এ এটা কোথায় দেখা যায়: ইউআই লেআউট ইনিশিয়ালাইজার।
    def __init__(self):
        self.panel_x = 24.0
        self.panel_y = SCREEN_HEIGHT - 62.0
        self.panel_w = 340.0
        self.panel_h = 46.0

    # কী করছে: প্লেয়ারের অবশিষ্ট জীবন লাল হার্ট ও সংখ্যা দিয়ে স্ক্রিনে আঁকে।
    # কেন লাগছে: খেলোয়াড়ের কতটি সুযোগ বাকি আছে তা স্পষ্টভাবে তুলে ধরতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def _draw_lives(self, lives: int):
        draw_stroke_text("LIVES:", self.panel_x + 16.0, self.panel_y + 14.0, scale=0.12, color=theme.COLOR_TEXT_MUTED)
        # হার্ট আইকন সার্কেল
        start_hx = self.panel_x + 85.0
        for i in range(max(0, lives)):
            cx = start_hx + i * 16.0
            draw_circle(cx, self.panel_y + 22.0, 5.0, theme.COLOR_HEALTH_HEART, filled=True, segments=12)

    # কী করছে: অর্জিত স্কোর ও মোট সময় বিটম্যাপ এবং স্ট্রোক ফন্ট দিয়ে আঁকে।
    # কেন লাগছে: টেক্সট লেবেলে স্ট্রোক ফন্ট ও সংখ্যায় স্পষ্ট বিটম্যাপ ফন্ট সমন্বয় করতে।
    # real world-এ এটা কোথায় দেখা যায়: ভেক্টর ও রাস্টার হাইব্রিড টেক্সট ডিসপ্লে।
    def _draw_stats(self, score: int, elapsed_time: float):
        # স্কোর টেক্সট
        draw_stroke_text("SCORE:", self.panel_x + 145.0, self.panel_y + 14.0, scale=0.12, color=theme.COLOR_TEXT_MUTED)
        score_str = f"{score:05d}"
        draw_bitmap_text(score_str, self.panel_x + 210.0, self.panel_y + 16.0, theme.ACCENT_GOLD)

        # সময় টেক্সট
        time_str = f"{int(elapsed_time)}s"
        draw_stroke_text("TIME:", self.panel_x + 265.0, self.panel_y + 14.0, scale=0.12, color=theme.COLOR_TEXT_MUTED)
        draw_bitmap_text(time_str, self.panel_x + 310.0, self.panel_y + 16.0, theme.COLOR_WHITE)

    # কী করছে: শীর্ষ কোণায় নির্দেশিকা (কন্ট্রোলস গাইড) আঁকে।
    # কেন লাগছে: নতুন খেলোয়াড় যাতে কিবোর্ড বোতাম সহজে মনে রাখতে পারে।
    # real world-এ এটা কোথায় দেখা যায়: ইন-গেম টিপস ও শর্টকাট ওভারলে।
    def _draw_controls_hint(self):
        hint = "A/D: Move | SPACE: Jump | F: Sword | ESC: Pause"
        hx = SCREEN_WIDTH - 380.0
        draw_stroke_text(hint, hx, SCREEN_HEIGHT - 38.0, scale=0.09, color=theme.COLOR_TEXT_MUTED, line_width=1.2)

    # কী করছে: সম্পূর্ণ হাড প্যানেল ও সব পরিসংখ্যান স্ক্রিনে আঁকে।
    # কেন লাগছে: গেমপ্লে চলাকালীন ফ্রেমবাফারে ড্যাশবোর্ড ফুটিয়ে তুলতে।
    # real world-এ এটা কোথায় দেখা যায়: গেমপ্লে রেন্ডার পাস (HUD Pass)।
    def draw(self, score: int, lives: int, elapsed_time: float):
        # রাউন্ডেড বেজিয়ার ব্যাকগ্রাউন্ড প্যানেল
        draw_rounded_rect(
            self.panel_x, self.panel_y, self.panel_w, self.panel_h,
            radius=12.0, fill_color=theme.PANEL_BG, border_color=theme.PANEL_BORDER, border_width=1.5
        )
        self._draw_lives(lives)
        self._draw_stats(score, elapsed_time)
        self._draw_controls_hint()
