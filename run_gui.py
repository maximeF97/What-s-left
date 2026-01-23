from gui import GameUI
import main


def start_gui():
    # Create the GUI on the main thread
    ui = GameUI()

    # Schedule the game entry point to run once the Tk event loop is running.
    # This keeps ALL Tk + game logic on the same (main) thread.
    ui.root.after(0, main.start_game)
    # Start Tkinter mainloop (must be in main thread)
    ui.run()


if __name__ == "__main__":
    start_gui()