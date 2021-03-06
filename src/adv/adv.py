#Standard Library
# import sys
import re
import textwrap
#Custom Modules
from room import Room
from roomList import rooms
from player import Player
import itemList
import npclist

# ________VARIABLES________
div = "________________________________"
playing = True


#________FUNCTIONS________
def playerAction(action):
    try:  
        global player
        global playing
        # check for N, S, E, or W, then move the player that direction
        if action == 'score':
            print('Current Score: ' + str(player.score))
        elif re.match(r'[n|N]', action):
            if hasattr(player.loc, 'n_to'):
                player.loc = player.loc.n_to
            else:
                print("You cannot go that way.")
        elif re.match(r'[s|S]', action):
            if hasattr(player.loc, 's_to'):
                player.loc = player.loc.s_to
            else:
                print("You cannot go that way.")
        elif re.match(r'[e|E]', action):
            if hasattr(player.loc, 'e_to'):
                player.loc = player.loc.e_to
            else:
                print("You cannot go that way.")
        elif re.match(r'[w|W]', action):
            if hasattr(player.loc, 'w_to'):
                player.loc = player.loc.w_to
            else:
                print("You cannot go that way.")
        elif re.match(r'[i|I]', action): # Print the inventory
            print(div)
            print("\nINVENTORY")
            for item in player.playerInv:
                print('\n' + item.name + ':')
                prettify = textwrap.wrap(item.description, width=100)
                for line in prettify:
                    print(line)
        elif re.match(r'[f|F]', action): # Print the inventory
            print(div)
            print("\nFOLLOWERS")
            for follower in player.followers:
                print('\n' + follower.name + ':')
                prettify = textwrap.wrap(follower.description, width=100)
                for line in prettify:
                    print(line)
        elif re.match(r'[h|H]', action):
            print("""
            Move North:  N, North, go North (change North to the direction you want to go in)
            Look Item:  Look <item name> (if it's not in your inventory)
            Take Item:  Take <item name>, Get <item name>
            Give Item:  Give <item name>
            Drop Item:  Drop <item name>
            Inventory:  I, Inventory
            Followers:  F, Followers
            Quit Game:  Q, Quit
            """)
        elif re.match(r'[q|Q]', action):  # Quit the game
            playing = False
    except:  # if a bad command was given, let the player know
        print("You have entered an unknown action.\n\n")
        print(div)
    return

def defeatMobs():
    global player
    for mob in player.loc.mobs:
        mob.vanquished = True
    # Change room description to show mobs defeated
    player.loc.description = player.loc.nextDesc
    # open up the paths
    if hasattr(player.loc, 'block_n_to'):
        player.loc.n_to = player.loc.block_n_to
    if hasattr(player.loc, 'block_s_to'):
        player.loc.s_to = player.loc.block_s_to
    if hasattr(player.loc, 'block_e_to'):
        player.loc.e_to = player.loc.block_e_to
    if hasattr(player.loc, 'block_w_to'):
        player.loc.w_to = player.loc.block_w_to

def getFollower():
    global player
    player.loc.npc[0].following = True
    player.loc.description = player.loc.nextDesc
    player.followers.append(player.loc.npc.pop())




print("\n-->Enter 'help' if you need a list of commands.<--\n")

# ________CREATE PLAYER________
player = Player(rooms['field'], [itemList.excaliber, itemList.coconuts, itemList.hamster], [npclist.patsy])

# ________GAME LOOP________
while playing is True:
    print(player.loc.name) # Print the room name

    # Print the room description before requiredItem is used
    prettify = textwrap.wrap(player.loc.description, width=100)
    for line in prettify:
        print(line)

    if len(player.loc.roomInv) > 0: # Print room's inventory
        items = ''
        for item in player.loc.roomInv:
            items += item.name + ' '
        print("\nItems you see: " + items)
    
    if len(player.loc.npc) > 0: # Print room's inventory
        people = ''
        for person in player.loc.npc:
            people += person.name + ' '
        print("\nPeople you see: " + people)

    if hasattr(player.loc, 'mobs') and player.loc.itemUsed == False:
        print("\nAlas!  Somebody stands in your way!")
        print("THE SOMEBODY(S)")
        for mob in player.loc.mobs:
            prettify = textwrap.wrap(mob.description , width=100)
            print('' + mob.name + ':')
            for line in prettify:
                print(line)
        print('\n')

# * Waits for user input and decides what to do.
    action = input("\nWhat are you going to do? ")
    print(div)
    matchAction = re.match(r'(\w+)\s(\w+)', action)  # check for 2 or 3 words
    if matchAction:
        action = [matchAction.group(1), matchAction.group(2)] # set action as two word command (get/take ___, go ___, drop ___)
    else:
        if re.match(r'[s|S][c|C][o|O][r|R][e|E]', action):
            action = 'score'
        else:
            action = action[0] # check for direction fully spelled(eg. north), and set action as single character command (n, s, e, w)
#
# If the user enters a cardinal direction, attempt to move to the room there.
    if action == 'score':
        playerAction(action)
    elif len(action) == 1:
        playerAction(action[0])
        print(div)
    elif len(action) == 2:
        try:
            if re.match(r'[g|G][e|E][t|T]|[t|T][a|A][k|K][e|E]', action[0]): # check for "get" or "take"
                for item in player.loc.roomInv:
                    if action[1].lower() == item.name.lower():
                        player.loc.roomInv.remove(item)
                        player.playerInv.append(item)
                        if hasattr(item, 'value'):
                            if item.scored == False:
                                item.scored = True
                                player.score += item.value
                        print("\nYou picked up the " + item.name.lower() + '\n')  # confirm that the player picked up this item by name
                        print(div)
                        found = True
                if found == False or found == None:
                    print("You don't see any of those here.")
                found = False
            if re.match(r'[g|G][o|O]', action[0]):  # check for "go"
                playerAction(action[1][0])  #move the player N, S, E, or W
                print(div)
            if re.match(r'[d|D][r|R][o|O][p|P]', action[0]): # check for "drop"
                if re.match(r'[i|I][t|T]', action[1]): # check for "it"
                    item = player.playerInv.pop() # remove the last item
                    player.loc.roomInv.append(item) # add that item to this room
                    print('\nYou have dropped the ' + item.name) # confirm with player that they dropped the item
                else:
                    confirmItem = False # used to check inventory
                    for item in player.playerInv:
                        if action[1].lower() == item.name.lower(): # compare command with inventory
                            confirmItem = True # if not confirmed, they don't have it to drop it
                            player.playerInv.remove(item) # remove from player
                            player.loc.roomInv.append(item) # add to room
                            print('\nYou have dropped the ' + item.name) # tell player what item they dropped
                            break # end the loop, so you only drop one
                    if confirmItem == False: # if the item was never dropped, tell them they don't have it.
                        print('\nYou do not have one of those.\n')
                print(div)
            if re.match(r'[u|U][s|S][e|E]', action[0]):
                confirmItem = False # used to check inventory
                for item in player.playerInv:
                    if action[1].lower() == item.name.lower(): # compare command with inventory
                        confirmItem = True # if not confirmed, they don't have it to drop it
                        itemToUse = item
                if confirmItem == True:
                    if itemToUse == player.loc.itemRequired[0]:
                        print("\nYou use " + itemToUse.name + ".")
                        defeatMobs()
                        player.loc.itemUsed = True
                        print(div)
                    else:
                        print("\nYou wave " + itemToUse.name + " around.  ...  wooooo...\n")
                        print(div)
                else:
                    print("You're a loony.  You can't use an item unless you first have it.")
                    print(div)

            if re.match(r'[g|G][i|I][v|V][e|E]', action[0]):
                confirmItem = False # used to check inventory
                for item in player.playerInv:
                    if action[1].lower() == item.name.lower(): # compare command with inventory
                        confirmItem = True # if not confirmed, they don't have it to drop it
                        itemToUse = item
                if confirmItem == True:
                    if itemToUse == player.loc.itemRequired[0]:
                        print("\nYou give the " + itemToUse.name + ".")
                        getFollower()
                        player.loc.itemUsed = True
                        print(div)
                    else:
                        print("\nYou wave " + itemToUse.name + " around.  ...  wooooo...\n")
                        print(div)
                else:
                    print("You're a loony.  You can't use an item unless you first have it.")
                    print(div)
                
            if re.match(r'[l|L][o|O][o|O][k|K]', action[0]):
                found = False
                for item in player.loc.roomInv:
                    if action[1].lower() == item.name.lower():
                        print('\n' + item.name + ':')
                        prettify = textwrap.wrap(item.description, width=100)
                        for line in prettify:
                            print(line)
                        print(div)
                        found = True
                if found == False or found == None:
                    print("\nYou don't see any of those here.\n")
                found = False
        except:
            print("\nYou have entered an unknown action.\n")