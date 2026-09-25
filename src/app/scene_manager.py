"""
# কী করছে: সম্পূর্ণ অ্যাপ্লিকেশনের দৃশ্য ও সিন ব্যবস্থাপনা পরিচালনা করছে।
# কেন লাগছে: সিন সুইচিং, ক্রস-ফেড ট্রানজিশন এবং ইনপুট ফরোয়ার্ডিং কেন্দ্রীয়ভাবে নিয়ন্ত্রণ করতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিনের ডিরেক্টর বা সিন ম্যানেজার (যেমন Cocos2d / Unity SceneManagement)।
"""

from typing import Optional
from src.scenes.base_scene import BaseScene
from src.ui.transition import SceneTransition


class SceneManager:
    """
    # কী করছে: সক্রিয় দৃশ্য ও পরবর্তী দৃশ্যের ট্রানজিশন স্টেট ধারণ করে।
    # কেন লাগছে: গেমের এক স্টেজ থেকে অন্য স্টেজে স্মুথ পরিবর্তন ঘটাতে।
    # real world-এ এটা কোথায় দেখা যায়: স্টেট প্যাটার্ন আর্কিটেকচার।
    """

    # কী করছে: সিন ম্যানেজার অবজেক্ট ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্রারম্ভিক সিন ও ট্রানজিশন রেফারেন্স সেট করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম আর্কিটেকচার ইনিশিয়ালাইজার।
    def __init__(self):
        self.current_scene: Optional[BaseScene] = None
        self.next_scene: Optional[BaseScene] = None
        self.transition = SceneTransition()

    # কী করছে: নতুন সিনে স্যুইচ করার রিকোয়েস্ট প্রসেস করে।
    # কেন লাগছে: সরাসরি বা ট্রানজিশন ইফেক্টের মাধ্যমে দৃশ্য বদলানোর জন্য।
    # real world-এ এটা কোথায় দেখা যায়: গেম সিন লোডিং ও ফেড ট্রানজিশন।
    def switch_to(self, new_scene: BaseScene, with_transition: bool = False):
        new_scene.manager = self
        if with_transition and self.transition is not None and self.current_scene is not None:
            self.next_scene = new_scene
            self.transition.start()
        else:
            self.current_scene = new_scene
            self.next_scene = None

    # কী করছে: বর্তমান সিন এবং চলমান ট্রানজিশনের লজিক আপডেট করে।
    # কেন লাগছে: ফ্রেম ড্রপ ছাড়াই মসৃণ অ্যানিমেশন বজায় রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: মেইন গেম লুপের লজিক আপডেট পর্যায়।
    def update(self, dt: float):
        if self.transition and self.transition.is_active():
            self.transition.update(dt)
            if self.transition.should_switch_scene() and self.next_scene:
                self.current_scene = self.next_scene
                self.next_scene = None
        elif self.current_scene:
            self.current_scene.update(dt)

    # কী করছে: বর্তমান সিন এবং ট্রানজিশন স্ক্রিনে আঁকে।
    # কেন লাগছে: দৃশ্যমান গ্রাফিক্স ও ট্রানজিশন আলফা ওভারলে প্রদর্শন করতে।
    # real world-এ এটা কোথায় দেখা যায়: ফ্রেমবাফার রেন্ডারিং ও পোস্ট-প্রসেসিং লেয়ার।
    def draw(self):
        if self.current_scene:
            self.current_scene.draw()
        if self.transition and self.transition.is_active():
            self.transition.draw()

    # কী করছে: কিবোর্ড ইনপুট বর্তমান সিনে প্রেরণ করে।
    # কেন লাগছে: সক্রিয় দৃশ্যে ব্যবহারকারীর বোতাম প্রতিক্রিয়া নিশ্চিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: উইন্ডো ইভেন্ট রাউটিং।
    def on_key(self, key: str, is_down: bool):
        if self.current_scene:
            self.current_scene.on_key(key, is_down)

    # কী করছে: মাউস ইভেন্ট বর্তমান সিনে প্রেরণ করে।
    # কেন লাগছে: মেনু বা বাটনের ইন্টার‍্যাকশন বর্তমান সিনে পৌঁছাতে।
    # real world-এ এটা কোথায় দেখা যায়: ইউআই ইভেন্ট ডেলিগেটর।
    def on_mouse(self, x: float, y: float, button: int = -1, state: int = -1):
        if self.current_scene:
            self.current_scene.on_mouse(x, y, button, state)
