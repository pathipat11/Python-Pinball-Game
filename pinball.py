import turtle
import random
import pygame

# -------------------------
# Initialize pygame for sound
# -------------------------
pygame.mixer.init()
sound_bounce = pygame.mixer.Sound("assets/sounds/bounce.mp3")
sound_brick = pygame.mixer.Sound("assets/sounds/brick.mp3")
sound_powerup = pygame.mixer.Sound("assets/sounds/powerup.mp3")
sound_life = pygame.mixer.Sound("assets/sounds/life.mp3")
sound_levelup = pygame.mixer.Sound("assets/sounds/levelup.mp3")
sound_gameover = pygame.mixer.Sound("assets/sounds/gameover.mp3")

# -------------------------
# Setup screen
# -------------------------
screen = turtle.Screen()
screen.title("Pinball Game with Timed Power-ups")
screen.setup(width=1000, height=600)
screen.bgcolor("black")
screen.tracer(0)

# -------------------------
# Paddle
# -------------------------
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("cyan")
paddle.shapesize(stretch_wid=1, stretch_len=8)
paddle.penup()
paddle.goto(0, -250)
paddle_speed = 15

# -------------------------
# Balls
# -------------------------
balls = []
ball_speed_base = 2

def create_ball():
    b = turtle.Turtle()
    b.speed(0)
    b.shape("circle")
    b.color("red")
    b.penup()
    b.goto(0, -220)
    b.dx = 0
    b.dy = 0
    balls.append(b)
    return b

create_ball()

# -------------------------
# Scoreboard
# -------------------------
score = 0
heart = 3
level = 1

scoreBoard = turtle.Turtle()
scoreBoard.speed(0)
scoreBoard.penup()
scoreBoard.hideturtle()
scoreBoard.color("white")
scoreBoard.goto(0, 260)

def update_score():
    scoreBoard.clear()
    scoreBoard.write(f"Score: {score}  Heart: {heart}  Level: {level}", align="center", font=("Courier", 20, "bold"))

def add_score(points):
    global score
    score += points
    update_score()

# -------------------------
# Message
# -------------------------
msg_turtle = turtle.Turtle()
msg_turtle.hideturtle()
msg_turtle.speed(0)
msg_turtle.color("yellow")
msg_turtle.penup()
msg_turtle.goto(0, 0)

def show_message(text):
    msg_turtle.clear()
    msg_turtle.write(text, align="center", font=("Courier", 24, "bold"))

# -------------------------
# Bricks
# -------------------------
bricks = []

def create_bricks(level=1):
    global bricks
    bricks.clear()
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    y_start = 200
    rows = 4 + level
    for row in range(rows):
        for col in range(-7, 8):
            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            brick.color(colors[row % len(colors)])
            brick.shapesize(stretch_wid=1, stretch_len=3)
            brick.penup()
            brick.goto(col * 65, y_start - row * 30)
            bricks.append(brick)

# -------------------------
# Power-ups
# -------------------------
powerups = []
active_effects = {"paddle": False}

def spawn_powerup(x, y):
    t = turtle.Turtle()
    t.speed(0)
    t.shape("triangle")
    t.color(random.choice(["green", "yellow", "blue", "pink"]))
    t.penup()
    t.goto(x, y)
    t.dy = -1.5
    t.type = random.choice(["paddle", "life", "slow", "extra_ball"])
    powerups.append(t)

def apply_powerup(pu):
    global heart, balls
    if pu.type == "paddle":
        if not active_effects["paddle"]:
            active_effects["paddle"] = True
            paddle.shapesize(stretch_wid=1, stretch_len=12)
            pygame.mixer.Sound.play(sound_powerup)
            screen.ontimer(reset_paddle, 10000)
    elif pu.type == "life":
        heart += 1
        pygame.mixer.Sound.play(sound_powerup)
    elif pu.type == "slow":
        for b in balls:
            b.dx *= 0.7
            b.dy *= 0.7
        pygame.mixer.Sound.play(sound_powerup)
    elif pu.type == "extra_ball":
        new_ball = create_ball()
        new_ball.dx = random.choice([-ball_speed_base, ball_speed_base])
        new_ball.dy = ball_speed_base
        pygame.mixer.Sound.play(sound_powerup)

def reset_paddle():
    paddle.shapesize(stretch_wid=1, stretch_len=8)
    active_effects["paddle"] = False

# -------------------------
# Game state
# -------------------------
running = False
waiting = True
paused = False
just_restarted = False
ready_to_start = False

# -------------------------
# Paddle hold key movement
# -------------------------
keys = {"Left": False, "Right": False}

def key_press_right():
    keys["Right"] = True

def key_release_right():
    keys["Right"] = False

def key_press_left():
    keys["Left"] = True

def key_release_left():
    keys["Left"] = False

screen.onkeypress(key_press_right, "Right")
screen.onkeyrelease(key_release_right, "Right")
screen.onkeypress(key_press_left, "Left")
screen.onkeyrelease(key_release_left, "Left")

def move_paddle():
    if keys["Right"]:
        x = paddle.xcor() + paddle_speed
        if x > 430: x = 430
        paddle.setx(x)
    if keys["Left"]:
        x = paddle.xcor() - paddle_speed
        if x < -430: x = -430
        paddle.setx(x)

# -------------------------
# Ball & Level functions
# -------------------------
def reset_ball_positions():
    for b in balls:
        b.goto(0, -220)
        b.dx = 0
        b.dy = 0

def start_level():
    global running, waiting, ready_to_start, just_restarted
    if not ready_to_start:
        return
    speed = ball_speed_base + (level - 1) * 0.5
    for b in balls:
        b.dx = random.choice([-speed, speed])
        b.dy = speed
    running = True
    waiting = False
    ready_to_start = False
    just_restarted = False
    show_message("")

def launch_ball():
    global waiting, ready_to_start
    if waiting and heart > 0:
        if not balls:
            create_ball()
        show_message(f"Level {level}!\nGet Ready...")
        ready_to_start = True
        screen.ontimer(start_level, 1000)

def level_up():
    global running, waiting, ready_to_start
    running = False
    waiting = True
    ready_to_start = False
    pygame.mixer.Sound.play(sound_levelup)
    show_message("Press SPACE to Start")

def game_over():
    global running, waiting
    running = False
    waiting = True
    for b in balls: b.hideturtle()
    for pu in powerups: pu.hideturtle()
    for brick in bricks: brick.hideturtle()
    bricks.clear()
    pygame.mixer.Sound.play(sound_gameover)
    show_message(f"GAME OVER!\nFinal Score: {score}\nPress R to Restart")

def restart():
    global score, heart, level, running, waiting, balls, powerups, active_effects, bricks, just_restarted, ready_to_start
    score = 0
    heart = 3
    level = 1
    active_effects = {"paddle": False}
    just_restarted = True
    ready_to_start = False

    for b in balls: b.hideturtle()
    balls.clear()
    for pu in powerups: pu.hideturtle()
    powerups.clear()
    for brick in bricks: brick.hideturtle()
    bricks.clear()

    create_ball()
    reset_ball_positions()
    create_bricks(level)
    update_score()
    show_message("Press SPACE to Start")
    running = False
    waiting = True

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        show_message("Paused\nPress P to Resume")
    else:
        show_message("")

def lose_life():
    global heart
    heart -= 1
    update_score()
    pygame.mixer.Sound.play(sound_life)
    if heart > 0:
        reset_ball_positions()
        return True  # ยังมีชีวิต
    return False  # หมดชีวิต



# -------------------------
# Keyboard bindings
# -------------------------
screen.listen()
screen.onkeypress(launch_ball, "space")
screen.onkeypress(restart, "r")
screen.onkeypress(toggle_pause, "p")

# -------------------------
# Main setup
# -------------------------
reset_ball_positions()
create_bricks(level)
update_score()
show_message("Press SPACE to Start")

# -------------------------
# Main game loop
# -------------------------
while True:
    screen.update()
    move_paddle()  # Smooth paddle movement

    if paused:
        continue
    if not running:
        continue

    for b in balls[:]:
        b.setx(b.xcor() + b.dx)
        b.sety(b.ycor() + b.dy)

        # Wall collision X
        if b.xcor() > 480:
            b.setx(480)
            b.dx *= -1
            pygame.mixer.Sound.play(sound_bounce)
        if b.xcor() < -480:
            b.setx(-480)
            b.dx *= -1
            pygame.mixer.Sound.play(sound_bounce)

        # Wall collision Y
        if b.ycor() > 280:
            b.sety(280)
            b.dy *= -1
            pygame.mixer.Sound.play(sound_bounce)

        # Bottom collision
        if b.ycor() < -280:
            balls.remove(b)
            b.hideturtle()
            if not balls:
                if not lose_life():
                    game_over()
                else:
                    waiting = True
                    show_message("Press SPACE to Launch")


        # Paddle collision
        if (paddle.ycor() + 20 > b.ycor() > paddle.ycor() - 20 and
            paddle.xcor() + 80 > b.xcor() > paddle.xcor() - 80 and b.dy < 0):
            b.sety(paddle.ycor() + 20)
            b.dy *= -1
            b.dx += random.uniform(-0.05, 0.05)
            pygame.mixer.Sound.play(sound_bounce)
            if abs(b.dx) < 5: b.dx *= 1.03
            if abs(b.dy) < 5: b.dy *= 1.03

        # Brick collision
        for brick in bricks[:]:
            if (brick.ycor() + 15 > b.ycor() > brick.ycor() - 15 and
                brick.xcor() + 45 > b.xcor() > brick.xcor() - 45):
                bricks.remove(brick)
                brick.hideturtle()
                pygame.mixer.Sound.play(sound_brick)
                if random.random() < 0.2:
                    spawn_powerup(brick.xcor(), brick.ycor())
                if abs(b.ycor() - brick.ycor()) > 10:
                    b.dy *= -1
                else:
                    b.dx *= -1
                b.dx += random.uniform(-0.03, 0.03)
                add_score(10)
                break

    # Power-up movement & effect
    for pu in powerups[:]:
        pu.sety(pu.ycor() + pu.dy)
        if pu.ycor() < -280:
            pu.hideturtle()
            powerups.remove(pu)
        if (paddle.ycor() + 20 > pu.ycor() > paddle.ycor() - 20 and
            paddle.xcor() + 80 > pu.xcor() > paddle.xcor() - 80):
            apply_powerup(pu)
            pu.hideturtle()
            powerups.remove(pu)

    # Win condition
    if not bricks and running and not just_restarted:
        level += 1
        reset_ball_positions()
        create_bricks(level)
        update_score()
        level_up()
        running = False
        waiting = True
