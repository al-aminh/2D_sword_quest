"""
# কী করছে: গেমের পুরো লাইফসাইকেল ও স্টেট ট্রানজিশন ফ্লো স্বয়ংক্রিয়ভাবে টেস্ট করছে।
# কেন লাগছে: মেনু -> খেলা -> পজ -> রেজ্যুম -> এন্ড সিন সম্পূর্ণ প্রক্রিয়া ত্রুটিমুক্ত কিনা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: এন্ড-টু-এন্ড ইন্টিগ্রেশন টেস্টিং।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene
from src.scenes.play_scene import PlayScene
from src.scenes.pause_scene import PauseScene
from src.scenes.end_scene import EndScene
from src.core.config import FLAGPOLE_X


def test_entire_game_flow():
    sm = SceneManager()

    # ১. মেনু সিন শুরু
    menu = MenuScene(sm)
    sm.switch_to(menu)
    assert sm.current_scene == menu

    # ২. প্লেয়ার প্লে বাটনে ক্লিক করে
    menu._on_play_click()
    assert sm.transition.is_active()
    # ট্রানজিশন শেষ হওয়া পর্যন্ত আপডেট
    for _ in range(30):
        sm.update(0.02)
    assert isinstance(sm.current_scene, PlayScene)
    play = sm.current_scene

    # ৩. গেমপ্লে মুভমেন্ট ও ফিজিক্স টেস্ট
    init_x = play.player.x
    play.update(0.1)
    # সোর্ড আক্রমণ টেস্ট
    play.player.attack()
    assert play.player.sword.is_swinging
    play.update(0.1)

    # ৪. পজ টেস্ট (ESC চাপলে পজ হবে, স্টেট বজায় থাকবে)
    score_before_pause = play.score
    play.on_key('escape', True)
    assert isinstance(sm.current_scene, PauseScene)
    pause = sm.current_scene

    # পজ মেনুতে খেলা স্থগিত থাকা
    pause.update(0.1)
    assert play.score == score_before_pause

    # ৫. রেজ্যুম টেস্ট
    pause._on_resume()
    assert sm.current_scene == play
    assert play.score == score_before_pause

    # ৬. ফ্ল্যাগপোল পৌঁছে উইন কন্ডিশন টেস্ট
    play.player.x = FLAGPOLE_X
    play.update(0.05)
    # ফেড ট্রানজিশন শেষ হওয়া
    for _ in range(30):
        sm.update(0.02)
    assert isinstance(sm.current_scene, EndScene)
    assert sm.current_scene.is_win

    # ৭. এন্ড সিন থেকে প্লে এগেইন টেস্ট
    sm.current_scene._on_replay()
    for _ in range(30):
        sm.update(0.02)
    assert isinstance(sm.current_scene, PlayScene)

    print("ALL GAMEPLAY AND TRANSITION FLOWS TESTED AND VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    test_entire_game_flow()
