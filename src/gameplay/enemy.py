"""
# কী করছে: এনিমি দানব শ্রেণী যা পাহারা এআই, প্রিমিটিভ ড্রয়িং এবং স্কোয়াশ ডেথ অ্যানিমেশন চালায়।
# কেন লাগছে: গেমের চ্যালেঞ্জ ও যুদ্ধ মেকানিক্স কার্যকর করতে শত্রু তৈরি করা।
# real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
"""

from typing import Tuple
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glScalef, glColor4f,
    glBegin, glEnd, glVertex2f, GL_QUADS, GL_TRIANGLES, GL_LINES
)
from src.core.config import (
    ENEMY_SPEED, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SQUASH_DURATION,
    PARTICLE_COUNT_ENEMY
)
from src.render.effects import ParticleBurst
from src.ui import theme


class Enemy:
    """
    # কী করছে: শত্রুর গতিবিধি, পেট্রোল সীমা, জীবনাবস্থা ও ডেথ অ্যানিমেশন সংরক্ষণ করে।
    # কেন লাগছে: গেমের প্রতিটি দানবকে স্বতন্ত্রভাবে পরিচালনা করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম এআই এনটিটি সিস্টেম।
    """

    # কী করছে: শত্রুর প্রাথমিক অবস্থান, পেট্রোল সীমানা ও স্টেট ইনিশিয়ালাইজ করে।
    # কেন লাগছে: দানব যাতে নির্দিষ্ট সীমার মধ্যে হেঁটে পাহারা দিতে পারে।
    # real world-এ এটা কোথায় দেখা যায়: এআই প্যাট্রোল ইনিশিয়ালাইজার।
    def __init__(self, x: float, y: float, min_x: float, max_x: float):
        self.x = x
        self.y = y
        self.min_x = min_x
        self.max_x = max_x
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.vx = ENEMY_SPEED
        self.facing = 1
        self.state = 'ALIVE'
        self.squash_timer = 0.0

    # কী করছে: শত্রু জীবিত আছে কিনা তা নিশ্চিত করে।
    # কেন লাগছে: কোলিশন ও তরবারির আঘাতের শর্ত নির্ধারণ করতে।
    # real world-এ এটা কোথায় দেখা যায়: লাইফসাইকেল চেকার।
    def is_alive(self) -> bool:
        return self.state == 'ALIVE'

    # কী করছে: শত্রুর আয়তাকার বাউন্ডিং বক্স প্রদান করে।
    # কেন লাগছে: AABB কোলিশন শনাক্তকরণের জন্য সীমানা নির্ধারণ করতে।
    # real world-এ এটা কোথায় দেখা যায়: বাউন্ডিং ভলিউম ক্যালকুলেশন।
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        hw = self.width * 0.5
        return (self.x - hw, self.y, self.x + hw, self.y + self.height)

    # কী করছে: শত্রুর মৃত্যু শুরু করে এবং রক্তিম কণার বিস্ফোরণ তৈরি করে।
    # কেন লাগছে: তলোয়ারের আঘাতে শত্রুর নিখুঁত স্কোয়াশ ও পার্টিকেল জুস দিতে।
    # real world-এ এটা কোথায় দেখা যায়: গেমপ্লে ডেথ সিকোয়েন্স ও ইফেক্ট স্পনার।
    def kill(self) -> ParticleBurst:
        self.state = 'DYING'
        self.squash_timer = 0.0
        return ParticleBurst(
            self.x, self.y + self.height * 0.5,
            PARTICLE_COUNT_ENEMY, theme.COLOR_ENEMY
        )

    # কী করছে: পেট্রোল সীমার মধ্যে সামনে-পেছনে হাঁটা ও স্কোয়াশ টাইমার আপডেট করে।
    # কেন লাগছে: সীমানায় পৌঁছে ফিরে আসা ও মৃত্যুর পর অদৃশ্য হওয়া নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: সিম্পল স্টেট মেশিন পেট্রোল এআই।
    def update(self, dt: float):
        if self.state == 'ALIVE':
            self.x += self.vx * dt
            if self.x >= self.max_x:
                self.x = self.max_x
                self.vx = -abs(self.vx)
                self.facing = -1
            elif self.x <= self.min_x:
                self.x = self.min_x
                self.vx = abs(self.vx)
                self.facing = 1
        elif self.state == 'DYING':
            self.squash_timer += dt
            if self.squash_timer >= ENEMY_SQUASH_DURATION:
                self.state = 'DEAD'

    # কী করছে: প্রিমিটিভ বহুভুজ ও শৃঙ্গ এঁকে শত্রুর রূপ তৈরি করে।
    # কেন লাগছে: কোনো বহিরাগত স্প্রাইট ছাড়াই আদিম ড্রয়িং দিয়ে অনন্য দানব আঁকতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def _draw_body_primitives(self, alpha: float):
        hw = self.width * 0.5
        # দানবের প্রধান দেহ (ট্রাপিজিয়াম বহুভুজ)
        glColor4f(theme.COLOR_ENEMY[0], theme.COLOR_ENEMY[1], theme.COLOR_ENEMY[2], alpha)
        glBegin(GL_QUADS)
        glVertex2f(-hw, 0.0)
        glVertex2f(hw, 0.0)
        glVertex2f(hw * 0.8, self.height)
        glVertex2f(-hw * 0.8, self.height)
        glEnd()

        # মাথার দুটি ধারালো শিং (ট্রায়াঙ্গেল)
        glColor4f(theme.ACCENT_SECONDARY[0], theme.ACCENT_SECONDARY[1], theme.ACCENT_SECONDARY[2], alpha)
        glBegin(GL_TRIANGLES)
        # বাম শিং
        glVertex2f(-hw * 0.7, self.height)
        glVertex2f(-hw * 0.3, self.height)
        glVertex2f(-hw * 0.5, self.height + 10.0)
        # ডান শিং
        glVertex2f(hw * 0.3, self.height)
        glVertex2f(hw * 0.7, self.height)
        glVertex2f(hw * 0.5, self.height + 10.0)
        glEnd()

        # জ্বলন্ত চোখ
        glColor4f(1.0, 0.95, 0.2, alpha)
        glBegin(GL_LINES)
        glVertex2f(-6.0, self.height * 0.65)
        glVertex2f(-2.0, self.height * 0.65)
        glVertex2f(2.0, self.height * 0.65)
        glVertex2f(6.0, self.height * 0.65)
        glEnd()

    # কী করছে: স্কোয়াশ ট্রান্সফর্মেশন ও আলফা ফেড-আউট দিয়ে এনিমি রেন্ডার করে।
    # কেন লাগছে: মৃত্যুর সময় চ্যাপ্টা হওয়া ও মিলিয়ে যাওয়ার আধুনিক ভিজ্যুয়াল প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        if self.state == 'DEAD':
            return
        glPushMatrix()
        glTranslatef(self.x, self.y, 0.0)

        if self.state == 'DYING':
            prog = self.squash_timer / ENEMY_SQUASH_DURATION
            scale_y = max(0.12, 1.0 - prog * 0.88)
            scale_x = 1.0 + prog * 0.4
            alpha = max(0.0, 1.0 - prog)
            glScalef(scale_x, scale_y, 1.0)
        else:
            alpha = 1.0

        self._draw_body_primitives(alpha)
        glPopMatrix()
