# Sky Warrior

![SkyWarrior Banner](https://sky-warrior.s3.us-east-2.amazonaws.com/images/background.png)

**Sky Warrior** is a fast-paced 2D space combat game built with **Python** and **Pygame**. Pilot your spaceship through waves of AI-driven fighters, dodge missiles, and emerge victorious by unlocking higher levels. The gameplay features **intense dogfights**, **EMP attacks**, **turbo boosts**, **slow motion** mechanics, and a **score system** that rewards smart tactics.

---

## Table of Contents
- [Features](#features)
- [Gameplay](#gameplay)
- [Controls](#controls)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Running from the Pre-Built Distribution](#running-from-the-pre-built-distribution)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)
- [Contact](#contact)

---

## Features

1. **Multiple Levels & Level Unlocks**  
   - Progress through 5 levels of increasing difficulty.  
   - Levels are loaded from `levels.json` and controlled by an internal **SQLite** database.

2. **Diverse Enemy Fighters**  
   - **Standard Fighter**: Launches missiles and fires bullets.  
   - **EMP Fighter**: Fires an EMP pulse that slows or disables your ship for a short duration.

3. **Adaptive AI**  
   - A centralized AI (`brain.py`) dynamically controls how fighters maintain distance, slow down, or turn away from threats.

4. **Slow Motion Mechanic**  
   - Trigger slow motion with `Left Ctrl` / `Right Ctrl` for tactical advantages.

5. **Turbo Boost**  
   - Hit `Left Shift` for a speed burst—provided you have enough **turbo** charge left.

6. **Scenic Background & Clouds**  
   - Dynamic cloud images that wrap around the screen, giving the impression of a vast environment.

7. **Minimap**  
   - A small minimap helps you track nearby enemies, missiles, and important objects.

8. **Particle Effects & Explosions**  
   - Bullet trails, missile explosions, screen shake, and spark effects for an immersive experience.

9. **Database-Driven Progress**  
   - Your **high score** and **unlocked levels** are stored in a local SQLite database (`db/` folder) for persistence.

---

## Gameplay

You control a **player spaceship** in a top-down view. Survive waves of enemies, shoot them down, and avoid collisions:

- Use your **Throttle** to control speed, turning to outmaneuver enemy ships.  
- Launch bullets to deal continuous damage and keep foes at bay.  
- Fire or dodge **missiles**—they are lethal but have limited fuel.  
- Stay alert for **EMP blasts** that can halt your engines.  
- Complete each level by destroying all fighters on-screen.

**Objective:** Accumulate the highest possible score through efficient kills, minimal damage taken, and level completions.

---

## Controls

- **Movement & Steering**  
  - **Turn Left:** `A`  
  - **Turn Right:** `D`  
  - **Throttle Up (Increase Speed):** `W`  
  - *(Throttle Down can happen automatically when you release `W` or based on code logic.)*

- **Actions**  
  - **Shoot Bullets:** `Spacebar`  
  - **Turbo Boost:** `Left Shift`  
  - **Slow Motion:** `Left Ctrl` or `Right Ctrl`  

- **Pause / Menu**  
  - **Pause or Open Game Menu:** `Escape`  
  - **Navigate Menus:** Mouse click

---

## Score System

Your **Score** updates dynamically based on your performance:

1. **Enemy Destruction**  
   - **Standard Fighter:** +100 points  
   - **EMP Fighter:** +100 points, plus an extra **+50** bonus  

2. **Taking Damage**  
   - **Hit by Missile:** –50 points  
   - **Hit by Enemy Bullets:** –10 points  

3. **Level Completion**  
   - Clearing a level (all fighters and missiles destroyed) grants **+500** bonus points.

4. **Floating Score & Animation**  
   - Each point gain/loss is briefly displayed near the impact or destroyed entity.  
   - The current **Score** is always visible in the top-right HUD.

5. **High Score Tracking**  
   - If your total score exceeds the existing high score, it updates automatically in the local SQLite database.  
   - Compete against your personal best each session!

---

## Installation

### Prerequisites

- **Python 3.7 or higher**  
  Ensure Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/rushi1222/skywars.git
cd SKYWARRIOR
```

---

## Running the Game

1. **Navigate to the Project Directory:**

   ```bash
   cd source
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    # On Linux/Mac:
    source venv/bin/activate
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Game**:

   ```bash
   python main.py
   ```

   This command will launch the SkyWars game window. Use the controls outlined above to start playing.

---

## Running from the Pre-Built Distribution

For convenience, a **pre-built** version of **Sky Warrior** is available. You can:

1. **Download the ZIP** from:  
   [**dist.zip**](https://sky-warrior.s3.us-east-2.amazonaws.com/dist.zip)

2. **Extract** the ZIP to any folder on your system.

3. **Locate and run** `main.exe` in the **main directory** of the extracted folder:
   - Double-click `main.exe` to launch the game—no additional setup required.

*(Make sure your system allows executing files from unknown sources. On Windows, you might need to “Allow app to run” when prompted.)*

---

## Project Structure

```
skywarrior/
├── db/ *(SQLite database file)*
├── README.md
├── source/
  ├── levels.json
  ├── brain.py
  ├── bullet.py
  ├── clouds.py
  ├── config.py
  ├── database.py
  ├── emp.py
  ├── explosion.py
  ├── fighter.py
  ├── font.py
  ├── levelloader.py
  ├── main.py
  ├── menu.py
  ├── minimap.py
  ├── missile.py
  ├── object.py
  ├── particle.py
  ├── player.py
  ├── sound.py
  ├── spritesheet.py
  ├── vectors.py

```

---

## Key Systems and Code Modules

1. **`main.py`** – *Core loop:* Handles events, updates & draws sprites, checks collisions, and manages game states.  
2. **`brain.py`** – *AI logic:* Issues commands to fighters about distancing, slowing down, or turning away.  
3. **`fighter.py` & `emp.py`** – Define standard fighters and EMP-firing fighters.  
4. **`missile.py` & `bullet.py`** – Movement, collisions, and specialized rendering for projectiles.  
5. **`particle.py`** – Manages smoke trails, explosion particles, and spark effects.  
6. **`database.py`** – Stores and updates level progression and high scores in SQLite.  
7. **`levelloader.py`** – Loads level details (enemy counts, etc.) from `levels.json`.  
8. **`menu.py`** – UI system for main menus, pause menus, and level selection.  
9. **`minimap.py`** – Renders a small map in the corner showing positions of entities around the player.  
10. **`clouds.py`** – Draws large cloud sprites that scroll as the player moves.  
11. **`sound.py`** – Background music, gunfire, explosion sounds, and slow-motion “tick” effects.  
12. **`config.py`** – Central place for game constants and parameters (e.g., screen dimensions, speeds, health).  
13. **`object.py`** / **`vectors.py`** – Shared math for vector operations, angles, and movement.


## Credits

### Sprites and Images
- **Clouds:** [Some clouds](https://opengameart.org/content/some-clouds) *(re-edited for color, size, and borders)*
- **Background:** [Background]([https://opengameart.org/content/some-clouds](https://free-game-assets.itch.io/free-sky-with-clouds-background-pixel-art-set)) *(re-edited for color, size, and borders)*
- **Enemy Ship (Fighter):** [Space Shooter Assets 2](https://opengameart.org/content/space-shooter-assets-2) *(re-edited)*  
- **Player (Ship) and Enemy Ship (EMP):** [Kenney’s Space Shooter Redux](https://kenney.nl/assets/space-shooter-redux) *(re-edited)*  
- **Bullet, Missiles, Health, and Special Fuel Bar:** Custom Photoshop work by the developers.

*(**Note:** All images listed above have been modified for this project in color, size, and/or borders.)*

### Sounds
- **explosion01:** [Synthesized Explosion](https://opengameart.org/content/synthesized-explosion)  
- **explosion:** [Big Low Frequency Explosion Boom](https://opengameart.org/content/big-low-frequency-explosion-boom)  
- **shootbullet:** [Space Shoot Sounds](https://opengameart.org/content/space-shoot-sounds)  
- **bullethit:** [Retro Sounds 0](https://opengameart.org/content/retro-sounds-0)  
- **tick1:** [Tick and Tock](https://opengameart.org/content/tick-and-tock)  
- **gametrack:** [Funny Track with Ringtone Effects (C64 style)](https://opengameart.org/content/funny-track-with-ringtone-effects-c64-style)

*(All sounds are also tweaked as needed to fit the project.)*

---
## Contributing

Contributions are welcome! Whether it's reporting bugs, suggesting features, or submitting pull requests, your input is valuable to improve SkyWars.

### Steps to Contribute

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Make Your Changes**

4. **Commit Your Changes**

   ```bash
   git commit -m "Add your message here"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

6. **Create a Pull Request**

   Provide a clear description of your changes and why they should be merged.

---
## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software in compliance with the license terms.

---

## Contact

Have questions, ideas, or just want to say hello?

- **Email:** dhrumil1612@icloud.com  
- **GitHub:** [Rushi1222](https://github.com/rushi1222)  


Enjoy the thrill of **Sky Warrior**—and may your aim be true!

---

**“When in doubt, hit the turbo!”**  




