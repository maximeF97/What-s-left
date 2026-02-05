import tkinter as tk

from ui import set_ui


# ====== COLORS / STYLE ======
BG_ROOT = "#050505"
BG_PANEL = "#101010"
BG_PANEL_DARK = "#080808"
BG_INPUT = "#050505"
FG_TEXT = "#e0e0e0"
FG_MUTED = "#888888"
ACCENT = "#7cff6b"     # sickly green
BLOOD = "#b22222"      # dark red

FONT_STORY = ("Courier New", 12)
FONT_INV = ("Courier New", 11)
FONT_INPUT = ("Courier New", 13)
FONT_TITLE = ("Courier New", 18, "bold")
FONT_STATS = ("Courier New", 10)


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("What's Left of Us")
        self.root.geometry("1100x750")
        self.root.configure(bg=BG_ROOT)

        # Track which panel is shown (True = inventory, False = character)
        self.showing_inventory = True
        
        # Store inventory and player data
        self._cached_inventory = {}
        self._cached_player = None

        # ====== MAIN CONTAINER ======
        main_container = tk.Frame(self.root, bg=BG_ROOT)
        main_container.pack(fill="both", expand=True)

        # ====== CONTENT (LEFT PANEL + CENTER TEXT) ======
        content_frame = tk.Frame(main_container, bg=BG_ROOT)
        content_frame.pack(side="top", fill="both", expand=True)

        # --- LEFT: SINGLE PANEL CONTAINER ---
        left_container = tk.Frame(content_frame, bg=BG_ROOT)
        left_container.pack(side="left", fill="both", expand=False)

        # Main panel frame
        panel_frame = tk.Frame(
            left_container,
            width=260,
            bg=BG_PANEL_DARK,
            relief="ridge",
            borderwidth=2,
        )
        panel_frame.pack(side="top", fill="both", expand=True, padx=(8, 4), pady=8)
        panel_frame.pack_propagate(False)

        # Panel header with title
        self.panel_label = tk.Label(
            panel_frame,
            text="INVENTORY",
            font=FONT_INV,
            fg=ACCENT,
            bg=BG_PANEL_DARK,
        )
        self.panel_label.pack(pady=(6, 2))

        # Main text widget (used for both inventory and character)
        self.panel_text = tk.Text(
            panel_frame,
            wrap="word",
            state="disabled",
            bg=BG_PANEL_DARK,
            fg=FG_TEXT,
            insertbackground=ACCENT,
            font=FONT_INV,
            relief="flat",
        )
        self.panel_text.pack(fill="both", expand=True, padx=6, pady=(4, 2))

        # Swap button at bottom
        swap_button = tk.Button(
            panel_frame,
            text="▼ CHARACTER ▼",
            font=("Courier New", 9, "bold"),
            fg=ACCENT,
            bg=BG_PANEL,
            activeforeground=BG_PANEL_DARK,
            activebackground=ACCENT,
            relief="flat",
            cursor="hand2",
            command=self._toggle_panel
        )
        swap_button.pack(side="bottom", fill="x", padx=6, pady=(2, 6))
        self.swap_button = swap_button

        # --- CENTER: TEXT FRAME (TITLE + STORY) ---
        text_frame = tk.Frame(content_frame, bg=BG_ROOT)
        text_frame.pack(side="left", fill="both", expand=True, padx=(4, 8), pady=8)

        title_label = tk.Label(
            text_frame,
            text="WHAT'S LEFT OF US",
            font=FONT_TITLE,
            fg=BLOOD,
            bg=BG_ROOT,
        )
        title_label.pack(side="top", pady=(4, 4))

        story_container = tk.Frame(text_frame, bg=BG_ROOT)
        story_container.pack(side="top", fill="both", expand=True)

        self.story_text = tk.Text(
            story_container,
            wrap="word",
            state="disabled",
            bg=BG_PANEL,
            fg=FG_TEXT,
            insertbackground=ACCENT,
            font=FONT_STORY,
            relief="flat",
            padx=6,
            pady=4,
        )
        self.story_text.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)

        scrollbar = tk.Scrollbar(
            story_container,
            command=self.story_text.yview,
        )
        scrollbar.pack(side="right", fill="y", pady=6)

        self.story_text.config(yscrollcommand=scrollbar.set)

        # ====== INPUT FRAME (BOTTOM) ======
        input_frame = tk.Frame(
            
            main_container,
            bg=BG_PANEL_DARK,
            relief="ridge",
            borderwidth=2,
        )
        input_frame.pack(side="bottom", fill="x", padx=8, pady=(0, 8))

        prompt_label = tk.Label(
            input_frame,
            text=">",
            font=FONT_INPUT,
            fg=ACCENT,
            bg=BG_PANEL_DARK,
        )
        prompt_label.pack(side="left", padx=(10, 4))

        self.input_entry = tk.Entry(
            input_frame,
            font=FONT_INPUT,
            bg=BG_INPUT,
            fg=FG_TEXT,
            insertbackground=ACCENT,
            relief="flat",
        )
        self.input_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
            pady=10,        # makes bar visually taller
            ipady=6,
        )

        self.input_entry.bind("<Return>", self._on_enter)
        self.input_entry.focus_set()

        # ====== UI BINDING ======
        self._input_var = None
        set_ui(
            self._ui_print_line,
            self._ui_input,
            self._ui_write_raw,
            self._schedule,
            self.update_inventory,
            self.update_equipment
        )
        
        # Initialize display
        self.update_inventory({})

    # ---------- PANEL TOGGLE ----------
    def _toggle_panel(self):
        """Switch between inventory and character display"""
        self.showing_inventory = not self.showing_inventory
        
        if self.showing_inventory:
            self.panel_label.config(text="INVENTORY")
            self.swap_button.config(text="▼ CHARACTER ▼")
            self._render_inventory()
        else:
            self.panel_label.config(text="CHARACTER")
            self.swap_button.config(text="▲ INVENTORY ▲")
            self._render_character()

    def _render_inventory(self):
        """Render inventory display"""
        self.panel_text.config(state="normal", font=FONT_INV)
        self.panel_text.delete("1.0", tk.END)
        
        if not self._cached_inventory:
            self.panel_text.insert(tk.END, "• (empty)")
        else:
            for item, qty in self._cached_inventory.items():
                display_name = item.replace("_", " ").title()
                if qty > 1:
                    line = f"• {display_name} (x{qty})\n"
                else:
                    line = f"• {display_name}\n"
                self.panel_text.insert(tk.END, line)
        
        self.panel_text.config(state="disabled")

    def _render_character(self):
        """Render character stats/equipment display"""
        self.panel_text.config(state="normal", font=FONT_STATS)
        self.panel_text.delete("1.0", tk.END)
        
        player = self._cached_player
        if not player:
            self.panel_text.insert(tk.END, "• Loading...")
            self.panel_text.config(state="disabled")
            return
        
        # Stats section
        level = player.get("level", 1)
        health = player.get("health", 0)
        max_health = player.get("max_health", 0)
        experience = player.get("experience", 0)
        
        self.panel_text.insert(tk.END, f"LEVEL: {level}\n", "header")
        self.panel_text.insert(tk.END, f"HP: {health}/{max_health}\n", "health")
        self.panel_text.insert(tk.END, f"XP: {experience}\n\n", "header")
        
        # Equipment slots section
        self.panel_text.insert(tk.END, "═══ EQUIPPED ═══\n", "section")
        equipment = player.get("equipment", {})
        slots = ["head", "body", "hand", "feet", "implant"]
        
        for slot in slots:
            item = equipment.get(slot)
            slot_name = slot.capitalize()
            if item:
                display_name = item.replace("_", " ").title()
                self.panel_text.insert(tk.END, f"{slot_name}: ", "slot")
                self.panel_text.insert(tk.END, f"{display_name}\n", "equipped")
            else:
                self.panel_text.insert(tk.END, f"{slot_name}: ", "slot")
                self.panel_text.insert(tk.END, "(empty)\n", "empty")
        
        # Weapons section
        self.panel_text.insert(tk.END, "\n═══ WEAPONS ═══\n", "section")
        inventory = player.get("inventory", {})
        weapons = ["rusty_knife", "sharp_kitchen_knife", "revolver", "symbiotic_blood_pistol", 
                   "alien_laser_rifle", "shotgun", "magnum", "rifle"]
        found_weapons = [w for w in weapons if w in inventory]
        
        if found_weapons:
            for weapon in found_weapons:
                display_name = weapon.replace("_", " ").title()
                qty = inventory.get(weapon, 1)
                if qty > 1:
                    self.panel_text.insert(tk.END, f"• {display_name} (x{qty})\n", "item")
                else:
                    self.panel_text.insert(tk.END, f"• {display_name}\n", "item")
        else:
            self.panel_text.insert(tk.END, "• None\n", "empty")
        
        # Equipment items section
        self.panel_text.insert(tk.END, "\n═══ EQUIPMENT ═══\n", "section")
        equipment_items = ["cowboy_hat", "tactical_helmet", "respirator", "alien_scientist_suit", 
                          "shielded_jacket", "tactical_gloves", "weary_boots", "tactical_boots",
                          "neural_implant", "old_exoskeleton"]
        found_equipment = [e for e in equipment_items if e in inventory]
        
        if found_equipment:
            for eq in found_equipment:
                display_name = eq.replace("_", " ").title()
                qty = inventory.get(eq, 1)
                if qty > 1:
                    self.panel_text.insert(tk.END, f"• {display_name} (x{qty})\n", "item")
                else:
                    self.panel_text.insert(tk.END, f"• {display_name}\n", "item")
        else:
            self.panel_text.insert(tk.END, "• None\n", "empty")
        
        # Apply text tags for colors
        self.panel_text.tag_config("header", foreground=ACCENT)
        self.panel_text.tag_config("health", foreground=BLOOD)
        self.panel_text.tag_config("section", foreground=ACCENT, font=("Courier New", 10, "bold"))
        self.panel_text.tag_config("slot", foreground=FG_MUTED)
        self.panel_text.tag_config("equipped", foreground=ACCENT)
        self.panel_text.tag_config("empty", foreground=FG_MUTED)
        self.panel_text.tag_config("item", foreground=FG_TEXT)
        
        self.panel_text.config(state="disabled")

    # ---------- INTERNAL HELPERS ----------
    def _append_text(self, text: str):
        self.story_text.config(state="normal")
        self.story_text.insert(tk.END, text)
        self.story_text.see(tk.END)
        self.story_text.config(state="disabled")

    # ---------- OUTPUT API ----------
    def _ui_print_line(self, text: str):
        self._append_text(text + "\n")

    def _ui_write_raw(self, text: str):
        self._append_text(text)

    # ---------- INPUT API ----------
    def _ui_input(self, prompt: str = "> "):
        # Show prompt in story area, then wait for entry
        if prompt:
            self._ui_print_line(prompt)
        self._input_var = tk.StringVar()
        self.root.wait_variable(self._input_var)
        return self._input_var.get()

    def _on_enter(self, event):
        if self._input_var is not None:
            value = self.input_entry.get()
            self._input_var.set(value)
            self.input_entry.delete(0, tk.END)

    # ---------- INVENTORY DISPLAY ----------
    def update_inventory(self, inventory: dict, flash=False):
        """
        Update the inventory data and refresh if currently showing inventory.
        inventory: dict like {"rusty_knife": 1, "ammo_9mm": 3}
        flash: briefly highlight the frame
        """
        self._cached_inventory = inventory
        
        if self.showing_inventory:
            self._render_inventory()
        
        if flash:
            inv_frame = self.panel_text.master
            original_bg = inv_frame.cget("bg")
            inv_frame.config(bg=ACCENT)
            self.root.after(100, lambda: inv_frame.config(bg=original_bg))

    # ---------- EQUIPMENT/STATS DISPLAY ----------
    def update_equipment(self, player: dict):
        """
        Update the character data and refresh if currently showing character.
        player: player dict with level, health, experience, equipment, inventory
        """
        self._cached_player = player
        
        if not self.showing_inventory:
            self._render_character()

    # ---------- SCHEDULER ----------
    def _schedule(self, delay_ms: int, callback, *args):
        self.root.after(delay_ms, callback, *args)

    # ---------- MAIN LOOP ----------
    def run(self):
        self.root.mainloop()


def start():
    GameUI().run()
