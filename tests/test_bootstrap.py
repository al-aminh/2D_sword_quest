"""
# কী করছে: বুটস্ট্র্যাপ এবং উইন্ডো ইনিশিয়ালাইজেশন টেস্ট করছে।
# কেন লাগছে: গেম উইন্ডো ও গেমলুপ ক্র্যাশ ছাড়া রান হচ্ছে কিনা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: সিআই/সিডি অটোমেটেড জিইউআই স্মোক টেস্ট।
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import bootstrap
from src.scenes.base_scene import BaseScene


class TestScene(BaseScene):
    def update(self, dt: float):
        pass

    def draw(self):
        pass


def run_test():
    timer = threading.Timer(0.3, lambda: os._exit(0))
    timer.daemon = True
    timer.start()
    bootstrap.run(TestScene())


if __name__ == "__main__":
    run_test()
