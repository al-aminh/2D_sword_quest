"""
# কী করছে: গ্লুট স্ট্রোক ও বিটম্যাপ ফন্ট ব্যবহার করে স্কেলযোগ্য ও তীক্ষ্ণ টেক্সট রেন্ডার করে।
# কেন লাগছে: কোনো বাহ্যিক ফন্ট ফাইল ছাড়া টাইটেল ও স্কোর প্রদর্শন এবং টেক্সট সেন্টারিং করার জন্য।
# real world-এ এটা কোথায় দেখা যায়: vector graphics tools, Google Maps rendering
"""

from typing import Tuple
from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glScalef, glLineWidth,
    glColor4f, glRasterPos2f
)
from OpenGL.GLUT import (
    glutStrokeCharacter, glutStrokeWidth, glutBitmapCharacter,
    GLUT_STROKE_ROMAN, GLUT_BITMAP_HELVETICA_18
)


# কী করছে: স্ট্রোক ফন্টের সাহায্যে পরিমাপ করে টেক্সটের মোট প্রস্থ পিক্সেল এককে বের করে।
# কেন লাগছে: স্ক্রিনের ঠিক মাঝখানে বা বাটনের কেন্দ্রে টেক্সট সুন্দরভাবে বসাতে।
# real world-এ এটা কোথায় দেখা যায়: ভেক্টর টাইপোগ্রাফি ইঞ্জিন (যেমন FreeType / HarfBuzz)।
def get_stroke_text_width(text: str, scale: float = 0.15) -> float:
    total_w = 0.0
    for ch in text:
        total_w += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(ch))
    return total_w * scale


# কী করছে: ভেক্টর স্ট্রোক ফন্ট দিয়ে স্কেল ও রঙ অনুযায়ী সুন্দর টেক্সট স্ক্রিনে আঁকে।
# কেন লাগছে: গেমের শিরোনাম ও বোতামের লেখা বড় আকারে মসৃণভাবে প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
def draw_stroke_text(
    text: str, x: float, y: float,
    scale: float = 0.15,
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
    line_width: float = 2.0
):
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glScalef(scale, scale, 1.0)
    glLineWidth(line_width)
    glColor4f(*color)
    for ch in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
    glPopMatrix()


# কী করছে: সাধারণ বিটম্যাপ ফন্ট দিয়ে সরাসরি দ্রুত ও স্পষ্ট টেক্সট বা সংখ্যা আঁকে।
# কেন লাগছে: গেমের ইন-গেম হাড (স্কোর, সময়, লাইভস) হালকা রিসোর্সে প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: ওএসডি (On-Screen Display) ও টার্মিনাল ফন্ট রেন্ডারিং।
def draw_bitmap_text(
    text: str, x: float, y: float,
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
):
    glColor4f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
