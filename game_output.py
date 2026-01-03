ui = None

def set_ui(game_ui):
    global ui
    ui = game_ui

def game_print(text):
    if ui:
        ui.show_text(text)
    else:
        print(text)
