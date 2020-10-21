import tkinter as tk
from gui_manager import GuiManager
root = tk.Tk()           
    
root.title('A* algorithm')
guiManager = GuiManager(root)
guiManager.start()
root.mainloop()