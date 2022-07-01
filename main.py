from random import choice, randint
import random

print('Wumpus World Logical Agent')
print('Ahmad Navid Asghari')
print('Persian Gulf University')
print('github: https://www.github.com/Navid079')

print('=======================================')

print('Guide:')
print('Agent marks every block as a possible location of a pit or wumpus')
print('As agent moves on the world, it updates its map')
print('based on its sensors. For example if agent couldn\'t')
print('sense breeze in a location, it will remove the chance of ')
print('seeing a pit in nearby locations. In each step,')
print('agent finds the nearest "OK" location on its map')
print('and moves one tile towards it. The algorithm that')
print('agent uses to finds its path is "Hill Climbing with a static chance of')
print('random move.')
print(
    '------------------------------------------------------------------------')
print('Map Instructions:')
print('p: Pit')
print('w: Wumpus')
print('o: OK')
print('g: Gold')
print('-: Visited')
print('Capitalized Flag shows the location of the agent')
print(
    '------------------------------------------------------------------------')

# Random Seed
seed = int(input('Random Seed[0 for no seed]: '))
if seed: random.seed(seed)
else: print('No seed!')

# world parameters
width = int(input('Width[3~10]: '))
height = int(input('Height[3~10]: '))
pitChance = int(input('Chance of pit occurance(in percent)[10~50]: '))

# agent parameters
randomMoveChance = int(input('Chance of random move(in percent)[5~20]: '))

# fixing bad parameters
width = 3 if width < 3 else 10 if width > 10 else width
height = 3 if height < 3 else 10 if height > 10 else height
pitChance = 10 if pitChance < 10 else 50 if pitChance > 50 else pitChance
randomMoveChance = 5 if pitChance < 5 else 20 if pitChance > 20 else pitChance

# generating world
world = [['p' if randint(0, 99) < pitChance else 'o' for i in range(width)]
         for j in range(height)]

# placing gold, wumpus, and player
goldY, goldX = randint(0, height - 1), randint(0, width - 1)
wumpusY, wumpusX = randint(0, height - 1), randint(0, width - 1)
while (goldX, goldY) == (wumpusX, wumpusY):
  wumpusY, wumpusX = randint(0, height - 1), randint(0, width - 1)
playerY, playerX = randint(0, height - 1), randint(0, width - 1)
while (playerX, playerY) == (wumpusX, wumpusY) or (playerX,
                                                   playerY) == (goldX, goldY):
  playerY, playerX = randint(0, height - 1), randint(0, width - 1)

world[goldY][goldX] = 'g'
world[wumpusY][wumpusX] = 'w'
world[playerY][playerX] = 'o'

# removing nearby pits (to let agent have at least one possible safe move)
try:
  world[playerY][playerX - 1] = 'o' if world[playerY][
      playerX - 1] == 'p' else world[playerY][playerX - 1]
except:
  pass
try:
  world[playerY][playerX + 1] = 'o' if world[playerY][
      playerX + 1] == 'p' else world[playerY][playerX + 1]
except:
  pass
try:
  world[playerY -
        1][playerX] = 'o' if world[playerY -
                                   1][playerX] == 'p' else world[playerY -
                                                                 1][playerX]
except:
  pass
try:
  world[playerY +
        1][playerX] = 'o' if world[playerY +
                                   1][playerX] == 'p' else world[playerY +
                                                                 1][playerX]
except:
  pass

# generating agent's map
agentMap = [['wp' for i in range(width)] for j in range(height)]

# CONSTANTS
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# This function returns true if there is a pit nearby (breeze sensor)
def sensePit():
  global playerX, playerY
  left = world[playerY][playerX - 1] if playerX != 0 else '-'
  right = world[playerY][playerX + 1] if playerX != width - 1 else '-'
  up = world[playerY - 1][playerX] if playerY != 0 else '-'
  down = world[playerY + 1][playerX] if playerY != height - 1 else '-'
  return 'p' in [left, right, up, down]


# This function returns true if wumpus monster is nearby (stench sensor)
def senseWumpus():
  global playerX, playerY
  left = world[playerY][playerX - 1] if playerX != 0 else '-'
  right = world[playerY][playerX + 1] if playerX != width - 1 else '-'
  up = world[playerY - 1][playerX] if playerY != 0 else '-'
  down = world[playerY + 1][playerX] if playerY != height - 1 else '-'
  return 'w' in [left, right, up, down]


# This function updates agent's map if it didn't sense breeze
def removePitInNeigbor():
  global playerX, playerY, agentMap
  if playerX != 0:
    agentMap[playerY][playerX - 1] = agentMap[playerY][playerX - 1].replace(
        'p', '')
  if playerX != width - 1:
    agentMap[playerY][playerX + 1] = agentMap[playerY][playerX + 1].replace(
        'p', '')
  if playerY != 0:
    agentMap[playerY - 1][playerX] = agentMap[playerY - 1][playerX].replace(
        'p', '')
  if playerY != height - 1:
    agentMap[playerY + 1][playerX] = agentMap[playerY + 1][playerX].replace(
        'p', '')


# This function updates agent's map if it didn't sense stinch
def removeWumpusInNeigbor():
  global playerX, playerY
  if playerX != 0:
    agentMap[playerY][playerX - 1] = agentMap[playerY][playerX - 1].replace(
        'w', '')
  if playerX != width - 1:
    agentMap[playerY][playerX + 1] = agentMap[playerY][playerX + 1].replace(
        'w', '')
  if playerY != 0:
    agentMap[playerY - 1][playerX] = agentMap[playerY - 1][playerX].replace(
        'w', '')
  if playerY != height - 1:
    agentMap[playerY + 1][playerX] = agentMap[playerY + 1][playerX].replace(
        'w', '')


# Heuristic function for choosing best destination (to explore)
def findNearestOkTile():
  global playerX, playerY
  minI, minJ = 0, 0
  minValue = width + height
  for i, row in enumerate(agentMap):
    for j, tile in enumerate(row):
      if tile == 'o':
        distance = findDistance(playerX, playerY, j, i)
        if distance < minValue:
          minI, minJ, minValue = i, j, distance
  return minI, minJ, minValue


# Utility function that returns distance of two locations
def findDistance(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)


# Agent's acutuator (move)
def move(direction):
  global playerX, playerY, agentMap
  agentMap[playerY][playerX] = '-'
  if direction == LEFT:
    playerX -= 1
  elif direction == RIGHT:
    playerX += 1
  elif direction == UP:
    playerY -= 1
  elif direction == DOWN:
    playerY += 1


# Utility function to print directions more user firendly
def printDirections(input, end='\n'):
  if type(input) == int:
    if input == UP: print('UP', end=end)
    elif input == DOWN: print('DOWN', end=end)
    elif input == LEFT: print('LEFT', end=end)
    elif input == RIGHT: print('RIGHT', end=end)
  else:
    print('[', end='')
    for i in input:
      printDirections(i, end=',')
    print(']', end=end)


# Driver Code
while world[playerY][playerX] != 'g':
  agentMap[playerY][playerX] = 'X'

  # Get sensor data and update agent's KB with it
  if not sensePit():
    removePitInNeigbor()
  if not senseWumpus():
    removeWumpusInNeigbor()

  # Print Agent's map (KB)
  for row in agentMap:
    for i, tile in enumerate(row):
      if tile == '': row[i] = 'o'
      print(row[i], end='\t')
    print()
  print('============================')

  # Choose a destination
  i, j, value = findNearestOkTile()

  #If there is no good destination, agent will fail (maybe random move? Or try to locate and defeat wumpus?)
  if value == width + height:
    print('No Result found')
    break

  # Else, choose an action
  else:

    # Hill climbing algorithm will find the best greedy move that agent can choose
    bestGreedyMove = None
    bestGreedyValue = 8
    possibleMoves = []

    # Check the left tile if it is a possible or maybe the best move
    if playerX != 0 and (tileType :=
                         agentMap[playerY][playerX - 1]) in ['-', 'o']:
      distance = findDistance(playerX - 1, playerY, j, i)
      if distance < bestGreedyValue:
        bestGreedyValue = distance
        bestGreedyMove = LEFT
      possibleMoves.append(LEFT)

    # Check the right tile if it is a possible or maybe the best move
    if playerX != width - 1 and (tileType :=
                                 agentMap[playerY][playerX + 1]) in ['-', 'o']:
      distance = findDistance(playerX + 1, playerY, j, i)
      if distance < bestGreedyValue:
        bestGreedyValue = distance
        bestGreedyMove = RIGHT
      possibleMoves.append(RIGHT)

    # Check the upper tile if it is a possible or maybe the best move
    if playerY != 0 and (tileType :=
                         agentMap[playerY - 1][playerX]) in ['-', 'o']:
      distance = findDistance(playerX, playerY - 1, j, i)
      if distance < bestGreedyValue:
        bestGreedyValue = distance
        bestGreedyMove = UP
      possibleMoves.append(UP)

    # Check the lower tile if it is a possible or maybe the best move
    if playerY != height - 1 and (
        tileType := agentMap[playerY + 1][playerX]) in ['-', 'o']:
      distance = findDistance(playerX, playerY + 1, j, i)
      if distance < bestGreedyValue:
        bestGreedyValue = distance
        bestGreedyMove = DOWN
      possibleMoves.append(DOWN)

    # Do the best greedy move
    if randint(0, 99) >= randomMoveChance:
      print('Do best greedy move')
      print('Best greedy move is: ', end='')
      printDirections(bestGreedyMove)
      move(bestGreedyMove)
    # Or a random safe move
    else:
      print('Do a random safe move')
      print('Available moves: ', end='')
      printDirections(possibleMoves)
      randomMove = choice(possibleMoves)
      print('Random chosen move is: ', end='')
      printDirections(randomMove)
      move(randomMove)
  input('Press Enter to continue...')
  print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-')

agentMap[playerY][playerX] = world[playerY][playerX].upper()
print('Agent Map of World')
for row in agentMap:
  for i, tile in enumerate(row):
    print(row[i], end='\t')
  print()
print('============================')

print('Full Map of World')
for row in world:
  for i, tile in enumerate(row):
    print(row[i], end='\t')
  print()
