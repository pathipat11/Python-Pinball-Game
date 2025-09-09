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
ball_speed_base = 1.5
max_ball_speed = 2

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
# High Score & Scoreboard
# -------------------------
HIGH_SCORE_FILE = "highscore.txt"

def load_highscore():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except:
        pass

highscore = load_highscore()
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
    """อัปเดตคะแนนและแสดงบนหน้าจอ"""
    scoreBoard.clear()
    scoreBoard.write(f"Score: {score}  Heart: {heart}  Level: {level}  High: {highscore}",  align="center", font=("Courier", 20, "bold"))

def add_score(points):
    """เพิ่มคะแนนและบันทึก High Score ถ้าได้คะแนนสูงสุดใหม่"""
    global score, highscore
    score += points
    if score > highscore:
        highscore = score
        save_highscore(highscore)
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
    msg_turtle.goto(0, 20)
    msg_turtle.write(text, align="center", font=("Courier", 24, "bold"))
    msg_turtle.goto(0, 0)


# -------------------------
# Bricks
# -------------------------
bricks = []

def create_bricks(level=1):
    """
    สร้างบล็อกแบบสุ่มสนุกๆ ตาม level
    - จำนวนแถวเพิ่มตาม level
    - บล็อกบางตัวเป็นแข็ง (ต้องตี 2 ครั้ง)
    - บล็อกสีพิเศษ spawn power-up แน่นอน
    - Random layout มีช่องว่างและ zig-zag pattern
    """
    global bricks
    bricks.clear()
    
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    y_start = 200
    rows = 4 + level  # แถวเพิ่มตาม level

    for row in range(rows):
        # จำนวนคอลัมน์แบบสุ่ม (5-15)
        cols = random.randint(5, 15)
        start_col = -cols // 2

        for col in range(start_col, start_col + cols):
            # Zig-Zag หรือช่องว่าง 20%
            if random.random() < 0.2 or (row + col) % 2 == 0:
                continue

            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            
            # กำหนด HP (1=ปกติ, 2=แข็ง)
            brick.hp = 1
            if random.random() < 0.2 and level >= 3:  # 20% chance เป็นแข็ง
                brick.color("gray")
                brick.hp = 2
            # สีปกติ หรือ สีพิเศษ spawn power-up
            elif random.random() < 0.1 and level >= 3:
                brick.color("white")  # สีพิเศษ
                brick.hp = 1
            else:
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

def reset_paddle():
    paddle.shapesize(stretch_wid=1, stretch_len=8)
    active_effects["paddle"] = False

# -------------------------
# Power-up Visual
# -------------------------
powerup_msg = turtle.Turtle()
powerup_msg.hideturtle()
powerup_msg.speed(0)
powerup_msg.color("white")
powerup_msg.penup()
powerup_msg.goto(0, -280)

def show_powerup_message(text, color="white"):
    powerup_msg.clear()
    powerup_msg.color(color)
    powerup_msg.write(text, align="center", font=("Courier", 18, "bold"))
    screen.ontimer(powerup_msg.clear, 2000)

# -------------------------
# Apply Power-up
# -------------------------
def apply_powerup(pu):
    global heart, balls
    if pu.type == "paddle":
        if not active_effects["paddle"]:
            active_effects["paddle"] = True
            paddle.shapesize(stretch_wid=1, stretch_len=12)
            pygame.mixer.Sound.play(sound_powerup)
            show_powerup_message("Paddle +", "green")
            screen.ontimer(reset_paddle, 10000)
    elif pu.type == "life":
        heart += 1
        pygame.mixer.Sound.play(sound_powerup)
        update_score()
        show_powerup_message("Life +", "pink")
    elif pu.type == "slow":
        for b in balls:
            b.dx *= 0.5
            b.dy *= 0.5
        pygame.mixer.Sound.play(sound_powerup)
        show_powerup_message("Slow", "blue")
        # คืนความเร็วหลัง 5 วิ
        def restore_speed():
            for b in balls:
                if b.dx != 0: b.dx *= 2
                if b.dy != 0: b.dy *= 2
        screen.ontimer(restore_speed, 5000)
    elif pu.type == "extra_ball":
        new_ball = create_ball()
        new_ball.dx = random.choice([-ball_speed_base, ball_speed_base])
        new_ball.dy = ball_speed_base
        pygame.mixer.Sound.play(sound_powerup)
        show_powerup_message("Ball +", "red")

# -------------------------
# Game state
# -------------------------
running = False
waiting = True
paused = False
just_restarted = False
ready_to_start = False

# -------------------------
# Paddle smooth movement
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

paddle_last_x = paddle.xcor()

def move_paddle_smooth():
    global paddle_last_x
    if keys["Right"]:
        x = paddle.xcor() + paddle_speed
        if x > 430: x = 430
        paddle.setx(x)
    if keys["Left"]:
        x = paddle.xcor() - paddle_speed
        if x < -430: x = -430
        paddle.setx(x)
    paddle_last_x = paddle.xcor()
    screen.ontimer(move_paddle_smooth, 20)

move_paddle_smooth()


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
    # # เพิื่มเติม level
    # speed_x = min(ball_speed_base + (level - 1) * 0.3, max_ball_speed)
    # speed_y = min(ball_speed_base + (level - 1) * 0.2, max_ball_speed)
    # ไม่เพิ่มตาม level
    speed_x = ball_speed_base
    speed_y = ball_speed_base

    for b in balls:
        b.dx = random.choice([-speed_x, speed_x])
        b.dy = speed_y
    # Auto paddle boost every level >=5
    if level >= 5 and not active_effects["paddle"]:
        active_effects["paddle"] = True
        paddle.shapesize(stretch_wid=1, stretch_len=12)
        screen.ontimer(reset_paddle, 10000)
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
    msg_turtle.clear()
    msg_turtle.goto(0, 20)
    msg_turtle.write(f"💀 GAME OVER 💀\nScore: {score}\nHigh Score: {highscore}\nLevel Reached: {level}\nPress 'R' to Restart", align="center", font=("Courier", 24, "bold"))
    msg_turtle.goto(0, 0)

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
        return True
    return False

def clamp_speed(ball):
    speed = (ball.dx**2 + ball.dy**2) ** 0.5
    if speed > max_ball_speed:
        scale = max_ball_speed / speed
        ball.dx *= scale
        ball.dy *= scale



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

    if paused or not running:
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
        paddle_half_width = 20 * paddle.shapesize()[1]
        paddle_half_height = 20 * paddle.shapesize()[0]

        if (paddle.ycor() + paddle_half_height > b.ycor() > paddle.ycor() - paddle_half_height and
            paddle.xcor() + paddle_half_width > b.xcor() > paddle.xcor() - paddle_half_width and b.dy < 0):
            
            b.sety(paddle.ycor() + paddle_half_height)
            b.dy *= -1
            offset = b.xcor() - paddle.xcor()
            b.dx = (offset / paddle_half_width) * ball_speed_base
            paddle_dx = paddle.xcor() - paddle_last_x
            b.dx += paddle_dx * 0.2
            clamp_speed(b)
            pygame.mixer.Sound.play(sound_bounce)

        # Brick collision (full version)
        for brick in bricks[:]:
            if (brick.ycor() + 15 > b.ycor() > brick.ycor() - 15 and
                brick.xcor() + 45 > b.xcor() > brick.xcor() - 45):

                # ลด HP ของบล็อก
                brick.hp -= 1
                brick_destroyed = False

                if brick.hp <= 0:
                    bricks.remove(brick)
                    brick.hideturtle()
                    add_score(10)
                    brick_destroyed = True
                else:
                    # เปลี่ยนสีบอกว่าโดนตีแล้ว
                    brick.color("darkgray")

                # โอกาส drop power-up (20% หรือ เพิ่มตาม level)
                drop_chance = 0.2 + (level * 0.02)
                if brick_destroyed and random.random() < drop_chance:
                    spawn_powerup(brick.xcor(), brick.ycor())

                # Ball ตีกลับ
                if abs(b.ycor() - brick.ycor()) > 10:
                    b.dy *= -1
                else:
                    b.dx *= -1
                    
                clamp_speed(b)

                pygame.mixer.Sound.play(sound_brick)
                break

    # Power-up movement & effect
    for pu in powerups[:]:
        pu.sety(pu.ycor() + pu.dy)
        if pu.ycor() < -280:
            pu.hideturtle()
            powerups.remove(pu)
            continue

        if (paddle.ycor() + paddle_half_height > pu.ycor() > paddle.ycor() - paddle_half_height and
            paddle.xcor() + paddle_half_width > pu.xcor() > paddle.xcor() - paddle_half_width):
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
