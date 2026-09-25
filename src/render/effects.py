"""
# কী করছে: গ্রেডিয়েন্ট কালার ফিল, ফুল-স্ক্রিন ফ্ল্যাশ, স্ক্রিন শেক এবং পার্টিকেল বার্স্ট ইফেক্ট তৈরি করছে।
# কেন লাগছে: গেমপ্লে ও ইউআই-তে আধুনিক জুস এবং ভিজ্যুয়াল প্রতিক্রিয়া যোগ করার জন্য।
# real world-এ এটা কোথায় দেখা যায়: Photoshop paint bucket / UI hit-flash effects
"""

import random
from typing import Tuple, List
from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor4f, glLineWidth,
    glPushMatrix, glPopMatrix, glTranslatef,
    GL_QUADS, GL_LINES, GL_TRIANGLES
)
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


# কী করছে: উল্লম্বভাবে দুই রঙের মসৃণ গ্রেডিয়েন্ট দিয়ে একটি আয়তাকার ক্ষেত্র পূরণ করে।
# কেন লাগছে: আকাশের ব্যাকগ্রাউন্ডে টেক্সচারহীন আকর্ষণীয় আবহ তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: Photoshop paint bucket / UI hit-flash effects
def draw_gradient_fill(
    x: float, y: float, w: float, h: float,
    top_color: Tuple[float, float, float, float],
    bottom_color: Tuple[float, float, float, float]
):
    glBegin(GL_QUADS)
    glColor4f(*bottom_color)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glColor4f(*top_color)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


# কী করছে: স্ক্রিনে হঠাৎ আলো বা আঘাতের প্রতিক্রিয়া হিসেবে পুরো স্ক্রিন ফ্ল্যাশ করে।
# কেন লাগছে: প্লেয়ার আঘাত পেলে তাৎক্ষণিক ভিজ্যুয়াল ইমপ্যাক্ট ফিল তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: Photoshop paint bucket / UI hit-flash effects
def draw_screen_flash(color: Tuple[float, float, float], alpha: float):
    if alpha <= 0.001:
        return
    glColor4f(color[0], color[1], color[2], alpha)
    glBegin(GL_QUADS)
    glVertex2f(0.0, 0.0)
    glVertex2f(float(SCREEN_WIDTH), 0.0)
    glVertex2f(float(SCREEN_WIDTH), float(SCREEN_HEIGHT))
    glVertex2f(0.0, float(SCREEN_HEIGHT))
    glEnd()


# কী করছে: প্যারালাক্স অনুপাত অনুযায়ী ধীরে স্ক্রোল করা দূরের পাহাড়ের সিলুয়েট আঁকে।
# কেন লাগছে: ২ডি সমতলে ত্রিমাত্রিক গভীরতার অনুভূতি (Depth Perception) তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
def draw_parallax_mountains(camera_x: float):
    from src.core.config import PARALLAX_FACTOR, LEVEL_WIDTH
    glPushMatrix()
    glTranslatef(-camera_x * PARALLAX_FACTOR, 0.0, 0.0)

    # দূরবর্তী পর্বতস্তর (ধীর ও গাঢ়)
    glColor4f(0.09, 0.11, 0.16, 1.0)
    glBegin(GL_TRIANGLES)
    step = 260.0
    total_w = LEVEL_WIDTH * 1.5
    cx = -200.0
    while cx < total_w:
        glVertex2f(cx, 80.0)
        glVertex2f(cx + step, 80.0)
        glVertex2f(cx + step * 0.5, 260.0)
        cx += step * 0.8
    glEnd()

    # নিকটবর্তী শৈলস্তর (একটু দ্রুত)
    glColor4f(0.12, 0.15, 0.22, 1.0)
    glBegin(GL_TRIANGLES)
    step2 = 180.0
    cx = -150.0
    while cx < total_w:
        glVertex2f(cx, 80.0)
        glVertex2f(cx + step2, 80.0)
        glVertex2f(cx + step2 * 0.5, 180.0)
        cx += step2 * 0.7
    glEnd()

    glPopMatrix()


# কী করছে: কোহেন-সাদারল্যান্ড অ্যালগরিদম দিয়ে দৃশ্যমান উইন্ডোয় ক্লিপ করে ব্যাকগ্রাউন্ড গ্রিড আঁকে।
# কেন লাগছে: ভিউপোর্টের বাইরের অপ্রয়োজনীয় রেখাংশ বাদ দিয়ে ম্যানুয়াল ক্লিপিং প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: Line Clipping -> GPU rendering pipeline, viewport culling
def draw_clipped_background_grid(viewport_bounds: Tuple[float, float, float, float], spacing: float = 64.0):
    from src.physics.clipping import clip_line
    xmin, ymin, xmax, ymax = viewport_bounds
    glColor4f(0.30, 0.45, 0.65, 0.18)
    glLineWidth(1.0)
    glBegin(GL_LINES)

    start_x = int(xmin // spacing) * spacing
    end_x = int(xmax // spacing + 1) * spacing
    cx = start_x
    while cx <= end_x:
        res = clip_line(cx, ymin - 80.0, cx, ymax + 80.0, xmin, ymin, xmax, ymax)
        if res:
            glVertex2f(res[0], res[1])
            glVertex2f(res[2], res[3])
        cx += spacing

    start_y = int(ymin // spacing) * spacing
    end_y = int(ymax // spacing + 1) * spacing
    cy = start_y
    while cy <= end_y:
        res = clip_line(xmin - 80.0, cy, xmax + 80.0, cy, xmin, ymin, xmax, ymax)
        if res:
            glVertex2f(res[0], res[1])
            glVertex2f(res[2], res[3])
        cy += spacing
    glEnd()


class Particle:
    """
    # কী করছে: একটি একক পার্টিকেল কণার গতিবিধি, বেগ এবং লাইফটাইম ধারণ করে।
    # কেন লাগছে: কয়েন সংগ্রহ বা এনিমি ধ্বংসের সময় বিস্ফোরণ ইফেক্ট প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন পার্টিকেল সিমুলেশন সিস্টেম।
    """

    # কী করছে: একটি নতুন পার্টিকেল কণা নির্দিষ্ট গতি ও দিকে শুরু করে।
    # কেন লাগছে: এলোমেলো দিকে ক্ষুদ্র লাইন ফ্র্যাগমেন্ট ছিটকে পড়ার অনুভূতি দিতে।
    # real world-এ এটা কোথায় দেখা যায়: স্পার্ক ও স্মোক সিমুলেশন।
    def __init__(self, x: float, y: float, color: Tuple[float, float, float, float]):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0.0, 6.28318)
        speed = random.uniform(60.0, 220.0)
        import math
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.uniform(0.3, 0.55)
        self.age = 0.0
        self.length = random.uniform(4.0, 10.0)

    # কী করছে: সময় অতিবাহিত হওয়ার সাথে পার্টিকেলের অবস্থান ও গতি আপডেট করে।
    # কেন লাগছে: মহাকর্ষের টানে কণাগুলো নিচে পড়া এবং ধীরে ধীরে মুছে যাওয়া বাস্তবায়ন করতে।
    # real world-এ এটা কোথায় দেখা যায়: পয়েন্ট পার্টিকেল ডায়নামিক্স।
    def update(self, dt: float) -> bool:
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy -= 400.0 * dt  # গ্র্যাভিটি
        return self.age < self.lifetime

    # কী করছে: ম্লান হয়ে যাওয়া উজ্জ্বল ক্ষুদ্র রেখাংশ হিসেবে কণাটি আঁকে।
    # কেন লাগছে: দৃশ্যত মসৃণ ক্ষয়প্রাপ্ত পার্টিকেল প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: vector graphics tools, Google Maps rendering
    def draw(self):
        progress = self.age / self.lifetime
        alpha = max(0.0, 1.0 - progress) * self.color[3]
        scale = max(0.2, 1.0 - progress * 0.7)
        glColor4f(self.color[0], self.color[1], self.color[2], alpha)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + (self.vx * 0.02 * scale), self.y + (self.vy * 0.02 * scale))
        glEnd()


class ParticleBurst:
    """
    # কী করছে: একসাথে একাধিক কণার সমষ্টি (Particle Burst) পরিচালনা করে।
    # কেন লাগছে: গেমের গুরুত্বপূর্ণ ঘটনায় (হিট/কয়েন পিকআপ) বিস্ফোরণ দৃশ্য তৈরি করতে।
    # real world-এ এটা কোথায় দেখা যায়: VFX ইমিটার আর্কিটেকচার।
    """

    # কী করছে: নির্দিষ্ট অবস্থানে একগুচ্ছ কণা তৈরি করে রাখে।
    # কেন লাগছে: ইভেন্টের সাথে সাথে কণা সমষ্টির জন্ম দিতে।
    # real world-এ এটা কোথায় দেখা যায়: ভিজ্যুয়াল ইফেক্ট স্পনার।
    def __init__(self, x: float, y: float, count: int, color: Tuple[float, float, float, float]):
        self.particles = [Particle(x, y, color) for _ in range(count)]

    # কী করছে: সব পার্টিকেলকে একযোগে আপডেট করে এবং মৃত কণা বাদ দেয়।
    # কেন লাগছে: মেমরি ও সিপিইউ খরচ কমাতে শেষ হয়ে যাওয়া কণা মুছে ফেলতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম অবজেক্ট পুলিং ও পার্টিকেল সুইপার।
    def update(self, dt: float) -> bool:
        self.particles = [p for p in self.particles if p.update(dt)]
        return len(self.particles) > 0

    # কী করছে: এখনও সক্রিয় প্রতিটি কণা স্ক্রিনে আঁকে।
    # কেন লাগছে: সমস্ত সক্রিয় কণা এক রেন্ডার পাথে প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ব্যাচ পার্টিকেল রেন্ডারার।
    def draw(self):
        for p in self.particles:
            p.draw()
