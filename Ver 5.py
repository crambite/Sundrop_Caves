from random import randint

player = {}
PLAYER_NAMES = ["name", "x", "y", "copper", "silver", "gold", "load", "max_load", "GP", "day", "steps","total_steps", "turns", "portal_x", "portal_y", "pickaxe_level", "torch_level"]
game_map = []
check_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}

pickaxe_levels = {1 : "C", 2 : "S", 3 : "G"}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

torch_levels = {1 : 3, 2 : 5, 3 : 7}


# This function loads a map structure (a nested list) from a file
class map:

    #error catching if file does not exist
    try:
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
    
    except:
        print("Error: It appears that you do not have a map.\n")

    # This function loads the fog of war
    def initialise_fog(fog):

        fog.clear()

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
                    fog[view_y][view_x] = " "
        return fog

    
    # This function draws the entire map, covered by the fof
    def draw_map(game_map, fog, player):

        print()

        #drawing border
        print("+", end = "")
        print("-" * MAP_WIDTH, end = "")
        print("+")
        
        #y coordinate
        for coord_y, y in enumerate(game_map):

           #drawing border
            print("|", end = "")

            #x coordinate
            for coord_x, x in enumerate(y):

                #checks player's current coordinates and draws it on the map
                if coord_y == player["y"] and coord_x == player["x"]:
                    print("M", end = "")
                
                #checks for portal and draws it
                elif coord_y == player["portal_y"] and coord_x == player["portal_x"] and x != "T":
                    print("P", end="")

                #checks if fog of war has been cleared and replaces it with the actual map
                elif fog[coord_y][coord_x] == " ":                
                    print(x, end = "")

                #draws the fog of war
                else:
                    print("?", end = "")

            #drawing border
            if coord_x == MAP_WIDTH - 1:
                print("|")
            
        #drawing border
        print("+", end = "")
        print("-" * MAP_WIDTH, end = "")
        print("+")

        print()

class self:

    # This function shows the information for the player
    def show_information(player):

        print()

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
                
    # This function moves the player
    def move_player(player, action):

        max_steps = player["turns"]
        steps = player["steps"]
        load = player["load"]
        max_load = player["max_load"]
        action = action.upper()

        # This function checks is the space the player wants to move to contains an ore that the player can mine
        def minable_ore(player, action):
            
            coord_y = player["y"]
            coord_x = player["x"]
            pickaxe_level = player["pickaxe_level"]
            
            #up
            if action == "W":
                check_ore = game_map[coord_y - 1][coord_x].upper() 
            
            #down
            elif action == "S":
                check_ore = game_map[coord_y + 1][coord_x].upper()

            #left
            elif action == "A":
                check_ore = game_map[coord_y][coord_x - 1].upper()
            
            #right
            else:
                check_ore = game_map[coord_y][coord_x + 1].upper()

            #checking if next position the player wants to go contains an ore and that he can mine it
            #silver
            if check_ore == "S" and pickaxe_level < 2:
                print(f"Your pickaxe is not good enough to mine {mineral_names[check_ore]}.")
                return True
            
            #gold
            if check_ore == "G" and pickaxe_level < 3:
                print(f"Your pickaxe is too weak to mine {mineral_names[check_ore]}.")
                return True
            
            return False

        #check if player has used max num of steps and at max load
        if steps < max_steps and load < max_load:

            #up
            if action == "W" and player["y"] > 0:
                
                #prevents player from going up if he cannot mine the ore
                if minable_ore(player, action):
                    return None
                
                player["y"] = player["y"] - 1

            #down
            elif action == "S" and player["y"] < MAP_HEIGHT - 1:

                #prevents player from going down if he cannot mine the ore
                if minable_ore(player, action):
                    return None
                
                player["y"] = player["y"] + 1

            #left
            elif action == "A" and player["x"] > 0:
                
                #prevents player from going left if he cannot mine the ore
                if minable_ore(player, action):
                    return None
                
                player["x"] = player["x"] - 1
            
            #right
            elif action == "D" and player["x"] < MAP_WIDTH - 1:
                
                #prevents player from going right if he cannot mine the ore
                if minable_ore(player, action):
                    return None
                
                player["x"] = player["x"] + 1
        
            #adding to total number of steps
            player["steps"] = player["steps"] + 1
            player["total_steps"] = player["total_steps"] + 1
                
    # This function draws the viewport
    ###change the integer values to a variable for different view ranges
    def draw_view(game_map, fog, player):
        y = player["y"]
        x = player["x"]
        torch = torch_levels[player["torch_level"]]
        view = int((torch - 1) / 2)

        #border
        print("+", end = "")
        print("-" * torch, end = "")
        print("+")

        #rows
        for coord_y in range(-view, view + 1):
            print("|", end = "")

            #columns
            for coord_x in range(-view, view + 1):
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
        print("-" * torch, end = "")
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

        #check what ore it is and adding it to inventory
        #copper
        if current_ore == "C":

            #decides the amount of copper obtained
            copper = randint(1, 5)

            print(f"You mined {copper} piece(s) of {mineral_names[current_ore]}.")

            #enough storage
            if player["load"] + copper <= player["max_load"]:
                player["copper"] = player["copper"] + copper
                player["load"] = player["load"] + copper

            #not enough storage
            else:
                print(f"...but you can only carry {player["max_load"] - player["load"]} more piece(s)!")
                player["copper"] = player["copper"] + (player["max_load"] - player["load"])
                player["load"] = player["max_load"]
        
        #silver
        elif current_ore == "S":

            #decides the amount of silver obtained
            silver = randint(1, 3)
            
            print(f"You mined {silver} piece(s) of {mineral_names[current_ore]}.")

            #enough storage
            if player["load"] + silver <= player["max_load"]:
                player["silver"] = player["silver"] + silver
                player["load"] = player["load"] + silver

            #not enough storage
            else:
                print(f"...but you can only carry {player["max_load"] - player["load"]} more piece(s)!")
                player["silver"] = player["silver"] + (player["max_load"] - player["load"])
                player["load"] = player["max_load"]

        #gold
        elif current_ore == "G":

            #decides the amount of gold obtained
            gold = randint(1, 2)
            
            print(f"You mined {gold} piece(s) of {mineral_names[current_ore]}.")

            #enough storage
            if player["load"] + gold <= player["max_load"]:
                player["gold"] = player["gold"] + gold
                player["load"] = player["load"] + gold
            
            #not enough storage
            else:
                print(f"...but you can only carry {player["max_load"] - player["load"]} more piece(s)!")
                player["gold"] = player["gold"] + (player["max_load"] - player["load"])
                player["load"] = player["max_load"]

        #removing ore from map
        game_map[y_coord][x_coord] = " "

        return game_map
    
    # This function sells the player's ore
    def sell_ore(player):

        #sell price for each ore
        copper_price = player["copper"] * randint(prices["copper"][0], prices["copper"][1])
        silver_price = player["silver"] * randint(prices["silver"][0], prices["silver"][1])
        gold_price = player["gold"] * randint(prices["gold"][0], prices["gold"][1])

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
    
    #this function upgrades the player's bag
    def bag_upgrade(player):

        #checks if player has enough GP
        if player["GP"] >= player["max_load"] * 2:

            #reduce the player's GP
            player["GP"] = player["GP"] - player["max_load"] * 2
            
            #increase the player's inventory space
            player["max_load"] = player["max_load"] + 2

            print(f"Congratulations! You can now carry {player["max_load"]} items!", end = "")
        
        else:
            print("You do not have enough GP.", end = "")

    # This function upgrades the player's pickaxe
    def pickaxe_upgrade(player):

        #checks if player has enough GP
        if player["GP"] >= pickaxe_price[player["pickaxe_level"] - 1]:

            #reduce the player's GP
            player["GP"] = player["GP"] - pickaxe_price[player["pickaxe_level"] - 1]

            #upgrade the player's pickaxe level
            player["pickaxe_level"] = player["pickaxe_level"] + 1

            print(f"Congratulations! You can now mine {mineral_names[pickaxe_levels[player["pickaxe_level"]]]}!", end = "")
        
        else:
            print("You do not have enough GP.", end = "")

    #This function upgrades the player's torch
    def torch_upgrade(player):

        #checks if player has enough GP
        if player["GP"] >= player["torch_level"] * 50:
            
            #reduce the player's GP
            player["GP"] = player["GP"] - player["torch_level"] * 50

            #upgrades the player's torch level
            player["torch_level"] =  player["torch_level"] + 1

            print(f"Congratulations! You can now see in a {torch_levels[player["torch_level"]]} x {torch_levels[player["torch_level"]]} area")
        
        else:
            print("You do not have enough GP.", end = "")

class game:

    #this function initializes the game
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
        player["pickaxe_level"] = 1
        player["torch_level"] = 1

        map.clear_fog(fog, player)

    #this function respawns the ores with a 20% chance
    def replenish_ore(game_map, check_map):
        
        #rows
        for y_coord, y in enumerate(check_map):
         
            #columns
            for x_coord, x in enumerate(y):

                #chance of ore respawning (if check == 1, the ore will respawn)
                chance = randint(1, 5)

                #check if ore should respawn and that it dosent replace town (T)
                if chance == 1 and x.upper() in "CSG" and game_map[y_coord][x_coord] == " ":
                    game_map[y_coord][x_coord] = x
                
        return game_map


    # This function saves the game
    def save_game(game_map, fog, player):

        # save map into txt file
        with open("map_save.txt", 'w') as save_file:

            #rows
            for y_coord, y in enumerate(game_map):

                #columns
                for x in y:

                    #writing current x to save file
                    save_file.write(x)

                #new line
                save_file.write("\n")

        # save fog into txt file
        with open("fog_save.txt", 'w') as save_file:

            #rows
            for y_coord, y in enumerate(fog):
                #columns
                for x in y:

                    #writing current x to save file
                    save_file.write(x)

                #new line
                save_file.write("\n")

        # save player into txt file
        with open("player_save.txt", 'w') as save_file:

            # Write each value followed by newline
            for name in PLAYER_NAMES:
                save_file.write(f"{player[name]}\n")

    # This function saves the player's high scores
    def save_high_scores(player):

        #saving the high scores into a file
        with open("high_scores.txt", "a") as save_file:

            save_file.write(f"{player['name']},{player['day']},{player['total_steps']},{player['GP']}\n")

    # This function displays the players high scores in order by rank
    def load_high_scores():

        scores = []

        #error catching if file does not exist
        try:

            with open("high_scores.txt", "r") as save_file:

                #adding the score to scores
                for line in save_file:
                    name, days, steps, gp = line.strip().split(',')

                    #negative to make sort() later do descending order
                    scores.append((-int(days), -int(steps), -int(gp), name))
                
                # Sorting the scores in descending order
                scores.sort()

                print("\n--- TOP 5 SCORES ---")
                print("Rank  Name        Days  Steps   GP")
                for index, item in enumerate(scores):
                    days, steps, gp, name = item
                    print(f"{index + 1:2}    {name:<10}  {-days:<4}  {-steps:<6}  {-gp:<5}")
                print("-----------------------------------------------------------")

        #catches error   
        except:
            print("Error: No high scores recorded yet\n")

    
    # This function loads the game
    def load_game(game_map, fog, player):

        game_map.clear()
        fog.clear()
        player.clear()

        #error catching if file dose not exist
        try:

            # load map
            map.load_map("map_save.txt", game_map) 

            # load fog
            with open("fog_save.txt", 'r') as save_file:

                save_data = save_file.readlines()

                for line in save_data:
                    fog.append(list(line.strip()))

            # load player
            with open("player_save.txt", 'r') as save_file:

                save_data = save_file.readlines()

                #loops through the names of each of the item in dictionary and stores it back to the main dictionary for player
                for index, name in enumerate(PLAYER_NAMES):

                    value = save_data[index].strip("\n")

                    #convert values back into integers other than name since name is a str
                    if name != "name":
                        value = int(value)

                    #stores back to the main dictionary    
                    player[name] = value
            
            return True

        #catches error
        except:
            print("Error: No game save found. \n")
            return False

    def show_main_menu():
        print()
        print("--- Main Menu ----")
        print("(N)ew game")
        print("(L)oad saved game")
        print("(H)igh scores")
        print("(Q)uit")
        print("------------------")

    def show_town_menu():
        print()

        # TODO: Show Day
        print(f"DAY {player["day"]}")

        print("----- Sundrop Town -----")
        print("(B)uy stuff")
        print("See Player (I)nformation")
        print("See Mine (M)ap")
        print("(E)nter mine")
        print("Sa(V)e game")
        print("(Q)uit to main menu")
        print("------------------------")

    def show_buy_menu():

        print()

        print("----------------------- Shop Menu -------------------------")

        #ensures that if player has maxed out pickaxe upgrades, store will show that upgrades are maxed
        if player["pickaxe_level"] >= 3:
            print("(P)ickaxe maxed out")
        else:
            print(f"(P)ickaxe upgrade level {player["pickaxe_level"] + 1} to mine {mineral_names[pickaxe_levels[player["pickaxe_level"]]]} for {pickaxe_price[player["pickaxe_level"] - 1]}")

        print(f"(B)ackpack upgrade to carry {player["max_load"] + 2} items for {player["max_load"] * 2} GP")

        #ensures that if player has maxed out torch upgrades, store will show that upgrades are maxed
        if player["torch_level"] >= 3:
            print("(T)orch maxed out")
        else:
            print(f"(T)orch upgrade to see in a {torch_levels[player["torch_level"] + 1]} x {torch_levels[player["torch_level"] + 1]} area")

        print("(L)eave shop")
        print("-----------------------------------------------------------")
        print(player["GP"])
        print("-----------------------------------------------------------")

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

#game loop
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
            if choice.upper() not in "NLHQ":
                raise KeyError("Invalid choice input")

        #catches the keyerror and prints the error 
        except (ValueError, KeyError) as error:
            print(f"Error: {error}\n")
            continue

        #quit game
        if choice == "Q":
            print("Thanks for playing!")
            is_running = False
            game_state = "exit"
            break

        #load game
        elif choice == "L":
            if not game.load_game(game_map, fog, player):
                continue     

        #high score
        elif choice == "H":
            game.load_high_scores()
            continue

        #new game
        else:
            #initialize game
            game.initialize_game(game_map, fog, player)

            #setting the check map as a new list (a tool to check for the ore respawning)
            check_map = [list(row) for row in game_map]

            #player name
            
            #only allows player to progress if his name is of proper length
            while True:
                player["name"] = input("Greetings, miner! What is your name? ")

                #exits the loop if player name is of required length
                if len(player["name"]) <= 10:
                    break

                print("Error: Player name can only be 10 characters long")
            
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

        #winning the game
        if player["GP"] >= 500:
            print(f'''Woo-hoo! Well done, {player["name"]}, you have {player["GP"]} GP!
You now have enough to retire and play video games every day.
And it only took you {player["day"]} days and {player["total_steps"]} steps! You win!''')
            
            game.save_high_scores(player)

            #exiting to main menu
            game_state = "main"
            break
            
        
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
            print(f"Error: {error}\n")
            continue
    
        #buy menu
        if choice == "B":
            while True:

                game.show_buy_menu()

                #error catching
                try:
                
                    option = input("Your choice? ").upper().strip()

                    #raising error if input is blank
                    if not option:
                        raise ValueError("Input cannot be empty")

                    #raising error if input is not within given actions
                    if option not in "BLPT":
                        raise KeyError("Invalid choice input")
                    
                #catches the keyerror and prints the error 
                except (ValueError, KeyError) as error:
                    print(f"Error: {error}\n")
                    continue

                #if player upgrades backpack
                if option == "B":
                    self.bag_upgrade(player)
                    continue
                
                #if player upgrades pickaxe 
                elif option == "P":

                    #checks if player has maxed out pickaxe upgrades
                    if player["pickaxe_level"] < 3:
                        self.pickaxe_upgrade(player)

                    else:
                        print("You have maxed out your pickaxe upgrades")

                #if player upgrades torch
                elif option == "T":
                    
                    #checks if player has maxed out torch upgrades
                    if player["torch_level"] < 3:
                        self.torch_upgrade(player)

                    else:
                        print("You have maxed out your torch upgrades")

                #exit the buy menu
                else:
                    break

        #information menu
        elif choice == "I":
            self.show_information(player)
        
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
            print(f"Error: {error}\n")
            continue
    
    #border
    print()
    print("---------------------------------------------------")

    #if player runs out of steps or storage
    if player["turns"] - player["steps"] == 1 or player["load"] == player["max_load"]:

        #checks if player has reached max num of steps
        if player["turns"] - player["steps"] == 1:

            self.move_player(player, action)

            #mining ore
            self.mine_ore(game_map, player)

            print("You are exhausted.")

        #checks if player is at max load
        if player["load"] == player["max_load"]:
            print("You can't carry any more, so you can't go that way.")

        #warping back to town
        game_state = "town"
        self.portal(player)
        game.replenish_ore(game_map, check_map)
        continue

    #player movement
    if action in "WASD":
        self.move_player(player, action) 

        #mining ore
        self.mine_ore(game_map, player)

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
        game.replenish_ore(game_map, check_map)
        continue

    #information
    elif action == "I":
            self.show_information(player)
            
    #quitting to main menu
    elif action == "Q":
        game_state = "main"
        continue
    
    
    
    
