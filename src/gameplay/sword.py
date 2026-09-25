"""
# কী করছে: মেকানিকাল সোর্ড অ্যাটাক, বেজিয়ার ইজিং সুইং এবং ঘূর্ণন ট্রান্সফর্মেশন পরিচালনা করে।
# কেন লাগছে: প্লেয়ারের তলোয়ার চালনা, মসৃণ আর্ক অ্যানিমেশন এবং আক্রমণ হিটবক্স নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
"""

import math
from typing import Tuple, Optional
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glLineWidth,
    glBegin, glEnd, glVertex2f, glColor4f,
    GL_QUADS, GL_LINES
)
from src.core.config import (
    SWORD_RANGE, SWORD_SWING_DURATION, SWORD_COOLDOWN,
    SWORD_ARC_START, SWORD_ARC_END, SWORD_BLADE_WIDTH
)
from src.physics.curves import ease_in_out_cubic, lerp
from src.ui import theme


class Sword:
    """
    # কী করছে: তরবারির সুইং অবস্থা, কুলডাউন, কোণ এবং আক্রমণ হিটবক্স ধারণ করে।
    # কেন লাগছে: গেমের ওয়ান-হিট মিলিশিয়া কমব্যাট মেকানিক্স বাস্তবায়ন করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যাকশন গেম উইপন কন্ট্রোলার ও ট্র্যাজেক্টরি সিস্টেম।
    """

    # কী করছে: সোর্ড অবজেক্ট এবং আক্রমণ স্টেট টাইমার ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্রাথমিক কুলডাউন ও নিষ্ক্রিয় অবস্থা সেট করতে।
    # real world-এ এটা কোথায় দেখা যায়: ওয়েপন ইনস্ট্যানশিয়েশন।
    def __init__(self, owner):
        self.owner = owner
        self.is_swinging = False
        self.swing_timer = 0.0
        self.cooldown_timer = 0.0
        self.current_angle = SWORD_ARC_START

    # কী করছে: 'F' বোতাম চাপলে তরবারির সুইং আক্রমণ শুরু করে।
    # কেন লাগছে: কুলডাউন শেষ হওয়া সাপেক্ষে তরবারি ঘোরানো শুরু করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেমপ্লে অ্যাটাক ইনপুট ট্রিগার।
    def attack(self) -> bool:
        if self.cooldown_timer <= 0.0 and not self.is_swinging:
            self.is_swinging = True
            self.swing_timer = 0.0
            self.cooldown_timer = SWORD_COOLDOWN
            return True
        return False

    # কী করছে: বেজিয়ার ইজিং ব্যবহার করে তরবারির সুইং কোণ প্রতি ফ্রেমে আপডেট করে।
    # কেন লাগছে: তরবারির সুইং যাতে শুরুতে দ্রুত এবং শেষে প্রাকৃতিক আর্কে থামে।
    # real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
    def update(self, dt: float):
        if self.cooldown_timer > 0.0:
            self.cooldown_timer -= dt

        if self.is_swinging:
            self.swing_timer += dt
            if self.swing_timer >= SWORD_SWING_DURATION:
                self.is_swinging = False
                self.current_angle = SWORD_ARC_START
            else:
                prog = self.swing_timer / SWORD_SWING_DURATION
                eased_t = ease_in_out_cubic(prog)
                self.current_angle = lerp(SWORD_ARC_START, SWORD_ARC_END, eased_t)
        else:
            self.current_angle = SWORD_ARC_START

    # কী করছে: সক্রিয় আক্রমণ চলাকালীন তরবারির গ্লোবাল হিটবক্স বাউন্ডারি প্রদান করে।
    # কেন লাগছে: শত্রুর সাথে তলোয়ারের আঘাত শনাক্ত করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def get_hitbox(self) -> Optional[Tuple[float, float, float, float]]:
        if not self.is_swinging:
            return None
        facing = self.owner.facing
        px = self.owner.x
        py = self.owner.y + 24.0
        if facing > 0:
            return (px, py - 20.0, px + SWORD_RANGE, py + 45.0)
        else:
            return (px - SWORD_RANGE, py - 20.0, px, py + 45.0)

    # কী করছে: তরবারির হাতল এবং গার্ড লোকাল কোঅর্ডিনেটে আঁকে।
    # কেন লাগছে: ব্লেডের গোড়ায় বাস্তবসম্মত হাতল দৃশ্যমান করতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def _draw_hilt(self):
        glColor4f(0.45, 0.35, 0.25, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(-3.0, -10.0)
        glVertex2f(3.0, -10.0)
        glVertex2f(3.0, 0.0)
        glVertex2f(-3.0, 0.0)
        glEnd()

        # গোল্ডেন গার্ড
        glColor4f(*theme.ACCENT_GOLD)
        glBegin(GL_QUADS)
        glVertex2f(-8.0, 0.0)
        glVertex2f(8.0, 0.0)
        glVertex2f(8.0, 3.0)
        glVertex2f(-8.0, 3.0)
        glEnd()

    # কী করছে: তরবারির ধারালো ব্লেড ও গ্লো ইফেক্ট আঁকে।
    # কেন লাগছে: চকচকে রূপালী তরবারি স্ক্রিনে সুন্দরভাবে উপস্থাপন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ভেক্টর আর্ট ও ওয়েপন স্প্রাইটলেস রেন্ডারিং।
    def _draw_blade(self):
        glColor4f(*theme.COLOR_SWORD_BLADE)
        glBegin(GL_QUADS)
        glVertex2f(-SWORD_BLADE_WIDTH * 0.5, 3.0)
        glVertex2f(SWORD_BLADE_WIDTH * 0.5, 3.0)
        glVertex2f(SWORD_BLADE_WIDTH * 0.3, SWORD_RANGE - 8.0)
        glVertex2f(-SWORD_BLADE_WIDTH * 0.3, SWORD_RANGE - 8.0)
        glEnd()

        # ব্লেডের তীক্ষ্ণ ডগা (টিপ)
        glBegin(GL_QUADS)
        glVertex2f(-SWORD_BLADE_WIDTH * 0.3, SWORD_RANGE - 8.0)
        glVertex2f(SWORD_BLADE_WIDTH * 0.3, SWORD_RANGE - 8.0)
        glVertex2f(0.0, SWORD_RANGE)
        glVertex2f(0.0, SWORD_RANGE)
        glEnd()

    # কী করছে: ২ডি রোটেশন এবং ট্রান্সলেশন ম্যাট্রিক্স প্রয়োগ করে তরবারি আঁকে।
    # কেন লাগছে: সুইং করার সময় তরবারিকে খেলোয়াড়ের হাত থেকে বৃত্তাকার কোণে ঘোরাতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        glPushMatrix()
        glTranslatef(6.0, 24.0, 0.0)
        glRotatef(self.current_angle, 0.0, 0.0, 1.0)

        self._draw_hilt()
        self._draw_blade()

        glPopMatrix()
