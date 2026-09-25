"""
# কী করছে: প্লেয়ার ক্যারেক্টার ক্লাস যা ফিজিক্স, লোকাল শেপ ও ২ডি ট্রান্সফর্মেশন পরিচালনা করে।
# কেন লাগছে: গেমের মূল নায়কের মসৃণ চলাচল, লাফ ও দিক পরিবর্তন নিয়ন্ত্রণ করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
"""

import math
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glScalef, glLineWidth,
    glBegin, glEnd, glVertex2f, glColor4f,
    GL_QUADS, GL_LINES
)
from src.core.config import (
    PLAYER_SPEED, JUMP_VELOCITY, GRAVITY, PLAYER_WIDTH, PLAYER_HEIGHT
)
from src.render.primitives import draw_circle
from src.ui import theme


class Player:
    """
    # কী করছে: প্লেয়ারের অবস্থান, বেগ, ফেসিং ও অঙ্গপ্রত্যঙ্গের গঠন লোকাল স্পেসে ধারণ করে।
    # কেন লাগছে: গ্রাফিক্স পাইপলাইনে অবজেক্ট স্পেস থেকে ওয়ার্ল্ড স্পেসে রূপান্তর করে আঁকতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম অবজেক্ট হায়ারার্কিকাল মডেলিং।
    """

    # কী করছে: প্লেয়ারের প্রারম্ভিক স্থানাঙ্ক ও স্টেট ভ্যারিয়েবল ইনিশিয়ালাইজ করে।
    # কেন লাগছে: ক্যারেক্টারের প্রাথমিক জন্মস্থান ও শারীরিক পরামিতি সেট করতে।
    # real world-এ এটা কোথায় দেখা যায়: ক্যারেক্টার স্পনার ইনিশিয়ালাইজেশন।
    def __init__(self, x: float = 120.0, y: float = 80.0):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.facing = 1  # ১ হলে ডান, -১ হলে বাম
        self.is_grounded = True
        self.walk_time = 0.0
        from src.gameplay.sword import Sword
        self.sword = Sword(self)

    # কী করছে: প্লেয়ারের তলোয়ার দিয়ে আক্রমণ পরিচালনা করে।
    # কেন লাগছে: 'F' বোতাম চাপলে তরবারির সুইং শুরু করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যাকশন গেমপ্লে মেকানিক্স কন্ট্রোল।
    def attack(self) -> bool:
        if self.sword:
            return self.sword.attack()
        return False

    # কী করছে: কিবোর্ড ইনপুট, প্ল্যাটফর্ম কোলিশন এবং মহাকর্ষ প্রয়োগ করে প্লেয়ার আপডেট করে।
    # কেন লাগছে: বাস্তবসম্মত দৌড়, জাম্পিং এবং প্ল্যাটফর্মে স্থির থাকা নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: প্ল্যাটফর্মার ফিজিক্স ও কোলিশন সলভার।
    def update(self, dt: float, keys_down: set, platforms=None):
        move_x = 0.0
        if 'a' in keys_down or 'left' in keys_down:
            move_x -= 1.0
        if 'd' in keys_down or 'right' in keys_down:
            move_x += 1.0

        if move_x != 0.0:
            self.vx = move_x * PLAYER_SPEED
            self.facing = 1 if move_x > 0 else -1
            self.walk_time += dt * 10.0
        else:
            self.vx = 0.0
            self.walk_time = 0.0

        prev_y = self.y
        self.vy -= GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # প্ল্যাটফর্ম বাউন্ডারি ও কোলিশন পরীক্ষা
        if platforms:
            self._handle_platform_collisions(prev_y, platforms)
        elif self.y <= 80.0:
            self.y = 80.0
            self.vy = 0.0
            self.is_grounded = True

        if self.sword:
            self.sword.update(dt)

    # কী করছে: প্লেয়ারের পায়ের সাথে প্ল্যাটফর্মের উপরিতলের কোলিশন পরীক্ষা ও সমাধান করে।
    # কেন লাগছে: শূন্যে ভাসমান বা চলমান প্ল্যাটফর্মে সঠিকভাবে ল্যান্ড করা নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def _handle_platform_collisions(self, prev_y: float, platforms):
        landed = False
        half_w = self.width * 0.4
        for plat in platforms:
            plat_top = plat.y + plat.h
            if (plat.x - half_w) <= self.x <= (plat.x + plat.w + half_w):
                if prev_y >= plat_top - 6.0 and self.y <= plat_top and self.vy <= 0.0:
                    self.y = plat_top
                    self.vy = 0.0
                    self.is_grounded = True
                    landed = True
                    if hasattr(plat, 'dx'):
                        self.x += plat.dx
                        self.y += plat.dy
                    break
        if not landed and self.vy != 0.0:
            self.is_grounded = False

    # কী করছে: প্লেয়ারকে উপরের দিকে জাম্প ভেলোসিটি প্রদান করে।
    # কেন লাগছে: স্পেস বা আপ বোতাম চাপলে লাফানো শুরু করতে।
    # real world-এ এটা কোথায় দেখা যায়: প্ল্যাটফর্মার জাম্প ইমপালস লজিক।
    def jump(self):
        if self.is_grounded:
            self.vy = JUMP_VELOCITY
            self.is_grounded = False

    # কী করছে: লোকাল কোঅর্ডিনেটে ক্যারেক্টারের পা দুটি আঁকে।
    # কেন লাগছে: দৌড়ানোর সময় পায়ের প্রাকৃতিক মুভমেন্ট দৃশ্যমান করতে।
    # real world-এ এটা কোথায় দেখা যায়: ক্যারেক্টার স্কেলিটাল ও লিম্ব অ্যানিমেশন।
    def _draw_legs(self):
        leg_swing = math.sin(self.walk_time) * 5.0 if self.vx != 0.0 else 0.0
        glLineWidth(3.0)
        glColor4f(*theme.COLOR_PLATFORM)
        glBegin(GL_LINES)
        # বাম পা
        glVertex2f(-6.0, 14.0)
        glVertex2f(-6.0 - leg_swing, 0.0)
        # ডান পা
        glVertex2f(6.0, 14.0)
        glVertex2f(6.0 + leg_swing, 0.0)
        glEnd()

    # কী করছে: লোকাল কোঅর্ডিনেটে ক্যারেক্টারের বডি এবং বেল্ট আঁকে।
    # কেন লাগছে: ক্যারেক্টারের প্রধান ধড় রঙিন বহুভুজ দিয়ে দৃশ্যমান করতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def _draw_torso(self):
        glColor4f(*theme.COLOR_PLAYER_BODY)
        glBegin(GL_QUADS)
        glVertex2f(-9.0, 14.0)
        glVertex2f(9.0, 14.0)
        glVertex2f(9.0, 36.0)
        glVertex2f(-9.0, 36.0)
        glEnd()

        # হেডব্যান্ড বা বেল্ট লাইন
        glColor4f(*theme.ACCENT_PRIMARY)
        glBegin(GL_QUADS)
        glVertex2f(-9.0, 22.0)
        glVertex2f(9.0, 22.0)
        glVertex2f(9.0, 25.0)
        glVertex2f(-9.0, 25.0)
        glEnd()

    # কী করছে: লোকাল কোঅর্ডিনেটে ক্যারেক্টারের মাথা ও চোখ আঁকে।
    # কেন লাগছে: একটি মৌলিক ও চিত্তাকর্ষক মানবীয় মুখাবয়ব ফুটিয়ে তুলতে।
    # real world-এ এটা কোথায় দেখা যায়: প্রিমিটিভ ভিত্তিক অ্যানিমেটেড অ্যাভাটার ডিজাইন।
    def _draw_head(self):
        draw_circle(0.0, 44.0, 9.0, theme.COLOR_PLAYER_HEAD, filled=True, segments=16)
        # চোখের ডট
        glColor4f(0.1, 0.1, 0.1, 1.0)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glVertex2f(3.0, 44.0)
        glVertex2f(5.0, 44.0)
        glEnd()

    # কী করছে: ২ডি ম্যাট্রিক্স ট্রান্সফর্মেশন (Translate & Scale) দিয়ে প্লেয়ার স্ক্রিনে আঁকে।
    # কেন লাগছে: প্লেয়ারকে ওয়ার্ল্ডে সরানো ও বামে মুখ করলে ফ্লিপ করা নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)
        if self.facing < 0:
            glScalef(-1.0, 1.0, 1.0)

        self._draw_legs()
        self._draw_torso()
        self._draw_head()

        # সোর্ড আঁকার কল (যদি অ্যাটাচ করা থাকে)
        if self.sword:
            self.sword.draw()

        glPopMatrix()
