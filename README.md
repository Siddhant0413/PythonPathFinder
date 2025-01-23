This is a pathfinding algorithm and the basic structure for a machine learning algorithm.

The ship is a square grid, D X D, with a certain amount of blocked cells. A random cell is chose to be open. 
The bot will then occupy one of these cells where it is able to move to an adjacent cell at each time step.
A 'fire' starts at a random cell and spreads to an adjacent open cell at random. 
A button is located at a random empty cell and the task of the bot is to reach this button. 

Bot 1: Most basic bot that plans the shortest path to button, but ignores the spread of the fire.
Bot 2: At each time-step, the bot re-plans the shortest path to the button taking into account cells on fire.
Bot 3: Bot 3 does everything the other bots do, but also takes into account any adjacent cells of the fire.
Bot 4: Does the same as the previous bots but uses BFS pathfinding and heuristic-based evaluations.
