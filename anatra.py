#         _.-.
#    __.-' ,  \
#   '--'-'._   \
#           '.  \
#            )   \ __.--._
#           /   .'        '--.
#          .               _/-._
#          :       ____._/   _-'
#           '._          _.'-'
#              '-._    _.'
#                  \_|/
#                 __|||
#                 >__/'
#     ______                    __                     
#    /\  _  \                  /\ \__                  
#    \ \ \L\ \    ___      __  \ \ ,_\  _ __    __     
#     \ \  __ \ /' _ `\  /'__`\ \ \ \/ /\`'__\/'__`\   
#      \ \ \/\ \/\ \/\ \/\ \L\.\_\ \ \_\ \ \//\ \L\.\_ 
#       \ \_\ \_\ \_\ \_\ \__/.\_\\ \__\\ \_\\ \__/.\_\
#        \/_/\/_/\/_/\/_/\/__/\/_/ \/__/ \/_/ \/__/\/_/

"""
🦆 Did you know? Ducks move gracefully in water, but what you don't see is how hard
they're paddling underneath. From the surface, they look calm and effortless—yet below,
they’re focused, active, and working with rhythm.

# Anatra Techinique 

like the duck, your productivity doesn’t have to look forced or rigid.
It’s about finding your own rhythm —sometimes gliding, sometimes paddling— but
always moving with intention. Anatra recognizes the work you put in,
gives feedback when you need it, and reminds you that rewards come
not from pushing harder, but from moving smarter.
"""

# Anatra Techinique is based on direct feedback and reward.
# also the time is open to the user needs, 3h work go it, 10 min break yeah.
# the user then can see what he have been doing and decide what to do with it.
# Anatra does not force sessions, but each timer give feedback reward then the user
# decides if want to do a timer for break or continue a timer for working more.
# the idea is that we all do different things and we all have different focus and break periods
# sometimes longer sometimes shorter, depends on task, the day, etc ...
# Anatra helps you by providing a timer that you can work with your focus understanding.
# Anatra encourage that at the end of long sessions you do something you like
# you have to choose a reward, and have discipline to only received it when the timer ends
# If you take reward without work would make you less likely to work.
# you have to be disciplined with your reward or Anatra will bite you

# Duck stickers © Telegram. Used under Telegram’s sticker usage guidelines. Telegram is not affiliated with or endorsing this project.

import sys
import time
import csv
from datetime import datetime
import os
import argparse
import random
import json
from win11toast import toast
from colorama import Fore, Style, init

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
import winsound
#init(autoreset=True)
init()
console = Console()

config_folder = "files"

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir

os.makedirs(base_dir, exist_ok=True)

log_folder = os.path.join(base_dir, 'log')
log_file = os.path.join(log_folder, 'timer_log.csv')
STATE_FILE = os.path.join(log_folder, 'message_state.json')

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

achievement_messages = [
    ["🔥 Task on fire", "you crushed it", "fire-duck.gif"],
    ["🐸 Frog eaten", "that tough task is done", "frog.gif"],
    ["🌿 Growth recorded", "you're building habits", "herb.gif"],
    ["🍪 Focus complete", "here’s your cookie", "cookie.gif"],
    ["🧱 Brick placed", "solid progress made", "moai.gif"],
    ["🧠 Brain leveled up", "+1 focus", "magic.gif"],
    ["🌧️ Lightning strike", "fast, focused energy", "bolt.gif"],
    ["🍰 Sweet reward", "you earned your slice", "cake.gif"],
    ["🍩 Donut earned", "a focused loop complete", "donut.gif"],
    ["🧁 Cupcake claimed", "small win, sweet focus", "cupcake.gif"],
    ["🚀 Boost successful", "you launched deep work", "rocket.gif"],
    ["🍀 Lucky streak", "it all clicked into place", "clover.gif"],
    ["📦 Task wrapped", "shipped and done", "luggage.gif"],
    ["🏀 Swish!", "you scored with precision", "basketball.gif"],
    ["🌊 Flow caught", "smooth session", "fish.gif"],
    ["📈 One more up", "streak continues", "graph-up.gif"]
]

def load_message_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return []

def save_message_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def main():
    parser = argparse.ArgumentParser(
        description="Anatra Timer CLI",
        usage="anatra <hours> <minutes> <seconds> <category> <emoji> <title> [log | -v | --version]"
    )
    #parser.add_argument('--version', action='version', version='Anatra 1.0.0')
    parser.add_argument('-v', '-V', '--version', action='store_true', help='Show version and exit')
    parser.add_argument('args', nargs='*', help='Timer parameters or the "log" command')
    args = parser.parse_args()

    if args.version:
        print("Anatra 1.0.0")
        sys.exit(0)

    # Load or initialize
    messages_left = load_message_state()
    
    # If all messages have been shown or file was corrupt/missing, reset
    if not messages_left:
        messages_left = achievement_messages.copy()
        random.shuffle(messages_left)
    
    # Get and remove the next message
    selected_message = messages_left.pop()
    save_message_state(messages_left)
    
    # Use selected_message
    #text, gif = selected_message
    #print(f"Message: {text}, Image: {gif}")
    
    #selected_message = random.choice(achievement_messages)
    
    #def print_log_table(csv_path):
    #    console = Console()
    #    table = Table(show_header=True)
    #    header_colors = ["white", "green", "bright_white", "cyan", "white"]
    #    
    #    # Read CSV and add columns dynamically
    #    with open(csv_path, newline='', encoding='utf-8') as csvfile:
    #        reader = csv.reader(csvfile)
    #        headers = next(reader)
    #        for i, header in enumerate(headers):
    #            color = header_colors[i % len(header_colors)]
    #            table.add_column(header, header_style=f"bold {color}", style=f"bold {color}")
    #        for row in reader:
    #            table.add_row(*row)
    #    console.print(table)
    
    def print_log_table(csv_path, max_rows=20):
        console = Console()
        table = Table(show_header=True)
        header_colors = ["white", "green", "bright_white", "cyan", "white"]
        
        # Read CSV
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.reader(csvfile))
            if not reader:
                console.print("[bold red]The CSV file is empty.[/bold red]")
                return
            
            headers = reader[0]
            rows = reader[1:]
    
            # Only keep the last `max_rows` rows
            if len(rows) > max_rows:
                rows = rows[-max_rows:]
    
            # Add table columns
            for i, header in enumerate(headers):
                color = header_colors[i % len(header_colors)]
                table.add_column(header, header_style=f"bold {color}", style=f"bold {color}")
            
            # Add table rows
            for row in rows:
                table.add_row(*row)
        
        console.print(table)
    
    if args.args and args.args[0] == "log":
        print_log_table(log_file)
        sys.exit(0)

    if len(args.args) < 6:
        parser.print_help()
        sys.exit(1)
    
    try:
        hours = int(args.args[0])
        minutes = int(args.args[1])
        seconds = int(args.args[2])
    except ValueError:
        print("Hours, minutes, and seconds must be integers.")
        sys.exit(1)

    category = args.args[3]
    emoji = args.args[4]
    title = " ".join(args.args[5:]) 
    
    def readable_duration(hours, minutes, seconds):
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")
        return " ".join(parts)
    
    timer_duration = readable_duration(hours, minutes, seconds)
    
    duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    static_message = f"{emoji} {title}:"
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    
    # Construct initial box content with placeholder timer
    initial_content = f"{static_message} 00:00:00"
    
    # Print the box once
    panel = Panel(
        initial_content,
        padding=(1, 4),      # (top_bottom, left_right) padding
        border_style="cyan",
        expand=False,        # Do not expand to full width
        title="TIMER",
        title_align="left"
    )
    console.print(panel)
    
    text_line_index = 3
    lines_to_move_up = 4 - text_line_index + 2
    
    sys.stdout.write(f"\033[{lines_to_move_up}A")  # Move cursor up
    sys.stdout.flush()
    try:
        for remaining in range(total_seconds, -1, -1):
            h = remaining // 3600
            m = (remaining % 3600) // 60
            s = remaining % 60
            time_str = f"{h:02}:{m:02}:{s:02}"
        
            # Build updated timer text (same length to avoid flicker)
            updated_text = f"{static_message} {time_str}  "
        
            # Create new line keeping the box borders intact by replacing text inside
            new_line = f"{Fore.CYAN}│{Style.RESET_ALL}   {updated_text}   {Fore.CYAN}│{Style.RESET_ALL}"
            # Overwrite the line in-place, and stay there
            sys.stdout.write("\r" + new_line + "\033[K")  # \033[K clears to end of line
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        # ANSI escape codes
        CLEAR_EOL = '\033[K'       # tput el
        CURSOR_START = '\r'        # tput cr
        CLEAR_DOWN = '\033[J'      # tput ed
        CURSOR_UP = lambda n: f'\033[{n}A'  # tput cuu N
        
        print(CLEAR_EOL + CURSOR_START, end='')
        print(CURSOR_UP(2), end='')  # Move up 2 lines
        print(CLEAR_DOWN, end='')    # Clear from cursor down
        title_exit = f"[bright_white]{emoji} {title} — ❌ Task Canceled [/bright_white][bright_red][{timer_duration}, {category}][/bright_red]"
        
        panel_exit = Panel(
            title_exit,
            padding=(1, 4),      # (top_bottom, left_right) padding
            border_style="red",
            expand=False,        # Do not expand to full width
            title="TIMER",
            title_align="left"
        )
        console.print(panel_exit)
        sys.exit()
    
    # ANSI escape codes
    CLEAR_EOL = '\033[K'       # tput el
    CURSOR_START = '\r'        # tput cr
    CLEAR_DOWN = '\033[J'      # tput ed
    CURSOR_UP = lambda n: f'\033[{n}A'  # tput cuu N
    
    print(CLEAR_EOL + CURSOR_START, end='')
    print(CURSOR_UP(2), end='')  # Move up 2 lines
    print(CLEAR_DOWN, end='')    # Clear from cursor down
    
    title_task = f"[bright_white]{emoji} {title} — 🎯 Task Achieved [/bright_white][cyan][{timer_duration}, {category}][/cyan]"
    
    panel2 = Panel(
        title_task,
        padding=(1, 4),      # (top_bottom, left_right) padding
        border_style="yellow",
        expand=False,        # Do not expand to full width
        title="TIMER",
        title_align="left"
    )
    console.print(panel2)
    
    # Check if file exists to write header
    file_exists = os.path.isfile(log_file)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        if not file_exists:
            f.write('Date,Icon,Name,Time,Category\n')
        # Write a new CSV line with quoted fields
        line = f'"{start_time}","{emoji}","{title}","{duration_str}","{category}"\n'
        f.write(line)
    
    icon_path = os.path.join(base_dir, 'emojis', selected_message[2])
    
    icon = {
        'src': icon_path,
        'placement': 'appLogoOverride'
    }
    
    content = f"{selected_message[1]} — {timer_duration}"
    def noop(*args, **kwargs):
        pass
    
    sound_path = os.path.join(base_dir, 'sound', 'pop.wav')
    def duck(*args, **kwargs):
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        time.sleep(1)
    
    toast(
        title=f"{emoji} {title}",
        body=content,
        icon=icon,
        duration="long",
        button=selected_message[0],
        scenario='reminder',
        on_click=duck,
        on_dismissed=noop,
        on_failed=noop
    )

if __name__ == "__main__":
    main()
