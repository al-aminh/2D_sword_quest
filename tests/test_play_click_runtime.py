"""
# কী করছে: গেমের রিয়েল রানটাইমে প্লে বাটনে ক্লিক করে প্লে সিনে ট্রানজিশন টেস্ট করছে।
# কেন লাগছে: ব্যবহারকারী যেভাবে প্লে বাটনে ক্লিক করে দৃশ্য বদলায় তা হুবহু অনুকরণ করতে।
# real world-এ এটা কোথায় দেখা যায়: হেডলেস ইউজার ইন্টার‍্যাকশন অটোমেশন।
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import bootstrap
from src.scenes.menu_scene import MenuScene
from src.scenes.play_scene import PlayScene


def test_runtime_play_click():
    menu = MenuScene(bootstrap.scene_manager)

    def trigger_play():
        # প্লে বাটনে ক্লিক অনুকরণ
        bx = menu.btn_play.x + 20.0
        by = menu.btn_play.y + 20.0
        menu.btn_play.handle_click(bx, by, is_down=True)
        menu.btn_play.handle_click(bx, by, is_down=False)

    # ০.২ সেকেন্ড পর প্লে বাটনে ক্লিক এবং ০.৮ সেকেন্ড পর টেস্ট শেষ
    threading.Timer(0.2, trigger_play).start()
    threading.Timer(0.9, lambda: os._exit(0)).start()

    bootstrap.run(menu)


if __name__ == "__main__":
    test_runtime_play_click()
