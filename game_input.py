pending_choice = None

def get_choice():
    global pending_choice
    pending_choice = None
    return "__WAIT__"

def set_choice(choice):
    global pending_choice
    pending_choice = choice

def choice_ready():
    return pending_choice is not None

