"""
# কী করছে: সিন পরিবর্তনের সময় মসৃণ ক্রস-ফেড ট্রানজিশন (কালো পর্দা আসা ও যাওয়া) সম্পাদন করে।
# কেন লাগছে: সিন পরিবর্তনের সময় কোনো আকস্মিক কাট ছাড়াই সিনেমাটিক আধুনিক রূপান্তর দিতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
"""

from OpenGL.GL import glBegin, glEnd, glVertex2f, glColor4f, GL_QUADS
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, TRANSITION_DURATION
from src.physics.curves import ease_in_out_cubic


class SceneTransition:
    """
    # কী করছে: ফুল-স্ক্রিন আলফা ফেড ওভারলে স্টেট এবং টাইমার পরিচালনা করে।
    # কেন লাগছে: গেমের প্রতিটি স্টেজে ফেড-ইন এবং ফেড-আউট ইফেক্ট তৈরি করতে।
    # real world-এ এটা কোথায় দেখা যায়: ভিডিও এডিটিং সফটওয়্যার ফেডার ও গেম ট্রানজিশন ম্যানেজার।
    """

    # কী করছে: ট্রানজিশন ভ্যারিয়েবল ও ডুরেশন ইনিশিয়ালাইজ করে।
    # কেন লাগছে: ট্রানজিশন টাইমিং ট্র্যাক করতে প্রারম্ভিক মান সেট করা।
    # real world-এ এটা কোথায় দেখা যায়: অ্যানিমেশন কন্ট্রোলার ইনিশিয়ালাইজেশন।
    def __init__(self, duration: float = TRANSITION_DURATION):
        self.duration = duration
        self.progress = 0.0
        self.active = False
        self.switched = False

    # কী করছে: নতুন ফেড ট্রানজিশন শুরু করে।
    # কেন লাগছে: সিন পরিবর্তনের সংকেত পাওয়ার সাথে সাথে অ্যানিমেশন চালু করতে।
    # real world-এ এটা কোথায় দেখা যায়: স্ক্রিন ট্রানজিশন ট্রিগার।
    def start(self):
        self.progress = 0.0
        self.active = True
        self.switched = False

    # কী করছে: ট্রানজিশন বর্তমানে চলছে কিনা তা নির্দেশ করে।
    # কেন লাগছে: দৃশ্য আঁকা এবং ইনপুট ব্লকিং এর শর্ত পরীক্ষা করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যাক্টিভ স্টেট পলিস্কার।
    def is_active(self) -> bool:
        return self.active

    # কী করছে: নতুন সিন লোড করার সঠিক সময় হয়েছে কিনা জানায়।
    # কেন লাগছে: পর্দা যখন সম্পূর্ণ কালো (আলফা ১.০) তখন নেপথ্যে সিন বদলাতে।
    # real world-এ এটা কোথায় দেখা যায়: সিন লোডার মিডপয়েন্ট ইভেন্ট সিগন্যাল।
    def should_switch_scene(self) -> bool:
        if self.active and not self.switched and self.progress >= 0.5:
            self.switched = True
            return True
        return False

    # কী করছে: সময়ের সাথে ট্রানজিশন প্রগ্রেস আপডেট করে।
    # কেন লাগছে: ডেল্টা-টাইম যোগ করে পুরো ফেড সাইকেল সমাপ্ত করতে।
    # real world-এ এটা কোথায় দেখা যায়: অ্যানিমেশন টাইমলুপ আপডেট।
    def update(self, dt: float):
        if not self.active:
            return
        self.progress += dt / self.duration
        if self.progress >= 1.0:
            self.progress = 1.0
            self.active = False

    # কী করছে: পূর্ণ পর্দাজুড়ে ইজড আলফা মানের কালো কোয়াড আঁকে।
    # কেন লাগছে: মসৃণ ফেড-আউট এবং ফেড-ইন গ্রাফিক্স প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: Color Fill -> Photoshop paint bucket / UI hit-flash effects
    def draw(self):
        if not self.active:
            return
        # ০.০ থেকে ০.৫ এ ফেড-আউট (আলফা ০->১), ০.৫ থেকে ১.০ এ ফেড-ইন (আলফা ১->০)
        if self.progress < 0.5:
            raw_t = self.progress * 2.0
            alpha = ease_in_out_cubic(raw_t)
        else:
            raw_t = (self.progress - 0.5) * 2.0
            alpha = 1.0 - ease_in_out_cubic(raw_t)

        glColor4f(0.04, 0.05, 0.07, alpha)
        glBegin(GL_QUADS)
        glVertex2f(0.0, 0.0)
        glVertex2f(float(SCREEN_WIDTH), 0.0)
        glVertex2f(float(SCREEN_WIDTH), float(SCREEN_HEIGHT))
        glVertex2f(0.0, float(SCREEN_HEIGHT))
        glEnd()
