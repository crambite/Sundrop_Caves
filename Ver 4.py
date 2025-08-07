from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)



class map:
    # This function loads a map structure (a nested list) from a file
    # It also updates MAP_WIDTH and MAP_HEIGHT
    def load_map(filename, map_struct):
        map_file = open(filename, 'r')
        global MAP_WIDTH
        global MAP_HEIGHT
        
        map_struct.clear()
        
        # TODO: Add your map loading code here
        map = map_file.readlines()
        temp_y = []

        #stores map into map_struct
        for y in map:

            
            for x in y:

                #removes the \n and adds the current x to a temporary list for appending later
                temp_y += [x.strip("\n")]
            
            #adds current row into map_struct
            map_struct.append(temp_y)

            #resets the temporary list
            temp_y = []

        #Stores width and height of map into their repective global variables
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)
        map_file.close()

    # This function loads the fog of war
    def initialise_fog(fog):

        #num of ys
        for coord_y in range(MAP_HEIGHT):

            #temporary list to store current y of fog
            fog_y = []

            #xs in current y
            for coord_x in range(MAP_WIDTH):
                fog_y += ["?"]

            #stores current y of fog into fog
            fog.append(fog_y)
            

    # This function clears the fog of war around the player
    def clear_fog(fog, player):
        y = player["y"]
        x = player["x"]

        #rows
        for coord_y in range(-1, 2):

            #columns
            for coord_x in range(-1, 2):
                view_y = y + coord_y
                view_x = x + coord_x
                if not(view_y < 0 or view_y > MAP_HEIGHT - 1 or view_x < 0 or view_x >MAP_WIDTH - 1):
                    fog[view_y][view_x] = ""
        return fog

    
    # This function draws the entire map, covered by the fof
    def draw_map(game_map, fog, player):
        
        #y coordinate
        for coord_y, y in enumerate(game_map):

            #x coordinate
            for coord_x, x in enumerate(y):

                #checks player's current coordinates and draws it on the map
                if coord_y == player["y"] and coord_x == player["x"]:
                    print("M", end = "")
                
                #checks for portal and draws it
                elif coord_y == player["portal_y"] and coord_x == player["portal_x"] and player["portal_y"] != 0 and player["portal_x"] != 0:
                    print("P", end="")

                #checks if fog of war has been cleared and replaces it with the actual map
                elif fog[coord_y][coord_x] == "": 
                    print(x, end = "")

                #draws the fog of war
                else:
                    print("?", end = "")

                #allows code to print next rows
                if coord_x == MAP_WIDTH - 1:
                    print("\n", end = "")

class self:
    # This function shows the information for the player
    def show_information(player):
        return
                
    # This function moves the player
    def move_player(player, action):
        max_steps = player["turns"]
        steps = player["steps"]
        load = player["load"]
        max_load = player["max_load"]

        #check if player has used max num of steps and at max load
        if steps < max_steps and load < max_load:
            #up
            if action.upper() == "W" and player["y"] > 0:
                player["y"] = player["y"] - 1

            #down
            elif action.upper() == "S" and player["y"] < MAP_HEIGHT - 1:
                player["y"] = player["y"] + 1

            #left
            elif action.upper() == "A" and player["x"] > 0:
                player["x"] = player["x"] - 1
            
            #right
            elif action.upper() == "D" and player["x"] < MAP_WIDTH - 1:
                player["x"] = player["x"] + 1
        
            #adding to total number of steps
            player["steps"] = player["steps"] + 1
            player["total_steps"] = player["total_steps"] + 1
                
    # This function draws the viewport
    ###change the integer values to a variable for different view ranges
    def draw_view(game_map, fog, player):
        y = player["y"]
        x = player["x"]

        #border
        print("+", end = "")
        print("-" * 3, end = "")
        print("+")

        #rows
        for coord_y in range(-1, 2):
            print("|", end = "")

            #columns
            for coord_x in range(-1, 2):
                view_y = y + coord_y
                view_x = x + coord_x

                #boundary check
                if view_y < 0 or view_y > MAP_HEIGHT - 1 or view_x < 0 or view_x >MAP_WIDTH - 1:
                    print("#", end = "")
                
                #checking for middle of viewport and printing player
                elif coord_y == 0 and coord_x == 0:
                    print("M", end="")  

                #printing rest of viewport
                else:
                    print(game_map[view_y][view_x], end="")
            print("|")

        #border
        print("+", end = "")
        print("-" * 3, end = "")
        print("+")

        #clear fog
        map.clear_fog(fog, player)
        return fog
    
    # This function lets the player mine the ore
    def mine_ore(game_map, player):

        #player coordinates
        x_coord = player["x"]
        y_coord = player["y"]

        current_ore = game_map[y_coord][x_coord].upper()

        #check what ore it is and addig it to inventory
        #copper
        if current_ore == "C":
            copper = randint(1, 5)

            #enough storage
            if player["load"] + copper <= 10:
                player["copper"] = player["copper"] + copper
                player["load"] = player["load"] + copper

            #not enough storage
            else:
                player["copper"] = player["copper"] + (player["load"] - player["copper"])
                player["load"] = 10
        
        #silver
        elif current_ore == "S":
            silver = randint(1, 3)

            #enough storage
            if player["load"] + silver <= 10:
                player["silver"] = player["silver"] + silver
                player["load"] = player["load"] + silver

            #not enough storage
            else:
                player["silver"] = player["silver"] + (player["load"] - player["silver"])
                player["load"] = 10

        #gold
        elif current_ore == "G":
            gold = randint(1, 2)
            
            #enough storage
            if player["load"] + gold <= 10:
                player["gold"] = player["gold"] + gold
                player["load"] = player["load"] + gold
            
            #not enough storage
            else:
                player["gold"] = player["gold"] + (player["load"] - player["gold"])
                player["load"] = 10

        #removing ore from map
        game_map[y_coord][x_coord] = " "

        return game_map
    
    # This function sells the player's ore
    def sell_ore(player):

        #sell price for each ore
        copper_price = player["copper"] * randint(1, 3)
        silver_price = player["silver"] * randint(5, 8)
        gold_price = player["gold"] * randint(10, 18)

        #selling ore and adding to player GP
        player["GP"] = player["GP"] + copper_price + silver_price + gold_price

        #printing sell message
        #copper
        if copper_price > 0:
            print(f"You sell {player["copper"]} copper ore for {copper_price} GP.")

        #silver
        if silver_price > 0:
            print(f"You sell {player["silver"]} silver ore for {silver_price} GP.")

        #gold
        if gold_price > 0:
            print(f"You sell {player["gold"]} gold ore for {gold_price} GP.")

        #total GP
        if player["GP"] > 0 and (copper_price > 0 or silver_price > 0 or gold_price > 0):
            print(f"You now have {player["GP"]} GP!")

        #setting player's ore back to 0
        player["copper"] = 0
        player["silver"] = 0
        player["gold"] = 0

        #setting player's load back to 0
        player["load"] = 0
        
    # This function teleports the player back to town and makes it the next day when player uses portal stone
    def portal(player):

        #portal location
        player["portal_x"] = player["x"]
        player["portal_y"] = player["y"]

        #reset player location
        player["x"] = 0
        player["y"] = 0

        #reset player steps
        player["steps"] = 0 

        #next day
        player["day"] += 1

        print("You place your portal stone here and zap back to town.")
    
    '''#this function upgrades the player's bag
    def bag_upgrade(player):
'''

class game:
    def initialize_game(game_map, fog, player):
        # initialize map
        map.load_map("level1.txt", game_map)

        # TODO: initialize fog
        map.initialise_fog(fog)

        # TODO: initialize player
        #   You will probably add other entries into the player dictionary

        player["name"] = ""
        player['x'] = 0
        player['y'] = 0
        player['copper'] = 0
        player['silver'] = 0
        player['gold'] = 0
        player["load"] = 0
        player["max_load"] = 10
        player['GP'] = 0
        player['day'] = 1
        player['steps'] = 0
        player["total_steps"] = 0
        player['turns'] = TURNS_PER_DAY
        player["portal_x"] = 0
        player["portal_y"] = 0

        map.clear_fog(fog, player)

    # This function saves the game
    def save_game(game_map, fog, player):

        #save game into a txt file
        file_name = "save_file"
        with open(file_name, 'w') as save_file:

            # save map
            save_file.write(game_map)

            # save fog
            save_file.write(fog)

            # save player
            save_file.write(player) 

        return
    
    '''# This function loads the game
    def load_game(game_map, fog, player):

        #openeing the save file
        file_name = "save_file"
        with open(file_name, 'w') as save_file:
            save_file.readlines()

            # load map
            game_map.append
            # load fog
            # load player
        return'''

    def show_main_menu():
        print()
        print("--- Main Menu ----")
        print("(N)ew game")
        print("(L)oad saved game")
        #print("(H)igh scores")
        print("(Q)uit")
        print("------------------")

    def show_town_menu():
        print()

        # TODO: Show Day
        global player
        print(f"DAY {player["day"]}")

        print("----- Sundrop Town -----")
        print("(B)uy stuff")
        print("See Player (I)nformation")
        print("See Mine (M)ap")
        print("(E)nter mine")
        print("Sa(V)e game")
        print("(Q)uit to main menu")
        print("------------------------")

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
is_running = True

print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!

game.initialize_game(game_map, fog, player)
while is_running:

    #main menu
    while game_state == "main":
        game.show_main_menu()

        #error catching
        try:
            choice = input("Your choice? ").upper().strip()

            #raising error if input is blank
            if not choice:
                raise ValueError("Input cannot be empty")
            
            #raising error if input is not within given actions
            if choice.upper() not in "NLQ":
                raise KeyError("Invalid choice input")

        #catches the keyerror and prints the error 
        except (ValueError, KeyError) as error:
            print(f"Error: {error}")
            continue

        #quit game
        if choice == "Q":
            is_running = False
            game_state = "exit"
            break

        #load game
        elif choice == "L":
            None

        #new game
        else:
            player["name"] = input("Greetings, miner! What is your name? ")
            print(f"Pleased to meet you, {player["name"]}. Welcome to Sundrop Town!")

        game_state = "town"
        break   

    #exits the game
    if is_running == False:
        break

    #town menu
    while game_state == "town":

        #selling ore
        self.sell_ore(player)
        
        #printing town menu
        game.show_town_menu()

        #error catching
        try:
            choice = input("Your choice? ").upper().strip()

            #raising error if input is blank
            if not choice:
                raise ValueError("Input cannot be empty")

            #raising error if input is not within given actions
            if choice not in "BIMEVQ":
                raise KeyError("Invalid choice input")

        #catches the keyerror and prints the error 
        except (ValueError, KeyError) as error:
            print(f"Error: {error}")
            continue

        #buy menu
        if choice == "B":
            None
        
        #information menu
        elif choice == "I":
            print(f'''----- Player Information -----
Name: {player["name"]}
Portal position: ({player["portal_x"]}, {player["portal_y"]})
Pickaxe level: 1 (copper)
------------------------------
Load: {player["load"]} / {player["max_load"]}
------------------------------
GP: {player["GP"]}
Steps taken: {player["total_steps"]}
------------------------------''')
        
        #show map
        elif choice == "M":
            map.draw_map(game_map, fog, player)
            continue

        #enter mine
        elif choice == "E":
            print(f'''---------------------------------------------------
                     DAY {player["day"]}
---------------------------------------------------
''')
            #putting player at portal location if player placed portal
            player["x"] = player["portal_x"]
            player["y"] = player["portal_y"]

            #resetting portal position
            player["portal_x"] = 0
            player["portal_y"] = 0
            print(player["portal_x"], player["portal_y"])

            game_state = "exit"
            break

        #save game
        elif choice == "V":
            game.save_game(game_map, fog, player)

        #return to main menu
        else:
            game_state = "main"
            break

    #quit to main menu
    if game_state == "main":
        continue

    #displaying current day
    print(f"DAY {player["day"]}")

    #drawing player viewport
    self.draw_view(game_map, fog, player)
    
    #error catching 
    try:

        #input action
        action = input(f'''Turns left: {player["turns"] - player["steps"]}  Load: {player["load"]} / {player["max_load"]}   Steps: {player["total_steps"]}
(WASD) to move
(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu
Action? ''').upper().strip()
        
         #raising error if input is blank
        if not action:
            raise ValueError("Input cannot be empty")
        
        #raising error if input is not within given actions
        if action not in "WASDMIPQ":
            raise KeyError("Invalid action input")
    
    #catches the keyerror and prints the error
    except (ValueError, KeyError) as error:
            print(f"Error: {error}")
            continue
        
    #if player runs out of steps or storage
    if player["turns"] - player["steps"] == 1 or player["load"] == player["max_load"]:

        #checks if player has reached max num of steps
        if player["turns"] - player["steps"] == 1:

            self.move_player(player, action)
            self.mine_ore(game_map, player)
            print("You are exhausted.")

        #checks if player is at max load
        if player["load"] == player["max_load"]:
            print("You can't carry any more, so you can't go that way.")

        #warping back to town
        game_state = "town"
        self.portal(player)
        continue

    #player movement
    if action in "WASD":
        self.move_player(player, action) 

        #check if player returned to town
        if player["x"] == 0 and player["y"] == 0:
            game_state = "town"

    #map
    elif action == "M":
        map.draw_map(game_map,fog,player)

    #portal
    elif action == "P":
        game_state = "town"
        self.portal(player)
        continue

    #information
    elif action == "I":
            print(f'''----- Player Information -----
Name: {player["name"]}
Portal position: ({player["portal_x"]}, {player["portal_y"]})
Pickaxe level: 1 (copper)
------------------------------
Load: {player["load"]} / {player["max_load"]}
------------------------------
GP: {player["GP"]}
Steps taken: {player["total_steps"]}
------------------------------''')
            
    #quitting to main menu
    elif action == "Q":
        game_state = "main"
        continue
    
    #mining ore
    self.mine_ore(game_map, player)
