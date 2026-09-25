"""
# কী করছে: হোভার ও ক্লিক অ্যানিমেশনযুক্ত আধুনিক ইন্টারেক্টিভ বাটন উইজেট তৈরি করে।
# কেন লাগছে: মাউস ইন্টার‍্যাকশনে মসৃণ ভিজ্যুয়াল প্রতিক্রিয়া ও ক্লিক ইভেন্ট হ্যান্ডল করতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
"""

from typing import Callable, Optional
from src.physics.curves import lerp, ease_out_cubic
from src.render.primitives import draw_rounded_rect
from src.render.text import draw_stroke_text, get_stroke_text_width
from src.ui import theme


class Button:
    """
    # কী করছে: একটি ক্লিকযোগ্য বাটনের অবস্থান, আকার, স্টেট ও অ্যানিমেশন লুপ ধরে রাখে।
    # কেন লাগছে: গেমের ইউজার ইন্টারফেসে ইন্টারেক্টিভ বোতাম উপাদান প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ওয়েব ও গেম বাটন কম্পোনেন্ট (React / Flutter / Unity UI)।
    """

    # কী করছে: বাটন অবজেক্টের টেক্সট, ডাইমেনশন ও কলব্যাক ইনিশিয়ালাইজ করে।
    # কেন লাগছে: বাটনের প্রারম্ভিক অবস্থা এবং ক্লিকে কি ঘটবে তা নির্ধারণ করতে।
    # real world-এ এটা কোথায় দেখা যায়: ইউআই বাটন ইন্সট্যানশিয়েশন।
    def __init__(
        self, text: str, x: float, y: float, w: float, h: float,
        on_click: Optional[Callable[[], None]] = None
    ):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.on_click = on_click
        self.is_hovered = False
        self.is_pressed = False
        self.hover_progress = 0.0  # ০.০ থেকে ১.০ অ্যানিমেশন ট্র্যাকার

    # কী করছে: মাউস ভেতরে আছে কিনা দেখে হোভার অ্যানিমেশনের প্রগ্রেস আপডেট করে।
    # কেন লাগছে: তাত্ক্ষণিক পরিবর্তন না ঘটিয়ে মসৃণভাবে রঙের রূপান্তর আনতে।
    # real world-এ এটা কোথায় দেখা যায়: CSS Transition & Easing Effects (e.g. :hover transitions)।
    def update(self, dt: float, mouse_x: float, mouse_y: float):
        self.is_hovered = (
            self.x <= mouse_x <= self.x + self.w and
            self.y <= mouse_y <= self.y + self.h
        )
        target = 1.0 if self.is_hovered else 0.0
        step = dt * 8.0
        self.hover_progress = lerp(self.hover_progress, target, min(1.0, step))

    # কী করছে: মাউস ক্লিক ইভেন্ট প্রক্রিয়াকরণ করে এবং কলব্যাক এক্সিকিউট করে।
    # কেন লাগছে: ব্যবহারকারী বাটনে ক্লিক করলে নির্দিষ্ট গেম লজিক চালাতে।
    # real world-এ এটা কোথায় দেখা যায়: ক্লিক লিসেনার ও ইভেন্ট হ্যান্ডলার প্যাটার্ন।
    def handle_click(self, mouse_x: float, mouse_y: float, is_down: bool):
        inside = (self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h)
        if is_down:
            if inside:
                self.is_pressed = True
        else:
            if self.is_pressed and inside:
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
            else:
                self.is_pressed = False

    # কী করছে: বাটন এবং এর ভেতরের টেক্সট সঠিকভাবে স্ক্রিনে রেন্ডার করে।
    # কেন লাগছে: অ্যানিমেটেড বর্ডার, ফিল কালার ও টেক্সট সেন্টারিং প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def draw(self):
        eased_h = ease_out_cubic(self.hover_progress)
        offset_y = -2.0 if self.is_pressed else 0.0

        r = lerp(theme.ACCENT_PRIMARY[0], theme.ACCENT_HOVER[0], eased_h)
        g = lerp(theme.ACCENT_PRIMARY[1], theme.ACCENT_HOVER[1], eased_h)
        b = lerp(theme.ACCENT_PRIMARY[2], theme.ACCENT_HOVER[2], eased_h)
        border_col = (r, g, b, 1.0)

        bg_alpha = lerp(0.15, 0.35, eased_h)
        fill_col = (r * 0.4, g * 0.4, b * 0.4, bg_alpha)

        draw_rounded_rect(
            self.x, self.y + offset_y, self.w, self.h,
            radius=12.0, fill_color=fill_col, border_color=border_col, border_width=2.0
        )

        scale = 0.16
        txt_w = get_stroke_text_width(self.text, scale)
        tx = self.x + (self.w - txt_w) * 0.5
        ty = self.y + offset_y + (self.h - 18.0) * 0.5
        txt_col = theme.COLOR_WHITE if not self.is_hovered else theme.ACCENT_HOVER
        draw_stroke_text(self.text, tx, ty, scale=scale, color=txt_col, line_width=2.0)
