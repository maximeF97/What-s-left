
from text_effect import suspense_print,slow_print_word

from combat import fight_enemy, combats, get_enemy, gain_xp, player_attack
from inventory import add_item, remove_item
from systems import get_choice, handle_global_input, skill_check, get_current_weapon
from game_area.rooms import hospital_road, wasteland_4, game_over


def hospital(player):
    suspense_print(
        "you arrive at the hospital. the facade is mostly intact, but the front door is chained shut.\n"
        "the silence around it feels staged, like something is waiting for you to touch the handle."
    )
    while True:
        suspense_print("1) try to lockpick the door open")
        suspense_print("2) look for another way in")
        suspense_print("3) look through the windows")
        suspense_print("4) go back to the crossroad")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()   

        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("has_oppened_hospital_lock", False):
                suspense_print("the lock hangs open. the door waits in the dark.")
                hospital_inside(player)
                return
            else:
                if "bobby_pins" in player["inventory"]:
                    if skill_check(player, "lockpicking", 20):
                        suspense_print("the lock clicks. too loud in the dead air. you slip inside the hospital.")
                        player["has_oppened_hospital_lock"] = True
                        hospital_inside(player)
                        return
                    else:
                        suspense_print("the pins slip. the lock refuses you.")
                else:
                    suspense_print("you don't have any bobby pins.")
        elif choice == "2":
            suspense_print("you circle the building and find a side entrance. a strange cactus watches the doorway like a guard.")
            hospital_side_entrance(player)
            return
        elif choice == "3":
            if player["has_pass_window_check"]:
                suspense_print("you already looked through the windows and saw the alien inside the hospital.")
                continue
            else:
                suspense_print("you peer through grime-caked windows. shapes move where nothing should move.")
                if skill_check(player, "perception", 20):
                    suspense_print("an alien silhouette drifts through a corridor inside. it moves like it already knows you're here.")
                    player["has_pass_window_check"] = True
                else:
                    suspense_print("the glass gives you only shadows and static movement.")

        elif choice == "4":
            suspense_print("you go back to the crossroad")
            hospital_road(player)
            return
        else:
            suspense_print("Invalid choice")
def hospital_side_entrance(player):
    if player.get("has_deal_with_cactus", False):
        suspense_print("You are back at the side entrance of the hospital. The cactus is no longer a threat.\n"
                        "You step inside the hospital.")
        hospital_inside(player)
        return
    while True:
        suspense_print("1) sneak past the cactus")
        suspense_print("2) shoot the cactus")
        suspense_print("3) go back to the hospital entrance")
        suspense_print("I) Open inventory")

        choice = get_choice()

        if handle_global_input(choice, player):
            continue

        # 🥷 Sneak
        if choice == "1":
            suspense_print(
                "the wasteland has taught you to fear everything that stands still.\n"
                "you try to slip past the cactus without breathing too loud."
            )

            if skill_check(player, "stealth", 50):
                slow_print_word("you pass without a sound.")
            else:
                slow_print_word(
                    "your pulse hammers in your throat... but nothing lunges.\n"
                    "just a cactus. this time."

                )
            player["has_deal_with_cactus"] = True

            hospital_inside(player)
            return

        # 🔫 Shoot cactus
        elif choice == "2":
            weapon_name, weapon = get_current_weapon(player)

            if not weapon or weapon["type"] != "ranged":
                suspense_print("You have no ranged weapon.")
                continue
            

            if player.get("has_killed_cactus", False):
                suspense_print("the cactus is already shredded. no threat left in it.")
                continue
            suspense_print("you raise your weapon and steady your hands.")

            cactus = {
                "name": "innocent cactus",
                "health": 1
            }

            player_attack(player, cactus)  
                    
            suspense_print(
                
                "the cactus bursts into splinters.\n\n"
                "for a second, you could swear it twitched on the floor."
            )

            
            player["has_deal_with_cactus"] = True
            hospital_inside(player)
            return

        # 🔙 Go back
        elif choice == "3":
            suspense_print("you back away from the side entrance.")
            hospital(player)
            return

        else:
            suspense_print("Invalid choice.")
def hospital_inside(player):
    while True:
        if not player.get("hospital_metamorph_killed", False):

            if player.get("has_pass_window_check", False):
                hospital_metamorph_encounter(player)
                continue

            suspense_print("you step inside. a hidden tentacle lashes out from under a gurney and sweeps your legs.")
            player["health"] -= 2
            if player["health"] <= 0:
                game_over()
                return

            suspense_print(f"pain spikes through your hip. -2 health. health: {player['health']}")
            fight_enemy(player, {"health": 10, "hit_chance": 75, "xp": 70})
            player["hospital_metamorph_killed"] = True
            suspense_print("the metamorph stops moving. the hall feels worse now that it's quiet.")
            continue
        suspense_print("you stand in the hospital lobby. the metamorph carcass leaks across the tiles.")

        suspense_print("1) get up the stairs to the second floor")
        suspense_print("2) search the hospital right room")
        suspense_print("3) search the room ahead")
        suspense_print("4) search the left room")
        suspense_print("5) go to the back door")
        suspense_print("6) go back to the hospital entrance")
        suspense_print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            hospital_first_floor(player)
        elif choice == "2":
            suspense_print("you search the right room and find a safe with three keyholes.")
            if not player.get("has_opened_hospital_safe", False):

                if "hospital_safe_key" in player["inventory"] and "second_hospital_safe_key" in player["inventory"] and "third_hospital_safe_key" in player["inventory"]:
                    suspense_print(
                        "the three keys turn one after another.\n"
                        "inside is wet, black, and warm like living tissue.\n"
                        "you force your hand into the mucus and drag out medical supplies, an alien laser rifle, and an energy cell."
                    )
                    add_item(player, "medkit",1)
                    add_item(player, "healing_salve",1)
                    add_item(player, "alien_laser_rifle",1)
                    add_item(player, "alien_energy_cell",1)
                    if skill_check(player, "luck", 30):
                        suspense_print("your fingers close on one more vial. unlabeled. faintly pulsing.")
                        add_item(player, "strange_elixir",1)
                    add_item(player, "alien_energy_cell",2)
                    remove_item(player, "hospital_safe_key", 1)
                    remove_item(player, "second_hospital_safe_key", 1)
                    remove_item(player, "third_hospital_safe_key", 1)
                    player["has_opened_hospital_safe"] = True
                    continue
                else:
                    suspense_print("you need all three keys.")
                    continue
            else:
                suspense_print("the safe hangs open. empty and slick.")
                continue
        elif choice == "3":
            scavenger_room(player)
        elif choice == "4":
            if not player.get("has_hospital_left_room_been_searched", False):
                suspense_print("you search the left room. bobby pins lie near a vent. stairs descend into the basement.")
                add_item(player, "bobby_pins", 3)
                player["has_hospital_left_room_been_searched"] = True
                suspense_print("you pick up the bobby pins and add them to your inventory.")
                suspense_print("you take the stairs going down to the basement.")
                hospital_basement(player)
                return
            else:
                suspense_print("you take the stairs going down to the basement again.")
                hospital_basement(player)
        elif choice == "5":
            if not player.get("has_opened_hospital_back_door", False):
                if "hospital_back_door_key" in player["inventory"]:
                    suspense_print("You use the key and step out toward the wasteland.")
                    player["has_opened_hospital_back_door"] = True
                    wasteland_4(player)
                    return
                else:
                    suspense_print("The door is locked. You need a key.")
            else:
                suspense_print("The back door is already open.")
                wasteland_4(player)
                return
        elif choice == "6":
            suspense_print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            suspense_print("Invalid choice")
def scavenger_room(player):
    while True:
        if  player.get("hospital_scavenger_killed", False):
            suspense_print("You enter the room again. The scavenger lies motionless. Whatever it was, it's dead.")
            return

        suspense_print(
            "you enter the room ahead and find a scavenger body slumped against the wall.\n"
            "half his skull has been replaced with alien hardware. it is still warm."
        )

        if skill_check(player, "perception", 20):
            suspense_print("a red light blinks behind his ruined temple. active system. active host.")
        else:
            suspense_print("it looks dead enough. almost.")

        suspense_print("1) Search the body")
        suspense_print("2) Shoot the body with your revolver, just to be sure")
        suspense_print("3) Go back ")
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # --- SEARCH BODY ---
        if choice == "1":
            slow_print_word("the body jerks upright. metal and bone grind together. it attacks.")

            cyborg = get_enemy("cyborg_scavenger")

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                suspense_print("the scavenger collapses for good. the red light finally dies.")
                return
            else:
                exit()

        # --- SHOOT BODY ---
        elif choice == "2":
            if player.get("weapon") != "revolver":
                suspense_print("You don't have a revolver.")
                continue

            if not remove_item(player, "revolver_ammo", 1):
                suspense_print("Click! You're out of ammo.")
                continue

            if skill_check(player, "luck", 17):
                suspense_print(
                    "You fire a precise shot. The scavenger awakens badly damaged and attacks!"
                )
                cyborg = get_enemy("cyborg_scavenger")
                cyborg["health"] = cyborg["health"] // 2
            else:
                suspense_print(
                    "You miss! The scavenger awakens fully and attacks!"
                )
                cyborg = get_enemy("cyborg_scavenger")
                    

            result = combats(player, cyborg)
            if result["result"] == "win":
                gain_xp(player, cyborg["xp"])
                player["hospital_scavenger_killed"] = True
                add_item(player, "alien_implant", 1)
                suspense_print("You defeated the alien cyborg scavenger.")
                return
            
            else:
                exit()
        elif choice == "3":
            return
        else:
            suspense_print("Invalid choice.")
def hospital_metamorph_encounter(player):
    while True:
        suspense_print(
            "you step into the lobby again.\n"
            "you remember seeing movement through the window earlier.\n"
            "you do not remember that chair being there."
        )
        suspense_print("1) shoot the chair with your revolver")
        suspense_print("2) approach the chair")
        suspense_print("3) go back to the hospital entrance")
        suspense_print("I) Open inventory")
    
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if "revolver" not in player["inventory"]:
                suspense_print("You don't have a revolver.")
                continue
            if not remove_item(player, "revolver_ammo", 1):
                suspense_print("Click! You're out of ammo.")

            suspense_print("you fire into the chair. flesh erupts from under torn fabric. the metamorph dies before it can rise.")
            player["hospital_metamorph_killed"] = True
            add_item(player,"healing_salve", 1)

            gain_xp(player, 50)
            
            return
        elif choice == "2":
            suspense_print("you approach the chair. it unfolds into teeth and tendons and lunges.")
            alien = {"health": 10, "hit_chance": 75, "xp": 70}
            result = combats(player, alien)

            if result["result"] == "win":
                gain_xp(player, result["xp"])
                add_item(player, "healing_salve", 1)
                suspense_print("You defeated the alien metamorph.")
                player["hospital_metamorph_killed"] = True  
                return

            elif result["result"] == "lose":
                exit()
        elif choice == "3":
            suspense_print("you go back to the hospital entrance")
            hospital(player)
            return
        else:
            suspense_print("Invalid choice")  
def hospital_basement(player):
    
    suspense_print(
        "you descend into the basement. pained moans leak through the dark below.\n"
        "at the bottom stands a large humanoid alien in a torn white lab coat.\n"
        "it doesn't look surprised to see you."
    )

    while True:
        suspense_print("\n1) Try to sneak attack the alien")
        suspense_print("2) Charge at the alien with your weapon drawn")
        suspense_print("3) Look around the room")
        suspense_print("4) Go back upstairs")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")


        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # ───────────────────────────────
        # Sneak attack
        # ───────────────────────────────
        if choice == "1":
            if player.get("has_defeated_hospital_boss", False):
                hospital_basement_boss_defeated(player)
                return

            suspense_print("you lower your breathing and move in.")
            if skill_check(player, "stealth", 40):
                slow_print_word("you catch it off guard.")
                alien = {"health": 15, "hit_chance": 70, "xp": 150}
            else:
                slow_print_word("floor metal creaks. the alien turns, smiling.")
                alien = {"health": 20, "hit_chance": 70, "xp": 150}

            result = combats(player, alien)
            if result["result"] == "win":
                finish_hospital_boss(player, result["xp"])
                return
            else:
                exit()

        # ───────────────────────────────
        # Direct attack
        # ───────────────────────────────
        elif choice == "2":
            if player.get("has_defeated_hospital_boss", False):
                hospital_basement_boss_defeated(player)
                return

            suspense_print("you charge before fear can catch up.")
            alien = {"health": 20, "hit_chance": 70, "xp": 150}
            result = combats(player, alien)

            if result["result"] == "win":
                finish_hospital_boss(player, result["xp"])
                return
            else:
                exit()

        # ───────────────────────────────
        # Look around
        # ───────────────────────────────
        elif choice == "3":
            if not player.get("has_defeated_hospital_boss", False):
                suspense_print("you see a jailed man but the alien blocks your path — you’ll need to deal with it first.")
            else:
                hospital_basement_boss_defeated(player)
                return

        # ───────────────────────────────
        # Leave
        # ───────────────────────────────
        elif choice == "4":
            suspense_print("You retreat back upstairs.")
            hospital_inside(player)
            return

        else:
            suspense_print("Invalid choice.")
def finish_hospital_boss(player, xp):
    gain_xp(player, xp)
    suspense_print("the alien scientist crumples beside shattered equipment.")

    
    add_item(player, "second_hospital_safe_key", 1)
    add_item(player, "alien_scientist_suit", 1)
    add_item(player, "hospital_back_door_key", 1)
    

    player["has_defeated_hospital_boss"] = True
    hospital_basement_boss_defeated(player)
def hospital_basement_boss_defeated(player):
    suspense_print("tables are lined with failed experiments. jars of tissue, wires, restraints.\n"
                  "none of it should exist.")
    suspense_print("a cell sits in the corner. someone inside is still breathing.")
    while True:
        suspense_print("1) free the prisoner")
        suspense_print("2) ignore the prisoner")
        suspense_print("3) talk to the prisoner")
        suspense_print("4 go back upstairs")
        suspense_print("I) Open inventory")  
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if not player.get("has_help_basement_prisoner", False):
                suspense_print("you force the lock and free the prisoner.\n"
                              "he shakes, thanks you, and presses a map into your hand.\n"
                              "\"secret human base,\" he whispers. \"tell them john sent you.\"\n")
                add_item(player, "map_to_base",1)
                player["has_help_basement_prisoner"] = True
                return
            else:
                suspense_print("the prisoner is already free.")
                return
        elif choice == "2":
            suspense_print("you leave him in the dark. his voice follows you anyway.")
            return
        elif choice == "3":
            questione_prisoner(player)
        elif choice == "4":
            suspense_print("you go back upstairs")
            hospital_inside(player)
            return
        else:
            suspense_print("Invalid choice")
def questione_prisoner(player):
    while True:
        suspense_print("1) Ask about the alien metamorph")
        suspense_print("2) Ask about the alien cyborg scavenger")
        suspense_print("3) Ask about the alien scientist")
        suspense_print("4) Ask about what happened since the alien laser touchdown")
        suspense_print("5) Go back")
        suspense_print("I) Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "The prisoner tells you that the alien metamorph is a dangerous creature "
                "that can mimic human forms and is highly aggressive. However, they do not "
                "mimic perfectly, and with enough perception, you can spot them.")
        elif choice == "2":
            suspense_print(
                "The prisoner explains that the alien cyborg scavenger was a friend of his "
                "who got captured by the alien scientist and experimented on, turning him "
                "into a cyborg against his will. The aliens have heavily experimented on "
                "humans since the invasion, both technologically and biologically."
            )

        elif choice == "3":
            suspense_print(
                "The prisoner reveals that the alien scientist was conducting experiments "
                "on humans to create hybrid creatures for the aliens. He thanks you for "
                "your assistance, saying he was next."
            )

        elif choice == "4":
            suspense_print(
                "The prisoner recounts that a few weeks after the laser scorched the Earth, "
                "a massive ship from space landed and started terraforming. The area around "
                "the landing site became unbreathable for humans without proper equipment. "
                "If you see their flora, turn around."
            )

        elif choice == "5":
            return
def hospital_first_floor(player):
    while True:
        suspense_print("you climb the stairs to the second floor. two rooms. a flower pot. a rusted trash can.")
        suspense_print("1) go to the room on the left")
        suspense_print("2) go to the room on the right")
        suspense_print("3) inspect the flower pot")
        suspense_print("4) inspect the trash can")
        suspense_print("5) go back downstairs")
        suspense_print("I) Open inventory")
        choice = get_choice()   
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            Hospital_first_floor_left_room(player)
            return
        elif choice == "2":
            Hospital_first_floor_right_room(player)
            return
        elif choice == "3":
            Hospital_flower_pot(player)
        elif choice == "4" :
            if not player.get("hospital_trash_pot_check", False):
                suspense_print("You search through the trash and find some coins.")
                add_item(player, "coin",3)
                player["hospital_trash_pot_check"] = True
            else:
                suspense_print("The trash can is empty.")
        elif choice == "5":
            suspense_print("you go back downstairs")
            hospital_inside(player)
            return
        else:
            suspense_print("Invalid choice")                         
def Hospital_flower_pot(player):

    while True:
        if not player.get("hospital_flower_pot_checked", False):
            suspense_print("1) Check the flower pot")
            suspense_print("2) Go back")
            if skill_check(player, "perception", 30):
                suspense_print("Something feels off about a neat little flower pot in the middle of an alien-infested hospital.")
                suspense_print("3) Shoot the flower!")

        
        suspense_print("I) Open inventory")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print("You carefully examine the flower pot...")
            suspense_print("Suddenly, a tentacle lashes out!")
            alien = {"health": 3, "hit_chance": 70, "xp": 0}
            fight_enemy(player, alien)
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "3" and player.get("hospital_flower_pot_checked", False):
            suspense_print("You attack the flower pot before it can react. It dies instantly.")
            player["hospital_flower_pot_checked"] = True
            return

        elif choice == "2":
            return

        else:
            suspense_print("Invalid choice.")
def Hospital_first_floor_left_room(player):
    while True:
        suspense_print("you enter the left room. an old PC hums on a desk, still drawing power from somewhere.")

        # PC NOT hacked yet
        if not player.get("hospital_pc_hacked", False):
            suspense_print("1) Try to hack the PC")
            suspense_print("2) Go back")
            suspense_print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                if skill_check(player, "intelligence", 20):
                    player["hospital_pc_hacked"] = True
                    suspense_print("you break through the PC defenses.")
                else:
                    suspense_print("the PC locks you out. something is still protecting these files.")
            elif choice == "2":
                return
            else:
                suspense_print("Invalid choice")

        # PC hacked
        else:
            suspense_print("1) Read first message")
            suspense_print("2) Read second message")
            suspense_print("3) Unlock the desk safe")
            suspense_print("4) Read third message")
            suspense_print("5) Go back")
            suspense_print("I) Open inventory")

            choice = get_choice()
            if handle_global_input(choice, player):
                continue

            if choice == "1":
                suspense_print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "01/01/2000\n\n"
                    "Hey Millie, I hope you're doing well. The hospital is full of the usual "
                    "New Year missing fingers and drunk fools. I think I'll have to work all night."
                )

            elif choice == "2":
                suspense_print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "02/01/2000\n\n"
                    "God, Millie, what was that? A bright flash and most of everything wiped out. "
                    "The grid shut down, all patients on life support were lost. "
                    "I heard millions died. I hope you're alright. Please answer me."
                )

            elif choice == "3":
                if not player.get("has_taken_hospital_pc_safe", False):
                    suspense_print("You unlock the safe and find some ammo and a medkit.")
                    add_item(player, "revolver_ammo", 3)
                    add_item(player, "medkit", 1)
                    player["has_taken_hospital_pc_safe"] = True
                else:
                    suspense_print("The safe is empty.")
            elif choice == "4":
                suspense_print(
                    "From: Dr John Fry\n"
                    "To: Millie\n"
                    "03/01/2000\n\n"
                    "Millie, I don't know how much longer I can hold out. "
                    "The creatures are everywhere now. They change shape, "
                    "mimicking humans. I barely escaped an attack today. "
                    "If you get this, stay away from the hospital."
                )
            elif choice == "5":
                return
            else:
                suspense_print("Invalid choice")
def Hospital_first_floor_right_room(player):
    while True:
        suspense_print("you enter the room on the right.\n")
        if not player.get("Hospital_first_floor_right_room_note_taken", False):
            suspense_print(
            "a note lies on the floor beside dried smears.")
        suspense_print("1) read the note")
        suspense_print("2) go back")
        suspense_print("I) Open inventory")
        suspense_print("S) Save game")
        suspense_print("L) Load game")

        choice = get_choice()  

        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if not player.get("Hospital_first_floor_right_room_note_taken", False):
                add_item(player, "hospital_note_doctor", 1)
                player["Hospital_first_floor_right_room_note_taken"] = True
                suspense_print("you pick up the note. the paper is damp and cold.")
                suspense_print(
                    "The handwriting is shaky.\n\n"
                    "They can’t breathe our air.\n"
                    "That’s why they don’t stay long.\n\n"
                    "The small ones don’t mind.\n"
                    "They belong here now."
                        )           
            else:
                suspense_print("nothing else to do here.")
        elif choice == "2":
            return 
        else:
            suspense_print("Invalid choice")