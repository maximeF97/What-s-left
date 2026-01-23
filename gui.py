import tkinter as tk
import main
from ui import set_ui


class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("What's Left of Us")
        self.root.geometry("1000x700")

        # ========== TOP (optional title / image) ==========
        top_frame = tk.Frame(self.root)
        top_frame.pack(side="top", fill="x")

        title = tk.Label(
            top_frame,
            text="What's Left of Us",
            font=("Helvetica", 16, "bold")
        )
        title.pack(pady=5)

        # ========== MIDDLE (inventory + story) ==========
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(side="top", fill="both", expand=True)

        # --- Inventory (LEFT) ---
        inventory_frame = tk.Frame(
            middle_frame,
            width=220,
            relief="sunken",
            borderwidth=1
        )
        inventory_frame.pack(side="left", fill="y")

        inventory_label = tk.Label(
            inventory_frame,
            text="Inventory",
            font=("Helvetica", 12, "bold")
        )
        inventory_label.pack(pady=(5, 0))

        self.inventory_text = tk.Text(
            inventory_frame,
            wrap="word",
            state="disabled",
            width=28
        )
        self.inventory_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Prevent inventory from shrinking
        inventory_frame.pack_propagate(False)

        # --- Story text (CENTER) ---
        story_frame = tk.Frame(middle_frame)
        story_frame.pack(side="left", fill="both", expand=True)

        self.story_text = tk.Text(
            story_frame,
            wrap="word",
            state="disabled"
        )
        self.story_text.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=10
        )

        scrollbar = tk.Scrollbar(story_frame, command=self.story_text.yview)
        scrollbar.pack(side="right", fill="y")

        self.story_text.config(yscrollcommand=scrollbar.set)

        # ========== BOTTOM (input) ==========
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side="bottom", fill="x")

        self.input_entry = tk.Entry(bottom_frame)
        self.input_entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.input_entry.bind("<Return>", self._on_enter)

        # ========== UI BINDING ==========
        self._input_var = None
        set_ui(self.ui_print, self.ui_input)

        # Start game AFTER Tk is ready
        self.root.after(0, main.start_game)

    # ---------- UI OUTPUT ----------
    def ui_print(self, text: str):
        self.story_text.config(state="normal")
        self.story_text.insert(tk.END, text + "\n")
        self.story_text.see(tk.END)
        self.story_text.config(state="disabled")

    def ui_write(self, text: str):
        self.story_text.config(state="normal")
        self.story_text.insert(tk.END, text)
        self.story_text.see(tk.END)
        self.story_text.config(state="disabled")

    # ---------- UI INPUT ----------
    def ui_input(self, prompt="> "):
        self.ui_print(prompt)
        self._input_var = tk.StringVar()
        self.root.wait_variable(self._input_var)
        return self._input_var.get()

    def _on_enter(self, event):
        if self._input_var is not None:
            self._input_var.set(self.input_entry.get())
            self.input_entry.delete(0, tk.END)

    # ---------- RUN ----------
    def run(self):
        self.root.mainloop()


def start():
    ui = GameUI()
    ui.run()
