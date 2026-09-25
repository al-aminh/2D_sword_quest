# Sword Quest ⚔️
> **A Modern 2D Melee Platformer built with PyOpenGL & GLUT**  
> *Computer Graphics Sessional Final Project — Legacy Fixed-Function OpenGL*

---

## 🎮 Overview
**Sword Quest** is a 2D side-scrolling action platformer built strictly using **legacy fixed-function OpenGL** (`glBegin` / `glEnd`, `glOrtho`, matrix stacks, and GLUT callbacks). There are **no external game engines** (no Pygame, Arcade, or Godot) and **zero external art or font assets** — every character, enemy, button, rounded panel, particle, and typography element is hand-crafted and rendered directly from raw geometric primitives and mathematical curves.

Beyond gameplay, the project emphasizes a **modern, minimalist UI**:
- **Animated Vector Menus**: Title entry easing, interactive mouse hover highlights, and button press feedback.
- **Cinematic Scene Transitions**: Full-screen alpha cross-fades (`START` ➔ `PLAYING` ➔ `PAUSE` ➔ `WIN` / `GAME_OVER`).
- **Bezier Rounded Panels & Cards**: Dialogs and HUD panels feature rounded corners generated via cubic Bezier curve segments.
- **Smooth Eased Camera**: Follows the player with a lerp formula rather than a rigid clamp.
- **Game Juice & Micro-Interactions**: Particle bursts on enemy defeat and coin pickups, impact hit-flashes, and camera screen-shake.

---

## 🚀 Installation & Running

### 1. Requirements
- Python 3.8+ (tested on Python 3.11)
- OpenGL driver with GLUT/FreeGLUT support

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Installs `PyOpenGL==3.1.10` and `PyOpenGL-accelerate==3.1.10`)*

### 3. Run the Game
Run from the workspace directory:
```bash
python main.py
```

---

## 🕹️ Controls

| Control | Action |
|---|---|
| **A / D** or **Left / Right Arrow** | Move character left / right |
| **SPACE** or **Up Arrow** | Jump (gravity arc physics) |
| **F** | Sword Attack (eased swing arc, melee combat) |
| **ESC** | Pause / Resume Game |
| **Mouse Hover & Left Click** | Interactive Menu Buttons (Play, Resume, Restart, Quit) |

---

## 📐 Computer Graphics Techniques Mapping

This project explicitly implements all 5 core syllabus techniques with standalone implementations:

| # | Technique | Implementation Source | Specific File & Function | Real-World Mapping |
|---|---|---|---|---|
| **1** | **Line & Shape Drawing** | Hand-drawn character, patrolling horned enemy, flagpole, coin geometry, and UI widgets without external sprites | [`src/gameplay/enemy.py`](file:///src/gameplay/enemy.py) (`_draw_body_primitives`), [`src/render/primitives.py`](file:///src/render/primitives.py) (`draw_polygon`, `draw_circle`), [`src/gameplay/flagpole.py`](file:///src/gameplay/flagpole.py) | **vector graphics tools, Google Maps rendering** |
| **2** | **2D Transformations** | Translation, rotation, and non-uniform scaling via `glPushMatrix`, `glPopMatrix`, `glTranslatef`, `glRotatef`, `glScalef` | [`src/gameplay/player.py`](file:///src/gameplay/player.py) (`draw` - facing flip), [`src/gameplay/sword.py`](file:///src/gameplay/sword.py) (`draw` - swing rotation), [`src/gameplay/coin.py`](file:///src/gameplay/coin.py) (`draw` - spinning scale), [`src/physics/camera.py`](file:///src/physics/camera.py) (`apply`), [`src/render/effects.py`](file:///src/render/effects.py) (`draw_parallax_mountains`) | **game engines and animation systems** |
| **3** | **Color Fill** | Smooth Gouraud vertical sky gradient, full-screen hit-flash impact, and full-screen alpha cross-fades | [`src/render/effects.py`](file:///src/render/effects.py) (`draw_gradient_fill`, `draw_screen_flash`), [`src/ui/transition.py`](file:///src/ui/transition.py) (`draw`) | **Photoshop paint bucket / UI hit-flash effects** |
| **4** | **Line Clipping** | Standalone Cohen-Sutherland line clipping algorithm with 4-bit region codes (`INSIDE`, `LEFT`, `RIGHT`, `BOTTOM`, `TOP`), iterative boundary clipping applied to world background grid | [`src/physics/clipping.py`](file:///src/physics/clipping.py) (`clip_line`, `compute_region_code`), [`src/render/effects.py`](file:///src/render/effects.py) (`draw_clipped_background_grid`) | **GPU rendering pipeline, viewport culling** |
| **5** | **Bezier Curves** | Hand-rolled cubic Bezier curve evaluation $B(t)$ and easing functions used across gameplay and UI | [`src/physics/curves.py`](file:///src/physics/curves.py) (`evaluate_cubic_bezier`, `generate_bezier_points`, `ease_in_out_cubic`, `ease_out_cubic`), used in: <br>1. [`src/gameplay/platform.py`](file:///src/gameplay/platform.py) (moving platform trajectory)<br>2. [`src/gameplay/sword.py`](file:///src/gameplay/sword.py) (eased swing angular arc)<br>3. [`src/render/primitives.py`](file:///src/render/primitives.py) (rounded rectangle Bezier corners)<br>4. [`src/ui/transition.py`](file:///src/ui/transition.py) (eased screen cross-fade) | **animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design** |

---

## 🏛️ Project Architecture

```
sword/
├── main.py                        # Entry point: bootstrap.run(MenuScene())
├── requirements.txt               # PyOpenGL & PyOpenGL-accelerate
├── README.md                      # Comprehensive documentation and techniques map
├── docs/
│   ├── part1_problem_discovery.md # Syllabus Part 1 problem discovery template
│   └── part3_reflection_template.md# Syllabus Part 3 reflection questions template
├── tests/                         # Automated test suite (physics, clipping, curves, combat, flow)
└── src/
    ├── app/
    │   ├── bootstrap.py           # GLUT window setup, 60 FPS delta-time loop, callbacks
    │   ├── scene_manager.py       # Active scene orchestrator & cross-fade manager
    │   └── input.py               # Keyboard + mouse event processing & coordinate mapping
    ├── scenes/
    │   ├── base_scene.py          # Abstract Scene base interface
    │   ├── menu_scene.py          # Animated title + interactive hoverable Play/Quit buttons
    │   ├── play_scene.py          # Active gameplay world (player, camera, enemies, platforms, HUD)
    │   ├── pause_scene.py         # Non-destructive modal overlay (Resume / Restart / Quit)
    │   └── end_scene.py           # Win / Game Over summary with Play Again button
    ├── gameplay/
    │   ├── player.py              # Primitive humanoid, gravity physics, facing flip
    │   ├── sword.py               # Melee swing, Bezier easing curve, rotation, hitbox
    │   ├── enemy.py               # Patrol AI, squash animation, death sequence
    │   ├── platform.py            # Static platforms + Bezier moving platform
    │   ├── coin.py                # Collectible gold coins with spinning scale transform
    │   ├── flagpole.py            # End goal flagpole + waving victory banner
    │   └── level_data.py          # Centralized map layout & entity spawn points
    ├── physics/
    │   ├── curves.py              # Cubic Bezier evaluation & easing functions
    │   ├── clipping.py            # Cohen-Sutherland line clipping from scratch
    │   ├── collision.py           # AABB & hitbox intersection detection
    │   └── camera.py              # Smooth lerp-follow camera & viewport transforms
    ├── render/
    │   ├── primitives.py          # Polygons, circles, Bezier-corner rounded rectangles
    │   ├── effects.py             # Sky gradient, particle bursts, screen shake, clipped grid
    │   └── text.py                # GLUT stroke vector typography & bitmap numbers
    ├── ui/
    │   ├── theme.py               # Centralized dark-theme modern color palette
    │   ├── button.py              # Interactive button widget with hover/pressed states
    │   ├── panel.py               # Rounded frosted glass panel container
    │   ├── transition.py          # Eased full-screen cross-fade transition overlay
    │   └── hud.py                 # Live HUD panel (Lives hearts, Score, Time, Hints)
    └── core/
        └── config.py              # Zero magic numbers: all game constants centralized for viva
```

---

## 🎓 Viva & Live-Edit Readiness
Every function in the project was intentionally engineered for an academic computer graphics viva:
- **No Function Exceeds ~40 Lines**: Every function fits comfortably on a single screen without scrolling.
- **Zero Magic Numbers Outside `config.py`**: Changing `GRAVITY`, `PLAYER_SPEED`, `SWORD_RANGE`, `SWORD_COOLDOWN`, `CAMERA_FOLLOW_SPEED`, or `TRANSITION_DURATION` in [`src/core/config.py`](file:///src/core/config.py) instantly modifies gameplay live in front of the examiner.
- **Mandatory 3-Line Bangla Comments**: Every function and non-trivial block includes:
  ```python
  # কী করছে: <what this code does>
  # কেন লাগছে: <why it's needed>
  # real world-এ এটা কোথায় দেখা যায়: <real-world system using this technique>
  ```
- **Single-Function Deletion Clarity**: Removing any single function produces an obvious, easily explainable visual effect (e.g., removing `_draw_legs` removes character limbs, removing `clip_line` demonstrates lines rendering beyond the camera boundary).
