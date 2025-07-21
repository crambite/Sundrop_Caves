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

        #stores map into map_struct
        for y in map:

            #removes the \n
            map_struct.append(y.strip("\n"))

        #Stores width and height of map into their repective global variables
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)
        map_file.close()

    # This function loads the fog of war
    def initialise_fog(fog):

        #num of ys
        for y in range(MAP_HEIGHT):

            #temporary list to store current y of fog
            fog_y = []

            #xs in current y
            for x in range(MAP_WIDTH):
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

                #checks if fog of war has been cleared and replaces it with the actual map
                elif fog[coord_y][coord_x] == "": 
                    print(x, end = "")

                #draws the fog of war
                else:
                    print("?", end = "")

                #allows code to print next rows
                if coord_x == len(y) - 1:
                    print("\n", end = "")

class screen:
    # This function shows the information for the player
    def show_information(player):
        return
                
    # This function moves the player
    def move_player(player, action):

        #up
        if action.upper() == "W" and player["y"] > 0:
            player["y"] = player["y"] - 1
            print(player["y"])

        #down
        elif action.upper() == "S" and player["y"] < MAP_HEIGHT - 1:
             player["y"] = player["y"] + 1
             print(player["y"])

        #left
        elif action.upper() == "A" and player["x"] > 0:
            player["x"] = player["x"] - 1
            print(player["x"])
        
        #right
        elif action.upper() == "D" and player["x"] < MAP_WIDTH - 1:
            player["x"] = player["x"] + 1
            print(player["x"])
    
        #adding to total number of steps
        player['steps'] = player['steps'] + 1

        
                
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
        
    
    
class game:
    def initialize_game(game_map, fog, player):
        # initialize map
        map.load_map("level1.txt", game_map)

        # TODO: initialize fog
        map.initialise_fog(fog)

        # TODO: initialize player
        #   You will probably add other entries into the player dictionary
        player['x'] = 0
        player['y'] = 0
        player['copper'] = 0
        player['silver'] = 0
        player['gold'] = 0
        player['GP'] = 0
        player['day'] = 0
        player['steps'] = 0
        player['turns'] = TURNS_PER_DAY

        map.clear_fog(fog, player)

        
        

    # This function saves the game
    def save_game(game_map, fog, player):
        # save map
        # save fog
        # save player
        return
    
    # This function loads the game
    def load_game(game_map, fog, player):
        # load map
        # load fog
        # load player
        return

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
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!

game.initialize_game(game_map, fog, player)
while game_state == 'main':

    screen.draw_view(game_map, fog, player)
    map.draw_map(game_map,fog,player)
    #error catching 
    try:
        #input action
        action = input('''Turns left: 20 Load: 0 / 12 Steps: 0
(WASD) to move
(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu
Action? ''')
        
        #raising error if input is not within given actions
        if action.upper() not in "WASDMIPQ":
            raise KeyError("Invalid action input")
    
    #catches the keyerror and prints the error
    except KeyError as error:
            print(f"Error: {error}")
            continue
        
    screen.move_player(player, action)
    print(f"NEW PLAYER: {player}")

    #quitting game
    if action.upper() == "Q":
        game_state = ''
        break




