import json
import asyncio
import threading
import arcade
from entities import Player

WINDOW_X = 1920
WINDOW_Y = 1080
TITLE = "Project X"


class GameWindow(arcade.Window):
    menuActive = True
    menuItemSelected = 0
    titlescreenItems = ["Host Game", "Join Game", "Options", "Exit"]
    menuItems = titlescreenItems
    server = None

    optionsMenuActive = False
    optionsMenuItems = ["Back"]

    gameActive = False
    colorDict = {
        "grey": arcade.color.ASH_GREY,
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

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.set_fullscreen(True)
        self.level = None
        self.levels = {
            "Stalingrad": "stalingrad.json",
        }
        self.entities = []
        self.enemies = None
        self.player = None

    def on_draw(self):
        if self.player is not None and self.gameActive:
            self.player.update()
            for x in self.entities:
                x.update()

        arcade.start_render()

        if self.menuActive:
            self.draw_menu()
        if self.optionsMenuActive:
            self.draw_options_menu()
        if self.gameActive:
            self.draw_game()
            self.collisions(
                self.player, self.level["objects"])
        arcade.finish_render()

    # Draws a menu screen using arcade functions and is able to move around with the wasd keys
    # if the menuItem is selected, it will be highlighted
    def draw_menu(self):
        # draw title text
        arcade.draw_text("Project X", WINDOW_X / 2, WINDOW_Y /
                         2 + 200, arcade.color.WHITE, 100, anchor_x="center")
        # draw menu items
        for i in range(len(self.menuItems)):
            if i == self.menuItemSelected:
                arcade.draw_text(self.menuItems[i], WINDOW_X / 2, WINDOW_Y /
                                 2 - 70 * i, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.menuItems[i], WINDOW_X / 2, WINDOW_Y /
                                 2 - 70 * i, arcade.color.BLACK, 50, anchor_x="center")

    def draw_options_menu(self):
        for i in range(len(self.optionsMenuItems)):
            arcade.draw_text("WASD to move around", WINDOW_X / 2, WINDOW_Y /
                             2 + 200, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("WS and UP and DOWN to move through menu", WINDOW_X / 2,
                             WINDOW_Y / 2 + 100, arcade.color.BLACK, 50, anchor_x="center")
            arcade.draw_text("ENTER to select menu item", WINDOW_X / 2,
                             WINDOW_Y / 2, arcade.color.BLACK, 50, anchor_x="center")
            if i == self.menuItemSelected:
                arcade.draw_text(self.optionsMenuItems[i], WINDOW_X / 2, WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.WHITE, 50, anchor_x="center")
            else:
                arcade.draw_text(self.optionsMenuItems[i], WINDOW_X / 2, WINDOW_Y / 2 - (
                    100 * i)-100, arcade.color.BLACK, 50, anchor_x="center")

    # uses a series of functions to draw the game
    def draw_game(self):
        self.draw_level()
        self.draw_entities()
        self.draw_player()

    # draws a level defined in the levels dictionary which references a json file
    def draw_level(self):
        with open("assets\\levels\\" + self.levels["Stalingrad"]) as level:
            self.level = json.load(level)
        for i in self.level["objects"]:
            x = i["x"]
            y = i["y"]
            width = i["width"]
            height = i["height"]
            arcade.draw_rectangle_filled(
                x+(width/2), y+(height/2), width, height, self.colorDict[i["color"]])

    def draw_player(self):
        if self.player is None:
            self.player = Player(self)
        width = self.player.width
        height = self.player.height
        x = self.player.center_x
        y = self.player.center_y
        # placeholder for the player is a box
        arcade.draw_rectangle_filled(
            x, y+(height/2), width, height, arcade.color.RED)

    def draw_entities(self):
        for i in self.entities:
            x = i.center_x
            y = i.center_y
            width = i.width
            height = i.height
            color = i.color
            arcade.draw_rectangle_filled(x, y, width, height, color)

    def collisions(self, player, objects: list):
        # return the x and y speeds to make the player not collide with the objects it is colliding with
        for i in objects:
            if i["collision"] == True:
                if player.center_y - (player.height/2) > i["y"] and player.center_y - (player.height/2) < i["y"] + i["height"] and player.center_x + (player.width / 2) > i["x"] and player.center_x - (player.width / 2) < i["x"] + i["width"]:
                    if player.change_y < 0:
                        player.change_y = 0
                        player.center_y = i["y"] + i["height"]
                        player.in_air = False
                        player.on_ground = True
            else:
                player.in_air = True
                player.on_ground = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and self.menuActive:
            if self.menuItems[self.menuItemSelected] == "Host Game":
                self.menuItemSelected = 0
                self.menuActive = False
                self.gameActive = True
            if self.menuItems[self.menuItemSelected] == "Options":
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
                self.player.shoot()


if __name__ == "__main__":
    window = GameWindow(WINDOW_X, WINDOW_X, TITLE)
    arcade.run()

