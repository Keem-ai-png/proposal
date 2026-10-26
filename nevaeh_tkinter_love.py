import tkinter as tk
import math
import random
import time

# ============================================================
# NEVAEH MAMA LOVE ANIMATION
# Pure Python + tkinter: no Pygame and no extra pip installs.
# Run with: py nevaeh_tkinter_love.py
# ============================================================

WIDTH, HEIGHT = 1000, 720
BG_TOP = "#171334"
BG_BOTTOM = "#54265f"
PINK = "#ff6eaa"
HOT_PINK = "#ff438b"
PALE_PINK = "#ffd1e6"
WHITE = "#fff8fd"
LAVENDER = "#d6b5ff"
DARK = "#63264f"
GOLD = "#ffe6b0"

root = tk.Tk()
root.title("Forever Yours, Keem 💗")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.minsize(720, 560)
root.configure(bg=BG_TOP)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                   highlightthickness=0, bg=BG_TOP)
canvas.pack(fill="both", expand=True)

start_time = time.time()
last_time = start_time
heart_progress = 0.0
typed_count = 0
show_surprise = False
show_final = False
running = True
bunny_x = -80
particles = []
stars = []
buttons = {}
current_width, current_height = WIDTH, HEIGHT

def mix_color(a, b, amount):
    a = a.lstrip("#")
    b = b.lstrip("#")
    ar, ag, ab = int(a[0:2], 16), int(a[2:4], 16), int(a[4:6], 16)
    br, bg, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)
    return "#{:02x}{:02x}{:02x}".format(
        int(ar + (br-ar)*amount),
        int(ag + (bg-ag)*amount),
        int(ab + (bb-ab)*amount)
    )

def heart_xy(cx, cy, scale, t):
    x = 16 * math.sin(t) ** 3
    y = -(13 * math.cos(t) - 5 * math.cos(2*t)
          - 2 * math.cos(3*t) - math.cos(4*t))
    return cx + x * scale, cy + y * scale

def heart_points(cx, cy, scale, count=150):
    points = []
    for i in range(count + 1):
        x, y = heart_xy(cx, cy, scale, 2 * math.pi * i / count)
        points.extend((x, y))
    return points

def draw_heart(cx, cy, scale, fill=PINK, outline=WHITE, width=2):
    pts = heart_points(cx, cy, scale)
    canvas.create_polygon(pts, fill=fill, outline=outline,
                          width=width, smooth=True, tags="animated")

def add_particle():
    w = max(canvas.winfo_width(), 720)
    h = max(canvas.winfo_height(), 560)
    particles.append({
        "x": random.uniform(0, w),
        "y": random.uniform(0, h),
        "speed": random.uniform(18, 50),
        "size": random.randint(3, 7),
        "phase": random.uniform(0, math.tau)
    })

def reset_sky():
    global stars, particles
    w = max(canvas.winfo_width(), 720)
    h = max(canvas.winfo_height(), 560)
    stars = [{
        "x": random.uniform(0, w),
        "y": random.uniform(0, h),
        "r": random.choice([1, 1, 2, 2, 3]),
        "phase": random.random() * math.tau,
        "speed": random.uniform(.7, 2.5)
    } for _ in range(100)]
    particles = []
    for _ in range(32):
        add_particle()

def draw_background(t, w, h):
    # Vertical gradient, made from horizontal colour bands.
    bands = 55
    for i in range(bands):
        y0 = int(h * i / bands)
        y1 = int(h * (i + 1) / bands) + 1
        colour = mix_color(BG_TOP, BG_BOTTOM, i / max(1, bands - 1))
        canvas.create_rectangle(0, y0, w, y1, fill=colour,
                                outline=colour, tags="background")

    # Twinkling stars
    for s in stars:
        twinkle = (math.sin(t * s["speed"] + s["phase"]) + 1) / 2
        colour = mix_color("#7c6b9b", "#fff4ff", twinkle)
        r = s["r"]
        canvas.create_oval(s["x"]-r, s["y"]-r, s["x"]+r, s["y"]+r,
                           fill=colour, outline="", tags="animated")
        if r == 3 and twinkle > .86:
            canvas.create_line(s["x"]-5, s["y"], s["x"]+5, s["y"],
                               fill=colour, tags="animated")
            canvas.create_line(s["x"], s["y"]-5, s["x"], s["y"]+5,
                               fill=colour, tags="animated")

    # Moon
    mx, my = w - 90, 95
    canvas.create_oval(mx-34, my-34, mx+34, my+34,
                       fill=GOLD, outline="", tags="animated")
    canvas.create_oval(mx-13, my-43, mx+44, my+17,
                       fill=BG_TOP, outline=BG_TOP, tags="animated")

def draw_bunny(x, ground, t, kissing=False):
    bob = math.sin(t * 4) * 3
    x, ground = int(x), int(ground + bob)
    ear = math.sin(t * 3) * 5
    # Tail
    canvas.create_oval(x-38, ground-37, x-12, ground-11,
                       fill="#fff5fb", outline="#f6dce9", width=2,
                       tags="animated")
    # Ears
    canvas.create_oval(x-28, ground-132, x-5, ground-63,
                       fill="#fff8fd", outline="#f6dce9", width=2,
                       tags="animated")
    canvas.create_oval(x-22, ground-121, x-11, ground-72,
                       fill="#ff9cbe", outline="", tags="animated")
    canvas.create_oval(x+4, ground-134+ear, x+27, ground-65+ear,
                       fill="#fff8fd", outline="#f6dce9", width=2,
                       tags="animated")
    canvas.create_oval(x+10, ground-123+ear, x+21, ground-74+ear,
                       fill="#ff9cbe", outline="", tags="animated")
    # Body and feet
    canvas.create_oval(x-42, ground-61, x+40, ground-8,
                       fill="#fff8fd", outline="#f6dce9", width=2,
                       tags="animated")
    canvas.create_oval(x-38, ground-18, x-7, ground-3,
                       fill="#fff8fd", outline="#f6dce9", width=1,
                       tags="animated")
    canvas.create_oval(x+7, ground-18, x+38, ground-3,
                       fill="#fff8fd", outline="#f6dce9", width=1,
                       tags="animated")
    # Head
    canvas.create_oval(x-39, ground-117, x+39, ground-39,
                       fill="#fff8fd", outline="#f6dce9", width=2,
                       tags="animated")
    blink = int(t * 2.2) % 9 == 0 and math.sin(t * 11) > .82
    if blink:
        canvas.create_line(x-17, ground-81, x-8, ground-81,
                           fill=DARK, width=3, tags="animated")
        canvas.create_line(x+8, ground-81, x+17, ground-81,
                           fill=DARK, width=3, tags="animated")
    else:
        canvas.create_oval(x-16, ground-86, x-8, ground-77,
                           fill=DARK, outline="", tags="animated")
        canvas.create_oval(x+8, ground-86, x+16, ground-77,
                           fill=DARK, outline="", tags="animated")
        canvas.create_oval(x-14, ground-85, x-12, ground-83,
                           fill=WHITE, outline="", tags="animated")
        canvas.create_oval(x+10, ground-85, x+12, ground-83,
                           fill=WHITE, outline="", tags="animated")
    # Blushing cheeks, nose and smile
    canvas.create_oval(x-29, ground-73, x-15, ground-62,
                       fill="#ffb2cc", outline="", tags="animated")
    canvas.create_oval(x+15, ground-73, x+29, ground-62,
                       fill="#ffb2cc", outline="", tags="animated")
    canvas.create_polygon(x-4, ground-73, x+4, ground-73, x, ground-67,
                          fill=HOT_PINK, outline="", tags="animated")
    canvas.create_arc(x-9, ground-70, x, ground-60, start=200, extent=140,
                      style="arc", outline=DARK, width=2, tags="animated")
    canvas.create_arc(x, ground-70, x+9, ground-60, start=200, extent=140,
                      style="arc", outline=DARK, width=2, tags="animated")
    # Bunny's heart
    draw_heart(x+1, ground-42, .58, HOT_PINK, WHITE, 1)
    if kissing:
        draw_heart(x+43, ground-105, .36, HOT_PINK, WHITE, 1)
        draw_heart(x+59, ground-126, .22, PALE_PINK, WHITE, 1)
        canvas.create_text(x+54, ground-147, text="mwah!",
                           fill="#ffe7f3", font=("Segoe Script", 13, "italic"),
                           tags="animated")

def draw_glowing_heart(cx, cy, scale, pulse=1):
    # Soft rings behind the heart create a glow effect.
    for i in range(5, 0, -1):
        r = 16 * scale * (1 + i * .075)
        colour = mix_color("#52265f", "#e6539b", (6-i)/9)
        canvas.create_oval(cx-r, cy-r*.82, cx+r, cy+r*.82,
                           outline=colour, width=2, tags="animated")
    draw_heart(cx, cy, scale*pulse, "#f64b91", "#ffd6e9", 3)

def draw_button(key, x, y, w, h, label, mouse_x, mouse_y):
    hovered = x <= mouse_x <= x+w and y <= mouse_y <= y+h
    fill = "#ff438b" if hovered else "#e95a9d"
    lift = 4 if hovered else 0
    canvas.create_rectangle(x, y+5-lift, x+w, y+h+5-lift,
                            fill="#37183f", outline="", tags="buttons")
    canvas.create_rectangle(x, y-lift, x+w, y+h-lift,
                            fill=fill, outline="#ffd9eb" if hovered else fill,
                            width=2 if hovered else 1,
                            tags=("buttons", "button_"+key))
    canvas.create_text(x+w/2, y+h/2-lift, text=label,
                       fill=WHITE, font=("Arial", 12, "bold"),
                       tags=("buttons", "button_"+key))
    buttons[key] = (x, y-lift, x+w, y+h-lift)
    return hovered

def inside(box, x, y):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]

def burst_hearts():
    w, h = canvas.winfo_width(), canvas.winfo_height()
    for _ in range(22):
        x, y = random.randint(int(w*.35), int(w*.65)), random.randint(int(h*.35), int(h*.65))
        symbol = random.choice(["♡", "♥", "✦", "💗"])
        canvas.create_text(x, y, text=symbol, fill=random.choice([PALE_PINK, GOLD, WHITE]),
                           font=("Arial", random.randint(14, 24)), tags="burst")
        # Each burst piece is animated by the main loop.
        item = canvas.find_all()[-1]
        burst_items.append({"id": item, "vx": random.uniform(-2.5, 2.5),
                            "vy": random.uniform(-4.0, -1.0), "life": 35})

def toggle_surprise():
    global show_surprise
    show_surprise = not show_surprise
    burst_hearts()

def show_final_screen():
    global show_final
    show_final = True
    burst_hearts()

def replay():
    global show_final, show_surprise, start_time, heart_progress, typed_count, bunny_x
    show_final = False
    show_surprise = False
    start_time = time.time()
    heart_progress = 0.0
    typed_count = 0
    bunny_x = -80
    canvas.delete("all")
    reset_sky()

def on_click(event):
    if show_final:
        if "replay" in buttons and inside(buttons["replay"], event.x, event.y):
            replay()
        return
    if "more" in buttons and inside(buttons["more"], event.x, event.y):
        toggle_surprise()
    elif "forever" in buttons and inside(buttons["forever"], event.x, event.y):
        show_final_screen()

def on_key(event):
    if event.keysym == "Escape":
        root.destroy()
    elif event.keysym == "space":
        toggle_surprise()

def on_resize(event):
    global current_width, current_height
    if event.width != current_width or event.height != current_height:
        current_width, current_height = event.width, event.height
        reset_sky()

burst_items = []
mouse_x, mouse_y = -100, -100
def on_mouse_move(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>", on_mouse_move)
canvas.bind("<Configure>", on_resize)
root.bind("<Key>", on_key)

reset_sky()

def animate():
    global heart_progress, bunny_x, typed_count, last_time
    if not root.winfo_exists():
        return

    now = time.time()
    dt = min(now-last_time, .04)
    last_time = now
    t = now - start_time
    w = max(canvas.winfo_width(), 720)
    h = max(canvas.winfo_height(), 560)
    canvas.delete("background")
    canvas.delete("animated")
    canvas.delete("buttons")

    draw_background(t, w, h)

    canvas.create_text(w/2, 42, text="A LITTLE LOVE FOR YOU",
                       fill=WHITE, font=("Georgia", 27, "bold"),
                       tags="animated")
    canvas.create_text(w/2, 78, text="A tiny universe made just for Nevaeh♡",
                       fill=PALE_PINK, font=("Segoe Script", 14, "italic"),
                       tags="animated")

    # Heart draws itself progressively.
    heart_progress = min(1.0, heart_progress + dt * .34)
    hx, hy = w*.59, h*.43
    scale = min(w/100, h/80) * .83
    pts = heart_points(hx, hy, scale, 150)
    count = max(2, int(151 * heart_progress))
    flat = pts[:count*2]
    if heart_progress < 1:
        canvas.create_line(flat, fill=PALE_PINK, width=4,
                           smooth=True, tags="animated")
    else:
        pulse = 1 + .025 * math.sin(t*3.3)
        draw_glowing_heart(hx, hy, scale*.92, pulse)
        love_message = "I LOVE YOU NEVAEH"
        typed_count = min(len(love_message), max(0, int((t-2.0)*10)))
        canvas.create_text(hx, hy-2, text=love_message[:typed_count],
                           fill=WHITE, font=("Segoe Script", 17, "bold"),
                           width=w*.42, tags="animated")
        if typed_count >= len(love_message):
            canvas.create_text(hx, hy+34, text="You are my favourite person ♡",
                               fill=WHITE, font=("Segoe Script", 12, "italic"),
                               tags="animated")

    # Bunny enters and approaches the heart.
    bunny_x = min(w*.38, bunny_x + 72*dt)
    ground = h*.75
    draw_bunny(bunny_x, ground, t, kissing=(bunny_x > w*.32 and heart_progress >= 1))
    canvas.create_text(w*.22, ground+17, text="your little love bunny",
                       fill=PALE_PINK, font=("Segoe Script", 12, "italic"),
                       tags="animated")

    # Little floating hearts near the bunny.
    for i in range(3):
        px = bunny_x + 42 + i*20
        py = ground - 155 + math.sin(t*2+i)*10
        draw_heart(px, py, .23, PINK, WHITE, 1)

    if show_surprise and not show_final:
        panel_w = min(680, w-40)
        px, py = (w-panel_w)/2, h*.79
        canvas.create_rectangle(px, py, px+panel_w, py+64,
                                fill="#fff0f8", outline="#ffd0e5",
                                width=2, tags="animated")
        canvas.create_text(w/2, py+20,
                           text="Nevaeh , I love you more than all the stars in this sky.",
                           fill=DARK, font=("Segoe Script", 13, "bold"),
                           tags="animated")
        canvas.create_text(w/2, py+44,
                           text="If you were a bunny, I'd choose you every hop. ♡",
                           fill=DARK, font=("Segoe Script", 11, "italic"),
                           tags="animated")

    buttons.clear()
    if not show_final:
        bw, bh, gap = 190, 42, 14
        total = bw*2 + gap
        bx = (w-total)/2
        by = h-68
        draw_button("more", bx, by, bw, bh, "I LOVE YOU SO MUCH BABY", mouse_x, mouse_y)
        draw_button("forever", bx+bw+gap, by, bw, bh, "FOREVER YOURS", mouse_x, mouse_y)
        canvas.create_text(w/2, h-13,
                           text="Click a button for a surprise  •  SPACE also works  •  ESC to quit",
                           fill="#ead5f1", font=("Georgia", 10, "italic"),
                           tags="animated")
    else:
        canvas.create_rectangle(0, 0, w, h, fill="#28153e",
                                outline="", stipple="gray50", tags="animated")
        for i in range(14):
            a = t*.65 + i*math.tau/14
            xx = w/2 + math.cos(a)*(110+10*math.sin(t*2))
            yy = h*.36 + math.sin(a)*(70+8*math.cos(t*2))
            draw_heart(xx, yy, .35, HOT_PINK, WHITE, 1)
        draw_heart(w/2, h*.36, 5.1, "#f34b91", WHITE, 3)
        draw_bunny(w/2-155, h*.68, t, kissing=True)
        canvas.create_text(w/2+45, h*.57, text="Forever yours,",
                           fill=WHITE, font=("Segoe Script", 29, "bold"),
                           tags="animated")
        canvas.create_text(w/2+45, h*.65, text="Keem",
                           fill=WHITE, font=("Segoe Script", 36, "bold"),
                           tags="animated")
        canvas.create_text(w/2, h*.79, text="Nevaeh Mama, you have my heart. Always. ♡",
                           fill=PALE_PINK, font=("Segoe Script", 15, "italic"),
                           tags="animated")
        draw_button("replay", w/2-95, h-68, 190, 42,
                    "REPLAY OUR LOVE", mouse_x, mouse_y)

    # Animate the little burst symbols.
    for piece in burst_items[:]:
        try:
            canvas.move(piece["id"], piece["vx"], piece["vy"])
            piece["vy"] += .08
            piece["life"] -= 1
            if piece["life"] <= 0:
                canvas.delete(piece["id"])
                burst_items.remove(piece)
        except tk.TclError:
            burst_items.remove(piece)

    root.after(33, animate)

animate()
root.mainloop()
