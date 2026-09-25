"""
# কী করছে: লেভেলের শেষ প্রান্তের ফ্ল্যাগপোল ও বিজয় পতাকা রেন্ডারিং ও অ্যানিমেশন চালায়।
# কেন লাগছে: লেভেলের লক্ষ্য পূরণ শনাক্ত করা এবং খেলোয়াড়ের বিজয় নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: প্ল্যাটফর্মার গেম অবজেক্টিভ ও লেভেল কমপ্লিশন ট্রিগার।
"""

import math
from typing import Tuple
from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor4f, glLineWidth,
    GL_QUADS, GL_LINES
)
from src.core.config import (
    FLAGPOLE_X, FLAGPOLE_Y, FLAGPOLE_HEIGHT, FLAG_WIDTH, FLAG_HEIGHT
)
from src.render.primitives import draw_circle
from src.ui import theme


class Flagpole:
    """
    # কী করছে: পতাকাদণ্ড, চলমান পতাকার দোলা ও প্লেয়ার স্পর্শের কোলিশন বাউন্ডারি ধরে রাখে।
    # কেন লাগছে: গেমের ফিনিশ লাইন হিসেবে দৃশ্যমান প্রতীক উপস্থাপন করতে।
    # real world-এ এটা কোথায় দেখা যায়: লেভেল গোল এনটিটি।
    """

    # কী করছে: পতাকাদণ্ডের অবস্থান ও অ্যানিমেশন ভ্যারিয়েবল ইনিশিয়ালাইজ করে।
    # কেন লাগছে: লেভেলের শেষে নির্দিষ্ট স্থানাঙ্কে পতাকা স্থাপন করতে।
    # real world-এ এটা কোথায় দেখা যায়: অবজেক্টিভ স্পনার।
    def __init__(self, x: float = FLAGPOLE_X, y: float = FLAGPOLE_Y):
        self.x = x
        self.y = y
        self.height = FLAGPOLE_HEIGHT
        self.flag_w = FLAG_WIDTH
        self.flag_h = FLAG_HEIGHT
        self.wave_time = 0.0
        self.is_reached = False

    # কী করছে: বাতাসে পতাকার তরঙ্গায়িত দোলা প্রতি ফ্রেমে আপডেট করে।
    # কেন লাগছে: পতাকায় জীবন্ত অ্যানিমেশন ও বাতাসের দোলা দৃশ্যমান করতে।
    # real world-এ এটা কোথায় দেখা যায়: সাইনোসয়েডাল ক্লথ সিমুলেশন।
    def update(self, dt: float):
        self.wave_time += dt * 4.5

    # কী করছে: পতাকাদণ্ডের বাউন্ডিং বক্স প্রদান করে।
    # কেন লাগছে: প্লেয়ার পতাকা স্পর্শ করেছে কিনা তা পরীক্ষা করতে।
    # real world-এ এটা কোথায় দেখা যায়: গোল ভলিউম চেকার।
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        return (self.x - 12.0, self.y, self.x + 24.0, self.y + self.height)

    # কী করছে: পতাকাদণ্ড ও শীর্ষের সোনালী গোলক স্ক্রিনে আঁকে।
    # কেন লাগছে: মজবুত ধাতব খুঁটি ফুটিয়ে তুলতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def _draw_pole(self):
        # গোড়ার ভিত্তি
        glColor4f(*theme.COLOR_PLATFORM)
        glBegin(GL_QUADS)
        glVertex2f(self.x - 16.0, self.y)
        glVertex2f(self.x + 16.0, self.y)
        glVertex2f(self.x + 12.0, self.y + 16.0)
        glVertex2f(self.x - 12.0, self.y + 16.0)
        glEnd()

        # উল্লম্ব দণ্ড
        glColor4f(0.85, 0.88, 0.95, 1.0)
        glLineWidth(3.5)
        glBegin(GL_LINES)
        glVertex2f(self.x, self.y + 16.0)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

        # শীর্ষ গোলক
        draw_circle(self.x, self.y + self.height, 7.0, theme.ACCENT_GOLD, filled=True, segments=12)

    # কী করছে: বাতাসে দোদুল্যমান উজ্জ্বল বিজয় পতাকা আঁকে।
    # কেন লাগছে: জয়ের আনন্দময় সংকেত ফুটিয়ে তুলতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def _draw_flag(self):
        wave = math.sin(self.wave_time) * 4.5
        top_y = self.y + self.height - 10.0
        bot_y = top_y - self.flag_h

        # গ্রেডিয়েন্ট ফিলসহ পতাকা কোয়াড
        glBegin(GL_QUADS)
        glColor4f(*theme.ACCENT_PRIMARY)
        glVertex2f(self.x + 2.0, bot_y)
        glColor4f(*theme.ACCENT_GOLD)
        glVertex2f(self.x + 2.0 + self.flag_w, bot_y + wave)
        glVertex2f(self.x + 2.0 + self.flag_w, top_y + wave)
        glColor4f(*theme.ACCENT_PRIMARY)
        glVertex2f(self.x + 2.0, top_y)
        glEnd()

    # কী করছে: সম্পূর্ণ ফ্ল্যাগপোল অবজেক্ট স্ক্রিনে রেন্ডার করে।
    # কেন লাগছে: গেমের ফিনিশিং এলাকা দৃশ্যমান করতে।
    # real world-এ এটা কোথায় দেখা যায়: অবজেক্ট রেন্ডার ডিসপ্যাচ।
    def draw(self):
        self._draw_pole()
        self._draw_flag()
