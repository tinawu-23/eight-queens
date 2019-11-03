import random

## generate 8 random queens ##
def randQueens():
    queens = set()
    while len(queens) < 8:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if (x,y) in queens: 
            continue
        queens.add((x,y))
    return queens

## print game board ##
def printBoard(queens):
    for r in range(8): 
        row = ''
        for c in range(8):
            if (r,c) in queens:
                row += 'Q '
            else:
                row += '. '
        print(row)

## find queens in conflict and exclude one queen ##
def findConflict(q):
    conflictlst = []
    choice = ()
    for queen in q:
        tmp = q[:]
        tmp.remove(queen)
        # check if the current q has conflict with any other 7 queens
        conflicts = heuristic(tmp,queen)
        if conflicts > 0:
            conflictlst.append(queen)
    if conflictlst:
        choice = random.choice(conflictlst)
        q.remove(choice)
        
    return q, choice

## calculate the total conflict for a queen (cost function) ##
def heuristic(sevenQ, newQ):
    cost = 0
    r1, c1 = newQ[0], newQ[1]
    for q in sevenQ:
        r2, c2 = q[0], q[1]
        # if same row or same col or on diagonal
        if r1 == r2 or c1 == c2 or r1+c1 == r2+c2 or r1-c1 == r2-c2:
            cost += 1
    return cost

## find the best position to place the missing queen ##
def findMincostPos(sevenQ, prevQ):
    allcost = {}
    for r in range(8):
        for c in range(8):
            if (r, c) in sevenQ or (r,c) == prevQ:
                continue
            cost = heuristic(sevenQ, (r, c))
            if cost not in allcost:
                allcost[cost] = []
            allcost[cost].append((r,c))
    minkey = min(allcost.keys())
    allpos = allcost[minkey]
    pos = random.choice(allpos)
    return pos

if __name__ == '__main__':

    ## Randomize board (initial game state) ##
    queens = randQueens()
    print('\n==================')
    print('Random Board: ')
    printBoard(queens)
    print('==================\n')

    ## Solve for solution ##
    queens = list(queens)
    newqueens, removed = findConflict(queens) # consist of 7 queens (excluding the 1 queen we're repositioning)
    i = 0
    while len(newqueens) < 8:
        mincostpos = findMincostPos(newqueens, removed) # finding the position of where to put the new queen
        q = newqueens + [mincostpos] # queens is now: the previous 7 queens + the new queen we decided to put down; this generates a new board
        newqueens, removed = findConflict(q) # check to see whether there's conflict within the queens
        i += 1

    ## Solution (final game state) ##
    print('==================')
    print('Solution Board: ')
    printBoard(newqueens)
    print('==================\n')

    ## Record number of tries ##
    print("Number of tries: "+str(i))
    print()

    with open("record.txt", "a") as f:
        f.write(str(i)+'\n')
