from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from random import choice

WIDTH, HEIGHT = 500, 700
Window.size = (WIDTH, HEIGHT)

class CarGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.road_width = 300
        self.road_x = WIDTH // 2 - self.road_width // 2
        self.car_width, self.car_height = 50, 90
        self.car_x = WIDTH // 2 - self.car_width // 2
        self.car_y = 20
        self.obstacle_width, self.obstacle_height = 50, 90
        self.obstacle_speed = 8
        self.obstacles = []
        self.lanes = [self.road_x + 25, self.road_x + self.road_width//2 - 25, self.road_x + self.road_width - 75]
        self.score = 0
        self.game_over = False
        self.frame_count = 0

        with self.canvas:
            Color(0, 0.5, 0, 1)
            Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=(self.road_x, 0), size=(self.road_width, HEIGHT))
            Color(0.8, 0, 0, 1)
            self.car = Rectangle(pos=(self.car_x, self.car_y), size=(self.car_width, self.car_height))

        self.score_label = Label(text='Score: 0', pos=(10, HEIGHT - 50), size_hint=(None, None))
        self.add_widget(self.score_label)
        Clock.schedule_interval(self.update, 1/60)

    def on_touch_down(self, touch):
        if self.game_over:
            self.restart_game()
            return
        if touch.x < WIDTH/2 and self.car_x > self.road_x + 5:
            self.car_x -= 40
        elif touch.x > WIDTH/2 and self.car_x < self.road_x + self.road_width - self.car_width - 5:
            self.car_x += 40
        self.car.pos = (self.car_x, self.car_y)

    def spawn_obstacle(self):
        lane = choice(self.lanes)
        with self.canvas:
            Color(0, 0, 0, 1)
            obs = Rectangle(pos=(lane, HEIGHT), size=(self.obstacle_width, self.obstacle_height))
            self.obstacles.append([lane, HEIGHT, obs])

    def check_collision(self, car_x, car_y, obs_x, obs_y):
        return (car_x < obs_x + self.obstacle_width and
                car_x + self.car_width > obs_x and
                car_y < obs_y + self.obstacle_height and
                car_y + self.car_height > obs_y)

    def update(self, dt):
        if self.game_over: return
        self.frame_count += 1
        if self.frame_count % 50 == 0: self.spawn_obstacle()

        for obs in self.obstacles[:]:
            obs[1] -= self.obstacle_speed
            obs[2].pos = (obs[0], obs[1])
            if obs[1] < -self.obstacle_height:
                self.canvas.remove(obs[2])
                self.obstacles.remove(obs)
                self.score += 1
                self.score_label.text = f'Score: {self.score}'
                if self.score % 10 == 0: self.obstacle_speed += 0.5
            if self.check_collision(self.car_x, self.car_y, obs[0], obs[1]):
                self.game_over = True
                self.game_over_label = Label(text=f'Game Over!\nScore: {self.score}\nTap to Restart',
                                             center=(WIDTH/2, HEIGHT/2))
                self.add_widget(self.game_over_label)

    def restart_game(self):
        for obs in self.obstacles:
            self.canvas.remove(obs[2])
        self.obstacles = []
        self.car_x = WIDTH // 2 - self.car_width // 2
        self.car.pos = (self.car_x, self.car_y)
        self.score = 0
        self.obstacle_speed = 8
        self.game_over = False
        self.remove_widget(self.game_over_label)
        self.score_label.text = 'Score: 0'

class CarRunApp(App):
    def build(self):
        return CarGame()

if __name__ == '__main__':
    CarRunApp().run()