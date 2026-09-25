"""
# কী করছে: স্টেপ ৫-এর প্লেয়ার মুভমেন্ট, জাম্প আর্ভ ও ২ডি ট্রান্সফর্মেশন টেস্ট করছে।
# কেন লাগছে: ফিজিক্সের নিয়ম অনুযায়ী গ্র্যাভিটি এবং কিবোর্ড ইনপুট রেসপন্স যাচাই করতে।
# real world-এ এটা কোথায় দেখা যায়: গেমপ্লে ফিজিক্স ইউনিট টেস্টিং।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gameplay.player import Player


def test_player_movement_and_physics():
    p = Player(100.0, 80.0)

    # ডানে মুভমেন্ট টেস্ট
    p.update(0.1, {'d'})
    assert p.vx > 0.0
    assert p.x > 100.0
    assert p.facing == 1

    # বামে মুভমেন্ট ও ফ্লিপ টেস্ট
    p.update(0.1, {'a'})
    assert p.vx < 0.0
    assert p.facing == -1

    # জাম্প এবং গ্র্যাভিটি টেস্ট
    p.jump()
    assert not p.is_grounded
    assert p.vy > 0.0
    y_before = p.y
    p.update(0.05, set())
    assert p.y > y_before  # উপরে উঠছে

    # কয়েক ফ্রেম পর মাটিতে নামা
    for _ in range(60):
        p.update(0.05, set())
    assert p.is_grounded
    assert p.y == 80.0
    assert p.vy == 0.0

    print("STEP 5 Player movement, gravity arc, and flip transformations verified successfully!")


if __name__ == "__main__":
    test_player_movement_and_physics()
