import decimal
import random
from Cell import Cell
from Bot import Bot
from Button import Button
from Fire import Fire

decimal.getcontext().prec = 5

class Ship:
    def __init__(self, d, q):

        self.d = d #Size
        self.q = q #Flammability
        self.grid = [[Cell(f, g) for g in range(d)] for f in range(d)] #Grid Layout
        self.cells_fire = [] #Cells on fire
        self.blocked_neighbor = [] #Cells with 1 neighbor
        self.Onear_fire = [] #Open cells near fire 
        self.no_enter = [] #Cells that cannot be entered
        

        self.bot = None
        self.button = None
        self.initial_fire = None

    def __str__(self):
        s = "Ship:\n"
        for f in range(self.d):
            for g in range(self.d):
                if self.grid[f][g].on_fire is True:
                    s += "[F]"
                elif self.bot != None and self.grid[f][g] == self.bot.cell:
                    s += "[R]"
                elif self.button != None and self.grid[f][g] == self.button.cell:
                    s += "[B]"
                elif self.grid[f][g].is_open is True:
                    s += "[  ]"
                else:
                    s += "[C]"
            s += "\n"
        return s

    def addBot(self):
        tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)] #Random cell to spawn bot

        while tCell.is_open is False:
            tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.bot = Bot(tCell)

    def addButton(self):

        tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)] #Random cell to spawn button

        while tCell.is_open is False or tCell == self.bot.cell:
            tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.button = Button(tCell)

    def start_fire(self):

        tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)] #Random cell to spawn fire

        while tCell.is_open is False or tCell == self.button.cell or tCell == self.bot.cell:
            tCell = self.grid[random.randint(0, self.d - 1)][random.randint(0, self.d - 1)]
        self.initial_fire = Fire(tCell)

        self.setFire(tCell.f, tCell.g)
        self.cells_fire.append(self.grid[tCell.f][tCell.g])

    def get_neighbors(self, cell): #Gets the current cells neighbors 
        neighbors = []
        if cell.f - 1 >= 0:
            neighbors.append(self.grid[cell.f - 1][cell.g])
        if cell.f + 1 < self.d:
            neighbors.append(self.grid[cell.f + 1][cell.g])
        if cell.g - 1 >= 0:
            neighbors.append(self.grid[cell.f][cell.g - 1])
        if cell.g + 1 < self.d:
            neighbors.append(self.grid[cell.f][cell.g + 1])
        return neighbors

    def single_neighbor(self, cell):  #Checks if the cell given has one open neighbor

        num_neighbors = 0
        
        while (num_neighbors < 2):
            if cell.f - 1 >= 0:
                if self.grid[cell.f - 1][cell.g].is_open is True: #West
                    num_neighbors += 1
            if cell.f + 1 < self.d:
                if self.grid[cell.f + 1][cell.g].is_open is True: #East
                    num_neighbors += 1
            if cell.g + 1 < self.d:
                if self.grid[cell.f][cell.g + 1].is_open is True: #North
                    num_neighbors += 1
            if cell.g - 1 >= 0:
                if self.grid[cell.f][cell.g - 1].is_open is True: #South
                    num_neighbors += 1
            
            if num_neighbors == 1:
                return True
            return False
    
    def open_cell(self, f, g): #Method to open a cell

        if self.grid[f][g].is_open is True:
            return

        self.grid[f][g].is_open = True

        if self.single_neighbor(self.grid[f][g]) is True and self.grid[f][g] not in self.no_enter:
            self.no_enter.append(self.grid[f][g])

        elif self.single_neighbor(self.grid[f][g]) is False and self.grid[f][g] in self.no_enter:
            self.no_enter.remove(self.grid[f][g])

        if f - 1 >= 0:
            if self.grid[f - 1][g].is_open is False and self.single_neighbor(self.grid[f - 1][g]) is True: #West
                self.blocked_neighbor.append(self.grid[f - 1][g])
            
            elif self.grid[f - 1][g] in self.blocked_neighbor:
                self.blocked_neighbor.remove(self.grid[f - 1][g])

        if f + 1 < self.d:
            if self.grid[f + 1][g].is_open is False and self.single_neighbor(self.grid[f + 1][g]) is True: #East
                self.blocked_neighbor.append(self.grid[f + 1][g])
            
            elif self.grid[f + 1][g] in self.blocked_neighbor:
                self.blocked_neighbor.remove(self.grid[f + 1][g])

        if g + 1 < self.d:
            if self.grid[f][g + 1].is_open is False and self.single_neighbor(self.grid[f][g + 1]) is True: #North
                self.blocked_neighbor.append(self.grid[f][g + 1])
            
            elif self.grid[f][g + 1] in self.blocked_neighbor:
                self.blocked_neighbor.remove(self.grid[f][g + 1])   

        if g - 1 >= 0:
            if self.grid[f][g - 1].is_open is False and self.single_neighbor(self.grid[f][g - 1]) is True: #South
                self.blocked_neighbor.append(self.grid[f][g - 1])
            
            elif self.grid[f][g - 1] in self.blocked_neighbor:
                self.blocked_neighbor.remove(self.grid[f][g - 1])

    #For if the bot hits a dead end or if a cell is not open 
    def ifBlocked(self, cell):

        if cell.is_open is False or self.single_neighbor(cell) is False:
            return

        while True:
            i = random.randint(1, 4)

            if i == 1 and cell.f - 1 >= 0 and self.grid[cell.f - 1][cell.g].is_open is False: #West 
                self.grid[cell.f - 1][cell.g].is_open = True
                self.no_enter.remove(cell)
                return
            if i == 2 and cell.f + 1 < self.d and self.grid[cell.f + 1][cell.g].is_open is False: #East
                self.grid[cell.f + 1][cell.g].is_open = True
                self.no_enter.remove(cell)
                return
            if i == 3 and cell.g + 1 < self.d and self.grid[cell.f][cell.g + 1].is_open is False: #North
                self.grid[cell.f][cell.g + 1].is_open = True
                self.no_enter.remove(cell)
                return
            if i == 4 and cell.g - 1 >= 0 and self.grid[cell.f][cell.g - 1].is_open is False: #South
                self.grid[cell.f][cell.g - 1].is_open = True
                self.no_enter.remove(cell)
                return
   #Method that moves the fire based on the probability of the cells around them  
    def advance_fire(self): 
        t = random.random()
        
        for cell in self.Onear_fire[:]:
            if (cell.flammability >= t): #if above t set the cell on fire
                self.setFire(cell.f, cell.g)
                self.cells_fire.append(self.grid[cell.f][cell.g])
    
    #Check if the neighbor is on fire and if open
    def neighbors_fire(self, cell): 
        num_neighbors = 0

        if cell.f - 1 >= 0:
            if self.grid[cell.f - 1][cell.g].is_open is True and self.grid[cell.f - 1][cell.g].on_fire is True:
                num_neighbors += 1
        if cell.f + 1 < self.d:
            if self.grid[cell.f + 1][cell.g].is_open is True and self.grid[cell.f + 1][cell.g].on_fire is True:
                num_neighbors += 1
        if cell.g + 1 < self.d:
            if self.grid[cell.f][cell.g + 1].is_open is True and self.grid[cell.f][cell.g + 1].on_fire is True:
                num_neighbors += 1
        if cell.g - 1 >= 0:
            if self.grid[cell.f][cell.g - 1].is_open is True and self.grid[cell.f][cell.g - 1].on_fire is True:
                num_neighbors += 1
        
        return num_neighbors
    
    #Set a cell on fire based on the spread probability that is given
    def setFire(self, f, g): 
        
        self.grid[f][g].on_fire = True
        
        if self.grid[f][g] in self.Onear_fire:
            self.Onear_fire.remove(self.grid[f][g])
        
        if f - 1 >= 0 and self.grid[f - 1][g].is_open is True and self.grid[f - 1][g].on_fire is False: #west

            k = self.neighbors_fire(self.grid[f - 1][g])
            self.grid[f - 1][g].prob_fire(self.q, k)

            self.Onear_fire.append(self.grid[f - 1][g])

        if f + 1 < self.d and self.grid[f + 1][g].is_open is True and self.grid[f + 1][g].on_fire is False: #east
            k = self.neighbors_fire(self.grid[f + 1][g])
            self.grid[f + 1][g].prob_fire(self.q, k)
            self.Onear_fire.append(self.grid[f + 1][g])

        if g + 1 < self.d and self.grid[f][g + 1].is_open is True and self.grid[f][g + 1].on_fire is False: #north 
            k = self.neighbors_fire(self.grid[f][g + 1])
            self.grid[f][g + 1].prob_fire(self.q, k)
            self.Onear_fire.append(self.grid[f][g + 1])

        if g - 1 >= 0 and self.grid[f][g - 1].is_open is True and self.grid[f][g - 1].on_fire is False: #south
            k = self.neighbors_fire(self.grid[f][g - 1])
            self.grid[f][g - 1].prob_fire(self.q, k)
            self.Onear_fire.append(self.grid[f][g - 1])
    
    