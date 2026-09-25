"""
# কী করছে: স্টেপ ৪-এর সিন ক্রস-ফেড ট্রানজিশন টেস্ট করছে।
# কেন লাগছে: সিন পরিবর্তনের সময় ফেড-ইন এবং ফেড-আউট অ্যালগরিদম ঠিকমতো চলছে কিনা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: স্টেট মেশিন ট্রানজিশন ভেরিফিকেশন।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene
from src.scenes.play_scene import PlayScene


def test_transition():
    sm = SceneManager()
    menu = MenuScene(sm)
    play = PlayScene(sm)

    sm.switch_to(menu, with_transition=False)
    assert sm.current_scene == menu

    # মেনু থেকে প্লে সিনে ট্রানজিশন শুরু
    sm.switch_to(play, with_transition=True)
    assert sm.transition.is_active()
    assert sm.current_scene == menu  # এখনও মেনু দেখানো হচ্ছে
    assert sm.next_scene == play

    # ডেল্টা টাইম দিয়ে ট্রানজিশন ৫০% পার করা
    half_time = sm.transition.duration * 0.55
    sm.update(half_time)
    assert sm.current_scene == play  # কালো পর্দায় নতুন সিন অদলবদল হয়েছে
    assert sm.transition.is_active()  # ফেড ইন চলছে

    # বাকি ৫০% পার করা
    sm.update(half_time)
    assert not sm.transition.is_active()
    assert sm.current_scene == play
    print("STEP 4 Scene Transitions verified successfully!")


if __name__ == "__main__":
    test_transition()
