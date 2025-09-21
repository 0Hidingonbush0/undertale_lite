# Undertale Lite

A text-based Undertale-inspired game, heavily inspired by Toby Fox's masterpiece "Undertale".

## Description

Undertale Lite recreates the core mechanics and spirit of Undertale in a lightweight, text-based format. Experience the memorable dialog system, unique battle mechanics, and moral choices that made the original so beloved.

## Features

### Core Undertale Mechanics
- **Dialog System**: Typewriter effect text display just like the original
- **Battle System**: Classic FIGHT/ACT/ITEM/MERCY menu system
- **Monster Encounters**: Various monsters with unique personalities and ACT options
- **Pacifist Route**: Spare monsters instead of fighting them
- **Character Progression**: Level up system with HP, ATK, and DEF stats
- **Save System**: Save and load your progress

### Game Elements
- **Stats Tracking**: HP, LV (LOVE), EXP, ATK, DEF, and GOLD
- **Inventory System**: Use items like Bandages to heal
- **Multiple Monsters**: Face Froggits, Whimsuns, and Moldsmals
- **ACT Commands**: Unique interaction options for each monster type
- **Mercy System**: Spare monsters when they're ready to be merciful

## How to Play

### Installation
No installation required! Just run the Python script:

```bash
python3 undertale_lite.py
```

Or use the launcher:
```bash
python3 play.py
```

### Game Controls
- **Main Menu**: Choose numbers 1-3 or type options
- **Battle Menu**: 
  - Type `fight` or `f` to attack
  - Type `act` or `a` to interact with monsters
  - Type `item` or `i` to use inventory items
  - Type `mercy` or `m` to spare monsters
- **Navigation**: Follow on-screen prompts and type your choices

### Battle System
1. **FIGHT**: Deal damage to monsters (violent route)
2. **ACT**: Interact with monsters in unique ways
   - **Check**: View monster stats and description
   - **Monster-specific actions**: Each monster has unique ACT options
3. **ITEM**: Use healing items or other inventory items
4. **MERCY**: Spare monsters (some need to be calmed via ACT first)

### Monsters
- **Froggit**: "Life is difficult for this enemy." - Can be complimented or threatened
- **Whimsun**: "This monster is too sensitive to fight..." - Can be consoled or terrorized  
- **Moldsmal**: "Stereotypical: cuddly, cute, and only somewhat toxic." - Can be imitated or flirted with

## Game Philosophy

Like the original Undertale, this game explores themes of:
- **Mercy vs Violence**: You don't have to kill anyone
- **Consequences**: Your choices affect the game world
- **Determination**: Keep going even when things get tough
- **Understanding**: Learn about monsters instead of just fighting them

## Technical Details

- **Language**: Python 3
- **Dependencies**: None (uses only standard library)
- **Platform**: Cross-platform (Windows, Mac, Linux)
- **Save Format**: JSON files for easy portability

## Playing Tips

1. **Try ACT first**: Most monsters can be spared if you understand them
2. **Check monsters**: Use ACT → Check to learn about each enemy
3. **Save often**: Use the save system to preserve your progress  
4. **Experiment**: Different ACT options have different effects
5. **Stay determined**: Don't give up if you die - you can always restart!

## Differences from Original Undertale

This is a simplified, text-based version that captures the core mechanics:
- No graphics or sound (text-based descriptions instead)
- Simplified battle system (no bullet-hell mechanics)
- Fewer monsters and areas (focused on core gameplay)
- Basic story (intro sequence only)

## Credits

Heavily inspired by "Undertale" by Toby Fox. This fan project aims to honor the original while providing an accessible, lightweight version of the core gameplay experience.

## License

This is a fan project created for educational and entertainment purposes. All original Undertale concepts, characters, and mechanics belong to Toby Fox.