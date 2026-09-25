"""
# কী করছে: গেমের সমস্ত ফিজিক্স, স্ক্রিন সাইজ, টাইমিং এবং স্পিড কনস্ট্যান্ট কেন্দ্রীয়ভাবে ডিফাইন করছে।
# কেন লাগছে: যাতে কোনো ম্যাজিক নাম্বার কোডে না থাকে এবং ভাইভায় এক জায়গায় চেঞ্জ করে লাইভ এডিট দেখানো যায়।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন কনফিগারেশন ফাইল (যেমন Unreal / Unity Settings / Game Config)।
"""

# Window & Display Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
WINDOW_TITLE = b"Sword Quest - Modern 2D Platformer"
TARGET_FPS = 60
FRAME_TIME_MS = 1000 // TARGET_FPS

# Physics & Player Constants
GRAVITY = 1200.0
PLAYER_SPEED = 240.0
JUMP_VELOCITY = 550.0
PLAYER_WIDTH = 34.0
PLAYER_HEIGHT = 52.0

# Melee Combat / Sword Constants
SWORD_RANGE = 52.0
SWORD_SWING_DURATION = 0.22
SWORD_COOLDOWN = 0.35
SWORD_ARC_START = -50.0
SWORD_ARC_END = 85.0
SWORD_BLADE_WIDTH = 6.0

# Camera & Level Constants
CAMERA_FOLLOW_SPEED = 5.0
CAMERA_LOOKAHEAD_X = 280.0
LEVEL_WIDTH = 3200.0
LEVEL_HEIGHT = 540.0

# Enemy Constants
ENEMY_SPEED = 75.0
ENEMY_WIDTH = 32.0
ENEMY_HEIGHT = 38.0
ENEMY_SQUASH_DURATION = 0.35

# Platform Constants
PLATFORM_DEFAULT_HEIGHT = 20.0

# Collectibles & Objectives
COIN_RADIUS = 11.0
COIN_PULSE_SPEED = 4.0
FLAGPOLE_X = 2960.0
FLAGPOLE_Y = 80.0
FLAGPOLE_HEIGHT = 280.0
FLAG_WIDTH = 60.0
FLAG_HEIGHT = 36.0

# Player Stats & Rules
TOTAL_LIVES = 3
INITIAL_SCORE = 0
COIN_SCORE = 100
ENEMY_SCORE = 250

# Visual Juice & Transitions
TRANSITION_DURATION = 0.30
SCREEN_SHAKE_DURATION = 0.25
SCREEN_SHAKE_INTENSITY = 7.0
HIT_FLASH_DURATION = 0.20
PARALLAX_FACTOR = 0.25
PARTICLE_COUNT_ENEMY = 22
PARTICLE_COUNT_COIN = 14
