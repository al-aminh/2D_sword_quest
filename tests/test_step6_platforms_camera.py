"""
# কী করছে: স্টেপ ৬-এর প্ল্যাটফর্ম, বেজিয়ার কার্ভ মুভমেন্ট ও লার্প ক্যামেরা টেস্ট করছে।
# কেন লাগছে: বেজিয়ার ম্যাথমেটিক্স এবং ক্যামেরা ট্র্যাকিং সঠিক নিয়মে কাজ করছে কিনা তা যাচাই করতে।
# real world-এ এটা কোথায় দেখা যায়: গেম মেকানিক্স অটোমেটেড টেস্টিং।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gameplay.level_data import create_level_platforms
from src.gameplay.platform import BezierMovingPlatform
from src.physics.camera import Camera
from src.gameplay.player import Player


def test_platforms_and_camera():
    platforms = create_level_platforms()
    bezier_plat = None
    for p in platforms:
        if isinstance(p, BezierMovingPlatform):
            bezier_plat = p
            break
    assert bezier_plat is not None

    # বেজিয়ার প্ল্যাটফর্ম গতি পরীক্ষা
    init_x, init_y = bezier_plat.x, bezier_plat.y
    bezier_plat.update(0.5)
    assert (bezier_plat.x != init_x) or (bezier_plat.y != init_y)
    assert bezier_plat.dx != 0.0 or bezier_plat.dy != 0.0

    # লার্প ক্যামেরা টেস্ট
    cam = Camera()
    assert cam.x == 0.0
    cam.update(800.0, 0.1)
    assert cam.x > 0.0  # মসৃণভাবে এগিয়ে এসেছে

    # প্লেয়ারের প্ল্যাটফর্মে ল্যান্ডিং টেস্ট
    p = Player(300.0, 220.0)  # প্ল্যাটফর্ম (280, 160, 160, 20) এর উপরে
    p.vy = -100.0
    p.update(0.1, set(), platforms)
    # প্ল্যাটফর্মের টপ হলো 160 + 20 = 180
    for _ in range(20):
        p.update(0.05, set(), platforms)
    assert p.y == 180.0
    assert p.is_grounded

    print("STEP 6 Platforms, Bezier curve moving platform, and Lerp Camera verified successfully!")


if __name__ == "__main__":
    test_platforms_and_camera()
