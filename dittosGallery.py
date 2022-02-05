'''
Created by Robert Williams
date

This software was created to generate random pokemon for use with the PokeRole 2.0 Role Playing Game
This software queries accompanying files that could potentially be edited by anyone.
It is advised that you only use files supplied from a trusted source. The user assumes all risk.

This software is available under the GNU General Public License, Ver 3, 29 June 2007
'''
import pandas as pd
import tkinter as tk
from tkinter import ttk
import math
#from pokedex import *
#import imposter #pokemon generation functions

###########
#gui parameters
mainWindow = tk.Tk()
mainWindow.title("Ditto's Gallery")
mainWindow.geometry('1250x400') #set size of main window
icon = tk.PhotoImage(file = 'icon.png')
mainWindow.iconphoto(True,icon)
###########
'''
###########
# menu
menubar = tk.Menu(mainWindow)
help = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label='Help', menu = help)
help.add_command(label= 'Read Me', command= readme())#open readme
help.add_command(label= 'About', command= None)#open creation, license info
help.add_command(label= 'Exit', command= mainWindow.destroy)
mainWindow.config(menu = menubar)
###########
'''
###########
#some labels we'll use later
regions = ['Avoid Base','Alola', 'Galar'] #Avoid Base will not pick base variant if a selected regional variant is available
ranks = ['Starter', 'Beginner', 'Amateur', 'Ace', 'Professional', 'Master', 'Champion']
types = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
dualType = {"Single type Only": 0, "From forced list": 1, "Any non-forbidden": 2}
###########

###########
#variables for buttons here
typesForced = {}
typesForbidden = {}
for pkmnType in types:
    typesForced[pkmnType] = tk.IntVar()
    typesForbidden[pkmnType] = tk.IntVar()

regionalVariants = {}
for region in regions:
    regionalVariants[region] = tk.IntVar()

allowRank = {}
for rank in ranks:
    allowRank[rank] = tk.IntVar()

dualTypeVar = tk.IntVar()
dualTypeVar.set(2) #default to non-forbidden

legendaryChance = tk.StringVar()
mythicalChance = tk.StringVar()
allowMega = tk.IntVar()
shinyChance = tk.StringVar()
alterChance = tk.StringVar()
alterKeepMoves = tk.IntVar()
numGen = tk.StringVar()
numGen.set('5')
###########

###########
#make all the checkboxes here
typeForceButtons = []
typeForbidButtons = []
for pkmnType in types:
    typeForceButtons.append(
        ttk.Checkbutton(mainWindow,
            text = pkmnType,
            variable = typesForced[pkmnType],
        )
    )
    typeForbidButtons.append(
        ttk.Checkbutton(mainWindow,
            text = pkmnType,
            variable = typesForbidden[pkmnType],
        )
    )

regionalVariantButtons = []
for region in regions:
    regionalVariantButtons.append(
        ttk.Checkbutton(mainWindow,
            text = region,
            variable = regionalVariants[region],
        )
    )

rankAllowedButtons = []
for rank in ranks:
    rankAllowedButtons.append(
        ttk.Checkbutton(mainWindow,
            text = rank,
            variable = allowRank[rank],
        )
    )
##########

##########
#button options
spinnerSpamDelay = 200
#arrange buttons on gui
offSet = [1,1] #row buffer on [top,bottom]
typeBlocks = 2
rowsInTypes = 4
colsInTypes = math.ceil(len(types)/rowsInTypes)
rowsInRegions = 1
colsInRegions = math.ceil(len(regions)/rowsInRegions)
rowsInRanks = 2
colsInRanks = math.ceil(len(ranks)/rowsInRanks)
maxEntryFieldsPerRow = 2
dualTypePerColumn = len(dualType)
dualTypeRows = math.ceil(len(dualType)/dualTypePerColumn)
dualTypeRadioColSpan = 2

columnGroups = [max(colsInTypes+1, len(dualType)*dualTypeRadioColSpan+1), max(colsInRegions+1, colsInRanks+1,2*maxEntryFieldsPerRow)]
columnRows = [typeBlocks*rowsInTypes+dualTypeRows+dualTypeRows, sum([rowsInRegions, rowsInRanks, 5])]
mainWinCols = sum(columnGroups)
mainWinRows = max(columnRows)+sum(offSet)
mainWindow.columnconfigure(mainWinCols)
mainWindow.rowconfigure(mainWinRows)

#1st Column
curRow = offSet[0]

tk.Label(mainWindow, text="All pokemon must have").grid(row=curRow, column=0)
curRow += 1

tk.Label(mainWindow, text="One of the following types:").grid(row=curRow, column=0)
for index, button in zip(range(len(typeForceButtons)), typeForceButtons):
    button.grid(row = index//colsInTypes +curRow, column = index % colsInTypes +1, sticky= tk.NW, pady = 5, padx = 5)
curRow += rowsInTypes

tk.Label(mainWindow, text="None of the following types:").grid(row=curRow, column=0)
for index, button in zip(range(len(typeForbidButtons)), typeForbidButtons):
    button.grid(row = index//colsInTypes +curRow, column = index % colsInTypes +1, sticky= tk.NW, pady = 5, padx = 5)
curRow += rowsInTypes

tk.Label(mainWindow, text="Second type of dual types:").grid(row=curRow, column=0)
for index, (text, value) in zip(range(len(dualType)), dualType.items()):
    tk.Radiobutton(mainWindow, text= text, variable= dualTypeVar, value= value).grid(row= curRow+index//dualTypePerColumn, column= (index % dualTypePerColumn)*dualTypeRadioColSpan +1, columnspan=dualTypeRadioColSpan, pady = 5, padx = 5)
curRow += dualTypeRows

#2nd Column
curRow = offSet[0]+1 #looks better starting lower

tk.Label(mainWindow, text="Regional Variants Allowed:").grid(row=curRow, column=columnGroups[0])
for index, button in zip(range(len(regionalVariantButtons)), regionalVariantButtons):
    button.grid(row= index//colsInRegions +curRow, column = index % colsInRegions +columnGroups[0]+1, sticky= tk.NW, pady = 5, padx = 5)
curRow += rowsInRegions

tk.Label(mainWindow, text="Ranks Allowed:").grid(row=curRow, column=columnGroups[0])
for index, button in zip(range(len(rankAllowedButtons)), rankAllowedButtons):
    button.grid(row= index//colsInRanks +curRow, column = index % colsInRanks +columnGroups[0]+1, sticky= tk.NW, pady = 5, padx = 5)
curRow += rowsInRanks

tk.Label(mainWindow, text="Ranks below default allowed").grid(row=curRow, column=columnGroups[0], sticky= tk.NE)
ranksBelowDefault = tk.Spinbox(mainWindow, from_= 0, to= len(ranks)-1, repeatdelay= spinnerSpamDelay).grid(row=curRow, column=columnGroups[0]+1, sticky= tk.NW)
tk.Label(mainWindow, text="Ranks above default allowed").grid(row=curRow, column=columnGroups[0]+2, sticky= tk.NE)
ranksBelowDefault = tk.Spinbox(mainWindow, from_= 0, to= len(ranks)-1, repeatdelay= spinnerSpamDelay).grid(row=curRow, column=columnGroups[0]+3, sticky= tk.NW)
curRow += 1

ttk.Checkbutton(mainWindow, text = 'Mega evolutions allowed', variable = allowMega).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text= 'Legendary chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=legendaryChance).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
tk.Label(mainWindow, text= 'Mythical chance').grid(row= curRow, column= columnGroups[0]+2, sticky= tk.NE)
tk.Entry(mainWindow, textvariable=mythicalChance).grid(row= curRow, column= columnGroups[0]+3, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text= 'Shiny chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=shinyChance).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text= 'Alter-Type chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=alterChance).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
ttk.Checkbutton(mainWindow, text = 'Lost type moves allowed', variable = alterKeepMoves).grid(row= curRow, column= columnGroups[0]+2, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text="Number to generate").grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=numGen).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
###########

###########
#generate them

def placeholder():
    #replace me with the generator function
    return 0

tk.Button(mainWindow, text="Generate Pokemon!", command= placeholder()).grid(row= mainWinRows-1, column= mainWinCols//2, columnspan= 2)


mainWindow.mainloop() #run the loop that triggers the window