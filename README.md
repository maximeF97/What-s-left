# 🩸 WHAT'S LEFT OF US
**Demo_V1**  
*(1st Demo Version — Full release planned. A 2D version may follow later.)*

A post-apocalyptic sci-fi horror text adventure with a dark GUI interface.

---

## 📖 THE STORY

A decade ago, something fell from the sky.

There was no warning.  
No invasion.  
No mercy.

In a single blink, the world ended.

Cities burned.  
The air changed.  
And not everything that survived is still human.

You are one of the last survivors, wandering through the ruins of civilization —  
searching for answers, supplies…  
and the terrifying truth of **what's left of us**.

---

## 🎮 HOW TO PLAY

### **Requirements**
- Python 3.8 or higher
- Tkinter (usually included with Python)

### **Quick Start - Automatic Installer (All Platforms)**

The easiest way to install and launch the game with desktop icons:

#### **Windows**
1. Navigate to the game folder in Windows File Explorer
2. Double-click `launch_game.bat` to launch the game
3. **For desktop shortcut with icon**: Double-click `create_windows_shortcut.vbs`
   - This automatically creates a shortcut on your desktop with the game icon

#### **Linux / WSL**
1. Open Terminal in the game folder
2. Run the installer:
   ```bash
   bash setup_launcher.sh
   ```
3. The game will be installed to your applications menu with icon
4. Launch by searching **"What's Left"** in your app launcher

#### **macOS**
1. Open Terminal in the game folder
2. Run the installer:
   ```bash
   bash setup_launcher.sh
   ```
3. The game will be installed as an app: `~/Applications/WhatsLeft.app`
4. Launch from Applications or Spotlight

---

### **Manual Installation & Running**

If you prefer to run manually without the installer:

#### **Windows**
1. Open Command Prompt (Win + R, type `cmd`)
2. Navigate to the game folder:
   ```cmd
   cd path\to\Whats_left
   ```
3. Run the game:
   ```cmd
   python run_gui.py
   ```

#### **macOS**
1. Open Terminal (Cmd + Space, type `Terminal`)
2. Navigate to the game folder:
   ```bash
   cd path/to/Whats_left
   ```
3. Run the game:
   ```bash
   python3 run_gui.py
   ```

#### **Linux**
1. Open Terminal (Ctrl + Alt + T)
2. Navigate to the game folder:
   ```bash
   cd path/to/Whats_left
 ```
3. Run the game:
   ```bash
   python3 run_gui.py
   ```

---

### **Cross-Platform Launcher Files**

The game includes multiple launcher options:

- **`launch.py`** - Universal Python launcher (all platforms)
- **`launch_game.bat`** - Windows batch launcher with error handling
- **`launch_game.sh`** - Linux/WSL bash launcher
- **`launch_game_macos.sh`** - macOS bash launcher
- **`create_windows_shortcut.vbs`** - Windows desktop shortcut creator with icon
- **`setup_launcher.sh`** - Automatic installer for all platforms
- **`Whats_Left.desktop`** - Linux desktop entry file

---

### **Desktop Icons**

The game includes custom icons for all platforms:
- **`assets/game_icon.ico`** - Windows/Linux icon
- **`assets/IMG_5863.png`** - Linux/macOS icon (PNG format)

Icons are automatically configured when using the installer scripts.

---

### **First Time Setup (Optional)**

If you want to use a virtual environment (recommended):

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
python run_gui.py
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 run_gui.py
```

---

## ☢️ THE WORLD

The wasteland is not empty.

Something watches.  
Something learns.  
Some things pretend.

Alien metamorphs stalk the ruins.

They don’t always look alien.

Sometimes…  
they look familiar.

---

## 🧠 SURVIVAL SYSTEMS

Every choice matters.  
Every mistake costs.

Your survival depends on your skills:

- **Stealth** – Move unseen through hostile areas
- **Perception** – Notice details you shouldn’t miss… or things you were never meant to see
- **Scavenging** – Find supplies before someone else does
- **Lockpicking** – Open doors that were meant to stay closed
- **Intelligence** – Understand alien technology and uncover hidden truths
- **Stamina** – Endure injuries, exhaustion, and fear
- **Luck** – The difference between survival… and sudden death
- **Charisma** – Talk your way out of situations where bullets won’t help

Skill checks can reveal secrets, avoid danger, or seal your fate.

---

## 🗡️ COMBAT & HORROR

- **Turn-based combat** with strategic depth
- **Enemies that ambush, adapt, and retaliate**
- **Skill checks** that can save you — or doom you

⚠️ **Not every threat should be fought.**

Sometimes, running away is the only sane choice.

---

## 🎒 INVENTORY & EQUIPMENT

Scavenge and manage your resources carefully:

- **Weapons, ammo, medical supplies**
- **Keys, notes, and alien artifacts**
- **Unique equipment** with gameplay effects

**Examples:**

- **Cowboy Hat** – Improves luck and survival odds
- **Alien Scientist Suit** – Protection against the unknown
- **Neural Implant** – Understand alien technology
- **Respirator** – Breathe in alien environments
- **Tactical Gloves** – Enhanced lockpicking and scavenging
- **Old Exoskeleton** – Multi-slot armor for maximum protection

Notes left behind by the dead can reveal lore, warnings…  
or instructions that might keep you alive.

---

## �️ GUI INTERFACE

The game features a **dark horror-themed GUI** with:

### **Left Panel (Toggle View)**
- **INVENTORY** – View all items you're carrying
- **CHARACTER** – View your stats, level, XP, HP, equipped items, weapons, and equipment
- **Toggle Button** – Click the **▼ CHARACTER ▼** or **▲ INVENTORY ▲** button at the bottom to switch between views

### **Center Panel**
- Main story text with character-by-character animation
- Combat messages and skill check results
- Atmospheric horror narrative

### **Bottom Input Bar**
- Input field for making choices and typing commands
- Press **Enter** to submit your choice

### **Color Scheme**
- **Sickly Green** (#7cff6b) – UI accents, level/XP indicators, equipped items
- **Dark Red** (#b22222) – Health, danger, title
- **Near-Black** backgrounds (#050505, #080808, #101010) for maximum horror atmosphere
- **Muted Gray** (#888888) – Empty slots and secondary text

---

## 💾 SAVE, LOAD & CONTROLS

Your progress is always in your hands:

### **In-Game Commands**
- **I** – Open Inventory menu
- **S** – Save Game (also automatically saves on level up)
- **L** – Load Game
- **C** – Continue from last save

### **Main Menu Options**
- **1** – Start New Game
- **2** – Quit Game
- **C** – Continue from last save
- **L** – Load specific save file
- **I** – Interactive Load Menu (browse all saves)
- **S** – Save current game

**Everything is saved:** Inventory, character stats, equipped items, story progress, skill levels, and key decisions.

Simple to play.  
Hard to survive.

---

## 🧪 STATUS

🚧 **Work in Progress Demo**

New areas, functions, enemies, items, interactions, and story elements are actively being developed.

### **Recent Updates (v1.0 GUI Edition)**
- ✅ Full GUI implementation with Tkinter
- ✅ Dark horror-themed interface
- ✅ Dynamic inventory and character panels with toggle view
- ✅ Character-by-character text animation for suspense
- ✅ Equipment system with multi-slot support (exoskeleton)
- ✅ Skill-based progression system with leveling
- ✅ Auto-save on level up
- ✅ Thread-safe, non-blocking architecture
- ✅ Equipment bonuses and stat aggregation
- ✅ Interactive save/load system
- ✅ Cross-platform launcher system (Windows/Linux/macOS)
- ✅ Automatic desktop icon installation
- ✅ Windows desktop shortcut creator with icon
- ✅ One-click installers for all platforms

### **Known Issues**
- Some rooms may still have legacy `print()` statements (being converted)
- Balance tweaks ongoing for combat and skill checks

---

## 🧬 FINAL WARNING

The wasteland remembers.

It watches you learn.  
And it changes.

**Don't trust what you see.**  
Don't sleep.

---

**Welcome to WHAT'S LEFT OF US.**

*Survive if you can.*

---

## 📝 CREDITS

**Development:** maximeF97  
**Engine:** Python 3 + Tkinter  
**Genre:** Post-Apocalyptic Sci-Fi Horror Text Adventure  

---

## 📄 LICENSE

This project is a work in progress. All rights reserved.