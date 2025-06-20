# notifier.py
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont, ImageTk, Image
import screeninfo
import threading
import time
import regex
import subprocess
import platform
from customtkinter import CTkImage
import os
import requests
from io import BytesIO
stop_sound_loop = False

def play_sound_native(path):
    system = platform.system()
    try:
        if system == "Windows":
            import winsound
            # winsound expects a normal Windows path string (no extra quotes)
            path_fixed = os.path.normpath(path)
            winsound.PlaySound(path_fixed, winsound.SND_FILENAME | winsound.SND_ASYNC)

        elif system == "Darwin":  # macOS
            subprocess.Popen(["afplay", path])

        elif system == "Linux":
            # Try common players: paplay, aplay, ffplay
            if shutil.which("paplay"):
                subprocess.Popen(["paplay", path])
            elif shutil.which("aplay"):
                subprocess.Popen(["aplay", path])
            elif shutil.which("ffplay"):
                subprocess.Popen(["ffplay", "-nodisp", "-autoexit", path])
            else:
                print("❌ No compatible audio player found on Linux.")
        else:
            print(f"❌ Unsupported platform: {system}")

    except Exception as e:
        print(f"Sound playback failed: {e}")

def play_sound_async(path):
    threading.Thread(target=play_sound_native, args=(path,), daemon=True).start()

base_dir = os.path.dirname(os.path.abspath(__file__))
gif_path = os.path.join(base_dir, "emojis", "magic.gif")
intro_sound = os.path.join(base_dir, "sound", "intro.wav")
click_sound = os.path.join(base_dir, "sound", "pop.wav")
pitch_sound = os.path.join(base_dir, "sound", "pitch.wav")

def show_notification(
    title_text="🧪 make magic potion",
    message="+1 focus — 3h",
    button_text="🧠 Brain leveled up",
    gif_path=gif_path,
    intro_sound=intro_sound,
    click_sound=click_sound,
    pitch_sound=pitch_sound,
    beep=False
):
    global stop_sound_loop
    stop_sound_loop = False

    # UI Constants
    WIDTH, HEIGHT = 360, 140
    ICON_SIZE = 48
    BG = "#222226"
    FG = "white"
    FG2 = "#c9c9c9"
    BTN_BG = "#2f2f32"
    BTN_HOVER = "#343435"
    BORDER_COLOR = "#434343"
    BORDER_WIDTH = 1
    TRANSPARENT_COLOR = "#123456"

    # Monitor Positioning
    screen = screeninfo.get_monitors()[0]
    final_x = screen.width - WIDTH - 15
    final_y = screen.height - HEIGHT - 15

    EMOJI_CACHE_DIR = "emoji_cache"

    def extract_emoji_cluster(text):
        match = regex.match(r'\X', text)
        return match.group(0) if match else text[0]
    def emoji_to_codepoints(emoji, strip_fe0f=True):
        codepoints = [f"{ord(c):x}" for c in emoji if not (strip_fe0f and ord(c) == 0xfe0f)]
        return "_".join(codepoints)  # Use underscore, not dash

    def get_emoji_image(emoji, size=24):
        emoji = extract_emoji_cluster(emoji)
        codepoints = emoji_to_codepoints(emoji)
        local_path = os.path.join(EMOJI_CACHE_DIR, f"{codepoints}.png")
        url = f"https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/128/emoji_u{codepoints}.png"

        if os.path.exists(local_path):
            try:
                img = Image.open(local_path).convert("RGBA")
                img = img.resize((size, size), Image.LANCZOS)
                return CTkImage(light_image=img, size=(size, size))
            except:
                pass

        try:
            os.makedirs(EMOJI_CACHE_DIR, exist_ok=True)
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content)).convert("RGBA")
            img.save(local_path)  # Cache it
            img = img.resize((size, size), Image.LANCZOS)
            return CTkImage(light_image=img, size=(size, size))
        except Exception as e:
            print(f"❌ Emoji load failed for '{emoji}' → {url} → {e}")
            return None


    def sound_loop():
        def loop():
            global stop_sound_loop

            max_times = 4 if beep else 6
            delay = 10 if beep else 20

            for i in range(max_times):
                if stop_sound_loop:
                    return

                if beep and (i == max_times - 2):
                    play_sound_async(pitch_sound)
                else:
                    play_sound_async(intro_sound)

                if i < max_times - 1:
                    for _ in range(delay * 10):
                        if stop_sound_loop:
                            return
                        time.sleep(0.1)

            if beep and not stop_sound_loop:
                root.after(0, slide_out)

        threading.Thread(target=loop, daemon=True).start()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    start_x = final_x + 30
    start_y = final_y + 30
    root.geometry(f"{WIDTH}x{HEIGHT}+{start_x}+{start_y}")
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.configure(fg_color=TRANSPARENT_COLOR)
    root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

    frame = ctk.CTkFrame(
        root,
        fg_color=BG,
        corner_radius=11,
        width=WIDTH - 2 * BORDER_WIDTH,
        height=HEIGHT - 2 * BORDER_WIDTH,
        border_width=BORDER_WIDTH,
        border_color=BORDER_COLOR
    )
    frame.place(x=BORDER_WIDTH, y=BORDER_WIDTH)

    title_emoji_img = get_emoji_image(title_text, size=24)
    button_emoji_img = get_emoji_image(button_text, size=20)

    gif = Image.open(gif_path)
    gif_frames = []
    try:
        while True:
            img_frame = gif.copy().resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
            gif_frames.append(CTkImage(light_image=img_frame, size=(ICON_SIZE, ICON_SIZE)))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    icon_label = ctk.CTkLabel(frame, text="", fg_color=BG, image=None)
    icon_label.place(x=20, y=25)

    def animate_gif(idx=0):
        icon_label.configure(image=gif_frames[idx])
        root.after(100, animate_gif, (idx + 1) % len(gif_frames))

    animate_gif()

    def remove_leading_emoji(text):
        cluster = extract_emoji_cluster(text)
        return text[len(cluster):]


    title_label = ctk.CTkLabel(frame, text=remove_leading_emoji(title_text), image=title_emoji_img, compound="left",
                               fg_color=BG, text_color=FG, padx=3,
                               font=ctk.CTkFont(family="Segoe UI", size=15))
    title_label.place(x=80, y=20)

    message_label = ctk.CTkLabel(frame, text=message, fg_color=BG, text_color=FG2,
                                 font=ctk.CTkFont(family="Segoe UI", size=14))
    message_label.place(x=80, y=45)

    def slide_in(duration=300):
        steps = 30
        delay = duration // steps
        out_distance = 180
        start_x = final_x + out_distance
        end_x = final_x

        def animate(step=0):
            if step <= steps:
                t = step / steps
                eased = 1 - (1 - t) * (1 - t)
                new_x = start_x + (end_x - start_x) * eased
                root.geometry(f"{WIDTH}x{HEIGHT}+{int(new_x)}+{final_y}")
                root.after(delay, animate, step + 1)
            else:
                root.geometry(f"{WIDTH}x{HEIGHT}+{final_x}+{final_y}")

        animate()
        sound_loop()

    def slide_out():
        snap_distance = -15
        snap_steps = 4
        snap_delay = 15
        snap_x = final_x + snap_distance

        def snap_back(step=0):
            if step <= snap_steps:
                t = step / snap_steps
                eased = t * t
                new_x = final_x + eased * snap_distance
                root.geometry(f"{WIDTH}x{HEIGHT}+{int(new_x)}+{final_y}")
                root.after(snap_delay, snap_back, step + 1)
            else:
                root.after(300, slide_forward)

        def slide_forward():
            out_distance = 500
            out_steps = 30
            out_delay = 14
            start_x = snap_x
            end_x = snap_x + out_distance

            def animate(step=0):
                if step <= out_steps:
                    t = step / out_steps
                    eased = 1 - (1 - t) * (1 - t)
                    new_x = start_x + eased * out_distance
                    root.geometry(f"{WIDTH}x{HEIGHT}+{int(new_x)}+{final_y}")
                    root.after(out_delay, animate, step + 1)
                else:
                    root.destroy()

            animate()

        snap_back()

    def on_button_click():
        global stop_sound_loop
        stop_sound_loop = True
        play_sound_async(click_sound)
        slide_out()

    # Outer frame acts as the border
    button_wrapper = ctk.CTkFrame(
        frame,
        fg_color=BORDER_COLOR,  # border color
        corner_radius=6,
        width=WIDTH - 40,
        height=28
    )
    button_wrapper.place(relx=0.5, y=90, anchor="n")

    # Inner label looks like button face
    button_label = ctk.CTkLabel(
        button_wrapper,
        text=remove_leading_emoji(button_text),
        image=button_emoji_img,
        compound="left",
        fg_color=BTN_BG,
        text_color=FG,
        font=ctk.CTkFont(family="Segoe UI", size=14),
        corner_radius=6,
        width=(WIDTH - 40 - 2 * BORDER_WIDTH),  # subtract border thickness
        height=(28 - 2 * BORDER_WIDTH),
        padx=3,
        anchor="center"
    )
    button_label.place(x=BORDER_WIDTH, y=BORDER_WIDTH)

    # Add hover effect
    def on_enter(e):
        button_label.configure(fg_color=BTN_HOVER)

    def on_leave(e):
        button_label.configure(fg_color=BTN_BG)

    button_label.bind("<Enter>", on_enter)
    button_label.bind("<Leave>", on_leave)

    # Add click behavior
    button_label.bind("<Button-1>", lambda e: on_button_click())
    button_label.configure(cursor="arrow")



    slide_in()
    root.mainloop()

