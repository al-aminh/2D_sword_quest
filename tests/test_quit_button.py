"""
# কী করছে: মেনু সিনের QUIT বাটনে ক্লিক করে অ্যাপ্লিকেশন সফলভাবে বন্ধ হচ্ছে কিনা টেস্ট করছে।
# কেন লাগছে: গ্লুট মেইনলুপে কোনো ক্র্যাশ বা এক্সেপশন ছাড়াই গেম এক্সিট নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: অ্যাপ্লিকেশন লাইফসাইকেল টার্মিনেশন টেস্ট।
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import bootstrap
from src.scenes.menu_scene import MenuScene


def test_quit_button_runtime():
    menu = MenuScene(bootstrap.scene_manager)

    def trigger_quit():
        # ক্যুইট বাটনে ক্লিক অনুকরণ
        bx = menu.btn_quit.x + 20.0
        by = menu.btn_quit.y + 20.0
        menu.btn_quit.handle_click(bx, by, is_down=True)
        menu.btn_quit.handle_click(bx, by, is_down=False)

    # ০.২ সেকেন্ড পর ক্যুইট বাটনে ক্লিক
    threading.Timer(0.2, trigger_quit).start()

    bootstrap.run(menu)


if __name__ == "__main__":
    test_quit_button_runtime()
