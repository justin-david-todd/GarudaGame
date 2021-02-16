# GarudaGame
This is a custom version of the game 'Phoenix' I loved playing as a kid. The project is still ongoing. 
My focus is to make the game's ships, lasers, and levels modular so their attributes can be easily upgraded or customized.

Features I have included:

***System Features***
- No Global Variables: All attributes used by objects are stored as private data members.
- GarudaGame class: One class to instantiate a new game which contains all objects (ships, lasers, etc.) the user will interact with.
- Game modularized - Object classes in separate files for better organization.
- A Title Screen with "Quit" and "New Game"
- Point System keeps track of the player's score as they play.


***Level Features***
- Level Sequence: Stores game levels in order, so that the player naturally progresses from one level to the next.
- Level Methods: Collection of GarudaGame methods used to create progressively more difficult levels.
- Enemy Spawn Patterns - Collection of GarudaGame methods used to mass-spawn enemies in a variety of patterns. Makes designing levels even easier.
- Added Variety of Enemy Spawn Patterns
- Level Start messaged displayed at each new level.
- Simple variety of pre-constructed levels.
- Endless "Heck Mode" begins when player finishes all constructed levels.

***Ship Features***
- Enemy "Species": This enemy characteristic pulls pre-defined enemy designs from a dictionary to enable simple design and spawning of new kinds of baddies.
- Laser "Types": Dictionary stores predefined player and enemy laser designs for easy assigning of different laser specifications.
- Movement Patterns: Collection of laser and enemy methods used to define how different enemies and lasers move/respond in their environment.
- Added Variety of Enemy Laser types and Movement patterns

***Upcoming Features***
- Downloadable .exe file format
- Multiple Lives
- Saving Progress and High Scores
- Ship power ups
- Store to purchase ship upgrades.


Special thanks to TechWithTim whose tutorials showed me how to interact with Pygame.
