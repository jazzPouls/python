from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window

class SnakePart(Widget):
    pass

class GameScreen(Widget):
    step_size = 40
    movement_x = 0
    movement_y = 0
    snake_parts = []

    def new_game(self):
        self.snake_parts = []
        self.movement_x = 0
        self.movement_y = 0
        head = SnakePart()
        head.pos = (0,0)
        self.snake_parts.append(head)
        self.add_widget(head)

    def on_touch_up(self, touch):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        if abs(dx) > abs(dy):
            self.movement_y = 0
            if dx > 0:
                self.movement_x = self.step_size
            else:
                self.movement_x = - self.step_size
        else:
            self.movement_x = 0
            if dy > 0:
                self.movement_y = self.step_size
            else:
                self.movement_y = - self.step_size

    def collides_widget(self, wid1, wid2):
        if wid1.right <= wid2.x:
            return False
        if wid1.x >= wid2.right:
            return False
        if wid1.top <= wid2.y:
            return False
        if wid1.y >= wid2.top:
            return False
        return True

    def next_frame(self, *args):

        #Move the Snake
        head = self.snake_parts[0]
        food = self.ids.food
        last_x = head.x
        last_y = head.y
        head.x += self.movement_x
        head.y += self.movement_y

        #move the body
        for part in self.snake_parts[1:]:
            part.x, last_x = last_x, part.x
            part.y, last_y = last_y, part.y

        # check for snake colliding with food
        if self.collides_widget(head,food):
            food.x = randint(0, Window.width-food.width)
            food.y = randint(0, Window.height-food.height)
            new_part = SnakePart()
            new_part.x = last_x
            new_part.y = last_y
            self.snake_parts.append(new_part)
            self.add_widget(new_part)

        #check for snake colliding with Snake
        for part in self.snake_parts[1:]:
            if self.collides_widget(head,part):
                self.new_game()
        #check for snake colliding with wall
        if not self.collides_widget(self,head):
            self.new_game()
        pass

    pass

class MainApp(App):
    def on_start(self):
        self.root.new_game()

        Clock.schedule_interval(self.root.next_frame, .25)
    pass

MainApp().run()
