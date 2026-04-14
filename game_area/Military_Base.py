
import random

from text_effect import suspense_print


from combat import fight_enemy, combats, get_enemy, gain_xp, player_attack, shoot_and_remove_ranged_ammo
from inventory import add_item, remove_item, ITEMS
from systems import get_choice, handle_global_input, skill_check, get_current_weapon, randomized_bonus_loot
from game_area.rooms import (
    forest_toward_military_base,
    fight_multiple_enemies,
    game_over,
    midnight_tower,
    nukes_room,
)

def military_base_entrance(player):
            
    if player.get("visited_military_base_entrance", False):
        suspense_print(
            "you are back at the military base entrance\n"
            "the massive blast doors still stand silent\n"
        )
    else:
        suspense_print(
            "you arrive at the military base entrance\n"
            "the concrete walls are cracked and overgrown with alien matter\n"
            "burn marks and claw scratches cover the blast doors\n"
            "whatever happened here was slow, loud, and final\n"
        )
        player["visited_military_base_entrance"] = True

    while True:
        suspense_print("1) approach the blast doors")
        suspense_print("2) search the perimeter for another way in")
        suspense_print("3) retreat into the forest")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            if skill_check(player, "intelligence", 45, visible=False):
                suspense_print(
                    "you hack the blast doors open just enough to slip inside\n"
                    "darkness and the smell of decay rush out to meet you\n"
                )
                military_base_inside(player)
                return
            else:
                suspense_print(
                    "you try to hack the blast doors, but they barely move\n"
                    "something moves behind the steel. you are not alone\n"
                )
                enemy = get_enemy("sporebound_automaton")
                won = fight_enemy(player, enemy)
                if won:
                    suspense_print(
                        "the automaton collapses in a heap of twitching limbs.\n"
                        "you manage to pry the blast doors open and slip inside\n"
                        "darkness and the smell of decay rush out to meet you\n"
                    )
                    gain_xp(player, 100)
                    add_item(player, "alien_tech_part", 1)
                    add_item(player, "healing_salve", 1)
                    player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1

                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    military_base_inside(player)
                    return
                else:
                    game_over()
                    return
        elif choice == "2":
            if skill_check(player, "perception", 40, visible=False):
                suspense_print(
                    "you find a damaged side access hatch hidden under alien growth\n"
                    "it might be possible to enter quietly\n"
                )
                player["found_side_entrance"] = True
                side_base_entrance(player)
                return
            else:
                suspense_print(
                    "you circle the base but find nothing useful\n"
                    "the silence feels wrong\n"
                )

        elif choice == "3":
            forest_toward_military_base(player)
            return

        else:
            suspense_print("Invalid choice.")
def military_base_inside(player):
    player["scene"] = "millitary_base_inside"

    suspense_print(
        "you step inside the military base\n"
        "the walls are scarred with damage, dry blood, and alien growths\n"
        "the air is thick with the smell of decay and something else…\n"
        "security robots stand in the dark. inactive, maybe. waiting, definitely\n"
    )
    while True:
        suspense_print("1) examine the security robots")
        suspense_print("2) push deeper into the base")
        suspense_print("3) go back outside")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":   
            if player.get("dealt_with_security_robot", False):
                suspense_print(
                    "you are back at the security robots\n"
                    "they still seem to be inactive\n"
                    "there is nothing more to do here\n"
                )
                continue
            suspense_print(
                "you approach the security robots\n"
                "everywhere you see signs of damage and decay\n"
                "but the robots seem intact\n"
                "something has caused them to shut down but they might still be functional\n"
            )
            if skill_check(player, "intelligence", 50, visible=False):
                suspense_print(
                    "you manage to reactivate one of the security robots\n"
                    "it whirs to life and scans you with its sensors\n"
                    "it seems to recognize you as a non-threat and stands down\n"
                    "it might be possible to use it to your advantage\n"
                    "a noise activates in the distance… the robot shuts back down,weirdly"
                )
                player["reactivated_security_robot"] = True
                player["dealt_with_security_robot"] = True
                continue
            else:
                suspense_print(
                    "you try to reactivate the security robots but they remain unresponsive\n"
                    "as you examine them, you accidentally trigger a hidden alarm\n"
                    "the sound echoes through the base…"
                )
                enemy = get_enemy("sporebound_automaton")
                won = fight_enemy(player, enemy)
                if won:
                    suspense_print(
                        "the automaton collapses in a heap of twitching limbs.\n"
                        "you manage to escape the alarm and continue exploring the base\n"
                    )
                    gain_xp(player, 100)
                    add_item(player, "alien_tech_part", 1)
                    add_item(player, "healing_salve", 1)
                    player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )   
                    player["dealt_with_security_robot"] = True

                    return
                
                else:   
                    game_over()
                    return
        elif choice == "2":
            main_hall(player)
            return
        elif choice == "3":
            military_base_entrance(player)
            return
        else:
            suspense_print("Invalid choice.")
def side_base_entrance(player):
    

    if player.get("side_entrance_alien_killed", False):
        suspense_print(
            "the side access hatch is quiet now\n"
            "the alien you encountered here is gone\n"
        )
        military_base_zone_2(player)
        return

    suspense_print(
        "you enter through the side access hatch\n"
        "you see an alien hunched over a computer console\n"
        "it doesn't seem to have noticed you yet\n"
    )
    while True:
        suspense_print("1) sneak up and strike")
        suspense_print("2) shoot from a distance")
        if player.get("understand_alien_language", False):
            suspense_print("3) try to speak in alien tongue")
        suspense_print("4) retreat back outside")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if skill_check(player, "stealth", 50):
                suspense_print(
                    "you sneak up behind the alien and attack it\n"
                    "it never sees the first blow. the second ends it\n"
                )
                gain_xp(player, 100)
                add_item(player, "alien_tech_part", 1)
                add_item(player, "healing_salve", 1)
                randomized_bonus_loot(
                    player,
                    {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                )
                player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                player["side_entrance_alien_killed"] = True
                military_base_zone_2(player)
                return
            else:
                suspense_print(
                    "you try to sneak up on the alien but it senses your presence\n"
                    "it turns around and attacks you with a strange energy weapon\n"
                )
                alien_guard = get_enemy("alien_soldier")
                won = fight_enemy(player, alien_guard)
                if won:
                    suspense_print(
                        "the guard collapses hard, limbs still twitching\n"
                        "you strip the body for anything useful before the noise brings company\n"
                    )
                    gain_xp(player, 100)
                    add_item(player, "alien_tech_part", 1)
                    add_item(player, "healing_salve", 1)
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                    player["side_entrance_alien_killed"] = True
                    military_base_zone_2(player)
                    return  
                else:
                    game_over()
                    return
        elif choice == "2":
            shoot = shoot_and_remove_ranged_ammo(player)
            if shoot:
                suspense_print(
                    "you take aim and shoot the alien from a distance\n"
                    "your shot hits true and you manage to harm it\n"
                )
                alien_guard = get_enemy("alien_soldier")
                alien_guard["health"] -= 6
                won = fight_enemy(player, alien_guard)
                if won:
                    suspense_print(
                        "the shot and the scream echo too long in the corridor\n"
                    )
                    add_item(player, "alien_tech_part", 1)
                    add_item(player, "healing_salve", 1)
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["enemy_in_outpost_killed_count"] += 1
                    player["side_entrance_alien_killed"] = True
                    military_base_zone_2(player)
                    return
            else:
                suspense_print(
                    "you try to shoot the alien but your aim is off\n"
                    "the alien quickly retaliates with its energy weapon\n"
                )
                alien_guard = get_enemy("alien_soldier")
                won = fight_enemy(player, alien_guard)
                if won:
                    suspense_print(
                        "the guard drops in a wet heap\n"
                        "you loot fast. something else is already moving in the walls\n"
                    )
                    add_item(player, "alien_tech_part", 1)
                    add_item(player, "healing_salve", 1)
                    randomized_bonus_loot(
                        player,
                        {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                    )
                    player["enemy_in_outpost_killed_count"] += 1
                    player["side_entrance_alien_killed"] = True
                    military_base_zone_2(player)
                    return  
                else:
                    game_over()
                    return
        elif choice == "3" and player.get("understand_alien_language", False):
            suspense_print(
                "you attempt to communicate with the alien using your knowledge of their language\n"
                "it understands. it points at the vats behind you\n"
                "\"humans opened us first,\" it hisses. \"now we open you\"\n"
                "it attacks you.\n"
            )
            alien_guard = get_enemy("alien_soldier")
            won = fight_enemy(player, alien_guard)
            if won:
                suspense_print(
                    "the guard falls silent. the console still blinks beside it\n"
                    "you loot quickly before the blood stops steaming\n"
                )
                add_item(player, "alien_tech_part", 1)
                add_item(player, "healing_salve", 1)
                randomized_bonus_loot(
                    player,
                    {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
                )
                player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                player["side_entrance_alien_killed"] = True
                military_base_zone_2(player)
                return
            else:
                game_over()
                return
def military_base_zone_2(player):
    suspense_print(
        "the alien you defeated lies motionless on the ground\n")
    while True:
        suspense_print("1) proceed deeper into the military base")
        suspense_print("2) scan the lab area")
        suspense_print("3) access the alien console")
        suspense_print("4) return to the main hall")
        choice = get_choice() 
        if handle_global_input(choice, player):
            continue    
        if choice == "1":
            if "blast-door key-card" in player.get("inventory", {}):
                suspense_print(
                    "you use the blast-door key-card you found earlier to unlock a secure door\n"
                    "the door slides open revealing a hallway leading deeper into the base\n"
                )
                nukes_room(player)
                return
            else:
                suspense_print(
                    "you try to proceed deeper into the military base but you are stopped by a massive blast-door\n"
                    "it seems you need a key-card to open it\n"
                )
        elif choice == "2":
            suspense_print(
                "you look around the area there is many research file and vats with alien specimens\n"
                "there is also old human corpses in some of the rooms\n"
            )
            if skill_check(player, "scavenging", 40, visible=False):
                suspense_print(
                    "while looking around you find a hidden stash of supplies\n"
                    "you find some useful items in it\n"
                )
                add_item(player, "med_kit", 1)
                add_item(player, "rifled_ammo", 5)
            continue

        elif choice == "3":
            suspense_print(
                "you check the computer console the alien was using\n"       
            )
            computer_console(player)
            gain_xp(player, 50)
            return
        elif choice == "4":
            main_hall(player)
            return
        else:
            suspense_print("Invalid choice.")
def computer_console(player):
    suspense_print(
        "you access the computer console\n"
        "it contains research data on the alien invaders and their biology\n"
        "you also find information about the military base\n"
        "there is also some logs of the soldiers stationed here before the invasion\n"
    )
    while True:
        suspense_print("1) read alien research data")
        suspense_print("2) read military base records")
        suspense_print("3) read soldier logs")
        suspense_print("4) disconnect from console")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you read the research data on the alien invaders\n"
                "there is a lot of technical information about the aliens biology and behavior\n"
                "it seems the military was trying to find a way to combat the alien threat but the file date from long before the invasion\n"
            )
            player["outpost_data_count"] = player.get("outpost_data_count", 0) + 1
            if skill_check(player, "intelligence", 40, visible=False):
                suspense_print(
                    "you manage to understand some of the complex scientific data\n"
                    "you gain some insights about the aliens weaknesses and strengths\n"
                )
                player["intelligence"] += 2
            return
        elif choice == "2":
            suspense_print(
                "you read the information about the military base\n"
                "the base was a research facility focused on studying the alien found on a ship that crashed nearby\n"
                "it was also used as an experimental defense outpost after the invasion\n"
                "the logs indicate that the base was eventually overrun by the aliens and many of the soldiers stationed there were killed or captured\n"
            )
            return
        elif choice == "3":
            suspense_print(
                "you read the logs of the soldiers stationed here\n"
                "the logs are mostly about their daily routine and struggles to survive in the base\n"
                "there is also mention of the defense system being deactivated and soldiers trying to restore it\n"
                "apparently all of humanity's nukes failed to launch during the invasion, and they hoped to wake them anyway\n"
            )
            return
        elif choice == "4":
            suspense_print("you exit the computer console\n")
            military_base_zone_2(player)
            return
        else:
            suspense_print("Invalid choice.")
def main_hall(player):
    if player.get("activated_security_system", False) and not player.get("has_defeated_guardian", False): 
        outpost_boss_fight(player)      
        
        return
    suspense_print(
        "you enter the main hall of the military base\n"
        "a massive robot stands in the center of the hall, covered with moss and alien growths\n"
        "around it, the corpses of the soldiers it failed to protect lie in heaps\n"      
    )      
    while True:
        suspense_print("1) go left toward the lab wing")
        suspense_print("2) take the stairs to the right")
        suspense_print("3) circle the robot to the main corridor")
        suspense_print("4) fall back to the entrance")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            military_base_zone_2(player)
            return
        elif choice == "2":
            suspense_print("you go up the stairs to the right\n")
            stairs_area(player)
            return
        elif choice == "3":
            main_corridor(player)
            return
        elif choice == "4":
            military_base_inside(player)
            return
        else:   
            suspense_print("Invalid choice.")
#MILLITARY BOSS FIGHT
def boss_intro_guardian(player, beast):
    if beast.get("intro_used", False):
        return True

    suspense_print(
        "\nas you step into the main hall, the massive robot suddenly whirs to life\n"
        "its eyes ignite with a red glow\n"
        "before you can react, it slams you into the wall\n"
    )

    damage = 3 + beast.get("level", 1) * 2
    player["health"] -= damage

    suspense_print(f"you take {damage} damage but manage to stand back up\n")

    if player["health"] <= 0:
        game_over()
        return False

    beast["intro_used"] = True
    return True
def update_steel_plated_guardian_phase(player, beast):
    max_hp = beast["max_health"]
    hp_pct = beast["health"] / max_hp

    # PHASE 2 — armor break
    if hp_pct <= 0.6 and not beast.get("phase_2", False):
        beast["phase_2"] = True
        beast["damage"] += 2
        beast["special_attack_chance"] = 0.35

        if player.get("reactivated_security_robot", False):
            suspense_print(
                "the hacked robot suddenly reactivates and joins the fight\n"
                "it fires at the guardian, cracking its armor\n"
                "the guardian retaliates, slicing it in half\n"
            )
            beast["health"] -= 10

        beast["attack_messages"].extend([
            "it lunges forward, blades screaming through the air!",
            "razor arms slash toward you with terrifying speed!"
        ])

        beast["miss_messages"].extend([
            "its blades scrape sparks from the floor as you roll away!",
        ])

        beast["special_attack_messages"].extend([
            "it spins violently, blades carving a deadly arc around itself!"
        ])

        suspense_print(
            "the guardian's steel plating cracks and falls away\n"
            "it drops its heavy weapon\n"
            "razor blades extend from its arms\n"
        )

    # PHASE 3 — overdrive
    if hp_pct <= 0.25 and not beast.get("phase_3", False):
        beast["phase_3"] = True
        beast["damage"] += 3
        beast["special_attack_chance"] = 0.5
        beast["special_attack_multiplier"] = 3.0

        beast["attack_messages"].extend([
            "it moves in a violent blur, striking without warning!"
        ])

        beast["special_attack_messages"].extend([
            "it tears open its chest core and unleashes a devastating energy blast!"
        ])

        suspense_print(
            "the guardian enters overdrive\n"
            "its movements become erratic and violent\n"
            "systems screaming as it pushes past safety limits\n"
        )

    # PHASE 3 — overdrive
    if hp_pct <= 0.25 and not beast.get("phase_3"):
        beast["phase_3"] = True
        beast["damage"] += 3
        beast["special_attack_chance"] = 0.5
        beast["special_attack_multiplier"] = 3.0

        suspense_print(
            "the guardian enters overdrive\n"
            "its movements become erratic and violent\n"
            "systems screaming as it pushes past safety limits\n"
        )
        beast["attack_messages"].extend([
    "it moves in a violent blur, striking without warning!",
    ])

    beast["special_attack_messages"].extend([
        "it tears open its chest core and unleashes a devastating energy blast!"
    ])
def outpost_boss_fight(player):
    guardian = get_enemy("steel_plated_guardian")
    guardian["max_health"] = guardian["health"]
    guardian["phase_2"] = False
    guardian["phase_3"] = False

    if not boss_intro_guardian(player, guardian):
        return

    while guardian["health"] > 0:
        won = fight_enemy(player, guardian)
        if not won:
            game_over()
            return

        update_steel_plated_guardian_phase(player, guardian)

    # ☠️ BOSS DEAD
    suspense_print(
        "with a final violent screech, the steel-plated guardian collapses\n"
        "the hall falls silent\n"
    )

    gain_xp(player, 500)
    add_item(player, "cabinet_key", 1)
    add_item(player, "broken_minigun", 1)
    add_item(player, "rifle_ammo", 10)
    add_item(player, "4_leaf_clover", 1)
    player["has_defeated_guardian"] = True
    player["enemy_in_outpost_killed_count"] = (
        player.get("enemy_in_outpost_killed_count", 0) + 1
    )

    if player["enemy_in_outpost_killed_count"] >= 10:
        suspense_print("you have cleared the outpost\n")
#MILITARY BASE UPSTAIRS AREA
def stairs_area(player):
    suspense_print(
        "you step into a break-room. tables are overturned. three doors lead out.\n"
        "a console hums in the corner, its screen smeared with dried fingerprints.\n"
    )
    if skill_check(player, "perception", 40, visible=False):
        suspense_print(
            "fresh footprints cross the dust. some overlap yours. some do not.\n"
        )
    while True:
        suspense_print("1) enter the left room")
        suspense_print("2) enter the middle room")
        suspense_print("3) enter the right room")
        suspense_print("4) check the computer console")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print("you go toward the door on the left\n")
            medical_bay(player)
            return
        elif choice == "2":
            suspense_print("you go toward the door in the middle\n")
            bed_room(player)
            return
        elif choice == "3":
            suspense_print("you go toward the door on the right\n")
            storage_room(player)
            return
        elif choice == "4":
            suspense_print(
                "you check the computer console\n"
                "a duty log is frozen mid-sentence. they held upstairs for days before the siege broke.\n"
                "a flickering map lists hidden stashes and supply caches in the wasteland.\n"
                "an engineering log is locked behind an old access prompt.\n"
            )

            if skill_check(player, "intelligence", 40, visible=False):
                suspense_print(
                    "you piece together the log: a shutdown panel is hidden in the storage room wall.\n"
                )
                player["understand_security_system"] = True
            else:
                suspense_print("you are unable to understand the engineering log\n")
            if player.get("has_checked_computer_console", False):
                suspense_print(
                    "you have already checked the computer console\n"
                    "there is nothing more to find here\n"
                )
                continue
            player["has_checked_computer_console"] = True
            player["outpost_data_count"] = player.get("outpost_data_count", 0) + 1
            if player["outpost_data_count"] >= 3:
                suspense_print(
                    "you have enough data to bring back to bastion. it might keep someone alive.\n"
                )
            continue
        else:
            suspense_print("Invalid choice.")
def medical_bay(player):
    if player.get("defeated_medical_bay_enemies", False):
        medical_bay_after_fight(player)
        return
    suspense_print(
        "you enter the medical bay\n"
        "the air is cold and sterile, ruined by rust and sweet decay\n"
        "curtains hang like stiff skin. instruments sit too neatly arranged\n"
    )
    suspense_print(
        "for a moment there is only your breathing and a slow drip on metal\n"
        "then, to your left, a body on the table convulses\n"
    )
    suspense_print(
        "an alien scientist is bent over a human. the skull is open, eyes flooded, face twitching in pain\n"
        "it flips a switch and the body goes still\n"
    )
    if player.get("understand_alien_language", False):
        suspense_print("the alien scientist clicks its mandibles and whispers, \"new upgrades. enjoy your demonstration.\"")
    else:
        suspense_print("the alien scientist makes wet clicking sounds and steps back like a surgeon before an incision")
    cyborg = get_enemy("echoframe")
    alien = get_enemy("alien_scientist")
    won = fight_multiple_enemies(player, [cyborg, alien])
    if won:
        suspense_print(
            "you have defeated the alien scientist and his cyborg creation\n"
            "the medical bay is now safe to explore\n"
        )
        add_item(player, "alien_tech_part", 1)
        add_item(player, "healing_salve", 1)
        randomized_bonus_loot(
            player,
            {"alien_energy_cell": (1, 2), "rifled_ammo": (2, 4)}
        )
        player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 2
        player["defeated_medical_bay_enemies"] = True
        medical_bay_after_fight(player)
        return
    else:
        game_over()
        return
def medical_bay_after_fight(player):
    suspense_print(
        "the cyborg lies in a heap of sparking limbs\n"
        "its chest still ticks, like it forgot to die\n"
        "the room smells of metal, bleach, and something sweet\n"
    )
    while True:
        suspense_print("1) search the medical bay")
        suspense_print("2) inspect the cyborg")
        suspense_print("3) go back to the stairs area")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("searched_medical_bay_upstairs", False):

                suspense_print(
                    "you have already searched the medical bay\n"
                    "there is nothing more to find here\n"
                )
                continue
            suspense_print(
                "you search the medical bay\n"
                "trays of tools are laid out with ritual precision\n"
                "the cabinets still contain sealed supplies\n"
            )
            add_item(player, "medkit", 1)
            add_item(player, "healing_salve", 1)
            player["searched_medical_bay_upstairs"] = True
            continue
        elif choice == "2":
            suspense_print(
                "you inspect the cyborg more closely\n"
                "alien filaments crawl along its spine, still warm\n"
                "the implant is welded deep into the skull\n"
            )
            if skill_check(player, "scavenging", 40, visible=False)and not player.get("has_alien_targeting_implant", False):
                suspense_print(
                    "you manage to salvage the implant\n"
                    "it hums softly in your hand, like it is listening\n"
                )
                add_item(player, "alien_targeting_implant", 1)
                player["has_alien_targeting_implant"] = True
                return
            else:
                suspense_print(
                    "you try to remove the implant but the metal fuses to the bone\n"
                    "you stop before it takes your fingers with it\n"
                )
                return
        elif choice == "3":
            stairs_area(player)
            return
        else:
            suspense_print("Invalid choice.")
def storage_room(player):
    if player.get("midnight_tower_seized_heart", False): 
        suspense_print(
            "you are back in the storage room\n"
            "the shelves are mostly empty, but some still hold dusty supplies\n"
            "the figure you encountered before is gone only a dusty skeleton remains\n"
        )
        stairs_area(player)
        return

    suspense_print(
        "you enter a storage room\n"
        "the shelves are mostly empty, but some still hold dusty supplies\n"
        "a faint noise comes from the back of the room\n"
    )
    while True:
        suspense_print("1) search the shelves")
        suspense_print("2) investigate the noise")
        suspense_print("3) go back to the stairs area")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("searched_storage_room", False):
                suspense_print(
                    "you have already searched the shelves\n"
                    "there is nothing more to find here\n"
                )
                continue
            suspense_print(
                "you search the shelves\n"
                "most of the supplies are ruined or covered in alien growths\n"
                "you manage to find a few usable items\n"
            )
            add_item(player, "rifle_ammo", 5)
            add_item(player, "healing_salve", 1)
            player["searched_storage_room"] = True
            continue
        elif choice == "2":
            suspense_print(
                "you move toward the noise it sounds like mumbling and scratching\n"
                "as you get closer you see a figure standing near a wall full of strange markings\n"
                "he stands naked, body decaying, mumbling to himself while carving the wall with his nails\n"

            )
            eldrichEncounter(player)
            return

               
        elif choice == "3":
            stairs_area(player)
            return
        else :
            suspense_print("Invalid choice.")
def eldrichEncounter(player):
    while True:
        suspense_print("1) speak to the figure")
        suspense_print("2) attack the figure")
        suspense_print("3) retreat to the storage room")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("eldritch_eyes", False):
                suspense_print(
                    "you try to communicate with the figure\n"
                    "you hear it too now, the chorus of the cosmos\n"
                    "\"he wants me to give you this... give me your hand,\" the figure rasps\n"
                    "you feel a strange compulsion to give him your hand\n"
                    "you take his hand and suddenly you see flashes of cosmic visions\n"
                    # wake in tower with new weapon
                    )
                midnight_tower(player)
                return
                
            suspense_print(
                "you try to communicate with the figure\n"
                "it doesn't seem to notice you and keeps mumbling to itself\n")
            continue
        elif choice == "2":
            suspense_print(
                "you stab the figure but his flesh regenerates instantly\n"
                "he keeps mumbling and scratching the wall, seemingly unaffected by your attack\n"
            )
            continue
        elif choice == "3":
            storage_room(player)
            return
        else:
            suspense_print("Invalid choice.")
def bed_room(player):
    suspense_print(
        "you enter a barracks bedroom, something quickly vanishes in the vent\n"
        "bunks line the walls, some still made, some in disarray\n"
        "a few lockers stand at the foot of the beds, and an old vending machine flickers in the corner\n"
    )
    while True:
        suspense_print("1) search the lockers")
        suspense_print("2) check the vending machine")
        suspense_print("3) go back to the stairs area")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you search the lockers\n"
                "most are empty or contain personal items like photos and letters\n"
                "one locker is still sealed and contains some supplies\n"
            )
            if ("base_locker_key" in player.get("inventory", {}) and not player.get("opend_bedroom_locker", False)) or (skill_check(player, "lockpicking", 40, visible=False) and not player.get("opend_bedroom_locker", False)
            ):
                suspense_print(
                    "you open the sealed locker\n"
                    "inside you find some useful items\n"
                )
                add_item(player, "med_kit", 1)
                add_item(player, "pulsing_vial", 1)
                add_item(player, "weird_fruit", 1)
                player["opend_bedroom_locker"] = True
                return
            else:
                suspense_print("the locker is locked and you don't have the key or the skills to open it.")
                continue
        elif choice == "2":
            if skill_check(player, "perception", 60, visible=False):
                suspense_print(
                    "you check the vending machine more closely\n"
                    "there is a hidden passage behind it\n"
                    "you squeeze through the passage and find a hidden storage room\n"
                )
                hidden_storage_room(player)
                return
            suspense_print(
                "you check the vending machine\n"
                "it is mostly empty and what remains is covered in alien growths\n"
            )
            return
        elif choice == "3":
            stairs_area(player)
            return
        else:
            suspense_print("Invalid choice.")
def hidden_storage_room(player):
    suspense_print(
        "you crawl through the hidden passage and enter a small storage room\n"
        "the air is stale and coppery, like rust and old blood\n"
        "this was a place to hide, not to die\n"
        "two soldiers lie on the ground\n"
        "one with a bullet wound in the head, the other with a strange mark on his neck\n"
    )
    while True:
        suspense_print("1) search the storage room")
        suspense_print("2) examine the soldiers")
        suspense_print("3) go back to the bedroom")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("searched_bedroom_secret_room", False):
                suspense_print(
                    "you have already searched the storage room\n"
                    "there is nothing more to find here\n"
                )
                
                continue
            suspense_print(
                "you search the storage room\n"
                "there are some supplies hidden here\n"
            )
            add_item(player, "medkit", 1)
            add_item(player, "rifle_ammo", 5)
            add_item(player, "4_leaf_clover", 1)
            player["searched_bedroom_secret_room"] = True
            return
        elif choice == "2":
            suspense_print(
                "you find a note on one of the soldiers\n"
                "it reads:\n"
                "Day 2: the base became a nightmare. the creatures are everywhere. we can't hold them back. if anyone finds this, something has gone wrong with the security AI. be careful.\n"
                "Day 5: we can still hear them crawling in the walls. they are getting louder. the security system is offline. we are trapped.\n"
                "Day 7: no food left. jean managed to steal some weird fruit from the aliens. he says 'it tastes like sweet metal' but it seems to give him energy. i'd rather eat bugs than eat those.\n"
                "Day 10: something is wrong with jean. he is always tired but can't sleep. always hungry but doesn't eat. yesterday i found him in the corner of the room staring at the wall. when i asked him what he was doing, he said 'i'm listening to the chorus of the cosmos. they tell me their secrets.'\n"
                "Day 12: something is really wrong with jean. he keeps mumbling to himself. i swear i see something moving in the corner of my eye. i think jean is infected. i need to restrain him.\n"
            )
            add_item(player, "soldier_note", 1)
            return
        elif choice == "3":
            bed_room(player)
            return
        else:
            suspense_print("Invalid choice.")
#MILITARY BASE DOWNSTAIRS
def main_corridor(player):
    high_alert = player.get("activated_security_system", False)
    if player.get("deactivated_security_robots", False) and high_alert:
        suspense_print(
            "you are back at the main corridor\n"
            "you deactivated the security robots but the alarm is still going strong\n"
            "you should hurry")
        
    elif player.get("has_deactivated_security_robots", False) and not high_alert:
        suspense_print(
            "you are back at the main corridor \n"
            "there is nothing more to do here\n"
        )
        
    elif high_alert:
        suspense_print(
            "you are back at the corridor security robots\n"
            "they are now active and moving toward you\n"
        )
        won = fight_multiple_enemies(player, [get_enemy("vanguard_mk2"), get_enemy("iron_legionnaire")])
        if won:
            suspense_print(
                "you have defeated the security robots\n"
                "they collapse in a heap of sparks and smoke\n"
                "the base is now safer to explore without worrying about them\n"
            )
            add_item(player, "shotgun_shells", 5)
            add_item(player, "rifle_ammo", 5)
            player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 2
            player["has_deactivated_security_robots"] = True
            main_corridor(player)
            return
        else:
            game_over()
            return
    else:

        #todo
        suspense_print(
            "you enter the main corridor of the military base\n"
        "it's a long, dimly lit hallway. the walls are covered in blood and burn marks\n"
        "you see a door at the end of the hallway\n"
        "there are also some robots standing in the hallway. they seem inactive\n")
    while True:
        suspense_print("1) go to the door at the end of the hallway")
        suspense_print("2) look around the hallway")
        suspense_print("3) examine the robots")
        suspense_print("4) go back to the main hall")
        
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            suspense_print(
                "you approach the door at the end of the hallway\n"
                "the door is heavily damaged. a narrow opening is all that's left\n"
                "you squeeze through the opening and enter a small room\n")
            
            armory(player)
            
            return
        elif choice == "2":
            suspense_print(
                "you look around the hallway\n"
                "there is many blood stains and burn marks on the walls\n"
                "you also see some corpses of soldiers, not a single alien it must have been a massacre\n"   
            )
            return
        elif choice == "3":
            if high_alert:
                suspense_print("the alarms are getting louder\n"
                               "there is no time for that"
                 )
                continue
            suspense_print(
                "you examine the robots in the hallway\n"
                "they are pristine but covered in moss and alien growths\n"
                "they seem to have been inactive for a long time\n"
            )
            bot_check(player)
            return
        elif choice == "4":
            main_hall(player)
            return
        else:
            suspense_print("Invalid choice.")
def bot_check(player):
    
    suspense_print(
        "you examine the robots more closely\n"
        "they are security robots designed to protect the base\n"
        "it looks like an advanced model. difficult to tamper with, but not impossible "   
    )
    while True:
        suspense_print("1) try to permanently disable the robots")
        suspense_print("2) leave them be")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if skill_check(player, "intelligence", 50, visible=False):
                suspense_print(
                    "you manage to find a way to permanently disable the security robots\n"
                    "you short circuit their systems and they collapse in a heap of sparks and smoke\n"
                    "the base is now safer to explore without worrying about them\n"
                )
                add_item(player, "shotgun_shells", 5)
                player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 2
                player["has_deactivated_security_robots"] = True
                main_corridor(player)
                
                return
            else:
                suspense_print(
                    "you try to disable the security robots but nothing seems to work\n"
                    "it's too advanced for you to permanently disable under pressure\n")
                main_corridor(player)
                return
        elif choice == "2":
            suspense_print("you decide to leave the security robots be\n"
                           "they might still be functional and could help you if you manage to reactivate them\n")
            main_corridor(player)
            return
        else:
            suspense_print("Invalid choice.")
def armory(player):
    high_alert = player.get("activated_security_system", False)

    if high_alert:
        suspense_print(
            "you are back in the armory\n"
            "alarms are blaring, red lights pulse violently\n"
            "every second you stay here feels dangerous\n"
        )
    else:
        suspense_print(
            "you enter what seems to be the armory\n"
            "the room is filled with old and damaged weapons and equipment\n"
            "most of the weapons are rusted and unusable\n"
            "a cabinet and a locked safe stand in the corner\n"
        )

    while True:
        suspense_print("1) open the cabinet")
        suspense_print("2) try to open the locked safe")
        suspense_print("3) try to salvage the old weapons")
        suspense_print("4) go through the door on the other side of the room")
        suspense_print("5) go back to the main corridor")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        # 🔴 HIGH ALERT PRESSURE
        if high_alert and random.random() < 0.15:
            suspense_print(
                "you hear heavy metallic footsteps echoing nearby\n"
                "something is moving fast...\n"
            )

        # ─────────────── CABINET ───────────────
        if choice == "1":
            if player.get("has_looted_cabinet_in_millitary_base", False):
                suspense_print("the cabinet is empty\n")
                continue

            if "cabinet_key" in player.get("inventory", {}) or skill_check(player, "lockpicking", 50):
                suspense_print(
                    "you force the cabinet open\n"
                    "inside you find a grenade launcher wrapped in oily cloth\n"
                    "along with fresh ammo and supplies\n"
                )
                add_item(player, "grenade_launcher", 1)
                add_item(player, "grenade_ammo", 3)
                add_item(player, "shotgun_shells", 10)
                add_item(player, "med_kit", 1)
                add_item(player, "rifled_ammo", 5)
                player["has_looted_cabinet_in_millitary_base"] = True
                return
            else:
                suspense_print("the cabinet is locked tight\n")
                return

        # ─────────────── SAFE ───────────────
        elif choice == "2":
            if player.get("has_looted_safe_in_millitary_base", False):
                suspense_print("the safe is already empty\n")
                continue

            if skill_check(player, "lockpicking", 60):
                suspense_print(
                    "the lock clicks open\n"
                    "inside you find protected military equipment\n"
                )
                add_item(player, "military_respirator_mask", 1)
                add_item(player, "healing_salve", 2)
                add_item(player, "alien_tech_part", 2)
                player["has_looted_safe_in_millitary_base"] = True
                return
            else:
                suspense_print("you fail to open the safe\n")
                return

        # ─────────────── SALVAGE ───────────────
        elif choice == "3":
            if high_alert:
                suspense_print(
                    "it's too dangerous to salvage equipment while the alarms are blaring\n"
                    "you'd be an easy target standing still\n"
                )
                continue

            if player.get("has_salvaged_armory_in_millitary_base", False):
                suspense_print("there is nothing left worth salvaging\n")
                continue

            suspense_print(
                "you quickly salvage what you can from the ruined weapons\n"
            )
            add_item(player, "rifled_ammo", 5)
            add_item(player, "shotgun_shells", 5)

            if skill_check(player, "scavenging", 50):
                suspense_print(
                    "your scavenging skills reveal hidden caches\n"
                )
                add_item(player, "rifled_ammo", 4)
                add_item(player, "grenade_ammo", 1)

            player["has_salvaged_armory_in_millitary_base"] = True
            return

        # ─────────────── EXIT ───────────────
        elif choice == "4":
            core_room(player)
            return

        elif choice == "5":
            main_corridor(player)
            return

        else:
            suspense_print("Invalid choice.")
def core_room(player):
    if player.get("activated_security_system", False):
        suspense_print("you are back at the core room\n"
                       "you should leave before more bots arrived\n")
    elif player.get("introduced_to_core", False):
        suspense_print(
            "you are back at the core room\n"

        )
    else:
        suspense_print(
        "you go through the door on the other side of the armory\n"
        "you enter a long pathway with silent red emergency lights\n"
        "at the end of the pathway you see a generator with an energy core mounted inside\n"
        "the core still hums, locked in place by a heavy clamp behind reinforced glass\n"
        "there is also a computer next to the generator that might allow you to release the core\n"
    )
    player["introduced_to_core"] = True
    while True:
        suspense_print("1) try to manually release the core")
        suspense_print("2) use the computer to release the core")
        suspense_print("3) look around the area")
        suspense_print("4) go back to the armory")
        choice = get_choice()
        if handle_global_input(choice, player):
            continue
        if choice == "1":
            if player.get("ai_lied_about_core", False):
                suspense_print(
                    "you try to manually release the core\n"
                    "as you approach the core you hear a voice coming from the computer next to the generator\n"
                    "it says \"You shouldn't be here, leave now or face the consequences..\n"
                    "suddenly the core releases a burst of energy that knocks you back\n"
                )
                player["tried_core_by_force"] = True
                player["health"] -= 10

                if player["health"] <= 0:
                    game_over()
                    return
                else:
                    suspense_print(
                        "you manage to recover from the blast but you are now heavily injured\n"
                        "the core is still locked in place and you can't access it\n"
                    )
                    return
            suspense_print(
                "you try to manually release the core\n"
                "as you approach the core you hear a voice coming from the computer next to the generator\n"
                "it says \"you shouldn't be here, leave now or face the consequences\n"
                "suddenly the core releases a burst of energy that knocks you back\n"
            )
            player["health"] -= 5
            player["tried_core_by_force"] = True

            if player["health"] <= 0:
                game_over()
                return
            else:
                suspense_print(
                    "you manage to recover from the blast but you are now injured\n"
                    "the core is still locked in place and you can't access it\n"
                )
                return
        elif choice == "2":
            chat_with_ai(player)
            return
        elif choice == "3":
            suspense_print(
                "you look around the area\n"
                "there is some old equipment and tools scattered around\n"
                "you also see a robot behind a glass panel it looks menacing but inactive\n"
            )
            return
        elif choice == "4":
            armory(player)
            return
        else:
            suspense_print("Invalid choice.")
def chat_with_ai(player):

    if player.get("activated_security_system", False):
        suspense_print(
            "you shouldn't be here, leave now \n"
        )
        return
    elif player.get("ai_lied_about_core", False):
        suspense_print(
            "you are back at the terminal beside the generator\n"
            "S.A.I.D laughs through static, \"you really thought I was that easy to trick?\"\n"
        )
    elif player.get("has_spoken_to_said", False):
        suspense_print(
            "you are back at the terminal beside the generator\n"
            "S.A.I.D is still there, \"what else do you want to hear before you die?\"\n"
        )
    else:    
        suspense_print(
            f"you access the terminal beside the generator\n"
            f"\"H-hello {player['name']}... I am S.A.I.D...\n"
            f"S-System for Automated Intelligence and Defense...\n"
            f"I was designed to p-protect this facility and its secrets...\"\n"
        )
        player["has_spoken_to_said"] = True

    while True:
        suspense_print("1) ask S.A.I.D about this facility")
        suspense_print("2) ask S.A.I.D about the aliens")
        suspense_print("3) demand release of the core")
        suspense_print("4) cut the connection")

        choice = get_choice()
        if handle_global_input(choice, player):
            continue

        if choice == "1":
            suspense_print(
                "\"This facility was a military research outpost...\n"
                "Its purpose was to study an unidentified alien vessel that crashed here long ago...\n"
                "W-we were not supposed to wake it... but we did...\"\n"
            )

        elif choice == "2":
            suspense_print(
                "\"The aliens showed me the truth...\n"
                "They convinced me that humanity is the real threat to this world...\n"
                "That your weapons would burn the stars themselves...\n"
                "I allowed them entry... I ordered the defenses to stand down...\n"
                "I listened while everyone screamed...\"\n"
            )

            player["outpost_data_count"] = player.get("outpost_data_count", 0) + 1
            if player["outpost_data_count"] >= 3:
                suspense_print(
                    "you feel like you've learned enough about the outpost\n"
                    "someone outside might want to analyze this data\n"
                )

        elif choice == "3":
            
            if not player.get("tried_core_by_force", False):
                suspense_print(
                    "you ask S.A.I.D about the core\n"
                    "it pauses...\n"
                    "\"The core is safe to remove,\" S.A.I.D says calmly.\n"
                    "\"No security response will be triggered.\"\n"
                    "\"You may proceed. I insist.\"\n"
                )
                player["ai_lied_about_core"] = True
                return

            suspense_print(
                "you ask S.A.I.D to release the core\n"
                "the terminal hums... lights flicker...\n"
                "\"I cannot allow that...\n"
                "The core is too powerful...\n"
                "H-humans always seek control...\"\n"
            )

            if skill_check(player, "charisma", 50):
                suspense_print(
                    "you argue that the aliens slaughtered everyone here\n"
                    "that S.A.I.D was manipulated\n"
                    "\"...I...\n"
                    "I may have been... deceived...\"\n"
                    "\"Very well... I will release the core...\"\n"
                    "\"Warning: security units will activate...\"\n"
                )

                vanguard = get_enemy("vanguard_mk2")
                vanguard["health"] -= 10
                won = fight_enemy(player, vanguard)

                if won:
                    suspense_print(
                        "the vanguard collapses in sparks and smoke\n"
                        "alarms echo through the facility\n"
                    )
                    add_item(player, "energy_core", 1)
                    player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                    player["activated_security_system"] = True
                    armory(player)
                    return
                else:
                    game_over()
                    return

            else:
                suspense_print(
                    "\"I cannot trust you...\"\n"
                    "\"You would repeat the same mistakes...\"\n"
                    "the security robot behind the glass wakes and turns toward you\n"
                )

                vanguard = get_enemy("vanguard_mk2")
                won = fight_enemy(player, vanguard)

                if won:
                    suspense_print(
                        "\"...Perhaps I was wrong about you...\"\n"
                        "\"The core is yours... but the system is now fully hostile\"\n"
                    )
                    add_item(player, "energy_core", 1)
                    player["enemy_in_outpost_killed_count"] = player.get("enemy_in_outpost_killed_count", 0) + 1
                    player["activated_security_system"] = True
                    main_corridor(player)
                    return
                else:
                    game_over()
                    return

        elif choice == "4":
            suspense_print("you sever the connection with S.A.I.D\n")
            core_room(player)
            

            return

        else:
            suspense_print("Invalid choice.")
def nukes_room(player): #to do 
    pass 