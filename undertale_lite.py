#!/usr/bin/env python3
"""
Undertale Lite - A text-based Undertale-inspired game
Heavily inspired by Undertale by Toby Fox
"""

import sys
import time
import random
import json
import os

class GameState:
    def __init__(self):
        self.player_name = "Frisk"
        self.hp = 20
        self.max_hp = 20
        self.lv = 1
        self.exp = 0
        self.at = 10
        self.df = 10
        self.gold = 0
        self.inventory = ["Stick", "Bandage"]
        self.killed = 0
        self.mercy_count = 0
        
    def save_game(self, filename="save_game.json"):
        save_data = {
            "player_name": self.player_name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "lv": self.lv,
            "exp": self.exp,
            "at": self.at,
            "df": self.df,
            "gold": self.gold,
            "inventory": self.inventory,
            "killed": self.killed,
            "mercy_count": self.mercy_count
        }
        with open(filename, 'w') as f:
            json.dump(save_data, f)
        
    def load_game(self, filename="save_game.json"):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                save_data = json.load(f)
            for key, value in save_data.items():
                setattr(self, key, value)
            return True
        return False

class Monster:
    def __init__(self, name, hp, at, df, exp_value, gold_value, flavor_text, act_options):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.at = at
        self.df = df
        self.exp_value = exp_value
        self.gold_value = gold_value
        self.flavor_text = flavor_text
        self.act_options = act_options
        self.mercy_ready = False
        self.check_text = f"* {name} - ATK {at} DEF {df}\n* {flavor_text}"

class UndertaleLite:
    def __init__(self):
        self.game_state = GameState()
        self.running = True
        
    def typewriter_print(self, text, delay=0.03):
        """Print text with typewriter effect like in Undertale"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def wait_for_input(self):
        """Wait for user input with prompt"""
        return input("\n> ").strip().lower()
    
    def display_stats(self):
        """Display player stats like in Undertale"""
        print("\n" + "="*50)
        print(f"❤ {self.game_state.player_name}   LV {self.game_state.lv}")
        print(f"HP {self.game_state.hp}/{self.game_state.max_hp}")
        print(f"EXP: {self.game_state.exp}   GOLD: {self.game_state.gold}")
        print("="*50)
    
    def main_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("           UNDERTALE LITE")
        print("      (Heavily inspired by Undertale)")
        print("="*50)
        print("\n1. New Game")
        print("2. Load Game") 
        print("3. Quit")
        
        choice = self.wait_for_input()
        
        if choice == "1":
            self.new_game()
        elif choice == "2":
            if self.game_state.load_game():
                self.typewriter_print("Game loaded successfully!")
                self.game_loop()
            else:
                self.typewriter_print("No save file found.")
                self.main_menu()
        elif choice == "3":
            self.running = False
        else:
            self.typewriter_print("Invalid choice.")
            self.main_menu()
    
    def new_game(self):
        """Start a new game with intro"""
        self.typewriter_print("\n* Long ago, two races ruled over Earth:")
        self.typewriter_print("* HUMANS and MONSTERS.")
        time.sleep(1)
        self.typewriter_print("* One day, war broke out between the two races.")
        self.typewriter_print("* After a long battle, the humans were victorious.")
        time.sleep(1)
        self.typewriter_print("* They sealed the monsters underground with a magic spell.")
        time.sleep(1)
        self.typewriter_print("* Many years later...")
        time.sleep(2)
        
        print("\nWhat is your name?")
        name = input("> ").strip()
        if name:
            self.game_state.player_name = name
        
        self.typewriter_print(f"\n* Your name is {self.game_state.player_name}.")
        self.typewriter_print("* You have fallen into the Underground.")
        self.typewriter_print("* Your journey begins now...")
        
        self.game_loop()
    
    def game_loop(self):
        """Main game loop"""
        while self.running:
            self.display_stats()
            print("\nWhat do you want to do?")
            print("1. Encounter a monster")
            print("2. Check inventory")
            print("3. Save game")
            print("4. Return to menu")
            
            choice = self.wait_for_input()
            
            if choice == "1":
                self.random_encounter()
            elif choice == "2":
                self.show_inventory()
            elif choice == "3":
                self.game_state.save_game()
                self.typewriter_print("Game saved!")
            elif choice == "4":
                self.main_menu()
                break
            else:
                self.typewriter_print("Invalid choice.")
    
    def show_inventory(self):
        """Show player inventory"""
        print("\n📦 INVENTORY:")
        if not self.game_state.inventory:
            print("* Empty")
        else:
            for i, item in enumerate(self.game_state.inventory, 1):
                print(f"{i}. {item}")
        
        if self.game_state.inventory:
            print("\nUse an item? (number or 'back')")
            choice = self.wait_for_input()
            if choice.isdigit() and 1 <= int(choice) <= len(self.game_state.inventory):
                self.use_item(int(choice) - 1)
    
    def use_item(self, item_index):
        """Use an item from inventory"""
        item = self.game_state.inventory[item_index]
        
        if item == "Bandage":
            heal = 10
            self.game_state.hp = min(self.game_state.max_hp, self.game_state.hp + heal)
            self.typewriter_print(f"* You used the Bandage. Recovered {heal} HP!")
            self.game_state.inventory.remove(item)
        elif item == "Stick":
            self.typewriter_print("* You threw the Stick away.")
            self.typewriter_print("* ... Why would you do that?")
            self.game_state.inventory.remove(item)
        else:
            self.typewriter_print("* You can't use that right now.")
    
    def random_encounter(self):
        """Start a random battle encounter"""
        monsters = [
            Monster("Froggit", 20, 15, 5, 3, 2, 
                   "Life is difficult for this enemy.", 
                   {"compliment": "You compliment Froggit.", "threaten": "You threaten Froggit."}),
            Monster("Whimsun", 10, 12, 0, 2, 2,
                   "This monster is too sensitive to fight...",
                   {"console": "You console Whimsun.", "terrorize": "You terrorize Whimsun."}),
            Monster("Moldsmal", 50, 6, 0, 5, 3,
                   "Stereotypical: cuddly, cute, and only somewhat toxic.",
                   {"imitate": "You lie immobile. Moldsmal comes closer.", "flirt": "You wiggle your hips. Moldsmal blushes."})
        ]
        
        monster = random.choice(monsters)
        self.battle(monster)
    
    def battle(self, monster):
        """Main battle system"""
        self.typewriter_print(f"\n* {monster.name} blocks the way!")
        
        while monster.hp > 0 and self.game_state.hp > 0:
            # Display battle status
            print("\n" + "="*40)
            print(f"❤ {self.game_state.player_name}   LV {self.game_state.lv}")
            print(f"HP {self.game_state.hp}/{self.game_state.max_hp}")
            print()
            print(f"{monster.name}: {monster.hp}/{monster.max_hp} HP")
            if monster.mercy_ready:
                print("💛 * Monster can be spared")
            print("="*40)
            
            # Battle menu
            print("\n🗡️ FIGHT    🎭 ACT")
            print("🎒 ITEM     💛 MERCY")
            
            choice = self.wait_for_input()
            
            if choice in ["fight", "f", "1"]:
                self.fight_action(monster)
            elif choice in ["act", "a", "2"]:
                self.act_action(monster)
            elif choice in ["item", "i", "3"]:
                self.item_action()
            elif choice in ["mercy", "m", "4"]:
                if self.mercy_action(monster):
                    return
            else:
                self.typewriter_print("* Invalid choice.")
                continue
            
            # Monster's turn (if still alive)
            if monster.hp > 0:
                self.monster_attack(monster)
        
        # Battle ended
        if self.game_state.hp <= 0:
            self.game_over()
        elif monster.hp <= 0:
            self.victory(monster)
    
    def fight_action(self, monster):
        """Handle fight action"""
        damage = max(1, self.game_state.at - monster.df + random.randint(-2, 2))
        monster.hp = max(0, monster.hp - damage)
        
        self.typewriter_print(f"* You attack {monster.name} for {damage} damage!")
        
        if monster.hp <= 0:
            self.typewriter_print(f"* {monster.name} is defeated!")
    
    def act_action(self, monster):
        """Handle act menu"""
        print(f"\n* ACT options for {monster.name}:")
        print("1. Check")
        
        act_num = 2
        for act, desc in monster.act_options.items():
            print(f"{act_num}. {act.title()}")
            act_num += 1
        
        choice = self.wait_for_input()
        
        if choice == "1" or choice == "check":
            self.typewriter_print(monster.check_text)
        else:
            # Handle other ACT options
            act_keys = list(monster.act_options.keys())
            try:
                if choice.isdigit():
                    act_index = int(choice) - 2
                    if 0 <= act_index < len(act_keys):
                        act_key = act_keys[act_index]
                        self.typewriter_print(f"* {monster.act_options[act_key]}")
                        # Some ACT options make monster mercyable
                        if random.random() < 0.4:
                            monster.mercy_ready = True
                            self.typewriter_print(f"* {monster.name} seems calmer.")
                else:
                    # Try to match by name
                    for act_key in act_keys:
                        if choice == act_key:
                            self.typewriter_print(f"* {monster.act_options[act_key]}")
                            if random.random() < 0.4:
                                monster.mercy_ready = True
                                self.typewriter_print(f"* {monster.name} seems calmer.")
                            break
                    else:
                        self.typewriter_print("* Invalid ACT.")
            except:
                self.typewriter_print("* Invalid ACT.")
    
    def item_action(self):
        """Handle item usage in battle"""
        if not self.game_state.inventory:
            self.typewriter_print("* Your inventory is empty.")
            return
            
        print("\n📦 Use which item?")
        for i, item in enumerate(self.game_state.inventory, 1):
            print(f"{i}. {item}")
        
        choice = self.wait_for_input()
        if choice.isdigit() and 1 <= int(choice) <= len(self.game_state.inventory):
            self.use_item(int(choice) - 1)
        else:
            self.typewriter_print("* Invalid item.")
    
    def mercy_action(self, monster):
        """Handle mercy action"""
        if monster.mercy_ready:
            self.typewriter_print(f"* You spared {monster.name}.")
            self.game_state.mercy_count += 1
            return True
        else:
            self.typewriter_print(f"* {monster.name} is not ready to be spared.")
            return False
    
    def monster_attack(self, monster):
        """Monster attacks player"""
        damage = max(1, monster.at - self.game_state.df + random.randint(-1, 3))
        self.game_state.hp = max(0, self.game_state.hp - damage)
        
        # Random attack messages
        attack_messages = [
            f"* {monster.name} attacks!",
            f"* {monster.name} strikes you!",
            f"* {monster.name} shows no mercy!"
        ]
        
        self.typewriter_print(random.choice(attack_messages))
        self.typewriter_print(f"* You took {damage} damage!")
        
        if self.game_state.hp <= 0:
            self.typewriter_print("* You died...")
    
    def victory(self, monster):
        """Handle victory"""
        self.typewriter_print(f"* You gained {monster.exp_value} EXP and {monster.gold_value} GOLD!")
        
        self.game_state.exp += monster.exp_value
        self.game_state.gold += monster.gold_value
        self.game_state.killed += 1
        
        # Level up check
        exp_needed = self.game_state.lv * 10
        if self.game_state.exp >= exp_needed:
            self.level_up()
    
    def level_up(self):
        """Handle level up"""
        self.game_state.lv += 1
        self.game_state.exp = 0
        hp_increase = random.randint(4, 8)
        self.game_state.max_hp += hp_increase
        self.game_state.hp = self.game_state.max_hp
        self.game_state.at += random.randint(1, 3)
        self.game_state.df += random.randint(1, 2)
        
        self.typewriter_print(f"* Your LOVE increased to {self.game_state.lv}!")
        self.typewriter_print(f"* Max HP increased by {hp_increase}!")
        self.typewriter_print("* ATK and DEF increased!")
    
    def game_over(self):
        """Handle game over"""
        self.typewriter_print("\n💀 GAME OVER 💀")
        self.typewriter_print("* You cannot give up just yet...")
        self.typewriter_print(f"* {self.game_state.player_name}! Stay determined!")
        
        print("\n1. Restart")
        print("2. Main Menu")
        
        choice = self.wait_for_input()
        if choice == "1":
            self.game_state = GameState()
            self.new_game()
        else:
            self.main_menu()
    
    def run(self):
        """Main game runner"""
        try:
            while self.running:
                self.main_menu()
        except KeyboardInterrupt:
            self.typewriter_print("\n\n* Thanks for playing Undertale Lite!")
            self.running = False
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            self.running = False

if __name__ == "__main__":
    game = UndertaleLite()
    game.run()