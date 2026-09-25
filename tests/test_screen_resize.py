"""
# কী করছে: স্ক্রিনের আকার পরিবর্তন (রিসাইজ) ও যেকোনো রেজোলিউশনে মাউস ক্লিক রূপান্তর টেস্ট করছে।
# কেন লাগছে: উইন্ডো বড় বা ম্যাক্সিমাইজ করলেও যাতে সমস্ত বাটন ক্লিক ও হোভার নিখুঁতভাবে কাজ করে।
# real world-এ এটা কোথায় দেখা যায়: মাল্টি-রেজোলিউশন ও ডিসপ্লে স্কেলিং টেস্ট স্যুট।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.bootstrap import setup_projection
from src.app.input import global_input
from src.scenes.menu_scene import MenuScene
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


def test_resize_and_mouse_mapping():
    from OpenGL.GLUT import glutInit, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow, GLUT_DOUBLE, GLUT_RGBA
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(960, 540)
    glutCreateWindow(b"Resize Test")

    menu = MenuScene()

    # ১. সাধারণ রেজোলিউশন (৯৬০ x ৫৪০)
    setup_projection(960, 540)
    global_input.handle_mouse_motion(480, 270)
    assert abs(global_input.mouse_x - 480.0) < 1e-3
    assert abs(global_input.mouse_y - 270.0) < 1e-3

    # ২. ফুল এইচডি বা দ্বিগুণ আকার (১৯২০ x ১০৮০)
    setup_projection(1920, 1080)
    # স্ক্রিনের কেন্দ্রবিন্দুতে মাউস (৯৬০, ৫৪০)
    global_input.handle_mouse_motion(960, 540)
    assert abs(global_input.mouse_x - 480.0) < 1.0
    assert abs(global_input.mouse_y - 270.0) < 1.0

    # প্লে বাটনের ওপর ক্লিক টেস্ট (ভার্চুয়াল কেন্দ্রে বাটন আছে)
    btn_center_x = menu.btn_play.x + menu.btn_play.w * 0.5
    btn_center_y = menu.btn_play.y + menu.btn_play.h * 0.5
    # ১৯২০x১০৮০ উইন্ডোতে এই বাটনের অবস্থান হবে দ্বিগুণ
    win_click_x = btn_center_x * 2.0
    win_click_y = 1080.0 - (btn_center_y * 2.0)

    global_input.handle_mouse_motion(win_click_x, win_click_y)
    menu.on_mouse(global_input.mouse_x, global_input.mouse_y)
    # বাটনে হোভার সক্রিয় হতে হবে
    assert menu.btn_play.is_hovered

    # ৩. আল্ট্রাওয়াইড স্ক্রিন (২৫৬০ x ১০৮০) - পিলারবক্স টেস্ট
    setup_projection(2560, 1080)
    # উইন্ডোর মাঝখানে মাউস আনলে ভার্চুয়াল মাঝখানই (৪৮০, ২৭০) হতে হবে
    global_input.handle_mouse_motion(1280, 540)
    assert abs(global_input.mouse_x - 480.0) < 1.0
    assert abs(global_input.mouse_y - 270.0) < 1.0

    # ৪. ৪:৩ রেজোলিউশন (১৬০০ x ১২০০) - লেটারবক্স টেস্ট
    setup_projection(1600, 1200)
    global_input.handle_mouse_motion(800, 600)
    assert abs(global_input.mouse_x - 480.0) < 1.0
    assert abs(global_input.mouse_y - 270.0) < 1.0

    print("SCREEN RESIZE AND MULTI-RESOLUTION CLICKS VERIFIED 100% SUCCESSFULLY!")


if __name__ == "__main__":
    test_resize_and_mouse_mapping()
