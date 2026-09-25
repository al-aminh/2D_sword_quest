"""
# কী করছে: গেমের স্ট্যাটিক এবং বেজিয়ার কার্ভ বরাবর চলমান প্ল্যাটফর্ম তৈরি ও পরিচালনা করে।
# কেন লাগছে: লেভেলের কাঠামো নির্মাণ এবং প্লেয়ারের জন্য চ্যালেঞ্জিং জাম্পিং সারফেস সরবরাহ করতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
"""

from typing import Tuple
from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor4f, glLineWidth,
    GL_QUADS, GL_LINES
)
from src.physics.curves import evaluate_cubic_bezier, ease_in_out_cubic
from src.ui import theme


class Platform:
    """
    # কী করছে: একটি স্থির প্ল্যাটফর্মের অবস্থান, আকার ও গ্রাফিক্স উপস্থাপন করে।
    # কেন লাগছে: ভূমির উপরে প্লেয়ারের দাঁড়ানোর জন্য নিরাপদ শক্ত ভিত্তি তৈরি করতে।
    # real world-এ এটা কোথায় দেখা যায়: আর্কিটেকচারাল ফ্ল্যাট জিওমেট্রি ও গেম লেভেল অবজেক্ট।
    """

    # কী করছে: স্ট্যাটিক প্ল্যাটফর্মের স্থানাঙ্ক ও মাত্রা ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্ল্যাটফর্মের দৈর্ঘ্য ও উচ্চতা নির্ধারণ করে মেমরিতে রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: কোলিশন শেপ ইনিশিয়ালাইজার।
    def __init__(self, x: float, y: float, w: float, h: float):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # কী করছে: প্ল্যাটফর্মের বডি এবং উপরের উজ্জ্বল প্রান্ত স্ক্রিনে আঁকে।
    # কেন লাগছে: ডার্ক থিমের সাথে মানানসই আধুনিক নিয়ন এজযুক্ত প্ল্যাটফর্ম প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: Line & Shape Drawing -> vector graphics tools, Google Maps rendering
    def draw(self):
        # প্ল্যাটফর্মের মূল দেহ
        glColor4f(*theme.COLOR_PLATFORM)
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.w, self.y)
        glVertex2f(self.x + self.w, self.y + self.h)
        glVertex2f(self.x, self.y + self.h)
        glEnd()

        # উপরের জ্বলন্ত নিয়ন বর্ডার
        glColor4f(*theme.COLOR_PLATFORM_EDGE)
        glLineWidth(2.5)
        glBegin(GL_LINES)
        glVertex2f(self.x, self.y + self.h)
        glVertex2f(self.x + self.w, self.y + self.h)
        glEnd()


class BezierMovingPlatform(Platform):
    """
    # কী করছে: ৪টি কন্ট্রোল পয়েন্ট দিয়ে সংজ্ঞায়িত কিউবিক বেজিয়ার কার্ভ বরাবর চলমান প্ল্যাটফর্ম।
    # কেন লাগছে: প্ল্যাটফর্মে মসৃণ, বাঁকা ও আধুনিক গতিবিধি যুক্ত করে আকর্ষণীয় গেমপ্লে তৈরি করতে।
    # real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
    """

    # কী করছে: বেজিয়ার কন্ট্রোল পয়েন্ট, আকার ও চলাচলের সময়কাল নির্ধারণ করে।
    # কেন লাগছে: প্ল্যাটফর্মের মসৃণ চলাচলের পথ এবং গতি নির্ধারণ করতে।
    # real world-এ এটা কোথায় দেখা যায়: প্যারামেট্রিক কার্ভ মোশন কন্ট্রোলার।
    def __init__(
        self,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        p3: Tuple[float, float],
        w: float, h: float, duration: float = 3.5
    ):
        super().__init__(p0[0], p0[1], w, h)
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.duration = duration
        self.time = 0.0
        self.direction = 1  # ১ হলে সামনে, -১ হলে পেছনে
        self.dx = 0.0
        self.dy = 0.0

    # কী করছে: কিউবিক বেজিয়ার সমীকরণ ও ইজিং প্রয়োগ করে প্রতি ফ্রেমে প্ল্যাটফর্মকে স্থানান্তর করে।
    # কেন লাগছে: উভয় প্রান্তে মসৃণভাবে থামানো ও বাঁকা পথে প্ল্যাটফর্মকে অবিরাম সচল রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
    def update(self, dt: float):
        self.time += self.direction * (dt / self.duration)
        if self.time >= 1.0:
            self.time = 1.0
            self.direction = -1
        elif self.time <= 0.0:
            self.time = 0.0
            self.direction = 1

        eased_t = ease_in_out_cubic(self.time)
        new_x, new_y = evaluate_cubic_bezier(self.p0, self.p1, self.p2, self.p3, eased_t)
        self.dx = new_x - self.x
        self.dy = new_y - self.y
        self.x = new_x
        self.y = new_y
