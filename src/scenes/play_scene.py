"""
# কী করছে: গেমের মূল ইন্টার‍্যাক্টিভ গেমপ্লে দৃশ্য পরিচালনা করে।
# কেন লাগছে: ফিজিক্স, এনিমি কমব্যাট, কয়েন পিকআপ, ফ্ল্যাগপোল উইন এবং হাড এক সূত্রে বাঁধতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিন ওয়ার্ল্ড স্টেজ / লেভেল সিন (Unity Scene / Unreal Map)।
"""

import random
from src.scenes.base_scene import BaseScene
from src.render.effects import (
    draw_gradient_fill, draw_parallax_mountains,
    draw_clipped_background_grid, draw_screen_flash
)
from src.gameplay.player import Player
from src.gameplay.enemy import Enemy
from src.gameplay.coin import Coin
from src.gameplay.flagpole import Flagpole
from src.gameplay.level_data import (
    create_level_platforms, get_enemy_spawn_data, get_coin_spawn_data
)
from src.physics.camera import Camera
from src.physics.collision import (
    check_sword_enemy_hit, check_player_enemy_contact, check_player_coin_pickup
)
from src.ui.hud import HUD
from src.scenes.pause_scene import PauseScene
from src.scenes.end_scene import EndScene
from src.core.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TOTAL_LIVES, INITIAL_SCORE,
    COIN_SCORE, ENEMY_SCORE, SCREEN_SHAKE_DURATION, SCREEN_SHAKE_INTENSITY,
    HIT_FLASH_DURATION
)
from src.app.input import global_input
from src.ui import theme


class PlayScene(BaseScene):
    """
    # কী করছে: লাইভ ওয়ার্ল্ডের ফিজিক্স, সত্ত্বাসমূহ ও রেন্ডার পাস নিয়ন্ত্রণ করে।
    # কেন লাগছে: গেমপ্লে চলাকালীন প্রতিটি ফ্রেমের ক্রিয়া-প্রতিক্রিয়া সমন্বয় করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেমপ্লে অর্কেস্ট্রেটর ক্লাস।
    """

    # কী করছে: প্লে সিনের প্লেয়ার, ক্যামেরা, লেভেল অবজেক্ট ও হাড ইনিশিয়ালাইজ করে।
    # কেন লাগছে: নতুন গেমপ্লে শুরু করার সম্পূর্ণ প্রেক্ষাপট প্রস্তুত করতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম স্টেট কনস্ট্রাক্টর।
    def __init__(self, manager=None):
        super().__init__(manager)
        self.player = Player(120.0, 80.0)
        self.camera = Camera()
        self.hud = HUD()
        self.flagpole = Flagpole()
        self.platforms = create_level_platforms()
        self.enemies = [Enemy(d["x"], d["y"], d["min_x"], d["max_x"]) for d in get_enemy_spawn_data()]
        self.coins = [Coin(x, y) for (x, y) in get_coin_spawn_data()]
        self.particle_bursts = []

        self.score = INITIAL_SCORE
        self.lives = TOTAL_LIVES
        self.elapsed_time = 0.0
        self.invulnerable_timer = 0.0
        self.shake_timer = 0.0
        self.flash_alpha = 0.0
        self.game_ended = False

    # কী করছে: তলোয়ারের আঘাত ও শত্রুর সাথে সংঘর্ষের ফলাফল আপডেট করে।
    # কেন লাগছে: ওয়ান-হিট শত্রু বধ ও ক্ষতিসাধন সঠিক নিয়মে হ্যান্ডল করতে।
    # real world-এ এটা কোথায় দেখা যায়: কমব্যাট রেজোলিউশন সিস্টেম।
    def _update_combat(self):
        sword_hitbox = self.player.sword.get_hitbox()
        if sword_hitbox:
            for enemy in self.enemies:
                if enemy.is_alive() and check_sword_enemy_hit(sword_hitbox, enemy):
                    burst = enemy.kill()
                    self.particle_bursts.append(burst)
                    self.score += ENEMY_SCORE

        if self.invulnerable_timer <= 0.0:
            for enemy in self.enemies:
                if enemy.is_alive() and check_player_enemy_contact(self.player, enemy):
                    self.lives -= 1
                    self.invulnerable_timer = 1.2
                    self.shake_timer = SCREEN_SHAKE_DURATION
                    self.flash_alpha = 0.45
                    if self.lives <= 0 and not self.game_ended:
                        self.game_ended = True
                        self.manager.switch_to(EndScene(self.manager, False, self.score, self.elapsed_time), True)
                    break

    # কী করছে: সংগ্রাহ্য কয়েন ও ফ্ল্যাগপোলের সাথে প্লেয়ারের ইন্টার‍্যাকশন চালায়।
    # কেন লাগছে: কয়েন কুড়ানো ও লেভেল সমাপ্তি চিহ্নিত করতে।
    # real world-এ এটা কোথায় দেখা যায়: পিকআপ অ্যান্ড অবজেক্টিভ ইভেন্ট লুপ।
    def _update_collectibles(self):
        for coin in self.coins:
            if not coin.collected and check_player_coin_pickup(self.player, coin):
                burst = coin.collect()
                self.particle_bursts.append(burst)
                self.score += COIN_SCORE

        # ফ্ল্যাগপোল স্পর্শ পরীক্ষা (বিজয়)
        if not self.game_ended:
            half_pw = self.player.width * 0.4
            p_box = (self.player.x - half_pw, self.player.y, self.player.x + half_pw, self.player.y + self.player.height)
            from src.physics.collision import check_aabb_overlap
            if check_aabb_overlap(p_box, self.flagpole.get_bounding_box()):
                self.game_ended = True
                self.score += 500  # বিজয় বোনাস
                self.manager.switch_to(EndScene(self.manager, True, self.score, self.elapsed_time), True)

    # কী করছে: স্ক্রিন শেক, হিট ফ্ল্যাশ এবং পার্টিকেল প্রভাবগুলোর সময় গণনা করে।
    # কেন লাগছে: আধুনিক জুস ইফেক্টগুলোকে মসৃণভাবে ক্ষয়প্রাপ্ত করতে।
    # real world-এ এটা কোথায় দেখা যায়: VFX লাইফটাইম কন্ট্রোলার।
    def _update_effects(self, dt: float):
        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt
        if self.flash_alpha > 0.0:
            self.flash_alpha = max(0.0, self.flash_alpha - dt * 2.5)

        if self.shake_timer > 0.0:
            self.shake_timer -= dt
            intensity = SCREEN_SHAKE_INTENSITY * (self.shake_timer / SCREEN_SHAKE_DURATION)
            self.camera.shake_x = random.uniform(-intensity, intensity)
            self.camera.shake_y = random.uniform(-intensity, intensity)
        else:
            self.camera.shake_x = 0.0
            self.camera.shake_y = 0.0

        self.particle_bursts = [pb for pb in self.particle_bursts if pb.update(dt)]

    # কী করছে: গেমপ্লের সামগ্রিক মেকানিক্স প্রতি ফ্রেমে আপডেট করে।
    # কেন লাগছে: খেলোয়াড়, শত্রু, ক্যামেরা ও ফিজিক্সের গতি বজায় রাখতে।
    # real world-এ এটা কোথায় দেখা যায়: গেম মেইন লজিক টিক।
    def update(self, dt: float):
        if self.game_ended:
            return
        self.elapsed_time += dt

        for plat in self.platforms:
            if hasattr(plat, 'update'):
                plat.update(dt)

        self.player.update(dt, global_input.keys_down, self.platforms)
        self.camera.update(self.player.x, dt)

        for enemy in self.enemies:
            enemy.update(dt)
        for coin in self.coins:
            coin.update(dt)
        self.flagpole.update(dt)

        self._update_combat()
        self._update_collectibles()
        self._update_effects(dt)

    # কী করছে: ক্যামেরা স্পেসে ওয়ার্ল্ড অবজেক্ট (প্ল্যাটফর্ম, প্লেয়ার, শত্রু, কয়েন) আঁকে।
    # কেন লাগছে: ক্যামেরার স্থানান্তরের প্রেক্ষিতে ওয়ার্ল্ড উপাদান রেন্ডার করতে।
    # real world-এ এটা কোথায় দেখা যায়: 2D Transformations -> game engines and animation systems
    def _draw_world(self):
        self.camera.apply()
        # ম্যানুয়াল কোহেন-সাদারল্যান্ড ক্লিপ করা গ্রিড
        draw_clipped_background_grid(self.camera.get_viewport_bounds())

        for plat in self.platforms:
            plat.draw()
        for coin in self.coins:
            coin.draw()
        self.flagpole.draw()
        for enemy in self.enemies:
            enemy.draw()
        for pb in self.particle_bursts:
            pb.draw()

        self.player.draw()
        self.camera.unapply()

    # কী করছে: ব্যাকগ্রাউন্ড গ্রেডিয়েন্ট, প্যারালাক্স পাহাড়, ওয়ার্ল্ড ও হাড রেন্ডার করে।
    # কেন লাগছে: গেমের সম্পূর্ণ ভিজ্যুয়াল লেয়ার স্ক্রিনে প্রস্তুত করতে।
    # real world-এ এটা কোথায় দেখা যায়: রেন্ডার পাইপলাইন কম্পোজিশন স্টেজ।
    def draw(self):
        draw_gradient_fill(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, theme.COLOR_SKY_TOP, theme.COLOR_SKY_BOTTOM)
        draw_parallax_mountains(self.camera.x)
        self._draw_world()
        draw_screen_flash((0.95, 0.25, 0.25), self.flash_alpha)
        self.hud.draw(self.score, self.lives, self.elapsed_time)

    # কী করছে: জাম্প, সোর্ড অ্যাটাক ও পজ কিবোর্ড ইভেন্ট হ্যান্ডল করে।
    # কেন লাগছে: কীবোর্ডের মাধ্যমে গেমপ্লে নিয়ন্ত্রণ ও ESC চাপে পজ সিনের ডাক দিতে।
    # real world-এ এটা কোথায় দেখা যায়: গেমপ্লে ইনপুট ডিসপ্যাচ।
    def on_key(self, key: str, is_down: bool):
        if is_down:
            if key == 'space' or key == 'up':
                self.player.jump()
            elif key == 'f':
                self.player.attack()
            elif key == 'escape':
                self.manager.switch_to(PauseScene(self.manager, self), with_transition=False)
