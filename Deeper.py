import pygame, random, pickle, time
from pygame.color import THECOLORS
blockImages = ["stone.png", "dirt.png", "CoalOre.png", "IronOre.png", "GoldOre.png", "Clay.png", "Bricks.png", "Mud.png", "grass.png", "lamp.png"]
Background = pygame.image.load("Background.png")
Logo = pygame.image.load("DeeperIcon.jpg")
ToolbarTile = pygame.image.load("Toolbar Tile.png")
CheckboxChecked = pygame.image.load("CheckboxChecked.png")
toolbarFile = []
toolbarData = [0, 1, 2, 3, 4]
cavePos = []
def loadToolbar():
    toolbarFile = open("toolbar.dat", "r")
    toolbarData = pickle.load(toolbarFile)
    toolbarFile.close()
    return toolbarData
def dumpToolbar():
    toolbarFile = open("toolbar.dat", "w")
    pickle.dump([0, 1, 2, 3, 4], toolbarFile)
    return [0, 1, 2, 3, 4]

try:
    toolbarData = loadToolbar()
except:
    toolbarData = dumpToolbar()

#Deeper - Version 0.1 Alpha:

#Release Notes:
# +Added Menu Screen.
# +Added Toolbar. (Saves to Hard Drive every time you quit the game.)
# +Added 2 World Types, Basic & Miners. (Miner's in my opinion is better, unless your a builder and just want an easy space to work with.)
# +Sight Effects, place Lamp Blocks (The Yellow-Neon looking blocks.), to see places far away.
# +10 Blocks to build with.
# +Caves! Dig around and see if you can find one! (Miners World Only)
# +Achievements!
# +Added In-Game Menu. (Press E)

class block(pygame.sprite.Sprite):
    def __init__(self, position, ID):
        pygame.sprite.Sprite.__init__(self)
        self.trueimage = pygame.image.load(blockImages[ID])
        self.id = ID
        self.rect = self.trueimage.get_rect()
        self.rect.centerx, self.rect.centery = position
        self.activated = False
        self.mined = False
        self.image = self.trueimage
        self.collideable = True
        self.shadedSurface = pygame.surface.Surface((10, 10))
        self.shadedSurface.fill([0, 0, 0])
    def activate(self):
        global mouseGrp
        if pygame.sprite.spritecollide(self, mouseGrp, False):
            self.activated = True
        else:
            self.activated = False
    def mine(self):
        global minedBlocks, player, blocksMined, screen
        if not self.rect.centerx <= player.rect.centerx - 50 or self.rect.centerx >= player.rect.centerx + 50 or self.rect.centery <= player.rect.centery - 50 or self.rect.centery >= player.rect.centery + 50:
            self.kill()
            minedBlocks.add(self)
            allBlocks.add(self)
            self.mined = True
            if screen == 'in_game':
                blocksMined += 1
    def place(self):
        global world, chosenBlock, Toolbar, player, blockImages
        if not self.rect.centerx <= player.rect.centerx - 50 or self.rect.centerx >= player.rect.centerx + 50 or self.rect.centery <= player.rect.centery - 50 or self.rect.centery >= player.rect.centery + 50:
            self.kill()
            world.add(self)
            allBlocks.add(self)
            self.image = pygame.image.load(blockImages[Toolbar[chosenBlock]])
            self.id = Toolbar[chosenBlock]
            self.mined = False
            if self.id == 9:
                blocklighting.add(self)
    def update(self, action):
        self.activate()
        global player, yVelocity, playerMove, playerMoveX
        if action == 'mine':
            if self.activated and not self.mined:
                self.mine()
            elif self.activated and self.mined:
                self.place()
        elif action == 'collide' and not self.mined:
            if pygame.sprite.collide_rect(self, player) and player.rect.bottom <= self.rect.top:
                playerMove = self.rect.top + 5
                playerWhere = 'bottom'
            elif pygame.sprite.collide_rect(self, player) and player.rect.top <= self.rect.bottom and player.rect.top >= self.rect.centery:
                playerMove = self.rect.bottom - 5
                playerWhere = 'top'
            elif pygame.sprite.collide_rect(self, player) and player.rect.right >= self.rect.left and player.rect.right <= self.rect.centerx and player.rect.centery >= self.rect.top and player.rect.centery <= self.rect.centery:
                playerMoveX = -3
            elif pygame.sprite.collide_rect(self, player) and player.rect.left <= self.rect.right and player.rect.left >= self.rect.centerx and player.rect.centery >= self.rect.top and player.rect.centery <= self.rect.centery:
                playerMoveX = 1
        elif action == 'startcollide' and not self.mined:
            if pygame.sprite.collide_rect(self, player):
                self.mine()
class LightingBlock(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([10, 10])
        self.image = self.image.convert()
        self.fakeimage = pygame.surface.Surface([20, 20])
        self.fakeimage = self.fakeimage.convert()
        self.rect = self.fakeimage.get_rect()
        self.rect.centerx, self.rect.centery = position
    def update(self):
        global blocklighting
        if pygame.sprite.spritecollide(self, blocklighting, False):
            self.image.set_alpha(0)
            window.blit(self.image, (self.rect.centerx, self.rect.centery))
        elif self.rect.centerx <= player.rect.centerx - 50 or self.rect.centerx >= player.rect.centerx + 50 or self.rect.centery <= player.rect.centery - 50 or self.rect.centery >= player.rect.centery + 50:
            self.image.set_alpha(500)
            window.blit(self.image, (self.rect.centerx, self.rect.centery))
        elif self.rect.centerx <= player.rect.centerx - 40 or self.rect.centerx >= player.rect.centerx + 40 or self.rect.centery <= player.rect.centery - 40 or self.rect.centery >= player.rect.centery + 40:
            self.image.set_alpha(200)
            window.blit(self.image, (self.rect.centerx, self.rect.centery))
        elif self.rect.centerx <= player.rect.centerx - 30 or self.rect.centerx >= player.rect.centerx + 30 or self.rect.centery <= player.rect.centery - 30 or self.rect.centery >= player.rect.centery + 30: 
            self.image.set_alpha(100)
            window.blit(self.image, (self.rect.centerx, self.rect.centery))
class mouse(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load("mouse.png")
        self.rect = self.img.get_rect()

class button(pygame.sprite.Sprite):
    def __init__(self, text, location, basecolor, excess_trim):
        pygame.sprite.Sprite.__init__(self)
        self.text = str(text)
        self.font = pygame.font.Font(None, 30)
        if excess_trim == None:
            self.excess_trim = int(0)
        else:
            try:
                self.excess_trim = int(excess_trim)
            except:
                self.excess_trim = int(0)
        self.surface = self.font.render(self.text, 1, (0, 0, 0))
        self.base = pygame.surface.Surface([(len(self.text) * 10 + 10) + self.excess_trim, 30])
        self.base.fill(THECOLORS[str(basecolor)])
        self.base = self.base.convert()
        self.rect = self.base.get_rect()
        self.rect.centerx, self.rect.centery = location
        self.activated = False
        self.clicked = False
        
    def display(self):
        global window
        window.blit(self.base, [self.rect.centerx - 5, self.rect.centery - 5])
        window.blit(self.surface, [self.rect.centerx, self.rect.centery])

    def checkmouse(self):
        global Mouse, MouseTriggerZone
        if MouseTriggerZone(self.rect.left, self.rect.top, self.rect.right, self.rect.bottom):
            self.activated = True
        else:
            self.activated = False
    def click(self):
        if self.activated:
            self.clicked = True

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Player.png")
        self.real_image = pygame.image.load("PlayerSkin.png")
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = position
    def update(self, action):
        global playerMove, playerMoveX, playerWhere, world, cavePos, achievements
        if pygame.sprite.spritecollide(self, world, False):
            world.update('collide')
        else:
            playerMove += 1
        self.rect.centerx += playerMoveX
        if playerWhere == 'bottom':
            self.rect.centery = playerMove
        elif playerWhere == 'top':
            self.rect.centery = playerMove
        else:
            self.rect.centery = playerMove
        if action == "jump":
            if pygame.sprite.spritecollide(self, world, False):
                for i in range(7):
                    playerMove -= 2
        if action == 'cavecheck':
            if self.rect.centery > cavePos[0] * 10 and self.rect.centery <= cavePos[4] * 10:
                achievements[1] = True
            
def background():
    window.blit(Background, [0, 0])

def MouseTriggerZone(x1, y1, x2, y2):
    if Mouse.rect.centerx >= x1 and Mouse.rect.centery >= y1 and Mouse.rect.centerx <= x2 and Mouse.rect.centery <= y2:
        triggered = True
    else:
        triggered = False
    return triggered

class in_game_menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([240, 240])
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = 120, 120
        self.image.fill([128, 128, 128])
        self.dimSurf = pygame.surface.Surface([480, 480])
        self.dimSurf.set_alpha(100)
    def display(self):
        global window, blockImages, chosenBlock, toolbar 
        window.blit(self.dimSurf, [0, 0])
        window.blit(self.image, [self.rect.centerx, self.rect.centery])
        MenuFont = pygame.font.Font(None, 20)
        toolbar(125, 125)
        Achievements(125, 200)
        MenuToolbarText = MenuFont.render("Press 0 to pick a new block.", 1, (0, 0, 0))
        window.blit(MenuToolbarText, (125, 150))
        
def menu():
    global window, menuButton, menuButton2, Logo
    background()
    window.blit(Logo, [100, 60])
    textFont = pygame.font.Font(None, 50)
    textRender = textFont.render("Deeper", 1, (0, 0, 0))
    window.blit(textRender, [175, 75])
    menuButton.display()
    menuButton.checkmouse()
    exitButton.display()
    exitButton.checkmouse()
    pygame.display.flip()

def new_world():
    background()
    goButton.display()
    goButton.checkmouse()
    basicButton.checkmouse()
    basicButton.display()
    nw_font = pygame.font.Font(None, 30)
    if world_type:
        nw_surface = nw_font.render("Basic World", 1, (0, 0, 0))
    else:
        nw_surface = nw_font.render("Miner's World", 1, (0, 0, 0))
    window.blit(nw_surface, [150, 325])
    pygame.display.flip()

def display_world():
    global world, window
    background()
    world.draw(window)

def generate_world(Basic):
    Id = 0
    Coal = 0
    Iron = 0
    Gold = 0
    Airspace = 0
    global player, players, playerSpawned, world, screen, achievements, cavePos
    cavePos.append(int(random.randint(1, 42)))
    playerSpawnX = random.randint(0, 47)
    if bool(Basic):
        for y in range(48):
            for x in range(48):
                if y == 0 and x == playerSpawnX:
                    player = Player([x * 10 + 2, y * 10 + 1])
                    playerSpawned = True
                    Id = None
                if not Id == None:
                    Block = block([(x*10) + 5, (y*10) + 5], Id)
                    lightingBlock = LightingBlock([(x*10), (y*10)])
                    world.add(Block)
                    allBlocks.add(Block)
                    lighting.add(lightingBlock)
                if Id == None:
                    Id = 0
                    Block = block([(x*10) + 5, (y*10) + 5], Id)
                    lightingBlock = LightingBlock([(x*10), (y*10)])
                    minedBlocks.add(Block)
                    allBlocks.add(Block)
                    lighting.add(lightingBlock)
                    Block.mined = True
                    Block.mine()
        window.fill(THECOLORS['black'])
        pygame.display.flip()
    else:
        for c in range(4):
            cavePos.append(cavePos[c] + 1)
        for y in range(48):
            for x in range(48):
                if y in cavePos:
                    Airspace = int(random.randint(1, 10))
                    if Airspace > 5:
                        Id = None
                    elif not cavePos[1] == y and not cavePos[2] == y and not cavePos[3] == y:
                        Id = 0
                else:
                    if y < 10:
                        Coal = int(random.randint(1, 10))
                        if Coal > 7:
                            Id = int(random.randint(0, 2))
                        else:
                            Id = int(random.randint(0, 1))
                            if Id == 1:
                                if int(random.randint(0, 4)) > 2:
                                    Id = 5
                                else:
                                    Id = 1
                        if y == 0 and x == playerSpawnX:
                            player = Player([x * 10 + 2, y * 10 + 1])
                            playerSpawned = True
                            Id = None
                                        
                    elif y > 20 and y < 30:
                        Iron = int(random.randint(1, 10))
                        Coal = int(random.randint(1, 10))
                        if Iron > 9:
                            Id = 3
                        else:
                            if Coal > 9:
                                Id = 2
                            else:
                                Id = 0
                    elif y > 30:
                        Iron = int(random.randint(1, 10))
                        Gold = int(random.randint(1, 10))
                        Coal = int(random.randint(1, 20))
                        if Gold > 9:
                            Id = 4
                        else:
                            if Iron > 9:
                                Id = 3
                            else:
                                if Coal > 19:
                                    Id = 2
                                else:
                                    Id = 0
                    else:
                        Coal = int(random.randint(1, 10))
                        if Coal == 10:
                            Id = 2
                        else:
                            Id = 0
                if not Id == None:
                    Block = block([(x*10) + 5, (y*10) + 5], Id)
                    lightingBlock = LightingBlock([(x*10), (y*10)])
                    world.add(Block)
                    allBlocks.add(Block)
                    lighting.add(lightingBlock)
                if Id == None:
                    Id = 0
                    Block = block([(x*10) + 5, (y*10) + 5], Id)
                    lightingBlock = LightingBlock([(x*10), (y*10)])
                    minedBlocks.add(Block)
                    allBlocks.add(Block)
                    lighting.add(lightingBlock)
                    Block.mined = True
                    Block.mine()
                window.fill(THECOLORS['black'])
                pygame.display.flip()
    world.update('startcollide')
    screen = 'in_game'
    achievements[0] = True

def toolbar(x, y):
    global chosenBlock
    window.blit(ToolbarTile, [x, y])
    if not Toolbar[0] == None:
        window.blit(pygame.image.load(blockImages[Toolbar[0]]), [x + 2, y + 2])
    window.blit(ToolbarTile, [x + 15, y])
    if MouseTriggerZone(x, y, x + 14, y + 14) and clicked:
        chosenBlock = 0
    if not Toolbar[1] == None:
        window.blit(pygame.image.load(blockImages[Toolbar[1]]), [x + 17, y + 2])
    window.blit(ToolbarTile, [x + 30, y])
    if MouseTriggerZone(x + 15, y, x + 29, y + 14) and clicked:
        chosenBlock = 1
    if not Toolbar[2] == None:
        window.blit(pygame.image.load(blockImages[Toolbar[2]]), [x + 32, y + 2])
    window.blit(ToolbarTile, [x + 45, y])
    if MouseTriggerZone(x + 30, y, x + 44, y + 14) and clicked:
        chosenBlock = 2
    if not Toolbar[3] == None:
        window.blit(pygame.image.load(blockImages[Toolbar[3]]), [x + 47, y + 2])
    window.blit(ToolbarTile, [x + 60, y])
    if MouseTriggerZone(x + 45, y, x + 59, y + 14) and clicked:
        chosenBlock = 3
    if not Toolbar[4] == None:
        window.blit(pygame.image.load(blockImages[Toolbar[4]]), [x + 62, y + 2])
    if MouseTriggerZone(x + 60, y, x + 74, y + 14) and clicked:
        chosenBlock = 4
    pygame.draw.rect(window, (0, 255, 255), (x + (chosenBlock * 15), y + 14, 14, 2))
def Achievements(x, y):
    global CheckboxChecked, blocksMined
    if achievements[0] == None:
        window.blit(ToolbarTile, [x, y])
    else:
        window.blit(CheckboxChecked, [x, y])
    achievementFont = pygame.font.Font(None, 20)
    achieve1 = achievementFont.render("Beginning - Start a World", 1, (0, 0, 0))
    window.blit(achieve1, [x + 20, y])
    if world_type == False:
        if achievements[1] == None:
            window.blit(ToolbarTile, [x, y + 25])
        else:
            window.blit(CheckboxChecked, [x, y + 25])
        achieve2 = achievementFont.render("Explorer - Find a cave", 1, (0, 0, 0))
        window.blit(achieve2, [x + 20, y + 25])
    if blocksMined >= 100:
        achievements[2] = True
    if achievements[2] == None:
        window.blit(ToolbarTile, [x, y + 50])
    else:
        window.blit(CheckboxChecked, [x, y + 50])
    achieve3 = achievementFont.render("Miner - Mine 100 Blocks", 1, (0, 0, 0))
    window.blit(achieve3, [x + 20, y + 50])
    
pygame.init()
version = "0.1.1"
window = pygame.display.set_mode([480, 480])
window.fill([128, 128, 128])
pygame.display.set_caption("Deeper " + version)
pygame.display.set_icon(pygame.image.load("DeeperIcon.jpg"))
Mouse = mouse((0, 0))
mouseGrp = pygame.sprite.Group()
world = pygame.sprite.Group()
minedBlocks = pygame.sprite.Group()
allBlocks = pygame.sprite.Group()
lighting = pygame.sprite.Group()
blocklighting = pygame.sprite.Group()
mouseGrp.add(Mouse)
menuButton = button("Start", [200, 200], "gray", None)
exitButton = button("Exit", [205, 250], "red", None)
goButton = button("Go!", [200, 200], "green", 5)
basicButton = button("Change World Type", [125, 275], "gray", 26)
gamemenu = in_game_menu()
running = True
GameMenu = False
world_type = True
playerSpawned = False
clicked = False
player = None
screen = 'menu'
yVelocity = 1
playerMove = 0
playerMoveX = 0
chosenBlock = 0
playerWhere = 'bottom'
Toolbar = list(toolbarData)
achievements = [None, None, None]
toolbarFile = open("toolbar.dat", "w")
mouseevent = 0
blocksMined = 0

print "Deeper v" + version +" Alpha"
print "We are in Alpha Testing!"
print "Due to that, some feautures may not exist/work properly."

while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.MOUSEMOTION:
            Mouse.rect.centerx = i.pos[0]
            Mouse.rect.centery = i.pos[1]
        elif i.type == pygame.MOUSEBUTTONDOWN:
            mouseevent = pygame.mouse.get_pressed()
            if mouseevent[0] == 1:
                clicked = True
                if screen == 'menu':
                    menuButton.checkmouse()
                    menuButton.click()
                    exitButton.checkmouse()
                    exitButton.click()
                    if menuButton.clicked:
                        screen = 'new_world'
                    elif exitButton.clicked:
                        running = False
                elif screen == 'new_world':
                    goButton.checkmouse()
                    goButton.click()
                    basicButton.checkmouse()
                    basicButton.click()
                    if goButton.clicked:
                        screen = 'generating'
                    if basicButton.clicked:
                        if world_type:
                            world_type = False
                        elif not world_type:
                            world_type = True
                        basicButton.clicked = False
                elif screen == 'in_game':
                    if not GameMenu:
                        if pygame.sprite.spritecollide(Mouse, world, False) and MouseTriggerZone(player.rect.centerx - 55, player.rect.centery - 55, player.rect.centerx + 55, player.rect.centery + 55):
                            world.update('mine')
                        elif pygame.sprite.spritecollide(Mouse, minedBlocks, False) and MouseTriggerZone(player.rect.centerx - 55, player.rect.centery - 55, player.rect.centerx + 55, player.rect.centery + 55):
                            minedBlocks.update('mine')
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_e:
                if GameMenu:
                    GameMenu = False
                else:
                    GameMenu = True
            if not GameMenu:
                if i.key == pygame.K_LEFT or i.key == pygame.K_a:
                    playerMoveX = -2
                elif i.key == pygame.K_RIGHT or i.key == pygame.K_d:
                    playerMoveX = 2
            elif i.key == pygame.K_1:
                chosenBlock = 0
            elif i.key == pygame.K_2:
                chosenBlock = 1
            elif i.key == pygame.K_3:
                chosenBlock = 2
            elif i.key == pygame.K_4:
                chosenBlock = 3
            elif i.key == pygame.K_5:
                chosenBlock = 4
            elif i.key == pygame.K_0:
                if not int(Toolbar[chosenBlock]) == (len(blockImages) - 1):
                    Toolbar[chosenBlock] = int(Toolbar[chosenBlock]) + 1
                else:
                    Toolbar[chosenBlock] = 0
            if not GameMenu:
                if i.key == pygame.K_SPACE:
                    if screen == "in_game":
                        player.update("jump")

    if screen == 'menu':
        menu()
    elif screen == 'new_world':
        new_world()
    elif screen == 'generating':
        generate_world(world_type)
    elif screen == 'in_game':
        display_world()
        lighting.update()
        if not world_type:
            player.update('cavecheck')
        else:
            player.update(None)
        window.blit(player.real_image, [player.rect.centerx, player.rect.centery])
        if GameMenu:
            gamemenu.display()
    pygame.display.flip()
    playerMoveX = 0
    clicked = False
pickle.dump(Toolbar, toolbarFile)
toolbarFile.close()
pygame.quit()
