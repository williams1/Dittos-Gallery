import pandas as pd
import tkinter


types = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']

regions = ['Alola', 'Galar']
ranks = ['Starter', 'Beginner', 'Amateur', 'Ace', 'Professional', 'Master', 'Champion']

rankBounds = [1,1] #max ranks below suggested, max ranks above suggested
#gui
window = tkinter.Tk()
window.title("Ditto's Gallery")

window.geometry('800x300') #set size of main window

#message box stuff


window.mainloop() #run the loop that triggers the window