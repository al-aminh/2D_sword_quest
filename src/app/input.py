"""
# কী করছে: গ্লোবাল ইনপুট স্টেট (কিবোর্ড ও মাউস) ম্যানেজ ও কনভার্ট করছে।
# কেন লাগছে: গেমের প্রতিটি ফ্রেমের মসৃণ কন্ট্রোল ও মাউস পজিশন নির্ভুলভাবে ট্র্যাক করতে।
# real world-এ এটা কোথায় দেখা যায়: ইনপুট অ্যাবস্ট্রাকশন লেয়ার (যেমন SDL2 / GLFW Input Handling)।
"""

from typing import Tuple
from OpenGL.GLUT import (
    GLUT_KEY_LEFT, GLUT_KEY_RIGHT, GLUT_KEY_UP, GLUT_KEY_DOWN,
    GLUT_LEFT_BUTTON, GLUT_DOWN, GLUT_UP
)
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


class InputState:
    """
    # কী করছে: কিবোর্ড ও মাউসের বর্তমান স্টেট এবং একশন ট্র্যাক করে।
    # কেন লাগছে: ফ্রেমভিত্তিক কি-প্রেস এবং মাউস ইন্টার‍্যাকশন আলাদাভাবে রেকর্ড রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিনের ইনপুট ম্যানেজার (Input Manager System)।
    """

    # কী করছে: ইনপুট স্টেট ভেরিয়েবল ও প্রাথমিক ভিউপোর্ট স্কেলিং ইনিশিয়ালাইজ করে।
    # কেন লাগছে: প্রারম্ভিক কিবোর্ড ও মাউস স্থিতি শূন্য অবস্থায় সেট করতে।
    # real world-এ এটা কোথায় দেখা যায়: ইনপুট সিস্টেম ইনিশিয়ালাইজেশন।
    def __init__(self):
        self.keys_down = set()
        self.keys_pressed = set()
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.mouse_left_down = False
        self.mouse_left_clicked = False
        self.vp_x = 0.0
        self.vp_y = 0.0
        self.vp_w = float(SCREEN_WIDTH)
        self.vp_h = float(SCREEN_HEIGHT)
        self.win_h = float(SCREEN_HEIGHT)

    # কী করছে: উইন্ডো রিসাইজ হলে বর্তমান ভিউপোর্ট মান আপডেট করে।
    # কেন লাগছে: ফুলস্ক্রিন বা বড় উইন্ডোতেও মাউস স্থানাঙ্ক সঠিকভাবে রূপান্তর করতে।
    # real world-এ এটা কোথায় দেখা যায়: ভিউপোর্ট টু ভার্চুয়াল স্ক্রিন কোঅর্ডিনেট ম্যাপিং।
    def update_viewport(self, vx: int, vy: int, vw: int, vh: int, win_h: int):
        self.vp_x = float(vx)
        self.vp_y = float(vy)
        self.vp_w = float(vw) if vw > 0 else 1.0
        self.vp_h = float(vh) if vh > 0 else 1.0
        self.win_h = float(win_h) if win_h > 0 else 1.0

    # কী করছে: উইন্ডোর মাউস পিক্সেলকে গেমের ভার্চুয়াল ২ডি কোঅর্ডিনেটে রূপান্তর করে।
    # কেন লাগছে: উইন্ডো বড় বা ছোট করলেও বাটন ক্লিক ও হোভার যাতে সঠিক জায়গায় থাকে।
    # real world-এ এটা কোথায় দেখা যায়: GUI Resolution Independent Scaling / Input Mapping।
    def _transform_mouse_coords(self, raw_x: float, raw_y: float) -> Tuple[float, float]:
        y_from_bot = self.win_h - raw_y
        norm_x = (raw_x - self.vp_x) / self.vp_w
        norm_y = (y_from_bot - self.vp_y) / self.vp_h
        vx = max(0.0, min(float(SCREEN_WIDTH), norm_x * float(SCREEN_WIDTH)))
        vy = max(0.0, min(float(SCREEN_HEIGHT), norm_y * float(SCREEN_HEIGHT)))
        return vx, vy

    # কী করছে: প্রতিটি ফ্রেমের শেষে ওয়ান-শট ইভেন্টগুলো ক্লিয়ার করে।
    # কেন লাগছে: একক ক্লিক বা কি-প্রেস যাতে একাধিকবার ট্রিগার না হয়।
    # real world-এ এটা কোথায় দেখা যায়: ফ্রেম বাফার ফ্ল্যাশ এবং ইভেন্ট রিসেট লজিক।
    def update_frame(self):
        self.keys_pressed.clear()
        self.mouse_left_clicked = False

    # কী করছে: যেকোনো সাধারণ কি প্রেস বা রিলিজ হ্যান্ডল করে।
    # কেন লাগছে: ক্যারেক্টার মুভমেন্ট ও জাম্পের বোতাম ট্র্যাক করতে।
    # real world-এ এটা কোথায় দেখা যায়: লো-লেভেল ওএস কিবোর্ড ইন্টারাপ্ট প্রসেসিং।
    def handle_keyboard(self, key, is_down: bool):
        key_str = self._normalize_key(key)
        if is_down:
            if key_str not in self.keys_down:
                self.keys_pressed.add(key_str)
            self.keys_down.add(key_str)
        else:
            self.keys_down.discard(key_str)

    # কী করছে: অ্যারো কি-এর মতো স্পেশাল কি প্রেস বা রিলিজ হ্যান্ডল করে।
    # কেন লাগছে: নেভিগেশন ও দিক নিয়ন্ত্রণের বোতাম শনাক্ত করতে।
    # real world-এ এটা কোথায় দেখা যায়: হার্ডওয়্যার স্পেশাল স্ক্যানকোড ম্যাপিং।
    def handle_special(self, key, is_down: bool):
        key_map = {
            GLUT_KEY_LEFT: 'left',
            GLUT_KEY_RIGHT: 'right',
            GLUT_KEY_UP: 'up',
            GLUT_KEY_DOWN: 'down'
        }
        name = key_map.get(key)
        if name:
            if is_down:
                if name not in self.keys_down:
                    self.keys_pressed.add(name)
                self.keys_down.add(name)
            else:
                self.keys_down.discard(name)

    # কী করছে: মাউসের ক্লিক ইভেন্ট ভার্চুয়াল কোঅর্ডিনেটে রূপান্তর করে সংরক্ষণ করে।
    # কেন লাগছে: যে কোনো সাইজের উইন্ডোতে ইউআই বাটন ক্লিক নিখুঁতভাবে রেজিস্টার করতে।
    # real world-এ এটা কোথায় দেখা যায়: উইন্ডোজ ও ম্যাক ওএস মাউস পয়েন্টার ট্র্যাকিং।
    def handle_mouse(self, button, state, x, y):
        self.mouse_x, self.mouse_y = self._transform_mouse_coords(float(x), float(y))
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                self.mouse_left_down = True
                self.mouse_left_clicked = True
            elif state == GLUT_UP:
                self.mouse_left_down = False

    # কী করছে: মাউস নাড়ালে ভার্চুয়াল কোঅর্ডিনেট হিসেব করে আপডেট করে।
    # কেন লাগছে: উইন্ডো বড় করলেও বাটনের ওপর কার্সার আনলে হোভার প্রতিক্রিয়া পেতে।
    # real world-এ এটা কোথায় দেখা যায়: ডেক্সটপ উইন্ডো ম্যানেজার মাউস মুভ ডিসপ্যাচ।
    def handle_mouse_motion(self, x, y):
        self.mouse_x, self.mouse_y = self._transform_mouse_coords(float(x), float(y))

    # কী করছে: বাইটস কিবোর্ড কোডকে সাধারণ টেক্সট স্ট্রিং-এ রূপান্তর করে।
    # কেন লাগছে: প্ল্যাটফর্ম বা পাইথন সংস্করণের ভিন্নতায় সঠিক কি ম্যাপিং করতে।
    # real world-এ এটা কোথায় দেখা যায়: ক্যারেক্টার এনকোডিং ও কীবোর্ড লেআউট পার্সিং।
    def _normalize_key(self, key) -> str:
        if isinstance(key, bytes):
            if key == b'\x1b':
                return 'escape'
            if key == b' ':
                return 'space'
            try:
                return key.decode('utf-8').lower()
            except UnicodeDecodeError:
                return ''
        if key == ' ':
            return 'space'
        return str(key).lower()


# গ্লোবাল ইনপুট ম্যানেজার ইনস্ট্যান্স
global_input = InputState()
