import os
from pathlib import Path
import pyautogui
import time
import random
import keyboard
import threading

def listen_for_quit():
    global stop_program
    while True:
        if keyboard.is_pressed('q'): 
            print("Quitting")
            os._exit(0)

threading.Thread(target=listen_for_quit, daemon=True).start()

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
    if grid[ly][lx] == 1:
        grid[ly][lx] = 0
        grid[dy][dx] = type
        pyautogui.mouseDown(lx*iconWidth+iconWidth/2, ly*iconHeight+iconHeight/4)
        pyautogui.mouseUp(dx*iconWidth+iconWidth/2, dy*iconHeight+iconHeight/4)
    else:
        print("Icon not in location!")

# for y, row in enumerate(grid):
#     for x, tile in enumerate(row):
#         pyautogui.moveTo(x*iconWidth+iconWidth/2, y*iconHeight+iconHeight/4)
#         time.sleep(0)

SnakeBody = []
direction = (-1, 0)

def Movement():
    global direction
    if keyboard.is_pressed('w'):
        direction = (0, -1)
    if keyboard.is_pressed('a'):
        direction = (-1, 0)
    if keyboard.is_pressed('s'):
        direction = (0, 1)
    if keyboard.is_pressed('d'):
        direction = (1, 0)

# Start Game
MoveIcon((0, 0), (23, 4), 2)
SnakeBody.append((23, 4))
MoveIcon((0, 1), (24, 4), 2)
SnakeBody.append((24, 4))
while True:
    applePos = (random.randint(desktopIconCount//10+1, 24), random.randint(0, 9))
    if applePos != SnakeBody:
        MoveIcon((0, 2), applePos, 3)
        break

for row in grid: print(row)