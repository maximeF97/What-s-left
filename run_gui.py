from gui import GameUI
import main
import sys
import traceback


def start_gui():
    try:
        # Create the GUI on the main thread
        ui = GameUI()

        # Schedule the game entry point to run once the Tk event loop is running.
        # This keeps ALL Tk + game logic on the same (main) thread.
        ui.root.after(0, main.start_game)
        # Start Tkinter mainloop (must be in main thread)
        ui.run()
    except Exception as e:
        print(f"\n{'='*60}")
        print("ERROR: Failed to start the game!")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        print(f"\n{'='*60}")
        print("Possible fixes:")
        print("1. Make sure Python/tkinter is installed correctly")
        print("2. Check that all game files are present")
        print("3. Try running: python -m tkinter (to test tkinter)")
        print(f"{'='*60}\n")
        input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    start_gui()