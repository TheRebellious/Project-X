from os import listdir
import random
import time
import arcade
from GraphicsEngine import GraphicsEngine
from entities import Player, PowerUp

WINDOW_X = 1920
WINDOW_Y = 1080
TITLE = "Project X"


class GameWindow(arcade.Window):
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
        self.player2 = None
        self.player = None
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
            # check if the entity is the player
            if i.ownerID == player.id:
                # if it is, continue with he next entity
                continue
            # check if the entity is colliding with the player
            if i.center_x > player.center_x - (player.width / 2) and i.center_x < player.center_x + (player.width / 2) and i.center_y - (i.height/2) < player.center_y + (player.height / 2) and i.center_y + i.height > player.center_y:
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

    def collisions(self, player, objects: list):
        # return the x and y speeds to make the player not collide with the objects it is colliding with
        for i in objects:
            if i["collision"] == True:
                if i["platform"]:
                    if player.center_y - (player.height/2) > i["y"] and player.center_y - (player.height/2) < i["y"] + i["height"] and player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]:
                        if player.change_y < 0:
                            if player.change_y < -7:
                                player.change_y = 5
                            else:
                                player.change_y = 0
                            player.center_y = i["y"] + i["height"]
                            player.in_air = False
                            player.on_ground = True
                    else:
                        player.on_ground = False
                        player.in_air = True
                else:
                    print((player.center_x + (player.width / 2) > i["x"] and player.center_x + (player.width/2) < i["x"]+50) and (
                        player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5))
                    print((player.center_x - (player.width / 2) < i["x"]+i["width"] and player.center_x - player.width > i["x"]+i["width"]-50) and (
                        player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5))
                    print((player.center_y + (player.height / 2) > i["y"] and player.center_y + (player.height/2) < i["y"]+50) and (
                        player.center_x + player.width > i["x"] and player.center_x < i["x"] + i["width"]-5))
                    # check if the player is colliding with the left side of the object
                    if (player.center_x + (player.width / 2) > i["x"] and player.center_x + (player.width/2) < i["x"]+50) and (player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5):
                        player.center_x = i["x"] - (player.width/2)
                        player.change_x = 0
                        player.in_air = False
                        player.on_ground = True
                    # check if the player is colliding with the right side of the object
                    elif (player.center_x - (player.width / 2) < i["x"]+i["width"] and player.center_x - player.width > i["x"]+i["width"]-50) and (player.center_y + player.height > i["y"] and player.center_y < i["y"] + i["height"]-5):
                        player.center_x = i["x"] + \
                            i["width"] + (player.width/2)
                        player.change_x = 0
                        player.in_air = False
                        player.on_ground = True
                    # check if the player is colliding with the top of the object
                    elif player.center_y - (player.height/2) > i["y"] and player.center_y - (player.height/2) < i["y"] + i["height"]+10 and (player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]):
                        if player.change_y < 0:
                            if player.change_y < -7:
                                player.change_y = 5
                            else:
                                player.center_y = i["y"] + (i["height"])
                                player.change_y = 0
                            player.in_air = False
                            player.on_ground = True
                    else:
                        player.in_air = True
                        player.on_ground = False
                    print(player.in_air, player.on_ground)

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
        if key == arcade.key.ENTER and self.menuActive:
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
        elif key == arcade.key.ENTER and self.optionsMenuActive:
            if self.optionsMenuItems[self.menuItemSelected] == "Back":
                self.menuItemSelected = 0
                self.menuActive = True
                self.optionsMenuActive = False
                self.menuItems = self.titlescreenItems
        elif key == arcade.key.ENTER and self.mapSelectActive:
            self.selectedMap = self.menuItems[self.menuItemSelected]
            self.menuItemSelected = 0
            self.menuActive = True
            self.mapSelectActive = False
            self.menuItems = self.titlescreenItems
        # change the menu item selected
        elif self.menuActive or self.optionsMenuActive:
            if (key == arcade.key.W or key == arcade.key.UP) and self.menuItemSelected > 0:
                self.menuItemSelected -= 1
            if (key == arcade.key.S or key == arcade.key.DOWN) and self.menuItemSelected < len(self.menuItems) - 1:
                self.menuItemSelected += 1
        elif self.mapSelectActive:
            if key == arcade.key.ESCAPE:
                self.menuItemSelected = 0
                self.menuActive = True
                self.mapSelectActive = False
                self.menuItems = self.titlescreenItems
            if key == arcade.key.W or key == arcade.key.UP:
                if self.menuItemSelected > 0:
                    self.menuItemSelected -= 4
                    if self.menuItemSelected < 0:
                        self.menuItemSelected = 0
            if key == arcade.key.S or key == arcade.key.DOWN:
                if self.menuItemSelected < len(self.menuItems) - 1:
                    self.menuItemSelected += 4
                    if self.menuItemSelected > len(self.menuItems) - 1:
                        self.menuItemSelected = len(self.menuItems) - 1
            if key == arcade.key.A or key == arcade.key.LEFT:
                if self.menuItemSelected > 0:
                    self.menuItemSelected -= 1
            if key == arcade.key.D or key == arcade.key.RIGHT:
                if self.menuItemSelected < len(self.menuItems) - 1:
                    self.menuItemSelected += 1
        elif self.mapPreviewActive:
            if key == arcade.key.ESCAPE:
                self.menuItemSelected = 0
                self.menuActive = True
                self.mapPreviewActive = False
                self.menuItems = self.titlescreenItems

        if self.gameActive and self.splitScreen:
            if key == arcade.key.T:
                self.player.powerupCounter = 3
                self.player2.powerupCounter = 3
                self.player.powerup = "line"
                self.player2.powerup = "line"
            if key == arcade.key.Y:
                self.player.powerupCounter = 10
                self.player2.powerupCounter = 10
                self.player.powerup = "shotgun"
                self.player2.powerup = "shotgun"
            if key == arcade.key.ESCAPE:
                # go back to the menu
                self.menuActive = True
                self.gameActive = False
                self.splitScreen = False
                self.player = None
                self.player2 = None
                self.menuItems = self.titlescreenItems
                self.menuItemSelected = 0
                self.powerups = []
                self.scores = []
                self.entities = []

            # player 1 controls
            if self.player is not None:
                if key == arcade.key.W:
                    if self.player.in_air:
                        self.player.change_y += 12
                    else:
                        self.player.change_y = 10
                elif key == arcade.key.S:
                    if self.player.in_air:
                        self.player.change_y -= 12
                    else:
                        self.player.change_y = -10
                elif key == arcade.key.A:
                    self.player.facing = "left"
                    if self.player.in_air:
                        self.player.change_x -= 12
                    else:
                        self.player.change_x = -10
                elif key == arcade.key.D:
                    self.player.facing = "right"
                    if self.player.in_air:
                        self.player.change_x += 12
                    else:
                        self.player.change_x = 10
                elif key == arcade.key.SPACE:
                    self.player.updatePowerup()
                    if self.player.powerup == "line":
                        self.player.shoot(200, 15, 7, 0, 0, "line")
                    elif self.player.powerup == "shotgun":
                        for i in range(-20, 21, 20):
                            self.player.shoot(5, 15, 20, i/10, i, "shotgun")
                    else:
                        self.player.shoot(5, 15, 20)

            # player 2 controls
            if self.player2 is not None:
                if key == arcade.key.UP:
                    if self.player2.in_air:
                        self.player2.change_y += 12
                    else:
                        self.player2.change_y = 10
                elif key == arcade.key.DOWN:
                    if self.player2.in_air:
                        self.player2.change_y -= 12
                    else:
                        self.player2.change_y = -10
                elif key == arcade.key.LEFT:
                    self.player2.facing = "left"
                    if self.player2.in_air:
                        self.player2.change_x -= 12
                    else:
                        self.player2.change_x = -10
                elif key == arcade.key.RIGHT:
                    self.player2.facing = "right"
                    if self.player2.in_air:
                        self.player2.change_x += 12
                    else:
                        self.player2.change_x = 10
                elif key == arcade.key.ENTER:
                    self.player2.updatePowerup()
                    if self.player2.powerup == "line":
                        self.player2.shoot(200, 15, 7, 0, 0, "line")
                    elif self.player2.powerup == "shotgun":
                        for i in range(-20, 21, 20):
                            self.player2.shoot(5, 15, 20, i/10, i, "shotgun")
                    else:
                        self.player2.shoot(5, 15, 20)


if __name__ == "__main__":
    window = GameWindow(WINDOW_X, WINDOW_X, TITLE)
    arcade.run()
