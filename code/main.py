import json
import os
import random
import threading
import arcade
from GraphicsEngine import GraphicsEngine
from entities import Player, PowerUp

WINDOW_X = 1920
WINDOW_Y = 1080
TITLE = "Project X"


class GameWindow(arcade.Window):
    menuActive = True
    menuItemSelected = 0
    titlescreenItems = ["Host Game", "Join Game",
                        "Split screen", "Controls", "Exit"]
    menuItems = titlescreenItems
    server = None

    optionsMenuActive = False
    optionsMenuItems = ["Back"]
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
            "Stalingrad": "stalingrad.json",
        }
        self.entities = []
        self.powerups = []
        self.scores = []
        self.player2 = None
        self.player = None

    def on_draw(self):
        if self.splitScreen:
            if len(self.powerups) <2:
                if random.randint(0, 100) == 1:
                    self.powerups.append(self.createPowerup())
            if self.player is not None and self.gameActive:
                self.player.update()
            if self.player2 is not None and self.gameActive:
                self.player2.update()
            for x in self.entities:
                x.update()
        else:
            if self.player is not None and self.gameActive:
                self.player.update()
                for x in self.entities:
                    x.update()

        if self.graphicsEngine is None:
            self.graphicsEngine = GraphicsEngine(self, WINDOW_X, WINDOW_Y)

        arcade.start_render()

        if self.menuActive:
            self.graphicsEngine.draw_menu()
        if self.optionsMenuActive:
            self.graphicsEngine.draw_options_menu()
        if self.gameActive:
            self.graphicsEngine.draw_game()
            self.collisions(
                self.player, self.level["objects"])
            self.getEntityCollisions(self.player, self.entities)
            self.getPowerUpCollisions(self.player, self.powerups)
            if self.splitScreen:
                self.collisions(
                    self.player2, self.level["objects"])
                self.getEntityCollisions(self.player2, self.entities)
                self.getPowerUpCollisions(self.player2, self.powerups)
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
            if i.center_x > player.center_x - (player.width / 2) and i.center_x < player.center_x + (player.width / 2) and i.center_y - (i.height/2) < player.center_y + (player.height / 2) and i.center_y + i.height > player.center_y:
                # if the entity is colliding with the player, remove the entity and deal damage to the player
                player.powerup = i.powerup
                if player.powerup == "shotgun":
                    player.powerupCounter = 10
                elif player.powerup == "line":
                    player.powerupCounter = 3
                self.powerups.remove(i)
    
    def collisions(self, player, objects: list):
        # return the x and y speeds to make the player not collide with the objects it is colliding with
        for i in objects:
            if i["collision"] == True:
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
                player.in_air = True
                player.on_ground = False

    def createPowerup(self):
        powerup = PowerUp(self,0,0,50,50)
        notcolliding = []
        while True:
            powerup.center_x = random.randint(0, WINDOW_X)
            powerup.center_y = random.randint(0, WINDOW_Y)
            for x in self.level["objects"]:
                if powerup.center_x > x["x"] and powerup.center_x < x["x"] + x["width"] and powerup.center_y - (powerup.height/2) < x["y"] + x["height"] and powerup.center_y + powerup.height > x["y"]:
                # if powerup.center_x - powerup.width/2 > x["x"] - x["width"]/2 and powerup.center_x + powerup.width/2 < x["x"] + x["width"]/2 and powerup.center_y - powerup.height/2 < x["y"] + x["height"]/2 and powerup.center_y + powerup.height/2 > x["y"] - x["height"]/2:
                    notcolliding.append(False)
                    continue
                else:
                    notcolliding.append(True)
            if False in notcolliding:
                notcolliding = []
            else:
                break
        self.powerups.append(powerup)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and self.menuActive:
            if self.menuItems[self.menuItemSelected] == "Host Game":
                self.host = True
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True
                threading.Thread(target=os.system, args=(
                    "python code/connection.py host",)).start()
            if self.menuItems[self.menuItemSelected] == "Join Game":
                self.host = False
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True
                threading.Thread(target=os.system, args=(
                    "python code/connection.py join",)).start()
            if self.menuItems[self.menuItemSelected] == "Split screen":
                self.splitScreen = True
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True

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
        # change the menu item selected
        elif self.menuActive or self.optionsMenuActive:
            if (key == arcade.key.W or key == arcade.key.UP) and self.menuItemSelected > 0:
                self.menuItemSelected -= 1
            if (key == arcade.key.S or key == arcade.key.DOWN) and self.menuItemSelected < len(self.menuItems) - 1:
                self.menuItemSelected += 1
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

        # multiplayer controls
        else:
            if key == arcade.key.W:
                if self.player.in_air:
                    self.player.change_y += 12
                else:
                    self.player.change_y = 10
            if key == arcade.key.S:
                if self.player.in_air:
                    self.player.change_y -= 12
                else:
                    self.player.change_y = -10
            if key == arcade.key.A:
                self.player.facing = "left"
                if self.player.in_air:
                    self.player.change_x -= 12
                else:
                    self.player.change_x = -10
            if key == arcade.key.D:
                self.player.facing = "right"
                if self.player.in_air:
                    self.player.change_x += 12
                else:
                    self.player.change_x = 10
            if key == arcade.key.SPACE:
                self.player.updatePowerup()
                if self.player.powerup == "line":
                    self.player.shoot(200, 15, 7)
                elif self.player.powerup == "shotgun":
                    for i in range(-20, 21, 20):
                        self.player.shoot(5, 15, 20, i/10, i)
                else:
                    self.player.shoot(5, 15, 20)


if __name__ == "__main__":
    with open("playerPositions.json", "r") as f:
        playerPositions = json.load(f)
    with open("code\\playerPositions.json", "w") as f:
        json.dump(playerPositions, f, indent=4)
    window = GameWindow(WINDOW_X, WINDOW_X, TITLE)
    arcade.run()
    # shtudown the server
    os.system("taskkill /f /im python.exe")
