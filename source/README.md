# SkyWarrior

![SkyWars Banner](images/background.png) *(Ensure you have a banner image in the `images` directory)*

**SkyWars** is an engaging 2D space combat game developed using Pygame. Take control of your spaceship, navigate through enemy-filled skies, and engage in intense battles against formidable foes. With dynamic AI opponents, strategic gameplay mechanics, and stunning visual effects, SkyWars offers an exhilarating experience for space enthusiasts and gamers alike.

---

## Table of Contents

- [Features](#features)
- [Gameplay](#gameplay)
- [Controls](#controls)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Features

- **Dynamic AI Opponents:** Intelligent enemy fighters that adapt their strategies based on player actions.
- **Multiple Levels:** Progress through various levels with increasing difficulty and diverse enemy types.
- **Visual Effects:** Stunning particle effects, explosions, and dynamic backgrounds enhance the visual experience.
- **Sound Effects & Music:** Immersive audio that complements the fast-paced gameplay.
- **Minimap:** Keep track of enemy positions and navigate the battlefield effectively.
- **Upgradeable Player Ship:** Utilize turbo boosts, manage health, and deploy EMPs to gain the upper hand.
- **Interactive Menu System:** User-friendly menus for easy navigation, level selection, and game settings.

---

## Gameplay

In **SkyWars**, you pilot a spaceship through challenging levels filled with enemy fighters and missiles. Your objective is to survive as long as possible, destroy enemy ships, and advance through the ranks. Utilize your ship's abilities, such as turbo boosts and EMPs, to outmaneuver and outgun your opponents. Manage your health and resources wisely to overcome increasingly difficult challenges.

---

## Controls

- **Movement:**
  - **Turn Left:** `A` key
  - **Turn Right:** `D` key
  - **Throttle Up (Increase Speed):** `W` key
  - **Throttle Down (Decrease Speed):** `S` key

- **Actions:**
  - **Shoot Bullets:** `Spacebar`
  - **Activate Turbo Boost:** `Left Shift`
  - **Activate Slow Motion:** `Left Ctrl` or `Right Ctrl`

- **Miscellaneous:**
  - **Pause Game / Open Game Menu:** `Escape` key
  - **Select Menu Options:** Mouse Click

---

## Installation

### Prerequisites

- **Python 3.7 or higher**  
  Ensure Python is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

- **Pygame Library**  
  Install Pygame using `pip`:

  ```bash
  pip install pygame
  ```

### Clone the Repository

```bash
git clone https://github.com/rushi1222/skywars.git
cd skywars
```

---

## Running the Game

1. **Navigate to the Project Directory:**

   ```bash
   cd skywars
   ```

2. **Ensure All Dependencies Are Installed:**

   As mentioned in the [Installation](#installation) section.

3. **Run the Game:**

   ```bash
   python main.py
   ```

   This command will launch the SkyWars game window. Use the controls outlined above to start playing.

---

## Project Structure

```
skywarrior/
├── images/
│   ├── background.png
│   ├── bullet.png
│   ├── clouds/
│   ├── empjet1.png
│   ├── hud.png
│   ├── lock.png
│   ├── mapoutline.png
│   ├── missile.png
│   ├── player.png
│   ├── ship.png
│   ├── sonic/
│   ├── top1.png
│   │   └── ... *(other image assets)*
├── sounds/
│   ├── explosion01.flac
│   ├── shootbullet.wav
│   ├── tick1.wav
│   ├── gametrack.ogg
│   ├── bullethit.flac
│   └── explosion.wav
└── font/
│   └── karma future.ttf
├── db/ *(SQLite database file)*
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
└── README.md
```

---

## Dependencies

- **Python 3.7+**
- **Pygame:**  
  A set of Python modules designed for writing video games.  
  Installation:

  ```bash
  pip install pygame
  ```

*(Ensure all other dependencies, if any, are installed as needed.)*

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

[MIT License](LICENSE)  

---

## Credits

- **Developed by:** Rushi and Dhrumil 
 

- **Special Thanks:**  
  - [Pygame Community](https://www.pygame.org/news)

---

## Contact

For any questions, suggestions, or feedback, feel free to reach out:

- **Email:** your.email@example.com
- **GitHub:** [yourusername](https://github.com/yourusername)
- **Twitter:** [@yourhandle](https://twitter.com/yourhandle)

---

Enjoy battling it out in the skies with **SkyWars**! 🚀✨
