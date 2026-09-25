"""
# কী করছে: স্টেপ ৮-এর কমব্যাট কোলিশন, এনিমি স্কোয়াশ ডেথ এবং হিট রিঅ্যাকশন টেস্ট করছে।
# কেন লাগছে: তরবারি দিয়ে শত্রু নিধন ও সরাসরি ধাক্কায় লাইফ হারানোর মেকানিক্স নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: অ্যাকশন প্ল্যাটফর্মার কমব্যাট ভেরিফিকেশন টেস্ট।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gameplay.player import Player
from src.gameplay.enemy import Enemy
from src.physics.collision import check_sword_enemy_hit, check_player_enemy_contact


def test_combat():
    player = Player(110.0, 80.0)
    enemy = Enemy(125.0, 80.0, 100.0, 200.0)

    # আক্রমণ ছাড়া সরাসরি ধাক্কা
    assert check_player_enemy_contact(player, enemy)

    # প্লেয়ার তরবারি চালায়
    player.attack()
    hitbox = player.sword.get_hitbox()
    assert hitbox is not None
    assert check_sword_enemy_hit(hitbox, enemy)

    # শত্রু নিধন
    burst = enemy.kill()
    assert burst is not None
    assert not enemy.is_alive()
    assert enemy.state == 'DYING'

    # মৃত শত্রুর সাথে আর কোলিশন হবে না
    assert not check_sword_enemy_hit(hitbox, enemy)
    assert not check_player_enemy_contact(player, enemy)

    print("STEP 8 Enemies, Combat Collision, and Shape Drawing verified successfully!")


if __name__ == "__main__":
    test_combat()
