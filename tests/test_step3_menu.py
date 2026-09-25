"""
# কী করছে: স্টেপ ৩-এর মেনু সিন, বাটন হোভার ও ক্লিক ইন্টার‍্যাকশন টেস্ট করছে।
# কেন লাগছে: মাউস মুভমেন্ট এবং ক্লিকের প্রতিক্রিয়া নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: হেডলেস ইউআই ইন্টারঅ্যাকশন অটোমেশন।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scenes.menu_scene import MenuScene
from src.ui.button import Button
from OpenGL.GLUT import GLUT_LEFT_BUTTON, GLUT_DOWN, GLUT_UP


def test_button_hover_and_click():
    clicked = [False]

    def on_click():
        clicked[0] = True

    btn = Button("TEST", 100, 100, 200, 50, on_click)
    # মাউস দূরে
    btn.update(0.1, 0, 0)
    assert not btn.is_hovered

    # মাউস বাটনের ওপর
    btn.update(0.1, 150, 125)
    assert btn.is_hovered
    assert btn.hover_progress > 0.0

    # মাউস ক্লিক
    btn.handle_click(150, 125, True)
    assert btn.is_pressed
    btn.handle_click(150, 125, False)
    assert not btn.is_pressed
    assert clicked[0]

    # মেনু সিনের ইনস্ট্যান্স ও আপডেট টেস্ট
    menu = MenuScene()
    menu.update(0.1)
    menu.on_mouse(menu.btn_play.x + 10, menu.btn_play.y + 10)
    assert menu.btn_play.is_hovered
    print("STEP 3 Menu and Button hover/click verified successfully!")


if __name__ == "__main__":
    test_button_hover_and_click()
