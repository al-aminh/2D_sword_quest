"""
# কী করছে: স্টেপ ২-এর রেন্ডার লেয়ার, বেজিয়ার রাউন্ডেড প্যানেল ও গ্রেডিয়েন্ট ফিল টেস্ট করে।
# কেন লাগছে: ওপেনজিএল প্রিমিটিভ ও থিম কালার ঠিকমতো ড্র হচ্ছে কিনা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: গ্রাফিক্স পাইপলাইন রিগ্রেশন টেস্টিং।
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import bootstrap
from src.scenes.base_scene import BaseScene
from src.render.primitives import draw_rounded_rect, draw_circle
from src.render.effects import draw_gradient_fill, ParticleBurst
from src.ui import theme
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


class Step2TestScene(BaseScene):
    def __init__(self, manager=None):
        super().__init__(manager)
        self.burst = ParticleBurst(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, 10, theme.ACCENT_PRIMARY)

    def update(self, dt: float):
        self.burst.update(dt)

    def draw(self):
        # গ্রেডিয়েন্ট স্কাই ব্যাকগ্রাউন্ড
        draw_gradient_fill(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, theme.COLOR_SKY_TOP, theme.COLOR_SKY_BOTTOM)
        # সেন্ট্রাল রাউন্ডেড প্যানেল (বেজিয়ার কোণা)
        draw_rounded_rect(200, 150, 560, 240, 24, theme.PANEL_BG, theme.PANEL_BORDER, 2.0)
        # ডেকোরেটিভ সার্কেল
        draw_circle(480, 270, 40, theme.ACCENT_PRIMARY, filled=True)
        self.burst.draw()


def run_test():
    timer = threading.Timer(0.3, lambda: os._exit(0))
    timer.daemon = True
    timer.start()
    bootstrap.run(Step2TestScene())


if __name__ == "__main__":
    run_test()
