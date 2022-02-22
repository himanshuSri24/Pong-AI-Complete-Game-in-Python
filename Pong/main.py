import math
import random
import sys
import os
import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
PADDLE_VEL_BK = 6
BALL_VEL_BK = 6

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong - Classic')

FONT = pygame.font.SysFont('comicsans', 50)
SFONT = pygame.font.SysFont('comicsans', 30)

SOUND = pygame.mixer.Sound(os.path.join('ball_paddle.mp3'))

PADDLE_HIT = pygame.USEREVENT + 1


class Paddle:
    COLOR = WHITE
    VEL = 9

    def __init__(self, x, y, width, height):
        self.x = self.ogx = x
        self.y = self.ogy = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.ogx
        self.y = self.ogy


class Ball:

    MAX_VEL = 9
    COLOR = WHITE

    def __init__(self, x, y, r):
        self.x = self.ogx = x
        self.y = self.ogy = y
        self.r = r
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.r)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.ogx
        self.y = self.ogy
        self.y_vel = 0
        self.x_vel *= 1


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_text = FONT.render(f"{left_score}", 1, WHITE)
    right_text = FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    win.blit(right_text, (WIDTH*3//4 - right_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 2, i, 4, HEIGHT//20))
    ball.draw(win)
    pygame.display.update()


def paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.r >= HEIGHT or ball.y - ball.r <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.r <= left_paddle.x + left_paddle.width:
                pygame.event.post(pygame.event.Event(PADDLE_HIT))
                middle = left_paddle.y + left_paddle.height / 2
                vel_ratio = (left_paddle.height / 2) / (ball.MAX_VEL / 1.13)
                distance = middle - ball.y
                ball.y_vel = -1 * distance / vel_ratio
                ball.x_vel = abs(math.sqrt(ball.MAX_VEL*ball.MAX_VEL - ball.y_vel*ball.y_vel))
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.r >= right_paddle.x:
                pygame.event.post(pygame.event.Event(PADDLE_HIT))
                middle = right_paddle.y + right_paddle.height / 2
                vel_ratio = (right_paddle.height / 2) / (ball.MAX_VEL / 1.13)
                distance = middle - ball.y
                ball.y_vel = -1 * distance / vel_ratio
                ball.x_vel = -1*abs(math.sqrt(ball.MAX_VEL*ball.MAX_VEL - ball.y_vel*ball.y_vel))
                # ai(ball, left_paddle, right_paddle)


def drawWaitTime(win):
    time3 = FONT.render("3", 1, WHITE)
    time2 = FONT.render("2", 1, WHITE)
    time1 = FONT.render("1", 1, WHITE)
    pygame.draw.rect(win, BLACK, (300, 0, 100, 500))
    win.blit(time3, (WIDTH//2 - time3.get_width()//2, HEIGHT//2 - time3.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.draw.rect(win, BLACK, (300, 0, 100, 500))
    win.blit(time2, (WIDTH//2 - time2.get_width()//2, HEIGHT//2 - time2.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.draw.rect(win, BLACK, (300, 0, 100, 500))
    win.blit(time1, (WIDTH//2 - time1.get_width()//2, HEIGHT//2 - time1.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000)


# AI Implementation begins here

# def ai(ball, left_paddle, right_paddle):
#     time_taken = ball.x_vel / (right_paddle.x - (left_paddle.x + PADDLE_WIDTH))
#     if ball.y_vel >= 0:
#         y_pos = ball.y + ball.y_vel*time_taken
#     else:
#         y_pos = (HEIGHT - ball.y) + ball.y_vel * time_taken * -1
#     even_bounce = False
#     if y_pos % HEIGHT == 2:
#         even_bounce = True
#     if even_bounce:
#         y_pos = HEIGHT - y_pos % HEIGHT
#     else:
#         y_pos = y_pos % HEIGHT
#     # pos_to_hit = random.randint(0, PADDLE_HEIGHT)
#     curr_pos = left_paddle.y
#     dist_paddle = y_pos - curr_pos
#     if dist_paddle > 0:
#         while dist_paddle > 0:
#             left_paddle.y += 7
#             dist_paddle -= 7
#             # pygame.time.delay(1000//60)
#             # ai(ball, left_paddle, right_paddle)
#     else:
#         while dist_paddle < 0:
#             left_paddle.y -= 7
#             dist_paddle += 7
#             # pygame.time.delay(1000//60)
#             # ai(ball, left_paddle, right_paddle)

def aiEasy(ball, left_paddle):
    if left_paddle.y + Paddle.VEL < HEIGHT - PADDLE_HEIGHT and ball.y > left_paddle.y + PADDLE_HEIGHT:
        left_paddle.y += (Paddle.VEL * random.uniform(0.1, 1))
    elif left_paddle.y - Paddle.VEL > 0 and ball.y < left_paddle.y:
        left_paddle.y -= (Paddle.VEL * random.uniform(0.1, 1))


def aiMedium(ball, left_paddle):
    if left_paddle.y + Paddle.VEL < HEIGHT - PADDLE_HEIGHT and ball.y > left_paddle.y + PADDLE_HEIGHT:
        left_paddle.y += (Paddle.VEL * random.uniform(0.3, 1))
    elif left_paddle.y - Paddle.VEL > 0 and ball.y < left_paddle.y:
        left_paddle.y -= (Paddle.VEL * random.uniform(0.3, 1))


def aiDifficult(ball, left_paddle):
    if left_paddle.y + Paddle.VEL < HEIGHT - PADDLE_HEIGHT and ball.y > left_paddle.y + PADDLE_HEIGHT:
        left_paddle.y += (Paddle.VEL * random.uniform(0.6, 1))
    elif left_paddle.y - Paddle.VEL > 0 and ball.y < left_paddle.y:
        left_paddle.y -= (Paddle.VEL * random.uniform(0.6, 1))


def aiImpossible(ball, left_paddle):
    if left_paddle.y + Paddle.VEL < HEIGHT - PADDLE_HEIGHT and ball.y > left_paddle.y + PADDLE_HEIGHT:
        left_paddle.y += Paddle.VEL
    elif left_paddle.y - Paddle.VEL > 0 and ball.y < left_paddle.y:
        left_paddle.y -= Paddle.VEL


def resetStuff(ball, left_paddle, right_paddle, left_score, right_score):
    ball.reset()
    left_paddle.reset()
    right_paddle.reset()
    draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
    # pygame.time.delay(2000)
    # newFPS = FPS
    drawWaitTime(WIN)
    Ball.MAX_VEL = BALL_VEL_BK
    Paddle.VEL = PADDLE_VEL_BK


def main_menu(win):
    WIN.fill(BLACK)
    choice = 0
    options = SFONT.render("Choose the difficulty mode! ", 1, WHITE)
    win.blit(options, (WIDTH // 2 - options.get_width() // 2, 150))
    choose_one = SFONT.render("1: Easy   2: Medium   3: Hard   4: Impossible", 1, WHITE)
    win.blit(choose_one, (WIDTH // 2 - choose_one.get_width() // 2, 250))
    click = SFONT.render("Press a key", 1, WHITE)
    win.blit(click, (WIDTH // 2 - click.get_width() // 2, 350))
    pygame.display.update()
    # pygame.time.delay(3000)
    while True:
        # pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_1 or event.key == pygame.K_KP1):
                return 1
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_2 or event.key == pygame.K_KP2):
                return 2
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_3 or event.key == pygame.K_KP3):
                return 3
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_4 or event.key == pygame.K_KP4):
                return 4
            # else:
            #     pygame.quit()
            #     sys.exit()


def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_WIDTH, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    left_score = 0
    right_score = 0
    # newFPS = FPS
    # hit_count = 0
    difficulty = main_menu(WIN)
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == PADDLE_HIT:
                SOUND.play()
                # hit_count += 1
                # if hit_count % 6 == 0:
                Ball.MAX_VEL += 1
                Paddle.VEL += 1
        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        if difficulty == 1:
            aiEasy(ball, left_paddle)
        elif difficulty == 2:
            aiMedium(ball, left_paddle)
        elif difficulty == 3:
            aiDifficult(ball, left_paddle)
        else:
            aiImpossible(ball, left_paddle)
        collision(ball, left_paddle, right_paddle)
        won = False
        won_text = "lmao"
        if ball.x < 0:
            right_score += 1
            if right_score == 10:
                won = True
                # newFPS = FPS
                won_text = "You Win!!"
            else:
                resetStuff(ball, left_paddle, right_paddle, left_score, right_score)
        if ball.x > WIDTH:
            left_score += 1
            if left_score == 10:
                won = True
                # newFPS = FPS
                won_text = "The AI Wins!!"
            else:
                resetStuff(ball, left_paddle, right_paddle, left_score, right_score)
        if won:
            winner_text = FONT.render(won_text, 1, WHITE)
            WIN.fill(BLACK)
            WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            # ball.reset()
            # left_paddle.reset()
            # right_paddle.reset()
            pygame.quit()
            sys.exit()
    pygame.quit()


main()

if '__name__' == '__main__':
    main()
