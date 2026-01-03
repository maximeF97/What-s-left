import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("What's Left")

        # ── Image area (TOP)
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # ── Text output (BOTTOM)
        self.text = tk.Text(self.root, height=12, bg="black", fg="white")
        self.text.pack(fill=tk.BOTH)

        # ── Input field
        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.send_input)

        self.show_room("wasteland.png")
        self.print_text("You wake up in the wasteland...\n")

        self.root.mainloop()

    def show_room(self, image_path):
        img = Image.open(image_path)
        img = img.resize((800, 400))
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)

    def print_text(self, message):
        self.text.insert(tk.END, message)
        self.text.see(tk.END)

    def send_input(self, event):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        self.print_text(f"> {user_input}\n")
        # 🔗 hook into your game logic here

GameUI()
