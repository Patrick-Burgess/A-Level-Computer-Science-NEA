import pygame, sys
import math
screenWidth, screenHeight = 992,576
fps = 60
#initalise global values
playerOneCharacterSelection = "NULL"
playerTwoCharacterSelection = "NULL"
winner = "NULL"
GAMESTATE = 'Menu'

class Game():
    #Gamestate tutorial followed online but expanded upon by adding more subclasses
    print("Gamestate = Game")
    def __init__(self):
        #Initialise Values
        pygame.init()
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        # Defining all the classes so they can be accessed by the game state manager
        self.gameStateManager = GameStateManager(GAMESTATE)
        self.Menu = MenuGameState(self.screen, self.gameStateManager)
        self.Playing = PlayingGameState(self.screen, self.gameStateManager)
        self.Help = HelpGameState(self.screen, self.gameStateManager)
        self.Paused = PausedGameState(self.screen, self.gameStateManager)
        self.End = EndGameState(self.screen, self.gameStateManager)
        self.states = {'Menu': self.Menu, 'Playing': self.Playing, 'Help': self.Help, 'Paused': self.Paused, 'End': self.End}

    def Run(self):
        pygame.display.set_caption('GAME GAMESTATE')
        global GAMESTATE
        #Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape pressed")
                        self.gameStateManager.set_state('Paused') #SET GAMESTATE TO PAUSED
                    elif event.key == pygame.K_y:
                        print("Y pressed")
                        self.gameStateManager.set_state('Menu') #SET GAMESTATE TO MENU
                    elif event.key == pygame.K_p:
                        print("p pressed")
                        self.gameStateManager.set_state('Playing') #SET GAMESTATE TO Playing
                    elif event.key == pygame.K_h:
                        print("H pressed")
                        self.gameStateManager.set_state('Help') #SET GAMESTATE TO HELP

            #Determines the game state it is in
            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()
            self.clock.tick(fps)
class PlayingGameState:
    global playerOneCharacterSelection
    global playerTwoCharacterSelection

    def __init__(self, display, gameStateManager):
        #Defines Attributes for the Game
        self.playerOneSprite = None
        self.playerTwoSprite = None
        #HealthPoints
        self.playerOneHealthPoints = 100
        self.playerTwoHealthPoints = 100
        self.display = display
        self.gameStateManager = gameStateManager
        self.tile_size = 32



    def PlayerOne(self,playerOneCharacterSelection):
        if playerOneCharacterSelection == "NULL":
            print("player one not selected")
        else:
            print('Player One selected :', playerOneCharacterSelection)
            tempPlayerOneCharacterSelection = ("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" +
                                               playerOneCharacterSelection + ".png")
            #creating the sprite for PlayerOne and making it a rectangle
            print(tempPlayerOneCharacterSelection)
            self.playerOneimage = pygame.image.load(tempPlayerOneCharacterSelection)
            self.playerOneSprite = self.playerOneimage
            self.player1Rect = self.playerOneimage.get_rect()
            self.player1Rect.x = 160
            self.player1Rect.y = 0
            self.player1RectVel = 0



    def PlayerTwo(self,playerTwoCharacterSelection):
        if playerTwoCharacterSelection == "NULL":
            print("player Two not selected")
        else:
            print('Player Two selected :', playerTwoCharacterSelection)
            tempPlayerTwoCharacterSelection = ("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" + playerTwoCharacterSelection + ".png")
            print(tempPlayerTwoCharacterSelection)
            #creating the sprite for PlayerTwo and making it a rectangle
            self.playerTwoImage = pygame.image.load(tempPlayerTwoCharacterSelection)
            self.playerTwoSprite = self.playerTwoImage
            self.player2Rect = self.playerTwoImage.get_rect()
            self.player2Rect.x = 32
            self.player2Rect.y = 0
            self.player2RectVel = 0

    def CreateWorld(self): #Creates the arena
        self.tile_list = []
        data = [# A 2d Array Repersenting all the tiles in the world
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 2
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 3
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 4
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 6
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 7
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 8
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Row 9
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],  # Row 10
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4],  # Row 11
            [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 6, 4],  # Row 12
            [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 6, 6, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 8, 4, 8, 4],  # Row 13
            [2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 6, 6, 6, 6, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 4, 6, 4, 8, 4, 8, 4],  # Row 14
            [2, 2, 2, 2, 2, 8, 8, 6, 6, 8, 8, 8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 3, 6, 8, 4, 6, 4, 8, 4, 8, 4],  # Row 15
            [2, 2, 2, 2, 2, 8, 6, 8, 8, 8, 8, 6, 8, 6, 8, 8, 8, 6, 8, 8, 8, 6, 8, 8, 4, 8, 4, 8, 4, 8, 4],  # Row 16
            [2, 2, 2, 2, 2, 8, 8, 6, 8, 6, 6, 8, 6, 8, 6, 8, 8, 8, 8, 6, 8, 8, 8, 6, 4, 6, 4, 8, 4, 8, 4],  # Row 17
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Row 18
        ]
        tile_size = 32
        #All the different tiles paths stored in variables
        AquariumBlock = pygame.image.load('/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/AquariumBlock.png')
        BrickBlock = pygame.image.load('/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/BrickBlock.png')
        GrassBlock = pygame.image.load('/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/GrassBlock.png')
        WoodenBoxBlock = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/WoodenBoxBlock.png")
        Box1 = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/Box1.png")
        Dirt2Block = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/temp.png")
        Box3 = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/Box3.png")
        DirtBlock = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Terrain/DirtBlock.png")
        row_count = 0
        #Loops through the 2d array and creates a new array with the data for each tile
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: #AQUARIUMBLOCK
                    img = pygame.transform.scale(AquariumBlock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2: #BRICKBLOCK
                    img = pygame.transform.scale(BrickBlock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3: #GRASSBLOCK
                    img = pygame.transform.scale(GrassBlock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 4: #WOODENBOX
                    img = pygame.transform.scale(WoodenBoxBlock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 5: #WOODENBOX1
                    img = pygame.transform.scale(Box1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 6: #DIRTBLOCK2
                    img = pygame.transform.scale(Dirt2Block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 7: #WOODENBOX3
                    img = pygame.transform.scale(Box3, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 8: #DIRT BLOCK
                    img = pygame.transform.scale(DirtBlock, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1
    def draw(self): #Function to draw the tiles on the screen
        for tile in self.tile_list:
            self.display.blit(tile[0], tile[1])
            pygame.draw.rect(self.display, (255, 255, 255), tile[1], 2)

    def Attack(self,player,type):#Function to deal with the attack system
        playerOneCharacterGun = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" +playerOneCharacterSelection +"Gun.png")
        playerOneCharacterKnife = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" +playerOneCharacterSelection +"Knife.png")
        playerTwoCharacterGun = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" +playerTwoCharacterSelection +"Gun.png")
        playerTwoCharacterKnife = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Main Characters/" +playerTwoCharacterSelection +"Knife.png")
        pygame.display.flip()
        x1 = self.player1Rect.x
        x2 = self.player2Rect.x
        y1 = self.player1Rect.y
        y2 = self.player2Rect.y
        xDistance = abs(x1-x2)
        yDistance = abs(y1-y2)
        #use pythagoras Theorm to calculate the distance between two sprites
        playerdistance = round(math.sqrt(xDistance*xDistance+yDistance*yDistance))
       #Nested IF statements to deal damage to either player
        if player == 1:
            if type == "melee":
                if playerdistance < 51:
                    self.playerTwoHealthPoints -= 30
                    self.playerOneSprite = playerOneCharacterKnife
                    print("player 2 hit:", self.playerTwoHealthPoints, )
            elif type == "projectile":
                if y1 == y2:
                    self.playerTwoHealthPoints -= 15
                    self.playerOneSprite = playerOneCharacterGun
                    print("player 2 Shot:",self.playerTwoHealthPoints,)
        elif player == 2:
            if type == "melee":
                if playerdistance < 51:
                    self.playerOneHealthPoints -= 30
                    self.playerTwoSprite = playerTwoCharacterKnife
                    print("player 1 stabbed:",self.playerOneHealthPoints,)
            elif type == "projectile":
                if y1 == y2:
                    self.playerOneHealthPoints -= 15
                    self.playerTwoSprite = playerTwoCharacterGun
                    print("player 1 shot:",self.playerOneHealthPoints,)


    def run(self): #Main Game loop
        global winner
        pygame.display.set_caption('PLAYING GAMESTATE')
        self.display.fill((189, 223, 236))
        self.CreateWorld() #Create world
        self.draw() #Draw the world
        self.PlayerOne(playerOneCharacterSelection) #Create Player One
        self.PlayerTwo(playerTwoCharacterSelection) # Create Player Two
        #VELOCITY OF PLAYERS in X COORDINATES
        player1RectVelX = 0
        player2RectVelX = 0
        while True:
            if self.playerOneHealthPoints > 0 and self.playerTwoHealthPoints > 0 :
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        #control both players jumps
                        if event.key == pygame.K_w:
                            print("UP Player1")
                            self.player1RectVel = -15
                            self.jumped1 = True
                            self.playerOneSprite = self.playerOneimage
                        if event.key == pygame.K_i:
                            print("UP Player2")
                            self.player2RectVel = -15
                            self.jumped2 = True
                            self.playerTwoSprite = self.playerTwoImage
                        #player one and two attack buttons
                        if event.key == pygame.K_x:
                            print("FireWeapon Player1")
                            self.Attack(1, "projectile")
                        if event.key == pygame.K_z:
                            print("melee player1")
                            self.Attack(1, "melee")
                        if event.key == pygame.K_m:
                            print("FireWeapon Player2")
                            self.Attack(2, "projectile")
                        if event.key == pygame.K_COMMA:
                            print("melee player2")
                            self.Attack(2, "melee")

                keys = pygame.key.get_pressed()
                #Change game state
                if keys[pygame.K_ESCAPE]:
                    print("Escape pressed")
                    self.gameStateManager.set_state('Paused')
                    return
                elif keys[pygame.K_y]:
                    print("Y pressed")
                    self.gameStateManager.set_state('Menu')
                    return
                elif keys[pygame.K_h]:
                    print("H pressed")
                    self.gameStateManager.set_state('Help')
                    return

                # PLAYER ONE movement
                elif keys[pygame.K_a]:
                    print("LEFT Player1")
                    player1RectVelX -= 16
                    self.playerOneSprite = self.playerOneimage
                elif keys[pygame.K_s]:
                    print("DOWN Player1")
                    self.playerOneSprite = self.playerOneimage
                elif keys[pygame.K_d]:
                    print("RIGHT Player1")
                    player1RectVelX += 16
                    self.playerOneSprite = self.playerOneimage

                # PLAYER TWO movement
                elif keys[pygame.K_j]:
                    print("LEFT Player2")
                    player2RectVelX -= 16
                    self.playerTwoSprite = self.playerTwoImage
                elif keys[pygame.K_k]:
                    print("DOWN Player2")
                    self.playerTwoSprite = self.playerTwoImage
                elif keys[pygame.K_l]:
                    print("RIGHT Player2")
                    player2RectVelX += 16
                    self.playerTwoSprite = self.playerTwoImage
                # Handle other key events
                else:
                    player1RectVelX = 0
                    player2RectVelX = 0
                    self.jumped1 = False
                    self.jumped2 = False
                # Maxing out velocity
                player1RectVelX = max(-1, min(1, player1RectVelX))
                player2RectVelX = max(-1, min(1, player2RectVelX))
                # GRAVITY Designed by Someone else
                self.player1RectVel += 1
                if self.player1RectVel > 10:
                    self.player1RectVel = 10
                self.player1Rect.y += self.player1RectVel

                self.player2RectVel += 1
                if self.player2RectVel > 10:
                    self.player2RectVel = 10
                self.player2Rect.y += self.player2RectVel
                #COLLISIONS
                #Borrowed from online pygame Platformer Game
                #Loops through all tiles to check for collisions
                for tile in self.tile_list:
                    # Check for collision in x direction for both players
                    if tile[1].colliderect(self.player1Rect.x + player1RectVelX, self.player1Rect.y, 32, 32):
                        player1RectVelX = 0
                    if tile[1].colliderect(self.player2Rect.x + player2RectVelX, self.player2Rect.y, 32, 32):
                        player2RectVelX = 0

                    #Checks for collision in Y direction for Player 1
                    if tile[1].colliderect(self.player1Rect.x, self.player1Rect.y + self.player1RectVel, 32, 32):
                       #Check if player is jumping
                        if self.player1RectVel > 0:
                            self.player1RectVel = tile[1].top - self.player1Rect.bottom
                            self.player1Rect.bottom = tile[1].top
                            self.jumped1 = False
                        #Check if player is falling
                        elif self.player1RectVel < 0:
                            self.player1RectVel = tile[1].bottom - self.player1Rect.top
                            self.player1Rect.top = tile[1].bottom
                    #Checks for collision in Y direction for Player 2
                    if tile[1].colliderect(self.player2Rect.x, self.player2Rect.y + self.player2RectVel, 32, 32):
                        # Check if player is jumping
                        if self.player2RectVel > 0:
                            self.player2RectVel = tile[1].top - self.player2Rect.bottom
                            self.player2Rect.bottom = tile[1].top
                            self.jumped2 = False
                        # Check if falling
                        elif self.player2RectVel < 0:
                            self.player2RectVel = tile[1].bottom - self.player2Rect.top
                            self.player2Rect.top = tile[1].bottom
                #Bottom Border
                if self.player1Rect.bottom > screenHeight:
                    self.player1Rect.bottom = screenHeight
                if self.player2Rect.bottom > screenHeight:
                    self.player2Rect.bottom = screenHeight
                #Right Border
                if self.player1Rect.right > screenWidth:
                    self.player1Rect.right = screenWidth
                if self.player2Rect.right > screenWidth:
                    self.player2Rect.right = screenWidth
                #Top Border
                if self.player1Rect.top <= 0:
                    self.player1Rect.top = 0
                if self.player2Rect.top <= 0:
                    self.player2Rect.top = 0
                #Left Border
                if self.player1Rect.left <= 0:
                    self.player1Rect.left = 0
                if self.player2Rect.left <= 0:
                    self.player2Rect.left = 0
                #Update player location
                self.player1Rect.x += player1RectVelX
                self.player2Rect.x += player2RectVelX
                #clearing the screen and redrawing sprites
                self.display.fill((189, 223, 236))
                self.draw()
                self.display.blit(self.playerOneSprite, self.player1Rect)
                #pygame.draw.rect(self.display, (255,255,255), self.player1Rect,2)
                self.display.blit(self.playerTwoSprite, self.player2Rect)
                pygame.display.flip()
            else:
                #game over condition
                print("game over")
                if self.playerOneHealthPoints < 1:
                    winner = "PLAYER 2"
                    print("player 2 wins")
                elif self.playerTwoHealthPoints < 1:
                    winner = "PLAYER 1"
                    print("player 1 wins")
                self.gameStateManager.set_state('End')
                break
class PausedGameState:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):

        pygame.display.set_caption('PAUSED GAMESTATE')
        global GAMESTATE
        while True:
            pausedimage = pygame.image.load('/Users/patrickburgess/Downloads/NEA/Assets_NEA/PausedAsset.jpg')
            self.display.fill((255, 0, 0))
            self.display.blit(pausedimage, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print("p pressed")
                        self.gameStateManager.set_state('Playing')
                        return
                    if event.key == pygame.K_y:
                        print("y pressed")
                        self.gameStateManager.set_state('Menu')
                        return


class HelpGameState:
    #Gamestate that allows the user to access more information in the Help gamestate
    print("Gamestate = Help")
    #intialises the display and gamestate manager
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        #prints the important information on the screen
        pygame.display.set_caption('HELP GAMESTATE')
        self.display.fill((153,204,255))
        keyboardGuide = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/HelpPageButtons.png")
        characterGuide = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/‎CharcterDescriptions.png")
        self.display.blit(keyboardGuide,(320,0))
        self.display.blit(characterGuide,(250,200))

        pygame.display.flip()
        while True:
            # Allows user to change gamestate using the gamestate manager class
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape pressed")
                        self.gameStateManager.set_state('Paused')
                        return
                    elif event.key == pygame.K_y:
                        print("Y pressed")
                        self.gameStateManager.set_state('Menu')
                        return
                    elif event.key == pygame.K_p:
                        print("P pressed")
                        self.gameStateManager.set_state('Playing')
                        return



class MenuGameState:
    print("Gamestate = Menu")

    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def ChooseCharacter(self, playerNumber, characterOption): #Function to select Character for each player
        global playerOneCharacterSelection, playerTwoCharacterSelection
        if playerNumber == 1:
            playerOneCharacterSelection = characterOption
            print(playerOneCharacterSelection)
        if playerNumber == 2:
            playerTwoCharacterSelection = characterOption
            print(playerTwoCharacterSelection)



    def run(self): #
        pygame.display.set_caption('MENU GAMESTATE')
        MenuImage = pygame.image.load("/Users/patrickburgess/Downloads/NEA/Assets_NEA/Menu Screen.png")
        self.display.fill((255,0,0))
        self.display.blit(MenuImage, (0, 0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        print("Escape pressed")
                        self.gameStateManager.set_state('Paused')
                        return
                    elif event.key == pygame.K_h:
                        print("H pressed")
                        self.gameStateManager.set_state('Help')
                        return
                    elif event.key == pygame.K_p:
                        print("p pressed")
                        self.gameStateManager.set_state('Playing')
                        return


                    #Player 1 Character selection
                    if event.key == pygame.K_1:
                        self.ChooseCharacter(1,"MaskDude")
                        print("Player 1 maskdude")
                    if event.key == pygame.K_2:
                        self.ChooseCharacter(1, "NinjaFrog")
                        print("Player 1 Ninjafrog")
                    if event.key == pygame.K_3:
                        self.ChooseCharacter(1, "PinkMan")
                        print("Player 1 Pinkman")
                    #Player 2 Character Selection
                    if event.key == pygame.K_4:
                        self.ChooseCharacter(2, "MaskDude")
                        print("Player 2 maskdude")
                    if event.key == pygame.K_5:
                        self.ChooseCharacter(2, "NinjaFrog")
                        print("Player 2 Ninjafrog")
                    if event.key == pygame.K_6:
                        self.ChooseCharacter(2, "PinkMan")
                        print("Player 2 Pinkman")
class EndGameState:
    global winner
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def draw_text(self,text, font, col, x, y): # Function to draw text on screen
        text = font.render(text, True, col)
        self.display.blit(text, (x,y))
        pygame.display.flip()
    def run(self):
        pygame.display.set_caption('END GAMESTATE')
        text_font = pygame.font.Font("/Users/patrickburgess/Downloads/NEA/Assets_NEA/PressStart2P-Regular.ttf",25)
        self.display.fill((255,255,0))
        textString = "Congrats to " + winner + " for winning!"
        self.draw_text(textString, text_font, (0, 0, 0), 0, 25)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_h:
                        print("H pressed")
                        self.gameStateManager.set_state('Help')
                        return
                    elif event.key == pygame.K_p:
                        print("p pressed")
                        self.gameStateManager.set_state('Playing')
                        return


class GameStateManager:
    #Defines attributes
    def __init__(self,currentState):
        self.currentState = currentState
        print("Gamestate = GameStateManager")
    #Function to get the current gamestate
    def get_state(self):
        return self.currentState
    #Sets new Gamestate
    def set_state(self, state):
        self.currentState = state
        print("GAMESTATEMANAGER state set to",state)


if __name__ == '__main__':
    game = Game()
    game.Run()