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

### **Installation & Running**

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