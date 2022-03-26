#the mechanics behind the generator
import numpy as np
import pandas as pd
import os
import pathlib
import random


#############
#fileDir = pathlib.Path(__file__).parent.resolve()
fileDir = os.getcwd() #set =str(tmpFileDir) when working from terminal
dirSplit = fileDir.split(os.path.split(fileDir)[1])[0][-1]
tmpFileDir = pathlib.Path(__file__).parent.resolve()
fileDir = os.getcwd() #set =str(tmpFileDir) when working from terminal
dirSplit = str(tmpFileDir).split(os.path.split(tmpFileDir)[1])[0][-1]

if not os.path.isdir(fileDir+dirSplit+'data'):
    os.mkdir(fileDir+dirSplit+'data')
    for dfile in ['abilities.csv','attacks.csv','pokemon.csv']:
        with open(str(tmpFileDir)+dirSplit+'data'+dirSplit+dfile,'r') as ifile:
            data = ifile.read()
        with open(fileDir+dirSplit+'data'+dirSplit+dfile,'w') as ofile:
            ofile.write(data)
############

#gather data
def fileData(f):
    fileName = fileDir+dirSplit+'data'+dirSplit+f
    with open(fileName) as g:
        enc = g.encoding
    return fileName, enc

fileName, enc = fileData('abilities.csv')
abilities = pd.read_csv(fileName, encoding=enc)
fileName, enc = fileData('attacks.csv')
attacks = pd.read_csv(fileName, encoding=enc)
fileName, enc = fileData('pokemon.csv')
pokemon = pd.read_csv(fileName, encoding=enc)
attributeNames = ['Strength', 'Dexterity', 'Vitality', 'Special', 'Insight']
skillNames = ['Brawl', 'Channel', 'Clash', 'Evasion', 'Alert', 'Athletic', 'Nature', 'Stealth', 'Allure', 'Etiquette', 'Intimidation', 'Perform']

allDFs= [abilities, attacks, pokemon]


#makes a list of all entries in dictionary that have entry that evaluates to true
def listBuilder(dictionary):
    out = []
    for i in dictionary:
        if dictionary[i].get():
            out.append(i)

    return out


def weightedChoice(weights):
    var = sum(weights)
    var = random.randrange(var)
    temp = weights[0]
    index = 0
    while temp < var:
        index += 1
        temp += weights[index]

    return index

#set all data entries to allow
def refreshGallery(entry= 'allow', frames= allDFs):
    for df in frames:
        df[entry] = True


def chooseRank(creature, ranksAllowed, rankVar, numRanks):
    rank = -1
    index = -1
    rankWeights = [((numRanks**2)+1)-(r**2) for r in rankVar] #weight choices, closer to default rank is more likely
    while rank not in ranksAllowed:
        #make sure we didn't somehow get in an impossible situation
        if len(rankVar) == 0:
            raise RuntimeError('Bug encountered in selecting Pokemon rank.')
        #if we choose a rankVar that didn't work, remove it so we don't pick it again
        if index > -1:
            rankWeights.pop(index)
            rankVar.pop(index)
        #determine what rankVar to try next
        index = weightedChoice(rankWeights)
        #set rank
        rank = creature['Rank'] + rankVar[index]
    
    return rank


def chooseAbility(creature):
    abilities = creature['Ability']
    abSplit = abilities.split('/')

    return abSplit[random.randrange(len(abSplit))]


def chooseStats(creature, rank):
    current = []
    possibleRemaining = []

    for stat in attributeNames:
        nums = creature[stat]
        current.append( int(nums.split('-')[0]) )
        possibleRemaining.append( int(nums.split('-')[1]) )
    current = np.array(current)
    possibleRemaining = np.array(possibleRemaining)
    possibleRemaining -= current
    
    if rank > 5:
        possibleRemaining += np.array([2]*len(possibleRemaining))
    
    extraRanks = 2*min(rank,4)
    while extraRanks > 0:
        if (possibleRemaining == 0).all():#run into max stats before done adding ranks
            break
        weights = [3*w+min(w*c,c) for w, c in zip(possibleRemaining, current)] #favors raising skills far below max while also giving skills with a lot of points in them an edge
        index = weightedChoice(weights)
        current[index] += 1
        possibleRemaining[index] -= 1
        extraRanks -= 1

    if rank > 5:
        possibleRemaining -= np.array([2]*len(possibleRemaining))

    out = [str(c)+f' (max {c+p})' for c, p in zip(current, possibleRemaining)]
    return out


def chooseSkills(creature, rank, attributes):
    probFight = 0.5
    probSurvival = 0.25
    #probSocial = 1-probFight-probSurvival
    
    #category of skill and attribute that deterimines how much pokemon favors it
    influence = [{'cat':0, 'stat':0}, #brawl- fight, str
                {'cat':0, 'stat':3}, #channel- fight, spec
                {'cat':0, 'stat':2}, #clash- fight, vit
                {'cat':0, 'stat':1}, #evasion- fight, dex
                {'cat':1, 'stat':4}, #alert- surv, insight
                {'cat':1, 'stat':0}, #athletic- surv, str
                {'cat':1, 'stat':3}, #nature- surv, spec
                {'cat':1, 'stat':1}, #stealth- surv, dex
                {'cat':2, 'stat':3}, #allure- soc, spec
                {'cat':2, 'stat':4}, #etiquette- soc, insight
                {'cat':2, 'stat':0}, #intimidation- soc, str
                {'cat':2, 'stat':1}] #perform- soc, dex
    skills= [0]*12 

    stats = [ int(stat.split('(')[0]) for stat in attributes ]

    numSkillPts = [5,9,12,14,15,15,16][min(rank, 6)]
    maxRank = min(rank+1, 5)

    #get at least 1 point in favored attack/defense skills
    if stats[0] > stats[3] or (stats[0] == stats[3] and random.random()>0.5):
        skills[0] += 1
    else:
        skills[1] += 1
    if stats[1] > stats[2] or (stats[1] == stats[2] and random.random()>0.5):
        skills[3] += 1
    else:
        skills[2] += 1
    numSkillPts -= 2

    weights = [0]*12
    while numSkillPts > 0:
        #choose category of skill
        cat = random.random()
        if cat < probFight:
            cat = 0
        elif cat < probFight+probSurvival:
            cat = 1
        else:
            cat = 2

        #determine weights for skills in that category
        for i in range(12):
            if influence[i]['cat'] != cat or skills[i] == maxRank:
                weights[i] = 0
            else:
                weights[i] = 2*stats[influence[i]['stat']] + skills[i] # favor specializtion and things pokemon is good at
        
        #give skill point to a skill
        if max(weights) > 0: #make sure we didn't pick a maxed out category
            index = weightedChoice(weights)
            skills[index] += 1
            numSkillPts -= 1

    
    out = ''
    maxInLine = 5
    numInLine = 0
    for pts, name in zip(skills, skillNames):
        if pts > 0:
            numInLine +=1
            out += name + f' {pts}'
            if numInLine == maxInLine:
                out += ',\n\t'
                numInLine = 0
            else:
                out += ',  '
    if out[-1] == '\t':
        out = out[:-3]
    else:
        out = out[:-2]

    return out


def alterType(transform, forceTypes, forbidTypes, dualType, allTypes):
    forceOnly = False
    #choose which type to replace
    #--single type only
    if dualType == 0:
        lose = transform['Type 1']
        save = transform['Type 2']
        forceOnly = True
    #--pokemon needs to lose a forbidden type
    elif transform['Type 1'] in forbidTypes:
        lose = transform['Type 1']
        save = transform['Type 2']
        forceOnly =  transform['Type 2'] not in forceTypes
    elif transform['Type 2'] in forbidTypes:
        lose = transform['Type 2']
        save = transform['Type 1']
        forceOnly =  transform['Type 1'] not in forceTypes
    #--pokemon needs two forced types and only has one
    elif dualType == 1 and transform['Type 1'] not in forceTypes:
        lose = transform['Type 1']
        save = transform['Type 2']
        forceOnly = True
    elif dualType == 1 and transform['Type 2'] not in forceTypes:
        lose = transform['Type 2']
        save = transform['Type 1']
        forceOnly = True
    #doesn't matter which type is picked if we get this far
    else:
        #--pokemon doesn't have a forced type
        if transform['Type 1'] not in forceTypes and transform['Type 2'] not in forceTypes:
            forceOnly = True
        if random.random() < 0.5:
            lose = transform['Type 1']
            save = transform['Type 2']
        else:
            lose = transform['Type 2']
            save = transform['Type 1']

    forceOnly |= dualType == 1 #both types must be forced
    if forceOnly:
        repeat = True
        while repeat:
            newType = forceTypes[random.randrange(len(forceTypes))]
            repeat = (newType == lose) or (newType == save) #didn't get a new type
    else:
        repeat = True
        allowedTypes = [t for t in allTypes if t not in forbidTypes]
        while repeat:
            newType = allowedTypes[random.randrange(len(allowedTypes))]
            repeat = (newType == lose) or (newType == save) #didn't get a new type

    return newType, save, lose


def chooseMoves(creature, rank, attributes, type1, type2, allTypes, lostType = None, keepLostMoves = False):
    numMoves = int(attributes[4].split('(')[0])+2
    movesKnown = []
    probMatchType = 0.2 #if we don't roll this, we still might stumble on one
    probSwitchAlter = 0.7 #if we are allowed to keep moves of old type, what's the probability we switch to our altertype anyway
    probMonoToDualAlter = 0.3 #if alterTyping turned a mono-type into a dual-type, then this is chance to learn move of new typing on top of same type prob
    #if altertype, prep attacks table by gathering all known attacks of appropriate type
    if lostType:
        alterAttacks = attacks.drop( attacks.loc[(attacks.Type != type1)].index )

    #listOfMoves
    listOfMoves = creature.Moves
    listOfMoves = listOfMoves.split('/')
    listOfMoves = { 'Rank':[int(move.split(' ')[0]) for move in listOfMoves],
                    'Type':[move.split(' ')[1] for move in listOfMoves],
                    'Name':[move.split(move.split(' ')[0]+' '+move.split(' ')[1]+' ')[1] for move in listOfMoves],
                    'allow':[int(move.split(' ')[0])<= rank for move in listOfMoves]
                    }
    listOfMoves = pd.DataFrame(listOfMoves)
    listOfMoves = listOfMoves.drop( listOfMoves.loc[np.invert(listOfMoves.allow)].index )

    maxRankGrabbed = True
    remainingMaxRank = rank
    while numMoves > 0 and len(listOfMoves)>0:
        #check if move type is predetermined this round
        moveType = None
        if random.random() < probMatchType:
            if random.random() < 0.5 and type2 in allTypes:
                moveType = type2
            else:
                moveType = type1
        elif lostType and (lostType in allTypes) and random.random() < probMonoToDualAlter:
            moveType = type1
        
        #determine rank of move to learn next
        if maxRankGrabbed:
            for i in range(remainingMaxRank,-1,-1):
                if (listOfMoves.Rank == i).any():
                    remainingMaxRank = i
                    break
    
        weights = [3*r+1 for r in range(remainingMaxRank+1)]
        rankChoice = weightedChoice(weights)
        maxRankGrabbed = (rankChoice == remainingMaxRank)
        #pick a move
        if lostType and moveType == type1: #picked an altertype move, go find a random one
            selection, foundOne = pickMove(alterAttacks, rankChoice)
            if foundOne:
                alterAttacks.allow[selection['index']] = False
        elif lostType and lostType == moveType and (not keepLostMoves or random.random() < probSwitchAlter): #replace lost type move with alterType move
            selection, foundOne = pickMove(listOfMoves, rankChoice, moveType)
            if foundOne:
                temp = selection['index']
                selection, foundOne = pickMove(alterAttacks, rankChoice)
                if foundOne:
                    listOfMoves.allow[temp] = False
                    alterAttacks.allow[selection['index']] = False
        else:
            selection, foundOne = pickMove(listOfMoves, rankChoice, moveType)
            if foundOne:
                if lostType and not keepLostMoves and selection.Type == lostType: #make sure we didn't pick a forbidden type
                    temp = selection['index']
                    selection, foundOne = pickMove(alterAttacks, rankChoice)
                    if foundOne:
                        listOfMoves.allow[temp] = False
                        alterAttacks.allow[selection['index']] = False
                else:
                    listOfMoves.allow[selection['index']] = False

        #bookkeeping
        if foundOne:
            movesKnown.append(attacks.loc[attacks.loc[attacks.Name== selection.Name].index[0]])
            numMoves -= 1
            listOfMoves = listOfMoves.drop( listOfMoves.loc[np.invert(listOfMoves.allow)].index )

    return movesKnown

#helper function for chooseMoves        
def pickMove(listOfAttacks, rank, type= None):
    listOfAttacks['temp'] = listOfAttacks.allow
    listOfAttacks.temp &= (listOfAttacks.Rank == rank)
    if type:
        listOfAttacks.temp &= (listOfAttacks.Type != type)
    tempDf = listOfAttacks.drop( listOfAttacks.loc[np.invert(listOfAttacks.temp)].index )
    
    if len(tempDf) == 0:
        return False, False

    tempDf = tempDf.reset_index()
    selection = tempDf.loc[random.randrange(len(tempDf))]

    return selection, True


#choose which pokemon we grab
def choosePokemon(forceTypes, forbidTypes, dualType, legend, mythical, mega, shiny, alter, alterMove, ranks, rankVar, regions, allRanks, allTypes):
    #bookkeeping
    refreshGallery()
    forceTypes = listBuilder(forceTypes)
    forbidTypes = listBuilder(forbidTypes)
    regions = listBuilder(regions)
    try:
        regions.remove('Avoid Base')
    except:
        regions.append('Base-Y')
    regions.append('Base-N')
    ranks = listBuilder(ranks)
    for i in range(len(ranks)):
        ranks[i] = allRanks.index(ranks[i])
    ranks = np.array(ranks)
    
    #check if alter type or shiny
    alter = random.random() < alter
    shiny =  random.random() < shiny

    #manage force types
    if len(forceTypes) > 0:
        if dualType == 1 and not alter: #only look at pokemon with both types in force list
            pokemon['allow'] &= pokemon['Type 1'].isin(forceTypes)
            pokemon['temp'] = pokemon['Type 2'].isin(forceTypes)
            pokemon['temp'] |= pokemon['Type 2'].str.startswith('-') #allow single types still
            pokemon['allow'] &= pokemon['temp']
        elif dualType == 1 or not alter: #only look at pokemon with at least one type in force list
            pokemon['temp'] = pokemon['Type 1'].isin(forceTypes)
            pokemon['temp'] |= pokemon['Type 2'].isin(forceTypes)
            pokemon['allow'] &= pokemon['temp']
        #if altertype and don't require a dual type with both forced, then alter-typing can force the type

    #manage forbid types
    if len(forbidTypes) > 0:
        if alter: #if altertype, just make sure we can remove all forbidden types with the alteration
            pokemon['temp'] = pokemon['Type 1'].isin(forbidTypes)
            pokemon['temp'] &= pokemon['Type 2'].isin(forbidTypes)
            pokemon['allow'] &= np.invert(pokemon['temp'])
        else:
            pokemon['temp'] = pokemon['Type 1'].isin(forbidTypes)
            pokemon['temp'] |= pokemon['Type 2'].isin(forbidTypes)
            pokemon['allow'] &= np.invert(pokemon['temp'])

    #check if single-type only was chosen
    if dualType == 0:
        pokemon['allow'] &= (pokemon['Type 2'] == '-')

    #check if legendaries are allowed
    if random.random() > legend:
        pokemon['temp'] = pokemon['Legendary'].str.startswith('L')
        pokemon['allow'] &= np.invert(pokemon['temp'])

    #check if mythicals are allowed
    if random.random() > mythical:
        pokemon['temp'] = pokemon['Legendary'].str.startswith('M')
        pokemon['allow'] &= np.invert(pokemon['temp'])

    #check if mega evolutions are allowed
    if not mega:
        pokemon['temp'] = pokemon['Pokemon'].str.startswith('Mega ')
        pokemon['temp'] |= pokemon['Pokemon'].str.startswith('Mega-')
        pokemon['allow'] &= np.invert(pokemon['temp'])

    #check regional variants
    pokemon['allow'] &= pokemon['Region'].isin(regions)

    #check ranks
    pokemon['temp'] = False
    for var in rankVar:
        pokemon['temp'] |= pokemon['Rank'].isin(ranks-var)
    pokemon['allow'] &= pokemon['temp']
    
    #of all pokemon allowed, pick which one ditto chooses
    stillAllowed = pokemon.drop(pokemon[np.invert(pokemon.allow)].index)
    stillAllowed = stillAllowed.reset_index()
    transform = stillAllowed.loc[random.randrange(len(stillAllowed))]

    #fill out stats
    abilityKnown = chooseAbility(transform)
    actualRank = chooseRank(transform, ranks, rankVar, len(allRanks)) #still number
    attributes = chooseStats(transform, actualRank) #each one is string now, order str dex vit spec ins
    skillsKnown = chooseSkills(transform, actualRank, attributes) #outputs string to be printed
    if alter:
        type1, type2, lostType =  alterType(transform, forceTypes, forbidTypes, dualType, allTypes)
        if not alterMove:
            movesKnown = chooseMoves(transform, actualRank, attributes, type1, type2, allTypes, lostType, alterMove)
    else:
        type1, type2 = transform['Type 1'], transform['Type 2']
        movesKnown = chooseMoves(transform, actualRank, attributes, transform['Type 1'], transform['Type 2'], allTypes)

    #create entry for pokemon
    entry = writeEntry(transform, [type1, type2], actualRank, allRanks, abilityKnown, attributes, skillsKnown, movesKnown, shiny)
    return entry


def formatString(text, width=100, numTabs = 0):
    finalText = ''
    while len(text)>width:
        i= 0
        while text[width-i] != ' ':
            i += 1
        finalText += text[:width-i] + '\n' + '\t'*numTabs
        while text[width-i] == ' ':
            i -= 1
        text = text[width-i:]
    finalText += text

    return finalText

def writeEntry(creature, types, rank, allRanks, ability, attributes, skills, moves, shiny):
    entry = ''
    #shiny
    if shiny:
        entry += 'Shiny '
    #name, type, hp, will
    entry += creature.Pokemon + f"\nType: {types[0]}, {types[1]}\tHP: {creature.HP+int(attributes[2].split('(')[0])}\tWill: {2+int(attributes[4].split('(')[0])}\n"
    #rank and nature
    nature = ['Adamant', 'Bashful', 'Bold', 'Brave', 'Calm', 'Careful', 'Docile', 'Gentle', 'Hardy', 'Hasty', 'Impish', 'Jolly', 'Lax', 'Lonely', 'Mild', 'Modest', 'Naive', 'Naughty', 'Quiet', 'Quirky', 'Rash', 'Relaxed', 'Sassy', 'Serious', 'Timid']
    nature = nature[random.randrange(len(nature))]
    entry += f'Rank: {allRanks[rank]}\tNature: {nature}\n'
    #ability
    ability = abilities.loc[abilities.loc[abilities.Name == ability].index[0]]
    entry += f'Ability: {ability.Name}\n\t' 
    entry += formatString(f'{ability.Exploration}', numTabs = 1)+'\n\t'
    entry += formatString(f'{ability.Combat}', numTabs = 1)+'\n'
    #attributes
    entry += 'Attributes:\n\t'
    for name, level in zip(attributeNames, attributes):
        entry +=f'{name}: {level},  '
    entry = entry[:-3]+'\n'
    #skills
    entry += 'Skills:\n\t'+ skills + '\n'
    #moves
    entry += 'Moves:\n\t'
    for attack in moves:
        entry += f'Name: {attack.Name}\tType: {attack.Type}\n\t\t'
        entry += f"Attack Type: {attack['Attack Type']}\tAccuracy: {attack.Accuracy}\tDamage: {attack['Damage Pool']}"
        if ({attack['Damage Pool']} != '-') and (attack.Type in types):
            entry += '+1 (STAB)'
        entry += '\n\t\t'
        entry += formatString(f"{attack['Added Effect']}",numTabs=2)+'\n\t'
    entry += '\n\n'
    
    return entry