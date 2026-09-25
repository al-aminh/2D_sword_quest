"""
# কী করছে: গেমের সমস্ত সত্ত্বার মধ্যে ২ডি কোলিশন ডিটেকশন (AABB ও হিটবক্স ইন্টারসেকশন) পরিচালনা করে।
# কেন লাগছে: প্লেয়ার, শত্রু, তরবারি ও পিকআপের সংঘর্ষ সঠিকভাবে শনাক্ত করতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন ফিজিক্স কোলিশন পাইপলাইন (AABB Tree & Broadphase/Narrowphase)।
"""

from typing import Tuple


# কী করছে: দুটি অক্ষ-সমান্তরাল আয়তক্ষেত্রের (AABB) মধ্যে ওভারল্যাপ পরীক্ষা করে।
# কেন লাগছে: দ্রুত ও দক্ষ উপায়ে দুটি গেম অবজেক্টের সীমানা স্পর্শ করেছে কিনা বুঝতে।
# real world-এ এটা কোথায় দেখা যায়: AABB বাউন্ডিং বক্স ইন্টারসেকশন অ্যালগরিদম।
def check_aabb_overlap(
    box_a: Tuple[float, float, float, float],
    box_b: Tuple[float, float, float, float]
) -> bool:
    return not (
        box_a[2] < box_b[0] or  # a_max_x < b_min_x
        box_a[0] > box_b[2] or  # a_min_x > b_max_x
        box_a[3] < box_b[1] or  # a_max_y < b_min_y
        box_a[1] > box_b[3]     # a_min_y > b_max_y
    )


# কী করছে: আক্রমণকালীন তরবারির আর্কের হিটবক্স শত্রুর দেহের সাথে লেগেছে কিনা পরীক্ষা করে।
# কেন লাগছে: শত্রুর ওপর তরবারির সফল আঘাত শনাক্ত করতে।
# real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
def check_sword_enemy_hit(sword_hitbox: Tuple[float, float, float, float], enemy) -> bool:
    if not sword_hitbox or not enemy.is_alive():
        return False
    enemy_box = enemy.get_bounding_box()
    return check_aabb_overlap(sword_hitbox, enemy_box)


# কী করছে: প্লেয়ারের দেহ এবং জীবিত শত্রুর দেহের মধ্যে সরাসরি স্পর্শ ঘটেছে কিনা পরীক্ষা করে।
# কেন লাগছে: প্লেয়ারের ক্ষতি হওয়া ও জীবন হারানোর শর্ত নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: ক্যারেক্টার হার্টবক্স কোলিশন ডিটেকশন।
def check_player_enemy_contact(player, enemy) -> bool:
    if not enemy.is_alive():
        return False
    half_pw = player.width * 0.4
    player_box = (
        player.x - half_pw, player.y,
        player.x + half_pw, player.y + player.height
    )
    enemy_box = enemy.get_bounding_box()
    return check_aabb_overlap(player_box, enemy_box)


# কী করছে: প্লেয়ারের সাথে কয়েনের সংঘর্ষ পরীক্ষা করে।
# কেন লাগছে: খেলোয়াড় কয়েন স্পর্শ করলে তা সংগ্রহ করতে।
# real world-এ এটা কোথায় দেখা যায়: ট্রিগার কোলিশন অ্যান্ড আইটেম পিকআপ সিস্টেম।
def check_player_coin_pickup(player, coin) -> bool:
    if coin.collected:
        return False
    half_pw = player.width * 0.5
    player_box = (
        player.x - half_pw, player.y,
        player.x + half_pw, player.y + player.height
    )
    coin_box = coin.get_bounding_box()
    return check_aabb_overlap(player_box, coin_box)
