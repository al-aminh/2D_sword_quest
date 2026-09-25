"""
# কী করছে: মৌলিক ২ডি গ্রাফিক্স প্রিমিটিভ (বহুভুজ, ওয়্যারফ্রেম, এবং বেজিয়ার কোণাযুক্ত আয়তক্ষেত্র) আঁকছে।
# কেন লাগছে: গেমের ক্যারেক্টার, বাটন ও প্যানেল কোনো এক্সটার্নাল ইমেজ ছাড়াই ওপেনজিএল দিয়ে সরাসরি রেন্ডার করতে।
# real world-এ এটা কোথায় দেখা যায়: vector graphics tools, Google Maps rendering
"""

import math
from typing import List, Tuple
from OpenGL.GL import (
    glBegin, glEnd, glVertex2f, glColor4f, glLineWidth,
    GL_POLYGON, GL_LINE_LOOP, GL_TRIANGLE_FAN, GL_LINES
)
from src.physics.curves import generate_bezier_points


# কী করছে: শীর্ষবিন্দুর (ভার্টেক্স) তালিকা থেকে একটি সলিড ফিল বহুভুজ আঁকে।
# কেন লাগছে: ইউআই এবং প্ল্যাটফর্মের বডি রেন্ডার করতে।
# real world-এ এটা কোথায় দেখা যায়: vector graphics tools, Google Maps rendering
def draw_polygon(vertices: List[Tuple[float, float]], color: Tuple[float, float, float, float]):
    glColor4f(*color)
    glBegin(GL_POLYGON)
    for vx, vy in vertices:
        glVertex2f(vx, vy)
    glEnd()


# কী করছে: শীর্ষবিন্দুগুলোর চারপাশে একটি বর্ডার বা ওয়্যারফ্রেম আউটলাইন আঁকে।
# কেন লাগছে: বাটন বা প্যানেলের ধার স্পষ্টভাবে ফুটিয়ে তুলতে।
# real world-এ এটা কোথায় দেখা যায়: CAD সফটওয়্যার ও আর্কিটেকচারাল ব্লুপ্রিন্ট ডিসপ্লে।
def draw_wireframe(vertices: List[Tuple[float, float]], color: Tuple[float, float, float, float], line_width: float = 1.5):
    glLineWidth(line_width)
    glColor4f(*color)
    glBegin(GL_LINE_LOOP)
    for vx, vy in vertices:
        glVertex2f(vx, vy)
    glEnd()


# কী করছে: কিউবিক বেজিয়ার কার্ভের সাহায্যে একটি গোলাকার আয়তক্ষেত্রের পরিধির শীর্ষবিন্দু তৈরি করে।
# কেন লাগছে: বেজিয়ার সূত্র ব্যবহার করে নিখুঁত আধুনিক স্মুথ কর্নার প্যানেল তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
def _build_rounded_rect_vertices(x: float, y: float, w: float, h: float, radius: float) -> List[Tuple[float, float]]:
    r = min(radius, w * 0.5, h * 0.5)
    k = 0.5522847498 * r  # বেজিয়ার কোণা বৃত্তাংশ কন্ট্রোল কনস্ট্যান্ট
    pts = []

    # নিচের বাম কোণা
    c_bl = generate_bezier_points((x, y + r), (x, y + r - k), (x + r - k, y), (x + r, y), segments=6)
    pts.extend(c_bl)

    # নিচের ডান কোণা
    c_br = generate_bezier_points((x + w - r, y), (x + w - r + k, y), (x + w, y + r - k), (x + w, y + r), segments=6)
    pts.extend(c_br)

    # উপরের ডান কোণা
    c_tr = generate_bezier_points((x + w, y + h - r), (x + w, y + h - r + k), (x + w - r + k, y + h), (x + w - r, y + h), segments=6)
    pts.extend(c_tr)

    # উপরের বাম কোণা
    c_tl = generate_bezier_points((x + r, y + h), (x + r - k, y + h), (x, y + h - r + k), (x, y + h - r), segments=6)
    pts.extend(c_tl)

    return pts


# কী করছে: বেজিয়ার কোণাযুক্ত একটি আয়তক্ষেত্র সলিড ফিল এবং বর্ডারসহ স্ক্রিনে আঁকে।
# কেন লাগছে: ইউআই কার্ড, বাটন ব্যাকগ্রাউন্ড এবং ডায়ালগ বক্সের আধুনিক লুক দিতে।
# real world-এ এটা কোথায় দেখা যায়: আধুনিক অপারেটিং সিস্টেম উইন্ডো ডিজাইন (macOS / iOS UI Panels)।
def draw_rounded_rect(
    x: float, y: float, w: float, h: float, radius: float,
    fill_color: Tuple[float, float, float, float],
    border_color: Tuple[float, float, float, float] = None,
    border_width: float = 1.5
):
    verts = _build_rounded_rect_vertices(x, y, w, h, radius)
    glColor4f(*fill_color)
    glBegin(GL_POLYGON)
    for vx, vy in verts:
        glVertex2f(vx, vy)
    glEnd()

    if border_color:
        draw_wireframe(verts, border_color, border_width)


# কী করছে: কেন্দ্র এবং ব্যাসার্ধ দিয়ে একটি মসৃণ বৃত্ত আঁকে।
# কেন লাগছে: কয়েন এবং ক্যারেক্টারের গোলাকার মাথা আঁকতে।
# real world-এ এটা কোথায় দেখা যায়: ভেক্টর বৃত্ত রেন্ডারিং ও রাডার ডিসপ্লে সিস্টেম।
def draw_circle(
    cx: float, cy: float, radius: float,
    color: Tuple[float, float, float, float],
    filled: bool = True, segments: int = 24
):
    glColor4f(*color)
    glBegin(GL_TRIANGLE_FAN if filled else GL_LINE_LOOP)
    if filled:
        glVertex2f(cx, cy)
    for i in range(segments + 1):
        angle = (2.0 * math.pi * i) / segments
        glVertex2f(cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
    glEnd()
