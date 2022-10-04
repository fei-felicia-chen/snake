import sys
import pygame
import random
from pygame.math import Vector2


class SNAKE:
    def __init__(self):
        # 3 body blocks to start with
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.dir = Vector2(0, 0)
        self.growing = False
        self.eat_sound = pygame.mixer.Sound('eat.wav')
        
    def draw_snake(self):
        # draw each pixel for each part of the body
        for body_part in self.body:
            body_rect = pygame.Rect(int(body_part.x * cell_size),
                                    int(body_part.y * cell_size),
                                    cell_size, 
                                    cell_size)
            pygame.draw.rect(screen, (0, 121, 255), body_rect)
    
    def move_snake(self):
        if self.growing:
            # retain last part of snake and insert at moving direction
            body_copy = self.body[:]                
            body_copy.insert(0, body_copy[0] + self.  dir)
            self.body = body_copy[:]
            self.growing = False
        else:
            # remove last part of snake and insert at moving direction
            body_copy = self.body[:-1]                
            body_copy.insert(0, body_copy[0] + self.dir)
            self.body = body_copy[:]
    
    def grow(self):
        self.growing = True
        self.eat_sound.play()
    
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.dir = Vector2(0, 0)
        
class FRUIT:
    def __init__(self):
        # get random coordinates
        self.randomize()

    def draw_fruit(self):
        # draw a square at a random coordinate
        fruit_rect = pygame.Rect(
            int(self.coords.x * cell_size),
            int(self.coords.y * cell_size),
            cell_size,
            cell_size,
        )
        screen.blit(apple, fruit_rect)
        #pygame.draw.rect(screen, (126, 111, 114), fruit_rect)
        
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.coords = pygame.math.Vector2(self.x, self.y)
        

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_loss()
        
    def draw_elements(self):
        self.grass() 
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.score()
        
    def check_collision(self):
        # collision when snake is on fruit
        if self.fruit.coords == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow()

        # fruit cannot spawn on snake
        for part in self.snake.body[1:]:
            if part == self.fruit.coords:
                self.fruit.randomize()
        
    def check_loss(self):
        # lose when snake head hits a wall or itself
        if (not 0 <= self.snake.body[0].x < cell_number or
            not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()
            
        for part in self.snake.body[1:]:
            if part == self.snake.body[0]:
                self.game_over()
            
    def game_over(self):
        self.snake.reset()
        
    def grass(self):
        # grass pixels at every other pixel, diagonal
        grass_color = (234, 254, 222)
        for i in range(cell_number):
            if i & 1:
                for j in range(cell_number):
                    if j & 1:
                        grass_rect = pygame.Rect(j * cell_size,
                                                 i * cell_size,
                                                 cell_size,
                                                 cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for j in range(cell_number):
                    if not j & 1:
                        grass_rect = pygame.Rect(j * cell_size,
                                                 i * cell_size,
                                                 cell_size,
                                                 cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def score(self):
        user_score = len(self.snake.body) - 3
        score_draw = game_font.render(str(user_score), True,(0, 153, 0))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        coords = score_draw.get_rect(center = (score_x, score_y))
        apple_c = apple.get_rect(midright = (coords.left, coords.centery - 6))
        encadrer = pygame.Rect(apple_c.left - 4, apple_c.top - 4, apple_c.width + coords.width + 10, apple_c.height + 8)
        
        pygame.draw.rect(screen, (204, 255, 241), encadrer)
        screen.blit(score_draw, coords)
        screen.blit(apple, apple_c)
        pygame.draw.rect(screen, (56, 74, 12), encadrer, 2)
        
    def pause(self):
        paused = True
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
        
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,
                                  cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('apple.png').convert_alpha()
game_font = pygame.font.Font('JoyFont.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)                   # triggers every 200 ms

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit game if close button is pressed
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            # update direction based on keys pressed
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main_game.snake.dir.y != 1:        # cannot go up when dir is down
                    main_game.snake.dir = Vector2(0, -1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.dir.x != -1:
                    main_game.snake.dir = Vector2(1, 0)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.dir.y != -1:
                    main_game.snake.dir = Vector2(0, 1)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.dir.x != 1:
                    main_game.snake.dir = Vector2(-1, 0)
            elif event.key == pygame.K_p:
                main_game.pause()

    screen.fill(pygame.Color(204, 255, 204))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)  # set a maximum fps
