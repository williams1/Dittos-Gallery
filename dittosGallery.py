'''
This software was created to generate random pokemon for use with the PokeRole 2.0 Role Playing Game
This software queries accompanying files that could potentially be edited by anyone.
It is advised that you only use files supplied from a trusted source. The user assumes all risk.
'''
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import os.path
import pathlib
import imposter
import pokedex

############
#handle file structure stuff
tmpFileDir = pathlib.Path(__file__).parent.resolve()
fileDir = os.getcwd() #set =str(tmpFileDir) when working from terminal
dirSplit = str(tmpFileDir).split(os.path.split(tmpFileDir)[1])[0][-1]
###########

###########
#gui parameters
mainWindow = tk.Tk()
mainWindow.title("Ditto's Gallery")
mainWindow.geometry('1030x350') #set size of main window
icon = tk.PhotoImage(file = str(tmpFileDir)+dirSplit+'icon.png')
mainWindow.iconphoto(True,icon)
###########

###########
# menu
menubar = tk.Menu(mainWindow)
help = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label='Help', menu = help)
help.add_command(label= 'Using this program', command= pokedex.readme)#open readme
help.add_command(label= 'Complete the pokedex', command= pokedex.contribute)
#help.add_command(label= 'About', command= None)#open creation, license info
help.add_command(label= 'Exit', command= mainWindow.destroy)
mainWindow.config(menu = menubar)
###########

###########
#some labels we'll use later
regions = ['Avoid Base', 'Alola', 'Galar'] #Avoid Base will not pick base variant if a selected regional variant is available
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
allowRank['Beginner'].set(1)
allowRank['Amateur'].set(1)
allowRank['Ace'].set(1)

dualTypeVar = tk.IntVar()
dualTypeVar.set(2) #default to non-forbidden

legendaryChance = tk.StringVar()
legendaryChance.set('0')
mythicalChance = tk.StringVar()
mythicalChance.set('0')
allowMega = tk.IntVar()
shinyChance = tk.StringVar()
shinyChance.set('1/8192')
alterChance = tk.StringVar()
alterChance.set('0')
alterKeepMoves = tk.IntVar()
numGen = tk.IntVar()
numGen.set(5)
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
rowsInRanks = 3
colsInRanks = math.ceil(len(ranks)/rowsInRanks)
maxEntryFieldsPerRow = 2
dualTypePerColumn = len(dualType)
dualTypeRows = math.ceil(len(dualType)/dualTypePerColumn)
dualTypeRadioColSpan = 2
entryFieldWidth = 10

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

tk.Label(mainWindow, text="Ranks allowed below default").grid(row=curRow, column=columnGroups[0], sticky= tk.NE)
ranksBelowDefault = tk.Spinbox(mainWindow, from_= 0, to= len(ranks)-1, repeatdelay= spinnerSpamDelay, width= entryFieldWidth)
ranksBelowDefault.grid(row=curRow, column=columnGroups[0]+1, sticky= tk.NW)
tk.Label(mainWindow, text="And above default").grid(row=curRow, column=columnGroups[0]+2, sticky= tk.NE)
ranksAboveDefault = tk.Spinbox(mainWindow, from_= 0, to= len(ranks)-1, repeatdelay= spinnerSpamDelay, width= entryFieldWidth)
ranksAboveDefault.grid(row=curRow, column=columnGroups[0]+3, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text= 'Legendary chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=legendaryChance, width= entryFieldWidth).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
tk.Label(mainWindow, text= 'Mythical chance').grid(row= curRow, column= columnGroups[0]+2, sticky= tk.NE)
tk.Entry(mainWindow, textvariable=mythicalChance, width= entryFieldWidth).grid(row= curRow, column= columnGroups[0]+3, sticky= tk.NW)
curRow += 1

tk.Label(mainWindow, text= 'Shiny chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=shinyChance, width= entryFieldWidth).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
ttk.Checkbutton(mainWindow, text = 'Mega evolutions allowed', variable = allowMega).grid(row= curRow, column= columnGroups[0]+2, columnspan= 2, sticky= tk.NW+tk.NE)
curRow += 1

tk.Label(mainWindow, text= 'Alter-Type chance').grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=alterChance, width= entryFieldWidth).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
ttk.Checkbutton(mainWindow, text = 'Lost type moves allowed', variable = alterKeepMoves).grid(row= curRow, column= columnGroups[0]+2, columnspan= 2, sticky= tk.NW+tk.NE)
curRow += 1

tk.Label(mainWindow, text="Number to generate").grid(row= curRow, column= columnGroups[0], sticky= tk.NE)
tk.Entry(mainWindow, textvariable=numGen, width= entryFieldWidth).grid(row= curRow, column= columnGroups[0]+1, sticky= tk.NW)
###########

###########
#generate them


def calculateChance(entry):
    if '/' in entry:
        num, denom = entry.split('/')
        num, denom = float(num), float(denom)
        if denom > 0.0000000001 and num > -0.0000000001:
            return num/denom, True
        else:
            return 0, False
    if ':' in entry:
        left, right = entry.split(':')
        left, right = float(left), float(right)
        if left > -0.0000000001 and (left+right) > 0.0000000001:
            return left/(left+right), True
        else:
            return 0, False
    try:
        entry = float(entry)
        if entry > -0.0000000001:
            return entry, True
        else:
            return 0, False
    except:
        return 0, False

    
def transform():
    #check for errors
    if dualTypeVar.get() == 1:
        numForced = 0
        for t in typesForced:
            numForced += typesForced[t].get()
        if numForced < 2:
            tk.messagebox.showerror(message='Cannot require dual types to have both types from Forced list if Forced list has less than two types.')
            return 0
    
    for t in typesForced:
        if typesForced[t].get() == 1 and typesForbidden[t].get() == 1:
            tk.messagebox.showerror(message=f'{t} cannot be both a Forced and Forbidden type.')
            return 0

    allForbidden = True
    for t in typesForbidden:
        if typesForbidden[t].get() == 0:
            allForbidden = False
            break
    if allForbidden:
        tk.messagebox.showerror(message='Cannot generate a pokemon if all types are forbidden.')
        return 0
    
    noRanks = True
    for r in allowRank:
        if allowRank[r].get() == 1:
            noRanks = False
            break
    if noRanks:
        tk.messagebox.showerror(message=f'There must be at least one allowed Rank of pokemon.')
        return 0

    legend, success = calculateChance(legendaryChance.get())
    if not success:
        tk.messagebox.showerror(message='Legendary Chance is not in a valid format. Check the ReadMe for details.')
        return 0
    mythical, success = calculateChance(mythicalChance.get())
    if not success:
        tk.messagebox.showerror(message='Mythical Chance is not in a valid format. Check the ReadMe for details.')
        return 0
    alter, success = calculateChance(alterChance.get())
    if not success:
        tk.messagebox.showerror(message='Alter Type Chance is not in a valid format. Check the ReadMe for details.')
        return 0
    shiny, success = calculateChance(shinyChance.get())
    if not success:
        tk.messagebox.showerror(message='Shiny Chance is not in a valid format. Check the ReadMe for details.')
        return 0

    #build rankVar
    rankVar = [i for i in range(-int(ranksBelowDefault.get()), int(ranksAboveDefault.get())+1)]

    #find name for output file
    outFile = fileDir+dirSplit+'Generated_Pokemon'
    if os.path.exists(outFile+'.txt'):
        index = 1
        while os.path.exists(outFile+str(index)+'.txt'):
            index += 1
        outFile += str(index)
    outFile += '.txt'

    try:
        for _ in range(numGen.get()):
            entry = imposter.choosePokemon(typesForced, typesForbidden, dualTypeVar.get(), legend, mythical, allowMega.get(), shiny, alter , alterKeepMoves.get(), allowRank, rankVar, regionalVariants, ranks, types)
            if entry == 0:
                with open(outFile, 'a') as ofile:
                    ofile.write('Ditto had trouble finding things that matched your parameters. You may need to expand the data files- see "Complete the pokedex" under the Help menu for more details.')
                break
            with open(outFile, 'a') as ofile:
                ofile.write(entry)

        tk.messagebox.showinfo(message=f'Ditto is done picking transformations and wrote them all to {outFile}.')
    except:
        tk.messagebox.showerror(message='Ditto fainted after getting into a harden match with a Metapod!\n\nYou encountered a bug during generation. Please inform the developer of the settings and data files you were using when you got this message.')

    return 0

tk.Button(mainWindow, text="Generate Pokemon!", command= transform).grid(row= mainWinRows-1, column= mainWinCols//2, columnspan= 2)


mainWindow.mainloop() #run the loop that triggers the window