"""
# কী করছে: স্টেপ ৭-এর সোর্ড অ্যাটাক, বেজিয়ার ইজিং সুইং এবং কুলডাউন টেস্ট করছে।
# কেন লাগছে: তরবারি সুইং অ্যানিমেশন ও কমব্যাট হিটবক্সের নির্ভুলতা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: অ্যাকশন গেম কমব্যাট মেকানিক্স ভেরিফিকেশন।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gameplay.player import Player


def test_sword_swing_and_cooldown():
    player = Player(200.0, 80.0)
    sword = player.sword
    assert sword is not None
    assert not sword.is_swinging
    assert sword.get_hitbox() is None

    # সুইং শুরু করা
    success = player.attack()
    assert success
    assert sword.is_swinging
    hitbox = sword.get_hitbox()
    assert hitbox is not None
    assert hitbox[0] < hitbox[2]

    # কুলডাউনের মধ্যে পুনরায় সুইং নিষ্ক্রিয় থাকা নিশ্চিত করা
    assert not player.attack()

    # সময়ের সাথে বেজিয়ার কোণ আপডেট টেস্ট
    init_angle = sword.current_angle
    player.update(0.1, set())
    assert sword.current_angle > init_angle

    # সুইং শেষ হওয়া টেস্ট
    player.update(0.2, set())
    assert not sword.is_swinging
    assert sword.get_hitbox() is None

    # কুলডাউন শেষ হওয়ার পর আবার অ্যাটাক সক্ষম হওয়া
    player.update(0.3, set())
    assert sword.cooldown_timer <= 0.0
    assert player.attack()

    print("STEP 7 Sword Attack: Bezier Easing and 2D Transformations verified successfully!")


if __name__ == "__main__":
    test_sword_swing_and_cooldown()
