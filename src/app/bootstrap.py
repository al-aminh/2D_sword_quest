"""
# কী করছে: গেমের মেইন উইন্ডো, ওপেনজিএল কন্টেক্সট এবং গেমলুপ বুটস্ট্র্যাপ করছে।
# কেন লাগছে: গেম উইন্ডো প্রদর্শন ও ডেল্টা-টাইম ভিত্তিক ফ্রেমরেট নিয়ন্ত্রণ করার জন্য।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন বুটস্ট্র্যাপ ও এন্ট্রি-পয়েন্ট লাইফসাইকেল।
"""

import time
from OpenGL.GL import (
    glMatrixMode, glLoadIdentity, glOrtho, glViewport,
    glClearColor, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
    GL_PROJECTION, GL_MODELVIEW
)
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutReshapeFunc, glutTimerFunc,
    glutKeyboardFunc, glutKeyboardUpFunc, glutSpecialFunc, glutSpecialUpFunc,
    glutMouseFunc, glutMotionFunc, glutPassiveMotionFunc, glutSwapBuffers,
    glutPostRedisplay, glutMainLoop,
    GLUT_DOUBLE, GLUT_RGBA, GLUT_DEPTH
)

from src.core.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FRAME_TIME_MS
)
from src.app.input import global_input
from src.app.scene_manager import SceneManager

# গ্লোবাল অ্যাপ রেফারেন্স
scene_manager = SceneManager()
_last_frame_time = 0.0


# গ্লোবাল ভিউপোর্ট ভ্যারিয়েবল
window_w = SCREEN_WIDTH
window_h = SCREEN_HEIGHT
viewport_x = 0
viewport_y = 0
viewport_w = SCREEN_WIDTH
viewport_h = SCREEN_HEIGHT


# কী করছে: অ্যাসপেক্ট রেশিও বজায় রেখে লেটারবক্স ভিউপোর্ট ও অর্থোগ্রাফিক প্রজেকশন সেট আপ করে।
# কেন লাগছে: উইন্ডো বড় করলেও গ্রাফিক্স না ছড়িয়ে সঠিক অনুপাতে সুন্দরভাবে প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: ২ডি গেম ক্যামেরা ও অর্থোগ্রাফিক প্রজেকশন পাইপলাইন।
def setup_projection(width: int, height: int):
    global window_w, window_h, viewport_x, viewport_y, viewport_w, viewport_h
    width = max(1, width)
    height = max(1, height)
    window_w = width
    window_h = height

    target_aspect = float(SCREEN_WIDTH) / float(SCREEN_HEIGHT)
    window_aspect = float(width) / float(height)

    if window_aspect >= target_aspect:
        viewport_h = height
        viewport_w = int(height * target_aspect)
        viewport_x = int((width - viewport_w) * 0.5)
        viewport_y = 0
    else:
        viewport_w = width
        viewport_h = int(width / target_aspect)
        viewport_x = 0
        viewport_y = int((height - viewport_h) * 0.5)

    global_input.update_viewport(viewport_x, viewport_y, viewport_w, viewport_h, window_h)

    glViewport(viewport_x, viewport_y, viewport_w, viewport_h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, float(SCREEN_WIDTH), 0.0, float(SCREEN_HEIGHT), -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# কী করছে: পুরো উইন্ডো ক্লিয়ার করে গেম ভিউপোর্টে সিন রেন্ডার করে।
# কেন লাগছে: উইন্ডো রিসাইজ হলেও চারপাশের মার্জিনসহ নিখুঁতভাবে ফ্রেম প্রদর্শন করতে।
# real world-এ এটা কোথায় দেখা যায়: ভিডিও গেম রেন্ডার পাস এক্সিকিউশন।
def display_callback():
    glViewport(0, 0, window_w, window_h)
    glClearColor(0.05, 0.06, 0.08, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glViewport(viewport_x, viewport_y, viewport_w, viewport_h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    scene_manager.draw()
    glutSwapBuffers()


# কী করছে: প্রতি ফ্রেমের ডেল্টা-টাইম হিসাব করে গেম লজিক আপডেট করে।
# কেন লাগছে: ৬০ এফপিএস রিফ্রেশ রেট বজায় রাখতে এবং স্মুথ অ্যানিমেশন দিতে।
# real world-এ এটা কোথায় দেখা যায়: ফিক্সড ও ডাইনামিক ফ্রেমরেট গেম লুপ।
def timer_callback(_):
    global _last_frame_time
    now = time.perf_counter()
    dt = now - _last_frame_time
    _last_frame_time = now

    # ফ্রেম ড্রপ সীমাবদ্ধ রাখা
    if dt > 0.05:
        dt = 0.05

    scene_manager.update(dt)
    global_input.update_frame()

    glutPostRedisplay()
    glutTimerFunc(FRAME_TIME_MS, timer_callback, 0)


# কী করছে: উইন্ডোর আকার পরিবর্তন হলেও নির্দিষ্ট প্রজেকশন ধরে রাখে।
# কেন লাগছে: ব্যবহারকারী উইন্ডো রিসাইজ করলে গ্রাফিক্স বিকৃত হওয়া রোধ করতে।
# real world-এ এটা কোথায় দেখা যায়: উইন্ডো ডিসপ্লে রেজোলিউশন অ্যাডাপ্টার।
def reshape_callback(width: int, height: int):
    setup_projection(width, height)
    glutPostRedisplay()


# কী করছে: সাধারণ কিবোর্ড ডাউন ইভেন্ট ইনপুট হ্যান্ডলারে পাঠায়।
# কেন লাগছে: মুভমেন্ট বা জাম্প বাটন প্রেস শনাক্ত করতে।
# real world-এ এটা কোথায় দেখা যায়: কীবোর্ড ইভেন্ট লিসেনার।
def keyboard_down_callback(key, x, y):
    global_input.handle_keyboard(key, True)
    key_str = global_input._normalize_key(key)
    scene_manager.on_key(key_str, True)


# কী করছে: কিবোর্ড বাটন ছেড়ে দিলে তা আপডেট করে।
# কেন লাগছে: বোতাম রিলিজের পর ক্যারেক্টার থামা নিশ্চিত করতে।
# real world-এ এটা কোথায় দেখা যায়: কীবোর্ড কি-আপ ইন্টারাপ্ট সার্ভিস।
def keyboard_up_callback(key, x, y):
    global_input.handle_keyboard(key, False)
    key_str = global_input._normalize_key(key)
    scene_manager.on_key(key_str, False)


# কী করছে: অ্যারো কি প্রেস শনাক্ত করে ইনপুটে পাঠায়।
# কেন লাগছে: তীর চিহ্নের সাহায্যে ক্যারেক্টার সরাতে।
# real world-এ এটা কোথায় দেখা যায়: স্পেশাল কি কোড ডিকোডার।
def special_down_callback(key, x, y):
    global_input.handle_special(key, True)
    kmap = {100: 'left', 102: 'right', 101: 'up', 103: 'down'}
    scene_manager.on_key(kmap.get(key, ''), True)


# কী করছে: অ্যারো কি ছেড়ে দিলে তা রেকর্ড করে।
# কেন লাগছে: তীর বোতাম ছেড়ে দেওয়ার সঠিক প্রতিক্রিয়া পেতে।
# real world-এ এটা কোথায় দেখা যায়: কীবোর্ড স্ট্যাটাস ট্র্যাকার।
def special_up_callback(key, x, y):
    global_input.handle_special(key, False)
    kmap = {100: 'left', 102: 'right', 101: 'up', 103: 'down'}
    scene_manager.on_key(kmap.get(key, ''), False)


# কী করছে: মাউস ক্লিক ইভেন্ট গ্রহণ করে সিনে পাঠায়।
# কেন লাগছে: ইউআই বোতাম ক্লিকে সাড়া দিতে।
# real world-এ এটা কোথায় দেখা যায়: মাউস ইন্টার‍্যাকশন সিস্টেম।
def mouse_callback(button, state, x, y):
    global_input.handle_mouse(button, state, x, y)
    scene_manager.on_mouse(global_input.mouse_x, global_input.mouse_y, button, state)


# কী করছে: মাউস কার্সার নাড়াচাড়া করলে পজিশন আপডেট করে।
# কেন লাগছে: বাটন হোভার অ্যানিমেশন স্মুথ করতে।
# real world-এ এটা কোথায় দেখা যায়: ইউআই কার্সার ট্র্যাকিং।
def motion_callback(x, y):
    global_input.handle_mouse_motion(x, y)
    scene_manager.on_mouse(global_input.mouse_x, global_input.mouse_y)


# কী করছে: ওপেনজিএল এবং গ্লুট উইন্ডো ইনিশিয়ালাইজ করে গেম শুরু করে।
# কেন লাগছে: পুরো অ্যাপ্লিকেশনটি রান ও ডিসপ্লে করার কেন্দ্রীয় সূচনা বিন্দু হিসেবে।
# real world-এ এটা কোথায় দেখা যায়: অ্যাপ্লিকেশন ইঞ্জিন রান মেথড।
def run(initial_scene=None):
    global _last_frame_time
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(WINDOW_TITLE)

    setup_projection(SCREEN_WIDTH, SCREEN_HEIGHT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    if initial_scene:
        scene_manager.switch_to(initial_scene)

    _last_frame_time = time.perf_counter()
    glutDisplayFunc(display_callback)
    glutReshapeFunc(reshape_callback)
    glutKeyboardFunc(keyboard_down_callback)
    glutKeyboardUpFunc(keyboard_up_callback)
    glutSpecialFunc(special_down_callback)
    glutSpecialUpFunc(special_up_callback)
    glutMouseFunc(mouse_callback)
    glutMotionFunc(motion_callback)
    glutPassiveMotionFunc(motion_callback)
    glutTimerFunc(FRAME_TIME_MS, timer_callback, 0)

    glutMainLoop()
