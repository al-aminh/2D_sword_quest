"""
# কী করছে: গেমের প্রতিটি দৃশ্য ও রেন্ডার ফাংশন একটি লাইভ ওপেনজিএল কন্টেক্সটে ড্র করে টেস্ট করছে।
# কেন লাগছে: কোনো ড্র ফাংশনে মিসিং ইম্পোর্ট বা ওপেনজিএল রানটাইম এরর আছে কিনা তা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: গ্রাফিক্স পাইপলাইন রেন্ডার পাস ইন্টিগ্রেশন টেস্ট।
"""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import bootstrap
from src.scenes.menu_scene import MenuScene
from src.scenes.play_scene import PlayScene
from src.scenes.pause_scene import PauseScene
from src.scenes.end_scene import EndScene


class RenderCheckScene:
    def __init__(self, manager):
        self.manager = manager
        self.menu = MenuScene(manager)
        self.play = PlayScene(manager)
        self.pause = PauseScene(manager, self.play)
        self.end_win = EndScene(manager, True, 1000, 45.2)
        self.end_lose = EndScene(manager, False, 250, 15.0)

    def update(self, dt):
        self.menu.update(dt)
        self.play.update(dt)
        self.pause.update(dt)
        self.end_win.update(dt)
        self.end_lose.update(dt)

    def draw(self):
        # প্রতিটি সিনের ড্র ফাংশন ধারাবাহিকভাবে কল করে নিশ্চিত করা
        self.menu.draw()
        self.play.draw()
        self.pause.draw()
        self.end_win.draw()
        self.end_lose.draw()
        print("ALL SCENE RENDER PASSES COMPLETED WITHOUT ERROR!")
        os._exit(0)

    def on_key(self, key, is_down):
        pass

    def on_mouse(self, x, y, button=-1, state=-1):
        pass


def run_test():
    timer = threading.Timer(2.0, lambda: (print("Test timed out"), os._exit(1)))
    timer.daemon = True
    timer.start()

    bootstrap.glutInit()
    bootstrap.glutInitDisplayMode(bootstrap.GLUT_DOUBLE | bootstrap.GLUT_RGBA | bootstrap.GLUT_DEPTH)
    bootstrap.glutInitWindowSize(bootstrap.SCREEN_WIDTH, bootstrap.SCREEN_HEIGHT)
    bootstrap.glutCreateWindow(b"Render Verification")
    bootstrap.setup_projection(bootstrap.SCREEN_WIDTH, bootstrap.SCREEN_HEIGHT)

    check_scene = RenderCheckScene(bootstrap.scene_manager)
    bootstrap.scene_manager.switch_to(check_scene)

    bootstrap.glutDisplayFunc(bootstrap.display_callback)
    bootstrap.glutTimerFunc(16, bootstrap.timer_callback, 0)
    bootstrap.glutMainLoop()


if __name__ == "__main__":
    run_test()
