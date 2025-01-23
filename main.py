import copy
import decimal
import random
import math
import queue
import heapq
from queue import PriorityQueue, Queue
from collections import deque
from Ship import Ship
from Bot import Bot

decimal.getcontext().prec = 5
ship_danger_factors = {}

#Basic BFS 
def bot1(ship):

    fringe = Queue() 
    closed_set = set()
    prev = {ship.bot.cell: ship.bot.cell}

    fringe.put(ship.bot.cell) # Start BFS from bot's initial position

    while not fringe.empty():
        curr = fringe.get() # Get current cell from the queue

        if curr == ship.button.cell: # Check if the bot has reached the button
            path = deque()
            path.append(ship.button.cell)
            
            cell = ship.button.cell 
            while cell != ship.bot.cell: # Reconstruct the path
                cell = prev[cell]
                path.appendleft(cell)
            
            while ship.bot.cell != ship.button.cell and len(path) > 0: # Move bot along the path
                if ship.bot.cell.on_fire:
                    return False
                
                ship.bot.cell = path.popleft()
                print("Next Bot Cell (", ship.bot.cell.f, ", ", ship.bot.cell.g, ")")
                ship.advance_fire()
            
            return True  # Return True if the bot reaches the button
        
        for neighbor in ship.get_neighbors(curr):
            if neighbor != ship.initial_fire.cell and neighbor.is_open and neighbor not in closed_set:
                fringe.put(neighbor) # Add open, unvisited neighbors to the queue
                prev[neighbor] = curr # Track the path
        
        closed_set.add(curr)
    
    return False # Return False if the bot cannot reach the button

# BFS search to find a path avoiding cells on fire
def bfs_bot2(ship):

    fringe = Queue()
    closed_set = set() # Set to track visited cells
    prev = {ship.bot.cell: ship.bot.cell} # Dictionary to reconstruct the path

    fringe.put(ship.bot.cell) 

    while not fringe.empty():
        curr = fringe.get()

        if curr == ship.button.cell:
            path = deque()
            path.append(ship.button.cell)

            cell = ship.button.cell
            while cell != ship.bot.cell:
                cell = prev[cell]
                path.appendleft(cell)
            path.popleft() # Remove the bot's initial position from the path
            return path

        for neighbor in ship.get_neighbors(curr): # Iterate over all neighbors of the current cell
            if not neighbor.on_fire and neighbor.is_open and neighbor not in closed_set:
                fringe.put(neighbor) # Add open, non-fire neighbors to the queue
                prev[neighbor] = curr

        closed_set.add(curr)
    return None

# Bot strategy that moves along the path found by run_bot2_bfs
def bot2(ship):
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False

        path = bfs_bot2(ship)
        if path is None:
            return False

        ship.bot.cell = path.popleft() # Move bot to the next cell in the path
        print("Next Bot Cell (", ship.bot.cell.f, ", ", ship.bot.cell.g, ")")
        ship.advance_fire()
    return True

# BFS search that prioritizes avoiding neighbors near fire first
def bfs_bot3(ship):

    fringe = Queue()
    closed_set = set()
    prev = {ship.bot.cell: ship.bot.cell}

    fringe.put(ship.bot.cell) 

    while not fringe.empty():
        curr = fringe.get()

        if curr == ship.button.cell:
            return prev

        for neighbor in ship.get_neighbors(curr):
            if not neighbor.on_fire and ship.neighbors_fire(neighbor) == 0 and neighbor.is_open and neighbor not in closed_set:
                fringe.put(neighbor) # Prioritize open neighbors with no fire exposure
                prev[neighbor] = curr

        closed_set.add(curr)

    # Fallback BFS without prioritizing fire exposure
    fringe = Queue()
    closed_set.clear()
    prev.clear()
    prev = {ship.bot.cell: ship.bot.cell}
    fringe.put(ship.bot.cell)

    while not fringe.empty():
        curr = fringe.get()

        if curr == ship.button.cell:
            return prev

        for neighbor in ship.get_neighbors(curr):
            if not neighbor.on_fire and neighbor.is_open and neighbor not in closed_set:
                fringe.put(neighbor)  # Add open, non-fire neighbors to the queue
                prev[neighbor] = curr

        closed_set.add(curr)

    return None

# Bot strategy that uses the path found by run_bot3_bfs
def bot3(ship):
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False

        prev = bfs_bot3(ship)
        if prev is None:
            return False

        path = deque()
        path.append(ship.button.cell)
        cell = ship.button.cell
        while cell != ship.bot.cell:
            cell = prev[cell]
            path.appendleft(cell)
        path.popleft()  
        ship.bot.cell = path.popleft()
        print("Next Bot Cell (", ship.bot.cell.f, ", ", ship.bot.cell.g, ")")
        ship.advance_fire()

    return True

# Helper function to compute 90 degree distance between two cells
def compute_distance(cell1, cell2):
    return abs(cell1.f - cell2.f) + abs(cell1.g - cell2.g)

# Heuristic to evaluate the danger of a cell based on neighboring fire exposure
def danger_heuristic(ship, cell):
    if cell.on_fire:
        return float('inf')
    fire_exposure = 0
    for neighbor in ship.get_neighbors(cell):
        if neighbor.on_fire:
            fire_exposure += 1 # Increase danger for each neighboring cell on fire
    return fire_exposure

# Search that uses both distance and fire danger as heuristics
def assessmentSearch(ship):
    fringe = []
    start = ship.bot.cell
    goal = ship.button.cell
    heapq.heappush(fringe, (0, start)) # Initialize the priority queue with the start cell
    came_from = {start: None}

    # Distance from start to current cell
    g_score = {start: 0} 
    # Estimated total cost from start to goal
    f_score = {start: compute_distance(start, goal)} 

    while fringe:
        _, current = heapq.heappop(fringe)

        if current == goal:
            path = []
            while current: # Reconstruct the path
                path.append(current)
                current = came_from[current]
            return path[::-1] # Reverse the path to get correct order

        #Evaluate and Update Cost Estimates For Each Cell
        for neighbor in ship.get_neighbors(current):
            if not neighbor.is_open or neighbor.on_fire:
                continue
            t_g_score = g_score[current] + 1
            if neighbor not in g_score or t_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = t_g_score
                f_score[neighbor] = t_g_score + compute_distance(neighbor, goal) + danger_heuristic(ship, neighbor)
                heapq.heappush(fringe, (f_score[neighbor], neighbor)) # Add neighbor to the heap

    return None

# Bot strategy that uses the search with distance and fire danger heuristics
def bot4(ship):
    while ship.bot.cell != ship.button.cell:
        if ship.bot.cell.on_fire:
            return False

        path = assessmentSearch(ship)
        if path is None:
            return False

        for next_cell in path[1:]:  
            ship.bot.cell = next_cell
            print("Next Bot Cell (", ship.bot.cell.f, ", ", ship.bot.cell.g, ")")
            ship.advance_fire()

            if ship.bot.cell.on_fire:
                return False

    return True

def main():

    print('Grid Value:')
    d = int(input())
    print('Q Value:')
    q = decimal.Decimal(input())
    print('Bot # to run:')
    bot_num = int(input())
    print('Number of simulations to run:')
    times_to_run = int(input())

    num_successes = 0
    num_failures = 0

    for indef in range(times_to_run):

        ship = Ship(d, q)

        f = random.randint(0, d - 1)
        g = random.randint(0, d - 1)

        ship.open_cell(f, g)
        #Open cell in ship 
        while (ship.blocked_neighbor):
            cell_to_open_indef = random.randint(0, len(ship.blocked_neighbor) - 1)
            cell_to_open = ship.blocked_neighbor.pop(cell_to_open_indef)

            ship.open_cell(cell_to_open.f, cell_to_open.g)
        #Remove cells that cannot be spawned
        for dead_end in ship.no_enter[:]:
            if ship.single_neighbor(dead_end) is False:
                ship.no_enter.remove(dead_end)
        #Open random blocked cell 
        for i in range(math.floor(len(ship.no_enter) / 2)):
            cell_to_open_indef = random.randint(0, len(ship.no_enter) - 1)
            ship.ifBlocked(ship.no_enter[cell_to_open_indef])
        
        ship.addBot()
        ship.addButton()
        ship.start_fire()

        print("---BEGIN SIMULATION---")
        print("Bot Location: (", ship.bot.cell.f, ", ", ship.bot.cell.g, ")")
        print("Button Location: (", ship.button.cell.f, ", ", ship.button.cell.g, ")")
        print("Fire Start Location: (", ship.initial_fire.cell.f, ", ", ship.initial_fire.cell.g, ")")
        print(ship)

        if bot_num == 1:
            if bot1(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 2:
            if bot2(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 3:
            if bot3(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        if bot_num == 4:
            if bot4(ship) is True:
                num_successes += 1
            else:
                num_failures += 1
        
        print(ship)
    
    print("Successes: ", num_successes)
    print("Failures: ", num_failures)

if __name__ == "__main__":
    main()