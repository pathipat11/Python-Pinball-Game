# breakout_powerup_time.py
import turtle
import random
import time

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

# -------------------------
# Balls
# -------------------------
balls = []

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

ball_speed_base = 2
ball = create_ball()

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

# -------------------------
# Message
# -------------------------
message = turtle.Turtle()
message.speed(0)
message.penup()
message.hideturtle()
message.color("yellow")
message.goto(0, 0)

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
active_effects = {"paddle": False}  # track timed effects

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
            # กำหนดเวลา 10 วินาที แล้วลดขนาด paddle
            screen.ontimer(lambda: reset_paddle(), 10000)
    elif pu.type == "life":
        heart += 1
    elif pu.type == "slow":
        for b in balls:
            b.dx *= 0.7
            b.dy *= 0.7
    elif pu.type == "extra_ball":
        new_ball = create_ball()
        new_ball.dx = random.choice([-ball_speed_base, ball_speed_base])
        new_ball.dy = ball_speed_base

def reset_paddle():
    paddle.shapesize(stretch_wid=1, stretch_len=8)
    active_effects["paddle"] = False

# -------------------------
# Game state
# -------------------------
running = False
waiting = True

# -------------------------
# Functions
# -------------------------
def update_score():
    scoreBoard.clear()
    scoreBoard.write(f"Score: {score}  heart: {heart}  Level: {level}", align="center", font=("Courier", 20, "bold"))

def show_message(text):
    message.clear()
    message.write(text, align="center", font=("Courier", 24, "bold"))

def movePadRight():
    x = paddle.xcor() + 40
    if x > 430:
        x = 430
    paddle.setx(x)

def movePadLeft():
    x = paddle.xcor() - 40
    if x < -430:
        x = -430
    paddle.setx(x)

def reset_ball_positions():
    for b in balls:
        b.goto(0, -220)
        b.dx = 0
        b.dy = 0

def start_level():
    global running, waiting
    speed = ball_speed_base + (level - 1) * 0.5
    for b in balls:
        b.dx = random.choice([-speed, speed])
        b.dy = speed
    waiting = False
    running = True
    show_message("")

def launch_ball():
    global waiting
    if waiting and heart > 0:
        if not balls:
            create_ball()
        start_level()

def show_big_message(text):
    # สร้าง Turtle ใหม่สำหรับข้อความนี้
    msg = turtle.Turtle()
    msg.hideturtle()
    msg.speed(0)
    msg.color("yellow")
    msg.penup()
    msg.goto(0, 0)
    msg.write(text, align="center", font=("Courier", 24, "bold"))
    return msg

def game_over():
    global running, waiting
    running = False
    waiting = True

    # ซ่อนลูกบอลและ power-up
    for b in balls:
        b.hideturtle()
    for pu in powerups:
        pu.hideturtle()

    # แสดงข้อความ GAME OVER อยู่ด้านบน
    show_big_message(f"GAME OVER!\nFinal Score: {score}\nPress R to Restart")

def level_up():
    global running, waiting, level
    running = False
    waiting = True
    # แสดงข้อความ Level Up อยู่ด้านบน
    show_big_message(f"Level {level}!\nPress SPACE to Start")
    
def restart():
    global score, heart, level, running, waiting, balls, powerups, active_effects, bricks
    score = 0
    heart = 3
    level = 1
    active_effects = {"paddle": False}

    # ซ่อนลูกบอลเก่า
    for b in balls:
        b.hideturtle()
    balls.clear()

    # ซ่อน power-up เก่า
    for pu in powerups:
        pu.hideturtle()
    powerups.clear()

    # รีเซ็ตลูกบอลใหม่
    create_ball()
    reset_ball_positions()

    # รีเซ็ต scoreboard
    update_score()

    # แสดงข้อความเริ่มต้น
    running = False
    waiting = True
    show_big_message("Press SPACE to Start")

# -------------------------
# Keyboard bindings
# -------------------------
screen.listen()
screen.onkeypress(movePadRight, "Right")
screen.onkeypress(movePadLeft, "Left")
screen.onkeypress(launch_ball, "space")
screen.onkeypress(restart, "r")

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

    if not running:
        continue

    # Move balls
    for b in balls[:]:
        b.setx(b.xcor() + b.dx)
        b.sety(b.ycor() + b.dy)

        # Wall collision X
        if b.xcor() > 480:
            b.setx(480)
            b.dx *= -1
        if b.xcor() < -480:
            b.setx(-480)
            b.dx *= -1

        # Wall collision Y
        if b.ycor() > 280:
            b.sety(280)
            b.dy *= -1

        # Bottom collision
        if b.ycor() < -280:
            balls.remove(b)
            b.hideturtle()
            if not balls:
                heart -= 1
                update_score()
                if heart > 0:
                    reset_ball_positions()
                    waiting = True
                    show_message("Press SPACE to Launch")
                else:
                    game_over()

        # Paddle collision
        if (paddle.ycor() + 20 > b.ycor() > paddle.ycor() - 20 and
            paddle.xcor() + 80 > b.xcor() > paddle.xcor() - 80 and b.dy < 0):
            b.sety(paddle.ycor() + 20)
            b.dy *= -1
            b.dx += random.uniform(-0.05, 0.05)
            if abs(b.dx) < 5:
                b.dx *= 1.03
            if abs(b.dy) < 5:
                b.dy *= 1.03

        # Brick collision
        for brick in bricks[:]:
            if (brick.ycor() + 15 > b.ycor() > brick.ycor() - 15 and
                brick.xcor() + 45 > b.xcor() > brick.xcor() - 45):
                bricks.remove(brick)
                brick.hideturtle()
                if random.random() < 0.2:
                    spawn_powerup(brick.xcor(), brick.ycor())
                    print("Spawn power-up at", brick.xcor(), brick.ycor())
                if abs(b.ycor() - brick.ycor()) > 10:
                    b.dy *= -1
                else:
                    b.dx *= -1
                b.dx += random.uniform(-0.03, 0.03)
                score += 10
                update_score()
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
    if not bricks and running:
        level += 1
        reset_ball_positions()
        create_bricks(level)
        update_score()
        level_up()
        running = False
        waiting = True
        show_message(f"Level {level}!\nPress SPACE to Start")
