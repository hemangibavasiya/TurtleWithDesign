# love_program.py
# Modern developer-style animated turtle UI
# Run: python love_program.py

import turtle as t
import time
import math
import random

# -------------------------
# CONFIG (customize here)
# -------------------------
TARGET_NAME = "Name"
MESSAGE_LINES = [
    "Booting up eternal_love.py...",
    f"Establishing secure connection to \"{TARGET_NAME}\" ❤️",
    "SSL handshake: Emotions encrypted and synced 🔐",
    "Pushing commits: trust, passion, and infinite affection 💫",
    f"Deployment complete: `love` branch successfully merged into `{TARGET_NAME}` 💜"
]
BG_TOP = (18, 32, 47)    # deep blue
BG_BOTTOM = (2, 8, 20)   # almost black
HEART_FILL = "#00eaff"   # cyan
HEART_EDGE = "#6a5acd"   # slate blue
TERMINAL_COLOR = "#ffff66"  # bright yellow
# Alternative options:
# TERMINAL_COLOR = "#ffffff"  # white
# TERMINAL_COLOR = "#39ff14"  # neon green
# TERMINAL_COLOR = "#ff00cc"  # magenta
TERMINAL_FONT = ("Consolas", 18, "bold")
SPEED = 0.0
WIDTH, HEIGHT = 900, 600
# -------------------------

def col(c):
    return (c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

screen = t.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("love.exe - compiled with 💙 by Hemangi")
screen.tracer(0)
screen.bgcolor(col(BG_BOTTOM))

def draw_gradient(top, bottom, steps=40):
    topc = top
    botc = bottom
    step_h = HEIGHT / steps
    drawer = t.Turtle()
    drawer.hideturtle()
    drawer.speed(0)
    drawer.penup()
    start_y = HEIGHT // 2
    for i in range(steps):
        ratio = i / (steps - 1)
        r = int(topc[0] * (1 - ratio) + botc[0] * ratio)
        g = int(topc[1] * (1 - ratio) + botc[1] * ratio)
        b = int(topc[2] * (1 - ratio) + botc[2] * ratio)
        drawer.fillcolor(col((r, g, b)))
        drawer.goto(-WIDTH//2, start_y - i * step_h)
        drawer.begin_fill()
        drawer.forward(WIDTH)
        drawer.right(90)
        drawer.forward(step_h)
        drawer.right(90)
        drawer.forward(WIDTH)
        drawer.right(90)
        drawer.forward(step_h)
        drawer.right(90)
        drawer.end_fill()
    drawer.clear()
    screen.update()

def heart_points(scale=1.0, offset=(0, 30), steps=200):  # moved up for better centering
    pts = []
    for i in range(steps + 1):
        tangle = math.pi * 2 * i / steps
        x = 16 * (math.sin(tangle) ** 3)
        y = 13 * math.cos(tangle) - 5 * math.cos(2 * tangle) - 2 * math.cos(3 * tangle) - math.cos(4 * tangle)
        pts.append((offset[0] + x * scale, offset[1] + y * scale))
    return pts

outline_turtle = t.Turtle()
outline_turtle.hideturtle()
outline_turtle.pensize(3)
outline_turtle.color(HEART_EDGE)
outline_turtle.speed(0)

fill_turtle = t.Turtle()
fill_turtle.hideturtle()
fill_turtle.speed(0)

text_turtle = t.Turtle()
text_turtle.hideturtle()
text_turtle.penup()

class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.6, 0.6)
        self.vy = random.uniform(0.5, 1.5)
        self.life = random.uniform(0.8, 2.0)
        self.size = random.uniform(2, 5)
        self.color = random.choice(["#00eaff", "#b2f7ef", "#ffffff", "#6a5acd"])

    def update(self, dt):
        self.x += self.vx * 60 * dt
        self.y += self.vy * 60 * dt
        self.vy -= 1.8 * dt
        self.life -= dt
        self.size *= 0.995

spark_turtle = t.Turtle()
spark_turtle.hideturtle()
spark_turtle.penup()

sparks = []

def spawn_sparks(x, y, n=8):
    for _ in range(n):
        s = Spark(x + random.uniform(-10, 10), y + random.uniform(-10, 10))
        sparks.append(s)

def draw_sparks():
    spark_turtle.clear()
    for s in sparks:
        if s.life > 0:
            spark_turtle.goto(s.x, s.y)
            spark_turtle.dot(max(1, int(s.size)), s.color)

def draw_filled_heart(points, fill_col, edge_col):
    fill_turtle.clear()
    fill_turtle.penup()
    fill_turtle.goto(points[0])
    fill_turtle.pendown()
    fill_turtle.color(edge_col, fill_col)
    fill_turtle.begin_fill()
    for p in points:
        fill_turtle.goto(p)
    fill_turtle.end_fill()

def animate_heart_draw(scale=14, duration=2.2):
    pts = heart_points(scale=scale, offset=(0, 20), steps=240)
    outline_turtle.clear()
    outline_turtle.penup()
    outline_turtle.goto(pts[0])
    outline_turtle.pendown()
    outline_turtle.color(HEART_EDGE)
    total = len(pts)
    start = time.time()
    for i, p in enumerate(pts):
        outline_turtle.goto(p)
        if i % 14 == 0:
            spawn_sparks(p[0], p[1], n=3)
        if i % 6 == 0:
            draw_sparks()
        if i % 2 == 0:
            screen.update()
    draw_filled_heart(pts, HEART_FILL, HEART_EDGE)
    spawn_sparks(0, 60, n=30)
    draw_sparks()
    screen.update()

def heartbeat(loop_seconds=4.5, beats=6):
    base_scale = 14
    tstart = time.time()
    elapsed = 0
    while elapsed < loop_seconds:
        elapsed = time.time() - tstart
        beat = 1 + 0.035 * math.sin(math.pi * 2 * elapsed * 2) + 0.02 * math.sin(math.pi * 4 * elapsed)
        pts = heart_points(scale=base_scale * beat, offset=(0, 20), steps=240)
        draw_filled_heart(pts, HEART_FILL, HEART_EDGE)
        if random.random() < 0.05:
            spawn_sparks(random.uniform(-80, 80), random.uniform(-10, 80), n=4)
        dt = 0.03
        for s in sparks[:]:
            s.update(dt)
            if s.life <= 0 or s.size < 0.5:
                sparks.remove(s)
        draw_sparks()
        screen.update()
        time.sleep(0.03)

def type_message(lines, x=0, start_y=-180, delay=0.03):  # Lower start
    text_turtle.clear()
    text_turtle.color(TERMINAL_COLOR)
    drawn_lines = []
    for idx, full_line in enumerate(lines):
        cur = ""
        y_line = start_y - idx * 32
        for ch in full_line:
            cur += ch
            text_turtle.clear()
            # Draw all previous lines
            for prev_idx, prev_line in enumerate(drawn_lines):
                prev_y = start_y - prev_idx * 32
                text_turtle.goto(x, prev_y)
                text_turtle.write(prev_line, align="center", font=TERMINAL_FONT)
            # Draw current line with cursor
            text_turtle.goto(x, y_line)
            text_turtle.write(cur + ("|" if (int(time.time()*2) % 2 == 0) else ""), align="center", font=TERMINAL_FONT)
            screen.update()
            time.sleep(delay)
        # After line is done, add to drawn_lines
        drawn_lines.append(cur)
        text_turtle.clear()
        # Draw all lines including the new one
        for prev_idx, prev_line in enumerate(drawn_lines):
            prev_y = start_y - prev_idx * 32
            text_turtle.goto(x, prev_y)
            text_turtle.write(prev_line, align="center", font=TERMINAL_FONT)
        spawn_sparks(x, y_line + 18, n=6)
        for _ in range(6):
            for s in sparks[:]:
                s.update(0.03)
                if s.life <= 0 or s.size < 0.5:
                    sparks.remove(s)
            draw_sparks()
            screen.update()
            time.sleep(0.02)

def write_name_in_heart(name):
    name_t = t.Turtle()
    name_t.hideturtle()
    name_t.penup()
    name_t.color(TERMINAL_COLOR)
    name_t.goto(0, 38)
    name_t.write(f"{name} 💻", align="center", font=("Consolas", 38, "bold"))

def show():
    draw_gradient(BG_TOP, BG_BOTTOM, steps=40)
    screen.update()
    time.sleep(0.15)
    animate_heart_draw(scale=14)
    time.sleep(0.18)
    heartbeat(loop_seconds=2.0)
    write_name_in_heart(TARGET_NAME)
    screen.update()
    time.sleep(0.6)
    type_message(MESSAGE_LINES, x=0, start_y=-180, delay=0.05)
    heartbeat(loop_seconds=3.2)
    spawn_sparks(0, 40, n=40)
    for _ in range(30):
        for s in sparks[:]:
            s.update(0.03)
            if s.life <= 0 or s.size < 0.3:
                sparks.remove(s)
        draw_sparks()
        screen.update()
        time.sleep(0.03)
    sign = t.Turtle()
    sign.hideturtle()
    sign.penup()
    sign.color("#b2f7ef")
    sign.goto(400, 300)
    sign.write("— coded with 💻 by Hemangi", align="left", font=("Consolas", 13, "italic"))
    screen.update()
    screen.tracer(1)
    t.done()

if __name__ == "__main__":
    show()