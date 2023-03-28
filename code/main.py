from os import listdir
import random
import time
import arcade
from GraphicsEngine import GraphicsEngine
from entities import Player, PowerUp
from controlHandler import MenuController, PlayerController

WINDOW_X = 1920
WINDOW_Y = 1080
TITLE = "Project X"


class GameWindow(arcade.Window):
    menuController = None
    menuActive = True
    menuItemSelected = 0
    titlescreenItems = ["Split screen", "Map select",
                        "Map preview", "Controls", "Exit"]
    menuItems = titlescreenItems

    optionsMenuActive = False
    optionsMenuItems = ["Back"]

    mapSelectItems = []
    mapSelectActive = False

    mapPreviewActive = False

    graphicsEngine = None
    gameActive = False
    splitScreen = False
    colorDict = {
        "grey": arcade.color.ASH_GREY,
        "aspargus": arcade.color.GRAY_ASPARAGUS,
        "green": arcade.color.GREEN,
        "blue": arcade.color.LIGHT_BLUE,
        "red": arcade.color.RED,
        "yellow": arcade.color.YELLOW,
        "black": arcade.color.BLACK,
        "white": arcade.color.WHITE,
        "brown": arcade.color.BROWN,
        "orange": arcade.color.ORANGE,
        "purple": arcade.color.PURPLE,
        "pink": arcade.color.PINK,
        "cyan": arcade.color.CYAN,
    }

    damage = {
        "line": 50,
        "shotgun": 10,
        "None": 10,
    }

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.set_fullscreen(True)
        self.level = None
        self.levels = {
            "stalingrad": "stalingrad.json",
        }
        self.entities = []
        self.powerups = []
        self.scores = []
        self.player = None
        self.playerController = None
        self.player2 = None
        self.player2Controller = None

        self.mapSelectItems = [f for f in listdir(
            "assets\\levels\\") if f.endswith(".json")]
        for x in self.mapSelectItems:
            if len(x)-5 > 15:
                self.mapSelectItems[self.mapSelectItems.index(
                    x)] = x[:15]+"..."
            else:
                self.mapSelectItems[self.mapSelectItems.index(x)] = x[:-5]
        print(self.mapSelectItems)
        self.selectedMap = self.mapSelectItems[0]

    def on_draw(self):
        if self.splitScreen:
            for x in self.powerups:
                if time.time()-x[1] > 10:
                    self.powerups.remove(x)

            if len(self.powerups) < 2:
                if random.randint(0, 100) == 1:
                    self.createPowerup()
            if self.player is not None and self.gameActive:
                self.player.update()
            if self.player2 is not None and self.gameActive:
                self.player2.update()
            for x in self.entities:
                x.update()

        if self.graphicsEngine is None:
            self.graphicsEngine = GraphicsEngine(self, WINDOW_X, WINDOW_Y)

        arcade.start_render()

        if self.menuActive:
            self.graphicsEngine.draw_menu()
        if self.optionsMenuActive:
            self.graphicsEngine.draw_options_menu()
        if self.mapSelectActive:
            self.graphicsEngine.draw_map_select()
            arcade.draw_text("Map Select", WINDOW_X/2, WINDOW_Y -
                             100, arcade.color.WHITE, 30, anchor_x="center")
        if self.mapPreviewActive:
            try:
                arcade.draw_text("There's an error in your json", WINDOW_X/2,
                                 WINDOW_Y/2, arcade.color.BLACK, 30, anchor_x="center")
                self.graphicsEngine.draw_level()
                arcade.draw_text("Map Preview", WINDOW_X/2, WINDOW_Y -
                                 100, arcade.color.BLACK, 30, anchor_x="center")
            except:
                pass
        if self.gameActive:
            self.graphicsEngine.draw_game()
            self.collisions(
                self.player, self.level["objects"])
            self.getEntityCollisions(self.player, self.entities)
            if self.powerups != [] and self.splitScreen:
                self.getPowerUpCollisions(self.player, self.powerups)
                self.getPowerUpCollisions(self.player2, self.powerups)
            if self.splitScreen:
                self.collisions(
                    self.player2, self.level["objects"])
                self.getEntityCollisions(self.player2, self.entities)

        arcade.finish_render()

    def getEntityCollisions(self, player: Player, entities: list):
        for i in entities:
            collided = False
            # check if the entity is the player
            if i.ownerID == player.id:
                # if it is, continue with he next entity
                continue
            # check if the player is colliding with the left side of the entity
            if (player.center_x + (player.width / 2) > i.__dict__["center_x"] and player.center_x + (player.width/2) < i.__dict__["center_x"]+50) and (player.center_y + player.height > i.__dict__["center_y"] and player.center_y < i.__dict__["center_y"] + i.__dict__["height"]-5):
                collided = True
            # check if the player is colliding with the right side of the entity
            elif (player.center_x - (player.width / 2) < i.__dict__["center_x"]+i.__dict__["width"] and player.center_x - player.width > i.__dict__["center_x"]+i.__dict__["width"]-50) and (player.center_y + player.height > i.__dict__["center_y"] and player.center_y < i.__dict__["center_y"] + i.__dict__["height"]-5):
                collided = True
            if collided:
                # if the entity is colliding with the player, remove the entity and deal damage to the player
                player.hp -= self.damage[i.powerup]
                if player.hp <= 0:
                    self.scores[i.ownerID] += 1
                self.entities.remove(i)

    def getPowerUpCollisions(self, player: Player, powerups: list):
        for i in powerups:
            # check if the powerup is colliding with the player
            if i[0].center_x > player.center_x - (player.width / 2) and i[0].center_x < player.center_x + (player.width / 2) and i[0].center_y - (i[0].height/2) < player.center_y + (player.height / 2) and i[0].center_y + i[0].height > player.center_y:
                # if the entity is colliding with the player, remove the entity and deal damage to the player
                player.powerup = i[0].powerup
                if player.powerup == "shotgun":
                    player.powerupCounter = 10
                elif player.powerup == "line":
                    player.powerupCounter = 3
                self.powerups.remove(i)

    def collisions(self, player: Player, objects: list):
        # return the x and y speeds to make the player not collide with the objects it is colliding with
        frictionlist = []
        for i in objects:
            if i["collision"] == True:
                if i["platform"]:
                    if player.center_y > i["y"] and player.center_y < i["y"] + i["height"]+10 and (player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]):
                        frictionlist.append(True)
                        if player.change_y < 0:
                            if player.change_y < -7:
                                player.change_y = 5
                            else:
                                player.center_y = i["y"] + (i["height"])
                                player.change_y = 0
                    else:
                        frictionlist.append(False)
                else:
                    # check if the player is colliding with the left side of the object
                    if (player.center_x + (player.width / 2) > i["x"] and player.center_x + (player.width/2) < i["x"]+50) and (player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5):
                        frictionlist.append(True)
                        player.center_x = i["x"] - (player.width/2)
                        player.change_x = 0
                    # check if the player is colliding with the right side of the object
                    elif (player.center_x - (player.width / 2) < i["x"]+i["width"] and player.center_x - player.width > i["x"]+i["width"]-50) and (player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5):
                        frictionlist.append(True)
                        player.center_x = i["x"] + \
                            i["width"] + (player.width/2)
                        player.change_x = 0
                    # check if the player is colliding with the top of the object
                    elif player.center_y > i["y"] and player.center_y < i["y"] + i["height"]+10 and (player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]):
                        frictionlist.append(True)
                        if player.change_y < 0:
                            if player.change_y < -7:
                                player.change_y = 5
                            else:
                                player.center_y = i["y"] + (i["height"])
                                player.change_y = 0
                    else:
                        frictionlist.append(False)

        if True in frictionlist:
            player.on_ground = True
            player.in_air = False
        else:
            player.on_ground = False
            player.in_air = True

    def createPowerup(self):
        powerup = PowerUp(self, 0, 0, 50, 50)
        notcolliding = []
        while True:
            powerup.center_x = random.randint(0, WINDOW_X)
            powerup.center_y = random.randint(0, WINDOW_Y)
            for x in self.level["objects"]:
                if powerup.center_x < x["x"] and powerup.center_x > x["x"] + x["width"] and powerup.center_y - (powerup.height/2) > x["y"] + x["height"] and powerup.center_y + powerup.height < x["y"]:
                    # if powerup.center_x - powerup.width/2 > x["x"] - x["width"]/2 and powerup.center_x + powerup.width/2 < x["x"] + x["width"]/2 and powerup.center_y - powerup.height/2 < x["y"] + x["height"]/2 and powerup.center_y + powerup.height/2 > x["y"] - x["height"]/2:
                    notcolliding.append(False)
                    continue
                else:
                    notcolliding.append(True)
            if False in notcolliding:
                notcolliding = []
            else:
                break
        self.powerups.append((powerup, time.time()))

    def on_key_press(self, key, modifiers):
        if self.menuController is None:
            self.menuController = MenuController(self, [(arcade.key.W, "up"), (arcade.key.S, "down"), (
                arcade.key.A, "left"), (arcade.key.D, "right"), (arcade.key.ENTER, "enter"), (arcade.key.ESCAPE, "back")])
        if key == self.menuController.controlDict["select"] and self.menuActive:
            if self.menuItems[self.menuItemSelected] == "Split screen":
                self.splitScreen = True
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True

            if self.menuItems[self.menuItemSelected] == "Map select":
                self.menuItemSelected = 0
                self.menuActive = False
                self.mapSelectActive = True
                self.menuItems = self.mapSelectItems

            if self.menuItems[self.menuItemSelected] == "Map preview":
                self.menuItemSelected = 0
                self.menuActive = False
                self.mapPreviewActive = True

            if self.menuItems[self.menuItemSelected] == "Controls":
                self.menuItemSelected = 0
                self.menuActive = False
                self.optionsMenuActive = True
                self.menuItems = self.optionsMenuItems
            if self.menuItems[self.menuItemSelected] == "Exit":
                arcade.close_window()
        elif key == self.menuController.controlDict["select"] and self.optionsMenuActive:
            if self.optionsMenuItems[self.menuItemSelected] == "Back":
                self.menuItemSelected = 0
                self.menuActive = True
                self.optionsMenuActive = False
                self.menuItems = self.titlescreenItems
        elif key == self.menuController.controlDict["select"] and self.mapSelectActive:
            self.selectedMap = self.menuItems[self.menuItemSelected]
            self.menuItemSelected = 0
            self.menuActive = True
            self.mapSelectActive = False
            self.menuItems = self.titlescreenItems
        # change the menu item selected
        elif self.menuActive or self.optionsMenuActive:
            self.menuController.handle_input(key)
        elif self.mapSelectActive:
            if key == self.menuController.controlDict["back"]:
                self.menuItemSelected = 0
                self.menuActive = True
                self.mapSelectActive = False
                self.menuItems = self.titlescreenItems
            else:
                self.menuController.handle_input(key)
        elif self.mapPreviewActive:
            if key == self.menuController.controlDict["back"]:
                self.menuItemSelected = 0
                self.menuActive = True
                self.mapPreviewActive = False
                self.menuItems = self.titlescreenItems

        if self.gameActive and self.splitScreen:
            if key == self.menuController.controlDict["back"]:
                # go back to the menu
                self.menuActive = True
                self.gameActive = False
                self.splitScreen = False
                self.player = None
                self.player2 = None
                self.playerController = None
                self.player2Controller = None
                self.menuItems = self.titlescreenItems
                self.menuItemSelected = 0
                self.powerups = []
                self.scores = []
                self.entities = []

            # player 1 controls
            if self.playerController is not None:
                if self.player is not None:
                    self.playerController.handle_input(key)
            else:
                if self.player is not None:
                    self.playerController = PlayerController(self, self.player, [(
                        arcade.key.W, "up"), (arcade.key.S, "down"), (arcade.key.A, "left"), (arcade.key.D, "right"), (arcade.key.SPACE, "shoot")])

            # player 2 controls
            if self.player2Controller is not None:
                if self.player2 is not None:
                    self.player2Controller.handle_input(key)
            else:
                if self.player2 is not None:
                    self.player2Controller = PlayerController(self, self.player2, [(
                        arcade.key.UP, "up"), (arcade.key.DOWN, "down"), (arcade.key.LEFT, "left"), (arcade.key.RIGHT, "right"), (arcade.key.ENTER, "shoot")])


if __name__ == "__main__":
    window = GameWindow(WINDOW_X, WINDOW_X, TITLE)
    arcade.run()
