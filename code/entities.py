import arcade


class Player():
    def __init__(self, window: arcade.Window, id, scale=1, gravity=0.25, friction=0.5, color="asparagus") -> None:
        super().__init__()
        self.window = window
        self.facing = "right"
        self.in_air = True
        self.width = 50 * scale
        self.height = 50 * scale
        self.center_x = 1920/2
        self.center_y = 700
        self.change_x = 0
        self.change_y = 0
        self.gravity = gravity
        self.friction = friction
        self.on_ground = False
        self.color = self.window.colorDict[color]
        self.id = id

    def update(self):
        if self.center_x > self.window._width or self.center_x < 0:
            self.change_x = 0
        if self.center_y > self.window._height or self.center_y < 0:
            self.change_y = 0
        if self.center_x + (self.width/2) > self.window._width:
            self.center_x = self.window._width - (self.width/2)
        if self.center_x - (self.width/2) < 0:
            self.center_x = (self.width/2)
        if self.change_x > 10:
            self.change_x = 10
        elif self.change_x < -10:
            self.change_x = -10
        if self.change_y > 10:
            self.change_y = 10
        elif self.change_y < -10:
            self.change_y = -10
        if self.on_ground and self.change_x > 0.01:
            self.change_x -= self.friction
        elif self.on_ground and self.change_x < -0.01:
            self.change_x += self.friction
        if self.in_air:
            self.change_y -= self.gravity
        self.center_y += self.change_y
        self.center_x += self.change_x

    def shoot(self):
        if self.facing == "right":
            self.window.entities.append(
                Entity(self.window, self.center_x, self.center_y+(self.height/2), 15, 5, 20, 0, arcade.color.RED))
        else:
            self.window.entities.append(
                Entity(self.window, self.center_x, self.center_y+(self.height/2), 15, 5, -20, 0, arcade.color.RED))


class Entity():

    def __init__(self, window: arcade.Window, x, y, width, height, change_x, change_y, color) -> None:
        super().__init__()
        self.window = window
        self.width = width
        self.height = height
        self.center_x = x
        self.center_y = y
        self.change_x = change_x
        self.change_y = change_y
        self.color = color

    def update(self):
        if self.center_x > self.window._width or self.center_x < 0:
            self.window.entities.remove(self)
        self.center_x += self.change_x
        self.center_y += self.change_y
