import os
from pathlib import Path
import pyautogui
import time
import random
import keyboard
import threading

stop_program = False
def listen_for_quit():
    global stop_program
    while True:
        if keyboard.is_pressed('q'): 
            print("Quitting")
            stop_program = True

threading.Thread(target=listen_for_quit).start()

desktopIconCount = len(os.listdir('C:/Users/Public/Desktop')) + len(os.listdir(f"{Path.home()}/Desktop")) - 1
screenSize = pyautogui.size()
screenSize = (screenSize[0], screenSize[1]-80)
iconWidth = screenSize[0]/25
iconHeight = screenSize[1]/10

grid = [[0 for _ in range(25)] for _ in range(10)]

print(f"Amount of Icons: {desktopIconCount}")
print(f"Screen size: (x:{screenSize[0]}, y:{screenSize[1]})")
for i in range(desktopIconCount):
    x, y = i // 10, i % 10
    grid[y][x] = 1

for row in grid: print(row)

def MoveIcon(location:tuple, destination:tuple, type:int=1):
    lx, ly = location
    dx, dy = destination
    if grid[ly][lx] != 0:
        grid[ly][lx] = 0
        grid[dy][dx] = type
        pyautogui.mouseDown(lx*iconWidth+iconWidth/2, ly*iconHeight+iconHeight/4)
        pyautogui.moveTo(dx*iconWidth+iconWidth/2, dy*iconHeight+iconHeight/4)
        pyautogui.mouseUp()
    else:
        print(f"Icon not in location!  x:{lx} y:{ly}")

# for y, row in enumerate(grid):
#     for x, tile in enumerate(row):
#         pyautogui.moveTo(x*iconWidth+iconWidth/2, y*iconHeight+iconHeight/4)
#         time.sleep(0)

SnakeBody = []
direction = (-1, 0)

def Movement():
    global direction
    while True:
        if keyboard.is_pressed('w'):
            direction = (0, -1)
        if keyboard.is_pressed('a'):
            direction = (-1, 0)
        if keyboard.is_pressed('s'):
            direction = (0, 1)
        if keyboard.is_pressed('d'):
            direction = (1, 0)

threading.Thread(target=Movement).start()
applecount = desktopIconCount - 3
def placeApple():
    global applecount
    while True:
        applePos = (random.randint(desktopIconCount//10+1, 24), random.randint(0, 9))
        if applePos != SnakeBody:
            MoveIcon(((applecount+2)//10, (applecount+2)%10), applePos, 3) # add 2 because we take 2 away from the start
            applecount -= 1
            break

def Reset():
    newtile = False
    for dy, row in enumerate(grid):
        for dx, tile in enumerate(row):
            if dx <= desktopIconCount // 10 and dy <= desktopIconCount % 10:
                if tile == 0:
                    for ly, row in enumerate(grid):
                        for lx, tile in enumerate(row):
                            if tile == 2 or tile == 3:
                                time.sleep(0.1)
                                MoveIcon((lx, ly), (dx, dy))
                                newtile = True
                                break
                        if newtile:
                            newtile = False
                            break
    os._exit(1)

# Start Game
MoveIcon((0, 0), (23, 4), 2)
SnakeBody.append((23, 4))
MoveIcon((0, 1), (24, 4), 2)
SnakeBody.append((24, 4))
placeApple()

for row in grid: print(row)

while True: # GAME LOOP
    time.sleep(0.1)
    print(SnakeBody)
    snakeHeadPos = SnakeBody[0]
    newSnakeHeadPos = (snakeHeadPos[0] + direction[0], snakeHeadPos[1] + direction[1])
    if grid[newSnakeHeadPos[1]][newSnakeHeadPos[0]] == 3: # If the tile is a fruit
        SnakeBody.insert(0, newSnakeHeadPos)
        grid[newSnakeHeadPos[1]][newSnakeHeadPos[0]] = 2
        placeApple()
    elif grid[newSnakeHeadPos[1]][newSnakeHeadPos[0]] == 2: # If you hit yourself
        print("You died")
        Reset()
    else:
        MoveIcon(SnakeBody[-1], newSnakeHeadPos, 2)
        SnakeBody.pop(-1)
        SnakeBody.insert(0, newSnakeHeadPos)
    if stop_program:
        Reset()
    

Reset()