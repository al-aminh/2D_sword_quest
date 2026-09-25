"""
# কী করছে: আধুনিক গোলাকার কোণাযুক্ত কন্টেইনার প্যানেল ক্লাস তৈরি করে।
# কেন লাগছে: মেনু ব্যাকগ্রাউন্ড এবং ডায়ালগ বক্স একটি মার্জিত আবহে প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: আধুনিক অপারেটিং সিস্টেম ও গেম ইন্টারফেস (Glassmorphism Cards)।
"""

from typing import Tuple
from src.render.primitives import draw_rounded_rect
from src.ui import theme


class Panel:
    """
    # কী করছে: স্ক্রিনে নির্দিষ্ট আকার ও রঙের একটি সেমি-ট্রান্সপারেন্ট প্যানেল উপস্থাপন করে।
    # কেন লাগছে: ইউআই উপাদানগুলোকে ব্যাকগ্রাউন্ড থেকে আলাদাভাবে স্পষ্টভাবে তুলে ধরতে।
    # real world-এ এটা কোথায় দেখা যায়: ইউআই কনটেইনার উইজেট আর্কিটেকচার।
    """

    # কী করছে: প্যানেলের স্থানাঙ্ক, সাইজ ও স্টাইলিং ভ্যালু ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্যানেলের অবস্থান ও দৃশ্যমান মাপ সংরক্ষণ করার জন্য।
    # real world-এ এটা কোথায় দেখা যায়: জিইউআই কম্পোনেন্ট কনস্ট্রাকশন।
    def __init__(
        self, x: float, y: float, w: float, h: float,
        radius: float = 18.0,
        fill_color: Tuple[float, float, float, float] = theme.PANEL_BG,
        border_color: Tuple[float, float, float, float] = theme.PANEL_BORDER,
        border_width: float = 1.8
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.radius = radius
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width

    # কী করছে: একটি বিন্দু প্যানেলের সীমানার ভেতর আছে কিনা তা পরীক্ষা করে।
    # কেন লাগছে: মাউস বা ক্লিকের অবস্থান প্যানেলের ওপর পড়েছে কিনা বুঝতে।
    # real world-এ এটা কোথায় দেখা যায়: টুডি বাউন্ডিং বক্স হিট টেস্টিং (Hit Test Algorithm)।
    def contains(self, px: float, py: float) -> bool:
        return self.x <= px <= self.x + self.w and self.y <= py <= self.y + self.h

    # কী করছে: বেজিয়ার কোণা সম্বলিত প্যানেলটি স্ক্রিনে রেন্ডার করে।
    # কেন লাগছে: ওপেনজিএল প্রিমিটিভ দিয়ে ফ্রস্টেড গ্লাস প্যানেল আঁকতে।
    # real world-এ এটা কোথায় দেখা যায়: vector graphics tools, Google Maps rendering
    def draw(self):
        draw_rounded_rect(
            self.x, self.y, self.w, self.h,
            self.radius, self.fill_color, self.border_color, self.border_width
        )
