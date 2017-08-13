import pygame, random, datetime, pickle, time, os, webbrowser
from pygame.color import THECOLORS
blockImages = ["stone.png", "dirt.png", "coalore.png", "ironore.png", "goldore.png", "clay.png", "bricks.png", "mud.png", "grass.png", "lamp.png", "legacypc.png", "craftshelf.png", "crate.png"]
itemImages = ["Pickaxe.png"]
Background = pygame.image.load("Background.png")
Logo = pygame.image.load("DeeperIcon.jpg")
ToolbarTile = pygame.image.load("ToolbarTile.png")
CheckboxChecked = pygame.image.load("CheckboxChecked.png")
OrionDark7 = pygame.image.load("OrionDark7.png")
toolbarFile = []
cavePos = []
crafting = False

#Deeper - v0.3.1:
#Release Notes:
# Multiple World Saving System! you can find your worlds in the ./worlds folder.
# Major GUI Improvements.
# Added a new menu, which has the value of 'choose_world'.
# New menu allows you to choose either 'Load World' or 'New World'.
# Re-created new world menu.
# Added load world menu.

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
    def findBlock(self):
        global Toolbar, item, screen
        itemNotFound = True
        for i in Toolbar:
            if not i == None:
                if i.type == "block" and i.image == blockImages[self.id] and itemNotFound and screen == 'in_game' and i.quantity < 99:
                    if i.quantity < 99:
                        if not Toolbar[chosenBlock] == None:
                            if Toolbar[chosenBlock].image == 'Pickaxe.png' and random.randint(1, 10) > 5:
                                i.quantity += 2
                            else:
                                i.quantity += 1
                        else:
                           i.quantity += 1
                    itemNotFound = False
        return itemNotFound
    def newBlock(self):
        global screen, Toolbar, item, chosenBlock
        if screen == 'in_game':
            if not Toolbar[chosenBlock] == None:
                if Toolbar[chosenBlock].image == 'Pickaxe.png' and random.randint(1, 10) > 5:
                    Toolbar[Toolbar.index(None)] = item(self.id, True, 2)
                else:
                    Toolbar[Toolbar.index(None)] = item(self.id, True, 1)
            else:
                Toolbar[Toolbar.index(None)] = item(self.id, True, 1)
    def mine(self):
        global minedBlocks, player, blocksMined, screen, Toolbar, item
        if not self.rect.centerx <= player.rect.centerx - 50 or self.rect.centerx >= player.rect.centerx + 50 or self.rect.centery <= player.rect.centery - 50 or self.rect.centery >= player.rect.centery + 50:
            self.kill()
            minedBlocks.add(self)
            allBlocks.add(self)
            self.mined = True
            itemNotFound = None
            if screen == 'in_game':
                blocksMined += 1
                itemNotFound = self.findBlock()
                if itemNotFound:
                    try:
                        self.newBlock()
                    except:
                        pass

    def place(self):
        global world, chosenBlock, Toolbar, player, blockImages
        if not self.rect.centerx <= player.rect.centerx - 50 or self.rect.centerx >= player.rect.centerx + 50 or self.rect.centery <= player.rect.centery - 50 or self.rect.centery >= player.rect.centery + 50:
            self.kill()
            world.add(self)
            allBlocks.add(self)
            self.image = pygame.image.load(Toolbar[chosenBlock].image)
            self.id = blockImages.index(Toolbar[chosenBlock].image)
            Toolbar[chosenBlock].use(1)
            self.mined = False
            if self.id == 9:
                blocklighting.add(self)

    def transfer(self):
        global saveblock
        saveBlock = saveblock(self.id, self.mined, [self.rect.centerx, self.rect.centery])
        return saveBlock
    def update(self, action, *sl):
        self.activate()
        global player, yVelocity, playerMove, playerMoveX, LegacyPC, pcOn, pcMenu, world, blockImages, Toolbar, chosenBlock, crafting, blocklighting
        if action == 'mine':
            if self.activated and not self.mined:
                self.mine()
                if self in blocklighting:
                    blocklighting.pop(blocklighting.index(self))
            elif not Toolbar[chosenBlock] == None:
                if self.activated and self.mined and Toolbar[chosenBlock].type == "block":
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
                self.kill()
                minedBlocks.add(self)
                allBlocks.add(self)
                self.mined = True
        elif action == 'interact' and not self.mined and self.activated:
            if self.id == 10:
                if pcOn:
                    pcOn = False
                else:
                    pcOn = True
                    pcMenu = "home"
                    LegacyPC.using = self.rect.centerx, self.rect.centery
            elif self.id == 11 and not crafting:
                crafting = True
        elif action == 'BuildX':
            for y in range(5):
                if LegacyPC.using[1] == self.rect.centery + (y * 10) - 20:
                    for x in range(5):
                        if LegacyPC.using[0] == self.rect.centerx + (x * 10) - 20:
                            Y = 4 - y
                            X = 4 - x
                            if LegacyPC.buildXdata[Y][X] == "NoneBlock.png":
                                self.kill()
                                minedBlocks.add(self)
                                allBlocks.add(self)
                                self.mined = True
                            else:
                                self.kill()
                                world.add(self)
                                allBlocks.add(self)
                                self.image = pygame.image.load(LegacyPC.buildXdata[Y][X])
                                self.id = blockImages.index(LegacyPC.buildXdata[Y][X].lower())
                                self.mined = False
                                if self.id == 9:
                                    blocklighting.add(self)
                        if LegacyPC.using[0] == self.rect.centerx and LegacyPC.using[1] == self.rect.centery and not self.id == 10:
                            pcOn = False
                        elif LegacyPC.using[0] == self.rect.centerx and LegacyPC.using[1] == self.rect.centery and self.mined:
                            pcOn = False

class saveblock():
    def __init__(self, ID, mined, position):
        self.id = ID
        self.mined = mined
        self.x, self.y = position
    def transfer(self):
        newBlock = block([self.x, self.y], self.id)
        if self.mined:
            newBlock.mined = True
        return newBlock

class item():
    def __init__(self, ID, Type, amount):
        global blockImages, itemImages
        if Type:
            self.image = blockImages[ID]
            self.type = "block"
        else:
            self.image = itemImages[ID]
            self.type = "item"
        if amount == 0:
            self.quantity = 1
        else:
            self.quantity = amount
    def use(self, times):
        global chosenBlock, Toolbar
        if not times == None:
            self.quantity -= times
        else:
            self.quantity -= 1
        if self.quantity <= 0:
            Toolbar[Toolbar.index(self)] = None

class craftingRecipe():
    def __init__(self, item, parts):
        self.item = item
        self.parts = parts
    def craft(self):
        global Toolbar
        foundItems = 0
        for i in self.parts:
            for j in Toolbar:
                if not j == None:
                    if i.quantity <= j.quantity and i.type == j.type and i.image == j.image:
                        foundItems += 1
                        j.use(i.quantity)
                        break
        if foundItems == len(self.parts):
            returnItem = self.item
        else:
            returnItem = None
        return returnItem

toolbarOld = []

def loadToolbar():
    global toolbarFile, toolbarOld
    toolbarFile = open("toolbar.dat", "r")
    toolbarData = pickle.load(toolbarFile)
    toolbarOld = toolbarData
    toolbarFile.close()
def dumpToolbar():
    global item, toolbarOld
    toolbarFile = open("toolbar.dat", "w")
    items = [item(0, False, 1), item(11, True, 1), None, None, None]
    toolbarOld = items
    pickle.dump(items, toolbarFile)

try:
    loadToolbar()
except:
    dumpToolbar()

worldLoaded = True
tutorialAccess = True

def loadWorlds():
    files = os.listdir('./worlds')
    new_files = []
    for i in files:
        if str(i).endswith('.deep'):
            new_files.append(i)
    return new_files

worlds = loadWorlds()

try:
    tutorialFile = open("./worlds/tutorial.deep", "r")
except:
    tutorialAccess = False

if tutorialAccess:
    tutorialData = pickle.load(tutorialFile)
    tutorialFile.close()

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
        self.font = pygame.font.Font("PixelFJVerdana12pt.TTF", 10)
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
        self.length = len(self.text) * 10 + 5 + self.excess_trim

    def display(self):
        global window
        window.blit(self.base, [self.rect.centerx - 5, self.rect.centery - 5])
        window.blit(self.surface, [self.rect.centerx, self.rect.centery])

    def checkmouse(self):
        global Mouse, MouseTriggerZone
        if MouseTriggerZone(self.rect.centerx, self.rect.top, self.rect.centerx + self.length, self.rect.bottom):
            self.activated = True
        else:
            self.activated = False
    def click(self):
        if self.activated:
            self.clicked = True
    def update(self, addclick):
        self.checkmouse()
        self.display()
        if addclick:
            self.click()

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
        self.upButton = pygame.image.load("UpButton.png")
        self.downButton = pygame.image.load("DownButton.png")
    def display(self):
        global window, blockImages, chosenBlock, toolbar, Toolbar, name
        window.blit(self.dimSurf, [0, 0])
        window.blit(self.image, [self.rect.centerx, self.rect.centery])
        MenuFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
        if not Toolbar[chosenBlock] == None:
            toolbartext = MenuFont.render(str(list(Toolbar[chosenBlock].image.split(".png"))[0]).capitalize(), 0, (0, 0, 0))
            window.blit(toolbartext, [225, 125])
        toolbar(125, 125)
        Achievements(125, 200)
        currenttext = MenuFont.render("Current World: "+name, 0, (0, 0, 0))
        window.blit(currenttext, [125, 345])
    def displayCraft(self):
        global window, Toolbar, craftClose, craftMenu, MouseTriggerZone, currentCraft, craftingRecipes
        window.blit(self.dimSurf, [0, 0])
        window.blit(self.image, [self.rect.centerx, self.rect.centery])
        window.blit(self.upButton, [125, 150])
        window.blit(self.downButton, [125, 170])
        MenuFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
        toolbar(125, 125)
        craftClose.checkmouse()
        craftClose.display()
        craftButton.checkmouse()
        craftButton.display()
        window.blit(pygame.image.load(craftingRecipes[currentCraft].item.image), [215, 160])

class textbox(pygame.sprite.Sprite):
    def __init__(self, width):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.surface.Surface([int(width), 30])
        self.rect = self.surf.get_rect()
        self.surf.fill([255, 255, 255])
        self.keys = ""
    def update(self, position):
        window.blit(self.surf, position)
        font = pygame.font.Font("PixelFJVerdana12pt.TTF", 10)
        text = font.render(self.keys, 1, (0, 0, 0))
        window.blit(text, [position[0]+2, position[1]+3])
    def write(self, key):
        if not len(self.keys) == 27:
            if key == 'space':
                self.keys = self.keys + " "
            elif key == 'backspace':
                self.keys = self.keys[0:len(self.keys) - 1]
            elif not key == 'right shift' and not key == 'left shift' and not key == 'return':
                self.keys = self.keys + str(key)
            elif key == 'backspace':
                self.keys = self.keys[0:len(self.keys) - 1]

class pcScreen(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.surface.Surface([240, 180])
        self.image2 = pygame.surface.Surface([280, 250])
        self.image2 = self.image2.convert()
        self.quitUI = pygame.image.load("ShutdownButton.png")
        self.quitUI2 = pygame.image.load("ShutdownButton2.png")
        self.buildX = pygame.image.load("BuildX.png")
        self.HomeButton = pygame.image.load("HomeButton.png")
        self.eraseButton = pygame.image.load("EraseButton.png")
        self.optionsButton = pygame.image.load("options.png")
        self.upButton = pygame.image.load("UpButton.png")
        self.downButton = pygame.image.load("DownButton.png")
        self.buildXdata = list([["Stone.png", "Stone.png", "Stone.png", "Stone.png", "Stone.png"], ["Stone.png", "Stone.png", "Stone.png", "Stone.png", "Stone.png"], ["Stone.png", "Stone.png", "LegacyPC.png", "Stone.png", "Stone.png"], ["Stone.png", "Stone.png", "Stone.png", "Stone.png", "Stone.png"], ["Stone.png", "Stone.png", "Stone.png", "Stone.png", "Stone.png"]])
        self.rect = self.image2.get_rect()
        self.rect.centerx, self.rect.centery = 120, 120
        self.image.fill([20, 20, 20])
        self.image2.fill([239, 228, 176])
        self.dimSurf = pygame.surface.Surface([480, 480])
        self.dimSurf.set_alpha(100)
        self.screen = "home"
        self.using = 5, 5
        self.eraser = False
        self.screenRGB = [150, 150, 150]
    def display(self, screen):
        global MouseTriggerZone, clicked, pcMenu, toolbar, blockImages, chosenBlock, Toolbar, buildXgenerate, allBlocks
        self.screen = str(screen)
        Font = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
        MonitorText = Font.render("LegacyPC", 1, (232, 216, 138))
        window.blit(self.dimSurf, [0, 0])
        window.blit(self.image2, [self.rect.centerx - 20, self.rect.centery - 20])
        if self.screen == "home":
            self.image.fill(self.screenRGB)
            window.blit(self.image, [self.rect.centerx, self.rect.centery])
            window.blit(self.quitUI2, [self.rect.centerx + 59, self.rect.centery])
            window.blit(self.buildX, [self.rect.centerx, self.rect.centery])
            window.blit(self.optionsButton, [self.rect.centerx + 79, self.rect.centery])
            if MouseTriggerZone(self.rect.centerx + 59, self.rect.centery, self.rect.centerx + 79, self.rect.centery + 20) and clicked:
                pcMenu = "off"
            elif MouseTriggerZone(self.rect.centerx, self.rect.centery, self.rect.centerx + 58, self.rect.centery + 20) and clicked:
                pcMenu = "BuildX"
            elif MouseTriggerZone(self.rect.centerx + 79, self.rect.centery, self.rect.centerx + 137, self.rect.centery + 20) and clicked:
                pcMenu = "Options"
        elif self.screen == "BuildX":
            self.image.fill([200, 200, 200])
            window.blit(self.image, [self.rect.centerx, self.rect.centery])
            BuildXtitle = Font.render("BuildX 1.0", 1, (0, 0, 0))
            window.blit(BuildXtitle, [self.rect.centerx + 5, self.rect.centery + 5])
            toolbar(self.rect.centerx + 5, self.rect.centery + 25)
            window.blit(self.HomeButton, [self.rect.centerx + 220, self.rect.centery])
            buildXgenerate.checkmouse()
            buildXgenerate.display()
            window.blit(self.eraseButton, [self.rect.centerx + 80, self.rect.centery + 25])
            for y in range(5):
                for x in range(5):
                    BlockImg = pygame.image.load(self.buildXdata[y][x])
                    window.blit(BlockImg, [self.rect.centerx + (x * 10) + 5, self.rect.centery + (y * 10) + 50])
                    if MouseTriggerZone(self.rect.centerx + (x * 10) + 5, self.rect.centery + (y * 10) + 50, self.rect.centerx + (x * 10) + 15, self.rect.centery + (y * 10) + 60) and clicked:
                        if self.eraser or Toolbar[chosenBlock] == None:
                            BlockImg = pygame.image.load("NoneBlock.png")
                            self.buildXdata[y][x] = "NoneBlock.png"
                        else:
                            if Toolbar[chosenBlock].type == 'block':
                                BlockImg = pygame.image.load(Toolbar[chosenBlock].image)
                                self.buildXdata[y][x] = Toolbar[chosenBlock].image
                                Toolbar[chosenBlock].use(1)
                    else:
                        BlockImg = pygame.image.load(self.buildXdata[y][x])
                    window.blit(BlockImg, [self.rect.centerx + (x * 10) + 5, self.rect.centery + (y * 10) + 50])
            if self.eraser:
                pygame.draw.rect(window, (0, 255, 255), (self.rect.centerx + 80, self.rect.centery + 45, 20, 2))
            if MouseTriggerZone(self.rect.centerx + 220, self.rect.centery, self.rect.centerx + 235, self.rect.centery + 15) and clicked:
                pcMenu = "home"
            elif MouseTriggerZone(self.rect.centerx + 80, self.rect.centery + 25, self.rect.centerx + 100, self.rect.centery + 45) and clicked:
                if self.eraser:
                    self.eraser = False
                else:
                    self.eraser = True
            elif buildXgenerate.activated and clicked:
                pcMenu = "BuildX Generate"
        elif self.screen == "BuildX Generate":
            self.image.fill([200, 200, 200])
            window.blit(self.image, [self.rect.centerx, self.rect.centery])
            allBlocks.update("BuildX", [self.rect.centerx, self.rect.centery])
            pcMenu = "BuildX"
        elif self.screen == "Options":
            self.image.fill([150, 150, 150])
            window.blit(self.image, [self.rect.centerx, self.rect.centery])
            ScrColor = Font.render("Screen Color", 1, (0, 0, 0))
            window.blit(ScrColor, [self.rect.centerx + 5, self.rect.centery + 5])
            Red = Font.render(str(self.screenRGB[0]), 1, (0, 0, 0))
            window.blit(Red, [self.rect.centerx + 5, self.rect.centery + 30])
            window.blit(self.upButton, [self.rect.centerx + 45, self.rect.centery + 30])
            window.blit(self.downButton, [self.rect.centerx + 45, self.rect.centery + 40])
            Green = Font.render(str(self.screenRGB[1]), 1, (0, 0, 0))
            window.blit(Green, [self.rect.centerx + 65, self.rect.centery + 30])
            window.blit(self.upButton, [self.rect.centerx + 105, self.rect.centery + 30])
            window.blit(self.downButton, [self.rect.centerx + 105, self.rect.centery + 40])
            Blue = Font.render(str(self.screenRGB[2]), 1, (0, 0, 0))
            window.blit(Blue, [self.rect.centerx + 125, self.rect.centery + 30])
            window.blit(self.upButton, [self.rect.centerx + 165, self.rect.centery + 30])
            window.blit(self.downButton, [self.rect.centerx + 165, self.rect.centery + 40])
            if MouseTriggerZone(self.rect.centerx + 45, self.rect.centery + 30, self.rect.centerx + 65, self.rect.centery + 39) and clicked and self.screenRGB[0] < 255:
                self.screenRGB[0] += 15
            elif MouseTriggerZone(self.rect.centerx + 45, self.rect.centery + 40, self.rect.centerx + 65, self.rect.centery + 49) and clicked and self.screenRGB[0] > 0:
                self.screenRGB[0] -= 15
            if MouseTriggerZone(self.rect.centerx + 105, self.rect.centery + 30, self.rect.centerx + 125, self.rect.centery + 39) and clicked and self.screenRGB[1] < 255:
                self.screenRGB[1] += 15
            elif MouseTriggerZone(self.rect.centerx + 105, self.rect.centery + 40, self.rect.centerx + 125, self.rect.centery + 49) and clicked and self.screenRGB[1] > 0:
                self.screenRGB[1] -= 15
            if MouseTriggerZone(self.rect.centerx + 165, self.rect.centery + 30, self.rect.centerx + 185, self.rect.centery + 39) and clicked and self.screenRGB[2] < 255:
                self.screenRGB[2] += 15
            elif MouseTriggerZone(self.rect.centerx + 165, self.rect.centery + 40, self.rect.centerx + 185, self.rect.centery + 49) and clicked and self.screenRGB[2] > 0:
                self.screenRGB[2] -= 15
        elif self.screen == "off":
            self.image.fill([20, 20, 20])
            window.blit(self.image, [self.rect.centerx, self.rect.centery])
        window.blit(self.quitUI, [self.rect.centerx + 220, self.rect.centery + 195])
        window.blit(MonitorText, [self.rect.centerx + 70, self.rect.centery + 195])
    def quitUIclicked(self):
        global MouseTriggerZone
        if MouseTriggerZone(self.rect.centerx + 220, self.rect.centery + 195, self.rect.centerx + 235, self.rect.centery + 210):
            isclicked = True
        else:
            isclicked = False
        return isclicked

def loading():
    global window
    window.fill((0, 0, 0))
    window.blit(OrionDark7, [221, 221])
    font = pygame.font.Font("PixelFJVerdana12pt.TTF", 10)
    urlfont = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
    credit = font.render("Built by OrionDark7", 1, (255, 255, 255))
    url = urlfont.render("http://oriondark7.com", 1, (255, 255, 255))
    window.blit(credit, [160, 265])
    window.blit(url, [190, 290])
    pygame.display.flip()

def menu():
    global window, Logo
    background()
    window.blit(Logo, [150, 60])
    textFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 15)
    textRender = textFont.render("Deeper", 1, (255, 255, 255))
    window.blit(textRender, [225, 75])
    menuButton.update(False)
    exitButton.update(False)
    helpButton.update(False)
    webButton.update(False)
    window.blit(OrionDark7, [2, 440])
    pygame.display.flip()

def help_menu():
    global window
    background()
    textFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 15)
    smallFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 7)
    helpText = textFont.render("Deeper Help Center", 1, (255, 255, 255))
    text1 = smallFont.render("Deeper is a 2D Sandbox Game about mining, building, & exploring.", 1, (255, 255, 255))
    text2 = smallFont.render("Press A & D to move, and press space to jump.", 1, (255, 255, 255))
    text3 = smallFont.render("To mine blocks, click on a block in range.", 1, (255, 255, 255))
    text4 = smallFont.render("To place blocks, click on an empty space in range.", 1, (255, 255, 255))
    text5 = smallFont.render("To access your toolbar & achievements, press E.", 1, (255, 255, 255))
    text6 = smallFont.render("To change the items, go to your toolbar, and click on the item.", 1, (255, 255, 255))
    text7 = smallFont.render("To interact with blocks, right-click on the block.", 1, (255, 255, 255))
    window.blit(helpText, [100, 25])
    window.blit(text1, [25, 75])
    window.blit(text2, [25, 90])
    window.blit(text3, [25, 105])
    window.blit(text4, [25, 120])
    window.blit(text5, [25, 135])
    window.blit(text6, [25, 150])
    window.blit(text7, [25, 165])
    backButton.update(False)

def choose_world():
    background()
    titlefont = pygame.font.Font("PixelFJVerdana12pt.TTF", 20)
    title = titlefont.render("Choose World", 0, (255, 255, 255))
    window.blit(title, [110, 10])
    loadButton.update(False)
    newButton.update(False)
    backButton.update(False)
    pygame.display.flip()

def new_world():
    global world_type
    background()
    titlefont = pygame.font.Font("PixelFJVerdana12pt.TTF", 20)
    title = titlefont.render("New World", 0, (255, 255, 255))
    font = pygame.font.Font("PixelFJVerdana12pt.TTF", 10)
    worldType = font.render("World Type", 0, (255, 255, 255))
    worldName = font.render("World Name", 0, (255, 255, 255))
    window.blit(title, [140, 10])
    window.blit(worldName, [15, 137])
    window.blit(worldType, [15, 237])
    if world_type:
        window.blit(CheckboxChecked, [15, 278])
        window.blit(ToolbarTile, [15, 328])
        window.blit(ToolbarTile, [15, 378])
    if not world_type:
        window.blit(ToolbarTile, [15, 278])
        window.blit(CheckboxChecked, [15, 328])
        window.blit(ToolbarTile, [15, 378])
    if world_type == 'tutorial':
        window.blit(ToolbarTile, [15, 278])
        window.blit(ToolbarTile, [15, 328])
        window.blit(CheckboxChecked, [15, 378])
    box.update([10, 175])
    goButton.update(False)
    basicButton.update(False)
    minersButton.update(False)
    tutorialButton.update(False)
    backButton.update(False)
    pygame.display.flip()

def load_world():
    background()
    titlefont = pygame.font.Font("PixelFJVerdana12pt.TTF", 20)
    title = titlefont.render("Load World", 0, (255, 255, 255))
    font = pygame.font.Font("PixelFJVerdana12pt.TTF", 10)
    worldName = font.render("World Name", 0, (255, 255, 255))
    window.blit(worldName, [50, 200])
    window.blit(title, [130, 10])
    worldbox.update([50, 225])
    goButton2.update(False)
    backButton.update(False)
    pygame.display.flip()

def display_world():
    global world, window
    background()
    world.draw(window)

def Tutorial():
    global window, pygame
    if tutorialIndex <= int(len(tutorial) - 1):
        surface = pygame.surface.Surface((480, 50))
        surface.fill([128, 128, 128])
        font = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
        text = font.render(tutorial[tutorialIndex], 1, (0, 0, 0))
        window.blit(surface, [0, 430])
        window.blit(text, [5, 450])

def generate_world(Basic):
    Id = 0
    Coal = 0
    Iron = 0
    Gold = 0
    Airspace = 0
    Crate = 0
    global player, players, playerSpawned, world, screen, achievements, cavePos, Toolbar, toolbarData, worldData, blocklighting
    cavePos.append(int(random.randint(1, 42)))
    playerSpawnX = random.randint(0, 47)
    if Basic == 'load':
        for i in worldData:
            Block = i.transfer()
            if Block.rect.centery == 5 and Block.rect.centerx == (playerSpawnX * 10) + 5:
                player = Player([Block.rect.centerx - 2, Block.rect.centery - 5])
                playerSpawned = True
            else:
                if Block.mined:
                    minedBlocks.add(Block)
                else:
                    world.add(Block)
            if Block.id == 9 and not Block.mined:
                blocklighting.add(Block)
            allBlocks.add(Block)
            lightBlock = LightingBlock([Block.rect.centerx - 5, Block.rect.centery - 5])
            lighting.add(lightBlock)
    elif Basic == 'tutorial':
        for i in tutorialData:
            Block = i.transfer()
            if Block.rect.centery == 5 and Block.rect.centerx == (playerSpawnX * 10) + 5:
                player = Player([Block.rect.centerx - 2, Block.rect.centery - 5])
                playerSpawned = True
            else:
                if Block.mined:
                    minedBlocks.add(Block)
                else:
                    world.add(Block)
            if Block.id == 9 and not Block.mined:
                blocklighting.add(Block)
            allBlocks.add(Block)
            lightBlock = LightingBlock([Block.rect.centerx - 5, Block.rect.centery - 5])
            lighting.add(lightBlock)
    elif Basic:
        for y in range(48):
            for x in range(48):
                if y == 0 and x == playerSpawnX:
                    player = Player([x * 10 + 2, y * 10])
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
                    if Airspace > 5 and not cavePos[1] == y and not cavePos[2] == y and not cavePos[3] == y:
                        Id = None
                    elif Airspace <= 5 and not cavePos[1] == y and not cavePos[2] == y and not cavePos[3] == y:
                        Id = 0
                    else:
                        Id = None
                else:
                    Crate = random.randint(1, 100)
                    if Crate == 1:
                        Id = 12
                    elif y < 10:
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
    screen = "in_game"
    achievements[0] = True

def toolbar(x, y):
    global chosenBlock
    ItemFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
    if not Toolbar[0] == None:
        item1 = ItemFont.render(str(Toolbar[0].quantity), 1, (255, 255, 255))
    else:
        item1 = None
    if not Toolbar[1] == None:
        item2 = ItemFont.render(str(Toolbar[1].quantity), 1, (255, 255, 255))
    else:
        item2 = None
    if not Toolbar[2] == None:
        item3 = ItemFont.render(str(Toolbar[2].quantity), 1, (255, 255, 255))
    else:
        item3 = None
    if not Toolbar[3] == None:
       item4 = ItemFont.render(str(Toolbar[3].quantity), 1, (255, 255, 255))
    else:
        item4 = None
    if not Toolbar[4] == None:
        item5 = ItemFont.render(str(Toolbar[4].quantity), 1, (255, 255, 255))
    else:
        item5 = None
    window.blit(ToolbarTile, [x, y])
    if not Toolbar[0] == None:
        window.blit(pygame.image.load(Toolbar[0].image), [x + 2, y + 2])
        window.blit(item1, [x - 2, y  - 2])
    else:
        Toolbar[0] = None
    window.blit(ToolbarTile, [x + 15, y])
    if MouseTriggerZone(x, y, x + 14, y + 14) and clicked:
        chosenBlock = 0
    if not Toolbar[1] == None:
        window.blit(pygame.image.load(Toolbar[1].image), [x + 17, y + 2])
        window.blit(item2, [x + 13, y - 2])
    else:
        Toolbar[1] = None
    window.blit(ToolbarTile, [x + 30, y])
    if MouseTriggerZone(x + 15, y, x + 29, y + 14) and clicked:
        chosenBlock = 1
    if not Toolbar[2] == None:
        window.blit(pygame.image.load(Toolbar[2].image), [x + 32, y + 2])
        window.blit(item3, [x + 28, y - 2])
    else:
        Toolbar[2] = None
    window.blit(ToolbarTile, [x + 45, y])
    if MouseTriggerZone(x + 30, y, x + 44, y + 14) and clicked:
        chosenBlock = 2
    if not Toolbar[3] == None:
        window.blit(pygame.image.load(Toolbar[3].image), [x + 47, y + 2])
        window.blit(item4, [x + 43, y - 2])
    else:
        Toolbar[3] = None
    window.blit(ToolbarTile, [x + 60, y])
    if MouseTriggerZone(x + 45, y, x + 59, y + 14) and clicked:
        chosenBlock = 3
    if not Toolbar[4] == None:
        window.blit(pygame.image.load(Toolbar[4].image), [x + 62, y + 2])
        window.blit(item5, [x + 58, y - 2])
    else:
        Toolbar[4] = None
    if MouseTriggerZone(x + 60, y, x + 74, y + 14) and clicked:
        chosenBlock = 4
    pygame.draw.rect(window, (0, 255, 255), (x + (chosenBlock * 15), y + 14, 14, 2))
def Achievements(x, y):
    global CheckboxChecked, blocksMined
    if achievements[0] == None:
        window.blit(ToolbarTile, [x, y])
    else:
        window.blit(CheckboxChecked, [x, y])
    achievementFont = pygame.font.Font("PixelFJVerdana12pt.TTF", 5)
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
version = "0.3.1"
window = pygame.display.set_mode([480, 480])
pygame.display.set_caption("Deeper " + version)
pygame.display.set_icon(pygame.image.load("DeeperIcon.jpg"))
Mouse = mouse((0, 0))
LegacyPC = pcScreen()
mouseGrp = pygame.sprite.Group()
world = pygame.sprite.Group()
minedBlocks = pygame.sprite.Group()
allBlocks = pygame.sprite.Group()
lighting = pygame.sprite.Group()
blocklighting = pygame.sprite.Group()
mouseGrp.add(Mouse)
gamemenu = in_game_menu()
webButton = button("Website", [400, 450], "gray", 0)
menuButton = button("Start", [200, 200], "gray", -5)
helpButton = button("Help", [202, 250], "gray", 0)
exitButton = button("Exit", [205, 300], "red", -5)
backButton = button("Back", [15, 15], "red", 3)
goButton = button("Go!", [15, 425], "green", 0)
goButton2 = button("Go!", [380, 230], "green", 0)
nextTutorialButton = button("Next", [420, 445], "green", 0)
doneTutorialButton = button("Done", [415, 445], "green", 5)
basicButton = button("Basic World", [44, 275], "gray", -10)
newButton = button("New World", [120, 240], "gray", 5)
loadButton = button("Load World", [240, 240], "gray", 0)
minersButton = button("Miner's World", [44, 325], "gray", -15)
tutorialButton = button("Tutorial World", [44, 375], "gray", -20)
buildXgenerate = button("Generate", [LegacyPC.rect.centerx + 10, LegacyPC.rect.centery + 150], "gray", 5)
craftClose = button("X", [gamemenu.rect.centerx + 215, gamemenu.rect.centery + 10], "red", 4)
craftButton = button("Craft", [160, 155], "gray", 15)
running = True
GameMenu = False
world_type = True
playerSpawned = False
clicked = False
pcOn = False
player = None
screen = 'loading'
pcMenu = "home"
yVelocity = 1
playerMove = 0
playerMoveX = 0
chosenBlock = 0
playerWhere = 'bottom'
lastscreen = ''
achievements = [None, None, None]
currentCraft = 0
tutorialIndex = 0
key_repeat = False
box = textbox(301)
box.keys = 'new world'
worldbox = textbox(301)

tutorial = ["Welcome to Deeper! Click Next to continue.", "Deeper is a game about exploring deeper, mining, and building.", "To start, try moving by pressing the A & D keys or arrow keys.", "See that? The little green guy moved! To make him jump, press the spacebar.", "Next, lets try mining. To mine a block, click it. It will be added to your inventory.", "To open your inventory, press E.", "When you are in your inventory, you can view your items, and achievements.", "In the top left corner are your items, to switch current items, just click it.", "You can also place blocks by clicking on any empty space.", "You can also interact wtih some blocks by right clicking them.", "That's about everything you need to know, you are about to exit the tutorial.", "If you have any questions, go to the help menu or contact @OrionDark7 on GitHub.", "Have fun!!!"]
craftingRecipes = [craftingRecipe(item(10, True, 1), [item(9, True, 4), item(3, True, 5)]), craftingRecipe(item(9, True, 4), [item(2, True, 3), item(4, True, 3)]), craftingRecipe(item(6, True, 4), [item(5, True, 4)]), craftingRecipe(item(8, True, 4), [item(1, True, 4)])]
toolbarFile = open("toolbar.dat", "w")
mouseevent = 0
blocksMined = 0

print "You're running Deeper " + version + " Alpha!"
print "We are in Alpha Testing!"
print "Due to that, some feautures may not exist/work properly."

while running:
    pygame.mouse.set_visible(False)
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
                    helpButton.checkmouse()
                    helpButton.click()
                    exitButton.checkmouse()
                    exitButton.click()
                    webButton.checkmouse()
                    webButton.click()
                    if menuButton.clicked:
                        screen = 'choose_world'
                        menuButton.clicked = False
                    elif helpButton.clicked:
                        screen = "help"
                        helpButton.clicked = False
                    elif exitButton.clicked:
                        running = False
                        exitButton.clicked = False
                    elif webButton.clicked:
                        web = webbrowser.open('http://oriondark7.com/deeper')
                        webButton.clicked = False
                elif screen == 'choose_world':
                    loadButton.checkmouse()
                    loadButton.click()
                    newButton.checkmouse()
                    newButton.click()
                    backButton.checkmouse()
                    backButton.click()
                    if loadButton.clicked:
                        world_type = 'load'
                        loadButton.clicked = False
                        screen = "load_world"
                    elif newButton.clicked:
                        newButton.clicked = False
                        screen = 'new_world'
                    elif backButton.clicked:
                        backButton.clicked = False
                        screen = 'menu'
                elif screen == 'new_world':
                    goButton.checkmouse()
                    goButton.click()
                    basicButton.checkmouse()
                    basicButton.click()
                    loadButton.checkmouse()
                    loadButton.click()
                    minersButton.checkmouse()
                    minersButton.click()
                    tutorialButton.checkmouse()
                    tutorialButton.click()
                    backButton.checkmouse()
                    backButton.click()
                    if goButton.clicked and pygame.sprite.spritecollide(goButton, mouseGrp, False):
                        if not box.keys+".deep" in worlds:
                            screen = 'generating'
                    if basicButton.clicked:
                        world_type = True
                        basicButton.clicked = False
                    if minersButton.clicked:
                        world_type = False
                        minersButton.clicked = False
                    if tutorialButton.clicked:
                        world_type = "tutorial"
                        tutorialButton.clicked = False
                    if backButton.clicked:
                        screen = 'choose_world'
                        backButton.clicked = False
                elif screen == 'load_world':
                    goButton2.checkmouse()
                    goButton2.click()
                    backButton.checkmouse()
                    backButton.click()
                    if goButton2.clicked:
                        if worldbox.keys+".deep" in worlds:
                            worldFile = open("./worlds/"+worldbox.keys+".deep", "r")
                            worldData = pickle.load(worldFile)
                            worldFile.close()
                            goButton.clicked = False
                            screen = 'generating'
                    elif backButton.clicked:
                        backButton.clicked = False
                        screen = 'choose_world'
                elif screen == 'help':
                    backButton.checkmouse()
                    backButton.click()
                    if backButton.clicked:
                        screen = 'menu'
                        backButton.clicked = False
                elif screen == 'in_game':
                    if crafting:
                        craftClose.checkmouse()
                        craftClose.click()
                        craftButton.checkmouse()
                        craftButton.click()
                        if MouseTriggerZone(125, 150, 145, 180):
                            if currentCraft == 0:
                                currentCraft = len(craftingRecipes) - 1
                            else:
                                currentCraft -= 1
                        elif MouseTriggerZone(125, 170, 145, 180):
                            if currentCraft == len(craftingRecipes) - 1:
                                currentCraft = 0
                            else:
                                currentCraft += 1
                        if craftClose.clicked:
                            crafting = False
                            craftClose.clicked = False
                        if craftButton.clicked:
                            findspot = False
                            try:
                                Toolbar[Toolbar.index(None)] = craftingRecipes[currentCraft].craft()
                            except:
                                findspot = True
                            if findspot:
                                for j in Toolbar:
                                    if j == None:
                                        pass
                                    elif j.image == craftingRecipes[currentCraft].item.image:
                                        j.quantity += craftingRecipes[currentCraft].item.quantity
                            craftButton.clicked = False
                    elif not GameMenu and not pcOn:
                        if pygame.sprite.spritecollide(Mouse, world, False) and MouseTriggerZone(player.rect.centerx - 55, player.rect.centery - 55, player.rect.centerx + 55, player.rect.centery + 55):
                            world.update('mine')
                        elif pygame.sprite.spritecollide(Mouse, minedBlocks, False) and MouseTriggerZone(player.rect.centerx - 55, player.rect.centery - 55, player.rect.centerx + 55, player.rect.centery + 55):
                            minedBlocks.update('mine')
                    elif pcOn:
                        if LegacyPC.quitUIclicked():
                            pcOn = False
                    if world_type == "tutorial":
                            nextTutorialButton.checkmouse()
                            nextTutorialButton.click()
                            doneTutorialButton.checkmouse()
                            doneTutorialButton.click()
                            if nextTutorialButton.clicked:
                                nextTutorialButton.clicked = False
                                tutorialIndex += 1
                            if doneTutorialButton.clicked:
                                doneTutorialButton.clicked = False
                                tutorialIndex += 1
            elif mouseevent[2] == 1:
                world.update('interact')
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_F11:
                print 'i'
                pygame.display.toggle_fullscreen()
            if screen == 'new_world':
                box.write(pygame.key.name(i.key))
                if len(box.keys) == 0:
                    pass
                elif box.keys in worlds:
                    pass
            elif screen == 'load_world':
                worldbox.write(pygame.key.name(i.key))
                if len(worldbox.keys) == 0:
                    pass
                elif not worldbox.keys in worlds:
                    pass
            elif screen == 'in_game':
                if i.key == pygame.K_e:
                    if GameMenu:
                        GameMenu = False
                    elif not crafting:
                        GameMenu = True
                if not GameMenu or pcOn:
                    if i.key == pygame.K_LEFT or i.key == pygame.K_a:
                        playerMoveX = -2
                    elif i.key == pygame.K_RIGHT or i.key == pygame.K_d:
                        playerMoveX = 2
                    if i.key == pygame.K_SPACE:
                        if screen == "in_game":
                            player.update("jump")
                if i.key == pygame.K_1:
                    chosenBlock = 0
                elif i.key == pygame.K_2:
                    chosenBlock = 1
                elif i.key == pygame.K_3:
                    chosenBlock = 2
                elif i.key == pygame.K_4:
                    chosenBlock = 3
                elif i.key == pygame.K_5:
                    chosenBlock = 4
    if screen == 'menu':
        menu()
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'loading':
        loading()
        time.sleep(3)
        screen = 'menu'
    elif screen == 'help':
        help_menu()
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'choose_world':
        choose_world()
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'load_world':
        load_world()
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'new_world':
        new_world()
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'generating':
        if not world_type == 'load':
            name = box.keys
        else:
            name = worldbox.keys
        Toolbar = toolbarOld
        generate_world(world_type)
        window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    elif screen == 'in_game':
        if not key_repeat:
            pygame.key.set_repeat(1, 50)
            key_repeat = True
        display_world()
        lighting.update()
        if not world_type:
            player.update('cavecheck')
        else:
            player.update(None)
        window.blit(player.real_image, [player.rect.centerx, player.rect.centery])
        if GameMenu and not pcOn:
            gamemenu.display()
        elif pcOn:
            LegacyPC.display(pcMenu)
        elif crafting:
            gamemenu.displayCraft()
        if world_type == "tutorial":
            Tutorial()
            if tutorialIndex < int(len(tutorial) - 1):
                nextTutorialButton.display()
            elif tutorialIndex < len(tutorial):
                doneTutorialButton.display()
        if not Toolbar[chosenBlock] == None and not crafting and not pcOn and not GameMenu:
            window.blit(pygame.image.load(Toolbar[chosenBlock].image), [Mouse.rect.centerx, Mouse.rect.centery])
        elif Toolbar[chosenBlock] == None or crafting or pcOn or GameMenu:
            window.blit(pygame.image.load("cursor.png"), [Mouse.rect.centerx, Mouse.rect.centery])
    pygame.display.flip()
    playerMoveX = 0
    clicked = False
if screen == "in_game":
    saveWorldFile = open("./worlds/"+name+".deep", "w")
    worldDataNew = []
    for i in allBlocks:
        worldDataNew.append(i.transfer())
    pickle.dump(worldDataNew, saveWorldFile)
    pickle.dump(Toolbar, toolbarFile)
    toolbarFile.close()
    saveWorldFile.close()
pygame.quit()
