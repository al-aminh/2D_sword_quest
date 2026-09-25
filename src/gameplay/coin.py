"""
# কী করছে: সংগ্রাহ্য গোল্ড কয়েন তৈরি করে যা স্কেলিং ট্রান্সফর্মেশন দিয়ে স্পিন ও পালস করে।
# কেন লাগছে: গেমের স্কোরিং ও পুরস্কার মেকানিক্স বাস্তবায়ন করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
"""

import math
from typing import Tuple
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glScalef
)
from src.core.config import COIN_RADIUS, COIN_PULSE_SPEED, PARTICLE_COUNT_COIN
from src.render.primitives import draw_circle
from src.render.effects import ParticleBurst
from src.ui import theme


class Coin:
    """
    # কী করছে: একটি একক কয়েনের অবস্থান, ঘূর্ণন ফেজ ও পিকআপ স্টেট ধারণ করে।
    # কেন লাগছে: লেভেলে ভাসমান চকচকে কয়েন প্রদর্শন ও প্লেয়ার সংগ্রহের ট্র্যাকিং করতে।
    # real world-এ এটা কোথায় দেখা যায়: পিকআপ আইটেম ক্লাস।
    """

    # কী করছে: কয়েনের স্থানাঙ্ক ও অ্যানিমেশন টাইমার ইনিশিয়ালাইজ করে।
    # কেন লাগছে: কয়েন স্পন করা এবং ঘূর্ণনের এলোমেলো শুরু নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: আইটেম স্পনার।
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = COIN_RADIUS
        self.collected = False
        self.spin_timer = 0.0

    # কী করছে: প্রতি ফ্রেমে কয়েনের ঘূর্ণন কোণ বৃদ্ধি করে।
    # কেন লাগছে: অবিরাম ত্রিমাত্রিক অনুভূতির স্পিনিং অ্যানিমেশন দিতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যানিমেশন সাইকেল আপডেট।
    def update(self, dt: float):
        self.spin_timer += dt * COIN_PULSE_SPEED

    # কী করছে: কয়েনের বাউন্ডিং বক্স প্রদান করে।
    # কেন লাগছে: প্লেয়ারের সাথে পিকআপ সংঘর্ষ পরীক্ষা করতে।
    # real world-এ এটা কোথায় দেখা যায়: বাউন্ডিং বক্স ক্যালকুলেশন।
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        r = self.radius
        return (self.x - r, self.y - r, self.x + r, self.y + r)

    # কী করছে: কয়েনটি সংগ্রহ করে এবং সোনালী কণার বিস্ফোরণ তৈরি করে।
    # কেন লাগছে: কয়েন কুড়ানোর আনন্দদায়ক ভিজ্যুয়াল জুস প্রদান করতে।
    # real world-এ এটা কোথায় দেখা যায়: আইটেম কনজিউম ও স্পার্ক ইমিটার।
    def collect(self) -> ParticleBurst:
        self.collected = True
        return ParticleBurst(self.x, self.y, PARTICLE_COUNT_COIN, theme.ACCENT_GOLD)

    # কী করছে: glScalef দিয়ে কয়েনটিকে স্পিন করিয়ে সোনালী বৃত্ত আঁকে।
    # কেন লাগছে: টুডি ট্রান্সফর্মেশন স্কেলিং প্রদর্শনের মাধ্যমে স্পিনিং কয়েন ফুটিয়ে তুলতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        if self.collected:
            return
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)

        # অনুভূমিক স্কেলিং দিয়ে স্পিনিং ইফেক্ট
        spin_scale_x = math.cos(self.spin_timer)
        pulse = 1.0 + 0.08 * math.sin(self.spin_timer * 1.5)
        glScalef(spin_scale_x * pulse, pulse, 1.0)

        # বাইরের সোনালী বৃত্ত
        draw_circle(0.0, 0.0, self.radius, theme.COLOR_COIN, filled=True, segments=16)
        # ভেতরের রিং
        draw_circle(0.0, 0.0, self.radius * 0.65, theme.ACCENT_GOLD, filled=False, segments=16)

        glPopMatrix()
