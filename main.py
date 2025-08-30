import os
from pathlib import Path

desktopIconCount = len(os.listdir('C:/Users/Public/Desktop')) + len(os.listdir(f"{Path.home()}/Desktop")) - 1

print(f"Amount of Icons: {desktopIconCount}")