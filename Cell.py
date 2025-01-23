import decimal

decimal.getcontext().prec = 5

class Cell:
    def __init__(cell, f, g):
        cell.f = f
        cell.g = g
        cell.is_open = False
        cell.on_fire = False
        cell.flammability = decimal.Decimal(0)

    def __lt__(cell, oCell):
        if cell.f < oCell.f:
            return True
        elif cell.f == oCell.f:
            return cell.g < oCell.g
        else:
            return False

    def prob_fire(cell, q, k):
        q = decimal.Decimal(q)

        if k == 0:
            cell.flammability = decimal.Decimal(0)
        else:
            cell.flammability = 1 - (1 - q) ** k

    def __hash__(cell):
        return hash((cell.f, cell.g))
    
    def __eq__(cell, oCell):
        if cell.f == oCell.f and cell.g == oCell.g:
            return True
        else:
            return False
        
    
    
    
    
    
    