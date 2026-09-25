"""
# কী করছে: গেমের ২ডি লার্প-ফলো ক্যামেরা এবং ওয়ার্ল্ড-স্ক্রিন কোঅর্ডিনেট রূপান্তর পরিচালনা করে।
# কেন লাগছে: প্লেয়ারের সাথে সাথে মসৃণভাবে দৃশ্য স্ক্রোল করা এবং স্ক্রিন শেক যুক্ত করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
"""

from typing import Tuple
from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef
from src.core.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_FOLLOW_SPEED,
    CAMERA_LOOKAHEAD_X, LEVEL_WIDTH
)


class Camera:
    """
    # কী করছে: ভিউপোর্ট ক্যামেরার অবস্থান, ট্র্যাকিং লার্প এবং রূপান্তর ম্যাট্রিক্স সংরক্ষণ করে।
    # কেন লাগছে: পুরো দৃশ্যকে ক্যামেরার বিপরীতে স্থানান্তরিত করে স্ক্রোলিং ইফেক্ট দিতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম ভিউপোর্ট ও ভার্চুয়াল ক্যামেরা কন্ট্রোলার (যেমন Cinemachine)।
    """

    # কী করছে: ক্যামেরা কোঅর্ডিনেট শূন্য এবং প্রাথমিক অফসেট দিয়ে শুরু করে।
    # কেন লাগছে: লেভেলের শুরুতে সঠিক অবস্থান থেকে ট্র্যাকিং চালু করতে।
    # real world-এ এটা কোথায় দেখা যায়: ক্যামেরা ইনিশিয়ালাইজার।
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.shake_x = 0.0
        self.shake_y = 0.0

    # কী করছে: লার্প অ্যালগরিদম ব্যবহার করে ক্যামেরাকে মসৃণভাবে প্লেয়ারের দিকে টেনে নেয়।
    # কেন লাগছে: কোনো ঝাঁকুনি ছাড়া আধুনিক স্মুথ ক্যামেরা মুভমেন্ট ও বাউন্ডারি ক্ল্যাম্পিং পেতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def update(self, target_x: float, dt: float):
        ideal_x = target_x - CAMERA_LOOKAHEAD_X
        max_x = max(0.0, LEVEL_WIDTH - float(SCREEN_WIDTH))
        clamped_target = max(0.0, min(max_x, ideal_x))
        # Eased Lerp Follow: smoothly closes gap
        self.x += (clamped_target - self.x) * CAMERA_FOLLOW_SPEED * dt
        self.x = max(0.0, min(max_x, self.x))

    # কী করছে: ওপেনজিএল মডেলভিউ ম্যাট্রিক্সে ক্যামেরার রূপান্তর প্রয়োগ করে।
    # কেন লাগছে: ক্যামেরার স্থানান্তরের প্রেক্ষিতে সমস্ত গেম অবজেক্ট সঠিক স্থানে প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ভিউ ম্যাট্রিক্স ট্রান্সফর্মেশন পাইপলাইন।
    def apply(self):
        glPushMatrix()
        glTranslatef(-self.x + self.shake_x, -self.y + self.shake_y, 0.0)

    # কী করছে: ক্যামেরার ভিউ ম্যাট্রিক্স পপ করে পূর্বাবস্থায় ফিরিয়ে নেয়।
    # কেন লাগছে: ইউআই উপাদানগুলো যাতে ক্যামেরার স্ক্রোলিং দ্বারা প্রভাবিত না হয়।
    # real world-এ এটা কোথায় দেখা যায়: ম্যাট্রিক্স স্ট্যাক পপ ও স্ক্রিন-স্পেস রেন্ডারিং।
    def unapply(self):
        glPopMatrix()

    # কী করছে: ক্যামেরা বর্তমানে লেভেলের কোন অংশটুকু দেখতে পাচ্ছে তার আয়তাকার সীমা রিটার্ন করে।
    # কেন লাগছে: ম্যানুয়াল লাইন ক্লিপিং এবং ব্যাকগ্রাউন্ড গ্রিড অপটিমাইজেশনের জন্য।
    # real world-এ এটা কোথায় দেখা যায়: ভিউ ফ্রাস্টাম ক্যালকুলেশন ও ভিউপোর্ট কাল্লিং।
    def get_viewport_bounds(self) -> Tuple[float, float, float, float]:
        return (self.x, self.y, self.x + float(SCREEN_WIDTH), self.y + float(SCREEN_HEIGHT))
