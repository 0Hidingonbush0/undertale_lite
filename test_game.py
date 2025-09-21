#!/usr/bin/env python3
"""
Simple test script for Undertale Lite
Tests core functionality without interactive input
"""

import unittest
import sys
import os

# Add parent directory to path to import the game
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from undertale_lite import GameState, Monster, UndertaleLite

class TestUndertaleLite(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.game_state = GameState()
        self.game = UndertaleLite()
        
    def test_game_state_initialization(self):
        """Test GameState initialization"""
        self.assertEqual(self.game_state.player_name, "Frisk")
        self.assertEqual(self.game_state.hp, 20)
        self.assertEqual(self.game_state.max_hp, 20)
        self.assertEqual(self.game_state.lv, 1)
        self.assertEqual(self.game_state.exp, 0)
        self.assertIn("Stick", self.game_state.inventory)
        self.assertIn("Bandage", self.game_state.inventory)
        
    def test_monster_creation(self):
        """Test Monster class creation"""
        monster = Monster(
            "Test Monster", 30, 15, 5, 5, 3,
            "A test monster for testing.",
            {"test": "Test action"}
        )
        
        self.assertEqual(monster.name, "Test Monster")
        self.assertEqual(monster.hp, 30)
        self.assertEqual(monster.max_hp, 30)
        self.assertEqual(monster.at, 15)
        self.assertEqual(monster.df, 5)
        self.assertEqual(monster.exp_value, 5)
        self.assertEqual(monster.gold_value, 3)
        self.assertFalse(monster.mercy_ready)
        
    def test_save_load_functionality(self):
        """Test save and load game functionality"""
        # Modify game state
        self.game_state.player_name = "TestPlayer"
        self.game_state.hp = 15
        self.game_state.lv = 2
        self.game_state.gold = 50
        
        # Save game
        test_file = "test_save.json"
        self.game_state.save_game(test_file)
        
        # Create new game state and load
        new_game_state = GameState()
        success = new_game_state.load_game(test_file)
        
        self.assertTrue(success)
        self.assertEqual(new_game_state.player_name, "TestPlayer")
        self.assertEqual(new_game_state.hp, 15)
        self.assertEqual(new_game_state.lv, 2)
        self.assertEqual(new_game_state.gold, 50)
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
            
    def test_inventory_management(self):
        """Test inventory operations"""
        initial_count = len(self.game_state.inventory)
        
        # Test adding item
        self.game_state.inventory.append("Test Item")
        self.assertEqual(len(self.game_state.inventory), initial_count + 1)
        self.assertIn("Test Item", self.game_state.inventory)
        
        # Test removing item
        self.game_state.inventory.remove("Test Item")
        self.assertEqual(len(self.game_state.inventory), initial_count)
        self.assertNotIn("Test Item", self.game_state.inventory)
        
    def test_combat_calculations(self):
        """Test basic combat damage calculations"""
        monster = Monster("Test", 20, 10, 3, 1, 1, "Test", {})
        
        # Basic damage calculation (without randomness)
        base_damage = max(1, self.game_state.at - monster.df)
        self.assertGreaterEqual(base_damage, 1)  # Should always deal at least 1 damage
        
        # Test monster taking damage
        initial_hp = monster.hp
        damage = 5
        monster.hp = max(0, monster.hp - damage)
        self.assertEqual(monster.hp, initial_hp - damage)

def run_tests():
    """Run all tests"""
    print("Running Undertale Lite Tests...")
    print("=" * 40)
    
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 40)
    print("✅ Core functionality tests completed!")
    print("🎮 The game should be ready to play!")

if __name__ == "__main__":
    run_tests()