import tkinter as tk
from tkinter import messagebox
import random, time, os, math, datetime, ctypes, subprocess, sys

try:
    import psutil
except ImportError:
    psutil = None


try:
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

PET_NAME = "Pebble"

HUNGER_EVERY_MIN = 20
WATER_EVERY_MIN = 45
QUOTE_EVERY_MIN = 30

WATCH_FOLDER = r"C:\Users\dhars\OneDrive\Desktop\Desktop-Pet"

SIT_REMIND_MIN = 60
WATCH_SCREEN = True

# ---- Pebble laptop companion settings ----
LOW_BATTERY_PERCENT = 20
BREAK_EVERY_MIN = 60
BATTERY_CHECK_MIN = 2

# Changed from 30 → 5 so music is detected quickly
ACTIVITY_CHECK_SEC = 5

# How often Pebble checks Windows audio
MUSIC_CHECK_SEC = 5

FILE_WATCH_EXTENSIONS = (".py", ".txt", ".json", ".csv", ".md")

AUTO_REACT_COOLDOWN_MIN = 10

NIGHT_START_HOUR = 23
NIGHT_END_HOUR = 7

LONG_OPEN_APPS = {
    "chrome.exe": 180,
    "notepad.exe": 60,
}
# =======================================================


W, H = 260, 230
KEY = "#010203"
GROUND_OFFSET = 48


QUOTES = [
    "You're doing better than you think! 🌟",
    "Small steps still move you forward. 🐾",
    "Bugs are just plot twists. You've got this!",
    "Breathe in, breathe out. You're awesome. 💖",
    "Progress, not perfection! ✨",
    "Every expert was once a beginner. 🌱",
    "Be proud of how far you've come!",
]

POKES = [
    "Hehe, that tickles! 😸",
    "Honk honk! 🐧",
    "*happy waddle*",
    "Boop! 👉🐽",
    "Hey! I was napping! 😾",
    "Pets are my favourite! 💕",
    "Wanna play? 🎾"
]

WATER = [
    "Penguins love water. You too! Drink up! 💧",
    "Hydration check! Drink up! 🥤",
    "Your brain is 75% water. Refill it! 💦"
]

FOODS = {
    "Fish": (
        "🐟",
        [
            "FISH!! Best day ever! 🐟",
            "Gulp! Straight down the hatch!"
        ]
    ),

    "Shrimp": (
        "🦐",
        [
            "Shrimpy snack! Yum! 🦐",
            "Crunchy and delicious!"
        ]
    ),

    "Ice cream": (
        "🍦",
        [
            "Brain freeze! ...worth it. 🍦",
            "A penguin eating ice cream. Peak comedy."
        ]
    ),

    "Pizza": (
        "🍕",
        [
            "Pizza?! You are my favourite human! 🍕",
            "Cheese stretch!! 🧀"
        ]
    ),

    "Broccoli": (
        "🥦",
        [
            "...Ew. Fine. *chews sadly* 🥦",
            "I ate it. Where's my fish?"
        ]
    ),
}

HUNGRY = [
    "My tummy just growled... 🥺",
    "I'm hungry! Got any fish? 🐟",
    "So hungry I could eat my own flippers! 😭",
    "Feed me fish or I'll start eating your cursor! 🖱️",
]

STUFFED = [
    "I'm stuffed! ...okay, maybe one tiny bite. 😋",
    "Can't... eat... more... *burp* 😳"
]

JOKES = [
    "What do you call a penguin in the desert? Lost! 🏜️",
    "Why did the penguin cross the road? To get to the other slide! 🛝",
    "Why do programmers prefer dark mode? Light attracts bugs! 🐛",
    "There are 10 kinds of people: those who get binary and those who don't. 🤓",
    "How do penguins say hello? 'Ice to meet you!' 🧊",
]

FACTS = [
    "Fun fact: some penguins propose with a pebble. That's where my name comes from! 🪨💙",
    "Fun fact: gentoo penguins swim around 35 km/h. Zoom! 🌊",
    "Fun fact: a group of penguins waddling on land is called a waddle! 🐧🐧🐧",
    "Fun fact: emperor penguins can dive deeper than 500 metres! 🤿",
]

SWEET_NOTES = [
    "Stand up, stretch, and look far away for 20 seconds. 💙",
    "Roll your shoulders and sip some water. I care about you! 🐧",
    "Take a tiny walk? I'll wait right here for you. 🥹",
    "You're doing amazing. Now rest those eyes a little. ✨",
    "Be kind to your body today, it carries all your big dreams. 💕",
]

WELCOME_BACK = [
    "Welcome back! I missed you! 🥹",
    "You're back! I kept your spot warm. 🐧",
    "Yay, you're awake! Did you dream of fish? 🐟",
]

BATTERY_MESSAGES = [
    "Umm... your battery is getting hungry too! 🔋🥺",
    "Pebble says: please charge the laptop! 🔌🐧",
    "Low battery alert! I don't want us to disappear! 😭🔋",
]

PLUG_MESSAGES = [
    "Yay! Power! 🔌✨",
    "We're charging! Pebble feels safe again. 🐧💙",
    "Connected to power! Time to get things done! ⚡",
]

UNPLUG_MESSAGES = [
    "Going mobile? I'll come with you! 🐧",
    "Charger unplugged! Adventure mode! 🎒",
]

WORK_MESSAGES = [
    "You've been working hard. Tiny break? 🐧💙",
    "Stretch break! Your penguin has spoken. 😌",
    "One minute away from the screen won't hurt. 👀✨",
]

NIGHT_MESSAGES = [
    "It's getting late... even penguins need sleep. 🌙🐧",
    "Pebble recommends sleepy mode now. 😴",
    "Still working? Your penguin is concerned. 🥺🌙",
]

NEW_FILE_MESSAGES = [
    "Ooh! Something changed in your project! 👀💻",
    "I saw you working on a file! Nice! 🐧✨",
    "New project activity detected! Keep going! 🚀",
]

# ================== MUSIC MESSAGES ==================

MUSIC_START_MESSAGES = [
    "MUSIC?! LET'S DANCE! 🎵🐧💃",
    "Ohhh! I hear music! Time to groove! 🎶🐧",
    "My favourite song! DANCE MODE ON! 🕺🎵",
    "Pebble has entered party mode! 🎉🐧",
]

MUSIC_STOP_MESSAGES = [
    "Aww... music stopped. 🥺🎵",
    "No more music? Back to waddling... 🐧",
    "Party's over... for now. 😴🎶",
]

# =====================================================


INTERACTIVE_EVENTS = [
    ("👀 Hey! Look at me!", "wave"),
    ("🐧 I'm bored... move your mouse and I'll chase you!", "chase"),
    ("🎮 Quick game? Right-click me!", "game"),
    ("💬 Tell me something!", "chat"),
    ("👉 Psst... poke me!", "poke"),
    ("🕺 Watch this!", "dance"),
    ("🐟 I could really go for a fish...", "hungry"),
]


WATCH_RULES = [
    (
        ["youtube", "netflix", "prime video", "hotstar"],
        [
            "Ooh, what are we watching? 🍿 Save me a seat!",
            "Movie time! Don't forget to blink! 👀"
        ]
    ),

    (
        ["visual studio code", "pycharm", "intellij", "sublime", "jupyter"],
        [
            "Coding time! Show those bugs who's boss! 💻",
            "I'll cheer quietly from here... 📣"
        ]
    ),

    (
        ["instagram", "facebook", "twitter", "reddit", "whatsapp"],
        [
            "Scrolling time? Remember to look up sometimes! 👀",
            "Say hi to everyone for me! 💬"
        ]
    ),

    (
        ["microsoft word", "excel", "powerpoint"],
        [
            "Working hard! So proud of you! 📊",
            "Productivity mode: ON! 🚀"
        ]
    ),
]


CODE_OK = [
    "Code looks clean! ✨",
    "No errors! You're a wizard 🧙",
    "Syntax looks purrfect! 😻"
]


class Pet:

    def __init__(s):

        s.root = r = tk.Tk()

        r.overrideredirect(True)
        r.attributes("-topmost", True)
        r.attributes("-transparentcolor", KEY)

        s.sw = r.winfo_screenwidth()
        s.sh = r.winfo_screenheight()

        s.ground = s.sh - H - GROUND_OFFSET

        s.x = random.randint(0, s.sw - W)
        s.y = s.ground

        s.c = tk.Canvas(
            r,
            width=W,
            height=H,
            bg=KEY,
            highlightthickness=0
        )

        s.c.pack()

        s.dir = 1
        s.mode = "idle"
        s.t = 0
        s.hop = 0
        s.vy = 0

        s.mode_until = 0
        s.last_catch = 0
        s.bubble_job = None

        s.press = None
        s.dragging = False

        s.mtimes = {}
        s.ask_cooldown = {}

        s.hunger = 0
        s.eating_until = 0
        s.food_emoji = ""

        s.look = (0, 0)
        s.game_win = None

        s.sit_start = None
        s.last_sit_note = 0
        s.last_loop = time.time()

        s.last_title = ""
        s.watch_cool = 0

        # ================= LAPTOP COMPANION =================

        s.last_battery_check = 0
        s.last_battery = None
        s.last_plugged = None

        s.last_activity_check = 0

        s.work_started = time.time()
        s.last_break_note = 0

        s.last_night_note = 0

        s.last_file_reaction = 0
        s.last_file_scan = 0
        s.file_mtimes = {}

        s.was_sleeping = False

        s.last_interaction_event = time.time()
        s.interaction_cooldown = random.uniform(120, 240)

        # ================= MUSIC STATE =================

        s.music_playing = False
        s.last_music_check = 0

        # ====================================================

        # Mouse events
        s.c.bind("<ButtonPress-1>", s.on_press)
        s.c.bind("<B1-Motion>", s.on_drag)
        s.c.bind("<ButtonRelease-1>", s.on_release)

        s.c.bind(
            "<Double-Button-1>",
            lambda e: s.interactive_event(force=True)
        )

        s.c.bind(
            "<Button-3>",
            lambda e: s.menu.tk_popup(e.x_root, e.y_root)
        )

        r.bind(
            "<space>",
            lambda e: s.interactive_event(force=True)
        )

        # ================= CONTEXT MENU =================

        s.menu = tk.Menu(r, tearoff=0)

        pm = tk.Menu(s.menu, tearoff=0)

        pm.add_command(
            label="🏃 Chase me",
            command=s.play
        )

        pm.add_command(
            label="🐟 Catch the fish",
            command=s.game_fish
        )

        pm.add_command(
            label="✊ Rock-paper-scissors",
            command=s.game_rps
        )

        s.menu.add_cascade(
            label="🎾 Play with me",
            menu=pm
        )

        fm = tk.Menu(s.menu, tearoff=0)

        for name, (emo, _) in FOODS.items():

            fm.add_command(
                label=f"{emo} {name}",
                command=lambda n=name: s.feed(n)
            )

        s.menu.add_cascade(
            label="🍽️ Feed me",
            menu=fm
        )

        s.menu.add_command(
            label="💬 Say something",
            command=s.chatter
        )

        s.menu.add_command(
            label="💧 Water reminder",
            command=lambda: s.say(random.choice(WATER))
        )

        s.menu.add_command(
            label="🔋 Laptop status",
            command=s.show_laptop_status
        )

        s.menu.add_command(
            label="✨ Surprise me",
            command=lambda: s.interactive_event(force=True)
        )

        s.menu.add_separator()

        s.menu.add_command(
            label="👋 Bye",
            command=r.destroy
        )

        # ================= START LOOPS =================

        s.place()

        r.after(1500, s.greet)

        r.after(50, s.tick)

        r.after(
            WATER_EVERY_MIN * 60000,
            s.water_loop
        )

        r.after(
            QUOTE_EVERY_MIN * 60000,
            s.quote_loop
        )

        r.after(
            60000,
            s.apps_loop
        )

        r.after(
            HUNGER_EVERY_MIN * 60000,
            s.hunger_loop
        )

        r.after(
            30000,
            s.presence_loop
        )

        if WATCH_SCREEN:
            r.after(
                15000,
                s.watch_loop
            )

        r.after(
            4000,
            s.code_loop
        )

        r.after(
            5000,
            s.companion_loop
        )


    def show_laptop_status(self):

        percent, plugged = self.get_battery()

        if percent is None:
            self.say(
                "I couldn't read the laptop battery right now. 🥺"
            )
            return

        power = (
            "plugged in 🔌"
            if plugged
            else
            "on battery 🔋"
        )

        self.say(
            f"Battery: {percent}% — {power}",
            7000
        )


    def say(self, text, ms=6000):

        c = self.c

        c.delete("bubble")

        if self.bubble_job:

            try:
                self.root.after_cancel(
                    self.bubble_job
                )
            except Exception:
                pass

        t = c.create_text(
            W // 2,
            86,
            text=text,
            width=210,
            anchor="s",
            font=("Segoe UI", 10),
            fill="#333",
            tags="bubble"
        )

        x1, y1, x2, y2 = c.bbox(t)

        r = c.create_rectangle(
            x1 - 9,
            y1 - 6,
            x2 + 9,
            y2 + 6,
            fill="white",
            outline="#ff8fab",
            width=2,
            tags="bubble"
        )

        tail = c.create_polygon(
            W // 2 - 8,
            y2 + 6,
            W // 2 + 8,
            y2 + 6,
            W // 2,
            y2 + 16,
            fill="white",
            outline="#ff8fab",
            width=2,
            tags="bubble"
        )

        c.tag_lower(tail, t)
        c.tag_lower(r, t)

        self.bubble_job = self.root.after(
            ms,
            lambda: c.delete("bubble")
        )


    def greet(self):

        h = datetime.datetime.now().hour

        part = (
            "Good morning"
            if h < 12
            else
            "Good afternoon"
            if h < 18
            else
            "Good evening"
        )

        msg = (
            f"{part}! I'm {PET_NAME} 🐾 "
            f"Ready to have a great day?"
        )

        if psutil and time.time() - psutil.boot_time() < 300:

            msg = (
                f"{part}! Fresh restart — "
                f"I missed you! 💖"
            )

        self.say(msg, 8000)

        self.hop = 15


    def water_loop(self):

        self.say(
            random.choice(WATER),
            8000
        )

        self.hop = 15

        self.root.after(
            WATER_EVERY_MIN * 60000,
            self.water_loop
        )


    def chatter(self):

        self.say(
            random.choice(
                QUOTES + QUOTES + JOKES + FACTS
            ),
            9000
        )

        self.hop = 15


    def quote_loop(self):

        self.chatter()

        self.root.after(
            int(
                QUOTE_EVERY_MIN *
                60000 *
                random.uniform(0.6, 1.4)
            ),
            self.quote_loop
        )



    def idle_seconds(self):

        try:

            class LII(ctypes.Structure):

                _fields_ = [
                    ("cbSize", ctypes.c_uint),
                    ("dwTime", ctypes.c_uint)
                ]

            li = LII()

            li.cbSize = ctypes.sizeof(li)

            ctypes.windll.user32.GetLastInputInfo(
                ctypes.byref(li)
            )

            k = ctypes.windll.kernel32

            k.GetTickCount.restype = ctypes.c_uint

            return (
                (
                    k.GetTickCount() -
                    li.dwTime
                )
                & 0xFFFFFFFF
            ) / 1000.0

        except Exception:

            return 0.0


    def presence_loop(self):

        now = time.time()

        if now - self.last_loop > 120:

            self.sit_start = None

            self.say(
                random.choice(WELCOME_BACK),
                8000
            )

            self.hop = 15

        self.last_loop = now

        if self.idle_seconds() > 300:

            self.sit_start = None

        else:

            if self.sit_start is None:
                self.sit_start = now

            sat = (
                now -
                self.sit_start
            ) / 60

            if (
                sat >= SIT_REMIND_MIN
                and
                now - self.last_sit_note > 30 * 60
            ):

                self.last_sit_note = now

                self.say(
                    f"You've been here {int(sat)} min. "
                    f"{random.choice(SWEET_NOTES)}",
                    12000
                )

                self.hop = 15

        self.root.after(
            30000,
            self.presence_loop
        )


    def active_title(self):

        try:

            u = ctypes.windll.user32

            h = u.GetForegroundWindow()

            n = u.GetWindowTextLengthW(h)

            buf = ctypes.create_unicode_buffer(
                n + 1
            )

            u.GetWindowTextW(
                h,
                buf,
                n + 1
            )

            return buf.value.lower()

        except Exception:

            return ""


    def watch_loop(self):

        title, now = (
            self.active_title(),
            time.time()
        )

        if (
            title
            and
            title != self.last_title
            and
            now > self.watch_cool
        ):

            for words, lines in WATCH_RULES:

                if any(
                    w in title
                    for w in words
                ):

                    self.say(
                        random.choice(lines),
                        7000
                    )

                    self.watch_cool = (
                        now +
                        10 * 60
                    )

                    break

        self.last_title = title

        self.root.after(
            15000,
            self.watch_loop
        )



    def interactive_event(self, force=False):

        now = time.time()

        if (
            not force
            and
            now - self.last_interaction_event
            <
            self.interaction_cooldown
        ):
            return

        self.last_interaction_event = now

        self.interaction_cooldown = random.uniform(
            120,
            300
        )

        message, action = random.choice(
            INTERACTIVE_EVENTS
        )

        if action == "wave":

            self.say(
                message,
                5000
            )

            self.hop = 15

        elif action == "chase":

            self.say(
                message,
                6000
            )

            self.set_mode(
                "chase",
                10
            )

        elif action == "game":

            self.say(
                message,
                5000
            )

            self.hop = 12

        elif action == "chat":

            self.chatter()

        elif action == "poke":

            self.say(
                random.choice(POKES),
                4000
            )

            self.hop = 18

        elif action == "dance":

            self.say(
                message,
                4500
            )

            self.set_mode(
                "dance",
                5
            )

        elif action == "hungry":

            self.hunger = max(
                self.hunger,
                1
            )

            self.say(
                random.choice(HUNGRY),
                6000
            )

            self.hop = 12



    def check_mouse_interaction(self):

        try:

            mx = self.root.winfo_pointerx()
            my = self.root.winfo_pointery()

            near_x = (
                self.x - 80
                <= mx
                <= self.x + W + 80
            )

            near_y = (
                self.y - 80
                <= my
                <= self.y + H
            )

            if (
                near_x
                and
                near_y
                and
                self.mode == "sleep"
                and
                not self.music_playing
            ):

                self.set_mode("idle")

                self.say(
                    random.choice(POKES),
                    3000
                )

                self.hop = 12

            if (
                near_x
                and
                near_y
                and
                self.mode == "idle"
            ):

                if random.random() < 0.015:

                    self.say(
                        "Hehe, I see you! 👀🐧",
                        2500
                    )

                    self.hop = 10

        except Exception:
            pass


    def music_is_playing(self):

        """
        Detect active Windows audio sessions.

        Requires:
            pip install pycaw
        """

        if not PYCAW_AVAILABLE:
            return False

        try:

            sessions = (
                AudioUtilities.GetAllSessions()
            )

            for session in sessions:

                try:

                    if not session.Process:
                        continue

                    volume = (
                        session._ctl.QueryInterface(
                            ISimpleAudioVolume
                        )
                    )

                    # Muted sessions are ignored.
                    if volume.GetMasterVolume() <= 0:
                        continue

                    # Windows audio session state:
                    # 1 = active
                    state = session._ctl.GetState()

                    if state == 1:

                        process_name = (
                            session.Process.name()
                            .lower()
                        )

                        # Ignore our own Python/Pebble audio
                        # if applicable.
                        if process_name in (
                            "python.exe",
                            "pythonw.exe"
                        ):
                            continue

                        return True

                except Exception:
                    continue

        except Exception:
            pass

        return False


    def check_music(self):

        """
        Automatically switch Pebble into dance mode
        whenever Windows audio is active.
        """

        now = time.time()

        if (
            now - self.last_music_check
            <
            MUSIC_CHECK_SEC
        ):
            return

        self.last_music_check = now

        playing = self.music_is_playing()

        # ================= MUSIC STARTED =================

        if (
            playing
            and
            not self.music_playing
        ):

            self.music_playing = True

            self.say(
                random.choice(
                    MUSIC_START_MESSAGES
                ),
                5000
            )

            self.hop = 20

            self.set_mode(
                "dance",
                999999
            )


        elif (
            not playing
            and
            self.music_playing
        ):

            self.music_playing = False

            self.set_mode(
                "idle"
            )

            self.say(
                random.choice(
                    MUSIC_STOP_MESSAGES
                ),
                3000
            )


    def get_battery(self):

        try:

            if not psutil:
                return None, None

            battery = (
                psutil.sensors_battery()
            )

            if battery is None:
                return None, None

            return (
                int(battery.percent),
                bool(battery.power_plugged)
            )

        except Exception:

            return None, None


    def check_battery_and_power(self):

        percent, plugged = (
            self.get_battery()
        )

        if percent is None:
            return

        now = time.time()

        if self.last_battery is None:

            self.last_battery = percent
            self.last_plugged = plugged

            return

        if (
            self.last_plugged is not None
            and
            plugged != self.last_plugged
        ):

            if plugged:

                self.say(
                    random.choice(
                        PLUG_MESSAGES
                    ),
                    6000
                )

                self.hop = 15

            else:

                self.say(
                    random.choice(
                        UNPLUG_MESSAGES
                    ),
                    5000
                )

                self.hop = 10

        if (
            percent <= LOW_BATTERY_PERCENT
            and
            now -
            self.last_battery_check
            >
            30 * 60
        ):

            self.last_battery_check = now

            self.say(
                f"{random.choice(BATTERY_MESSAGES)} "
                f"({percent}%)",
                8000
            )

            self.hop = 15

        self.last_battery = percent
        self.last_plugged = plugged

    def check_work_time(self):

        now = time.time()

        idle = self.idle_seconds()

        if idle >= 300:

            self.work_started = now

            return

        worked_min = (
            now -
            self.work_started
        ) / 60

        if (
            worked_min >= BREAK_EVERY_MIN
            and
            now -
            self.last_break_note
            >
            30 * 60
        ):

            self.last_break_note = now

            self.work_started = now

            self.say(
                f"You've been working for "
                f"{int(worked_min)} min. "
                f"{random.choice(WORK_MESSAGES)}",
                9000
            )

            self.hop = 15

    def check_night_mode(self):

        hour = datetime.datetime.now().hour

        is_night = (
            hour >= NIGHT_START_HOUR
            or
            hour < NIGHT_END_HOUR
        )

        if (
            is_night
            and
            time.time() -
            self.last_night_note
            >
            60 * 60
        ):

            self.last_night_note = time.time()

            if self.mode in (
                "idle",
                "walk"
            ):

                self.say(
                    random.choice(
                        NIGHT_MESSAGES
                    ),
                    8000
                )


    def check_project_activity(self):

        if (
            not WATCH_FOLDER
            or
            not os.path.isdir(
                WATCH_FOLDER
            )
        ):
            return

        now = time.time()

        if (
            now -
            self.last_file_scan
            <
            15
        ):
            return

        self.last_file_scan = now

        try:

            changed = False

            for root_, dirs, files in os.walk(
                WATCH_FOLDER
            ):

                dirs[:] = [
                    d
                    for d in dirs
                    if d not in (
                        ".git",
                        "venv",
                        ".venv",
                        "node_modules",
                        "__pycache__"
                    )
                ]

                for f in files:

                    if not f.lower().endswith(
                        FILE_WATCH_EXTENSIONS
                    ):
                        continue

                    path = os.path.join(
                        root_,
                        f
                    )

                    try:

                        mtime = os.path.getmtime(
                            path
                        )

                    except OSError:

                        continue

                    old = self.file_mtimes.get(
                        path
                    )

                    self.file_mtimes[path] = mtime

                    if (
                        old is not None
                        and
                        mtime != old
                    ):

                        changed = True

            if (
                changed
                and
                now -
                self.last_file_reaction
                >
                AUTO_REACT_COOLDOWN_MIN * 60
            ):

                self.last_file_reaction = now

                self.say(
                    random.choice(
                        NEW_FILE_MESSAGES
                    ),
                    6500
                )

                self.hop = 12

        except Exception:
            pass

    def companion_loop(self):

        try:

            self.check_battery_and_power()

            self.check_work_time()

            self.check_night_mode()

            self.check_project_activity()

            self.check_mouse_interaction()

            # NEW: MUSIC DETECTION
            self.check_music()

            # Spontaneous interaction
            # is disabled while music is playing
            # so Pebble stays dancing.
            if not self.music_playing:

                self.interactive_event()

        except Exception:
            pass

        self.root.after(
            ACTIVITY_CHECK_SEC * 1000,
            self.companion_loop
        )

    def end_game(self):

        if self.game_win:

            try:
                self.game_win.destroy()

            except Exception:
                pass

        self.game_win = None


    def game_fish(self):

        if self.game_win:
            return

        self.say(
            "Catch the fish! Click it 5 times before it swims away! 🐟",
            5000
        )

        win = self.game_win = tk.Toplevel(
            self.root
        )

        win.overrideredirect(True)

        win.attributes(
            "-topmost",
            True
        )

        win.attributes(
            "-transparentcolor",
            KEY
        )

        win.configure(
            bg=KEY
        )

        lbl = tk.Label(
            win,
            text="🐟",
            font=("Segoe UI Emoji", 32),
            bg=KEY,
            cursor="hand2"
        )

        lbl.pack()

        st = dict(
            x=random.randint(
                100,
                self.sw - 150
            ),
            y=random.randint(
                100,
                self.sh - 250
            ),
            vx=random.choice(
                [-6, 6]
            ),
            vy=random.choice(
                [-5, 5]
            ),
            score=0,
            end=time.time() + 25
        )


        def move():

            if self.game_win is not win:
                return

            st["x"] += st["vx"]
            st["y"] += st["vy"]

            if (
                st["x"] < 0
                or
                st["x"] > self.sw - 80
            ):
                st["vx"] = -st["vx"]

            if (
                st["y"] < 0
                or
                st["y"] > self.sh - 120
            ):
                st["vy"] = -st["vy"]

            win.geometry(
                f"+{int(st['x'])}+{int(st['y'])}"
            )

            if time.time() > st["end"]:

                self.end_game()

                self.say(
                    "Aww, the fish got away... let's try again! 😿"
                )

                return

            win.after(
                30,
                move
            )


        def caught(_e=None):

            st["score"] += 1

            if st["score"] >= 5:

                self.end_game()

                self.hunger = max(
                    self.hunger,
                    1
                )

                self.feed("Fish")

                return

            k = min(
                1.2,
                18 /
                max(
                    abs(st["vx"]),
                    1
                )
            )

            st["vx"] *= k
            st["vy"] *= k

            st["x"] = random.randint(
                50,
                self.sw - 150
            )

            st["y"] = random.randint(
                50,
                self.sh - 200
            )

            self.say(
                f"Got one! {st['score']}/5 — "
                f"it's getting faster! 😆",
                2000
            )

            self.hop = 10


        lbl.bind(
            "<Button-1>",
            caught
        )

        move()


    def game_rps(self):

        if self.game_win:
            return

        emo = {
            "rock": "✊",
            "paper": "✋",
            "scissors": "✌️"
        }

        beats = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }

        win = self.game_win = tk.Toplevel(
            self.root
        )

        win.title(
            f"Play with {PET_NAME}"
        )

        win.attributes(
            "-topmost",
            True
        )

        win.resizable(
            False,
            False
        )

        win.geometry(
            f"+{int(self.x)}+"
            f"{max(0, int(self.y) - 190)}"
        )

        win.protocol(
            "WM_DELETE_WINDOW",
            self.end_game
        )

        tk.Label(
            win,
            text="Rock, paper, scissors!",
            font=("Segoe UI", 11)
        ).pack(
            padx=16,
            pady=(12, 4)
        )

        row = tk.Frame(win)

        row.pack(
            padx=12,
            pady=10
        )


        def pick(me):

            mine = random.choice(
                list(emo)
            )

            if me == mine:

                msg = (
                    f"{emo[mine]} Tie! "
                    f"Great minds think alike! 🤝"
                )

            elif beats[me] == mine:

                msg = (
                    f"{emo[mine]} You win!! "
                    f"I demand a rematch! 😤"
                )

            else:

                msg = (
                    f"{emo[mine]} I win! "
                    f"Penguin power! 🐧🏆"
                )

            self.say(
                msg,
                4000
            )

            self.hop = 12


        for k in emo:

            tk.Button(
                row,
                text=emo[k],
                font=("Segoe UI Emoji", 22),
                width=3,
                command=lambda k=k: pick(k)
            ).pack(
                side="left",
                padx=4
            )

    def hunger_loop(self):

        self.hunger = min(
            self.hunger + 1,
            4
        )

        self.say(
            HUNGRY[self.hunger - 1],
            8000
        )

        self.hop = 15

        self.root.after(
            HUNGER_EVERY_MIN * 60000,
            self.hunger_loop
        )


    def feed(self, name):

        emo, lines = FOODS[name]

        self.food_emoji = emo

        self.eating_until = (
            time.time() + 3
        )

        self.hop = 15

        if self.hunger == 0:

            self.say(
                random.choice(STUFFED),
                5000
            )

        else:

            self.say(
                random.choice(lines),
                5000
            )

        self.hunger = max(
            0,
            self.hunger - 2
        )


    def apps_loop(self):

        if psutil:

            now = time.time()

            for p in psutil.process_iter(
                ["name", "create_time"]
            ):

                try:

                    name = (
                        p.info["name"]
                        or ""
                    ).lower()

                    limit = (
                        LONG_OPEN_APPS.get(
                            name
                        )
                    )

                    if (
                        not limit
                        or
                        now -
                        p.info["create_time"]
                        <
                        limit * 60
                    ):
                        continue

                    if (
                        now
                        <
                        self.ask_cooldown.get(
                            name,
                            0
                        )
                    ):
                        continue

                    mins = int(
                        (
                            now -
                            p.info["create_time"]
                        ) / 60
                    )

                    self.say(
                        f"{name} has been open "
                        f"{mins} min... 😴"
                    )

                    ok = messagebox.askyesno(
                        PET_NAME,
                        f"{name} has been open "
                        f"for {mins} minutes.\n"
                        f"Close it?"
                    )

                    self.ask_cooldown[name] = (
                        now + 30 * 60
                    )

                    if ok:

                        for q in psutil.process_iter(
                            ["name"]
                        ):

                            if (
                                q.info["name"]
                                or ""
                            ).lower() == name:

                                try:
                                    q.terminate()

                                except Exception:
                                    pass

                        self.say(
                            "Closed! Fresh start! 🧹"
                        )

                    break

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied
                ):
                    pass

        self.root.after(
            60000,
            self.apps_loop
        )


    def code_loop(self):

        try:

            for root_, dirs, files in os.walk(
                WATCH_FOLDER
            ):

                dirs[:] = [
                    d
                    for d in dirs
                    if d not in (
                        ".git",
                        "venv",
                        ".venv",
                        "node_modules",
                        "__pycache__"
                    )
                ]

                for f in files:

                    if not f.endswith(".py"):
                        continue

                    path = os.path.join(
                        root_,
                        f
                    )

                    m = os.path.getmtime(
                        path
                    )

                    old = self.mtimes.get(
                        path
                    )

                    self.mtimes[path] = m

                    if (
                        old is not None
                        and
                        m != old
                    ):

                        self.check_py(path)

        except Exception:
            pass

        self.root.after(
            3000,
            self.code_loop
        )


    def check_py(self, path):

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as fh:

                compile(
                    fh.read(),
                    path,
                    "exec"
                )

            if random.random() < 0.5:

                self.say(
                    f"{os.path.basename(path)}: "
                    f"{random.choice(CODE_OK)}"
                )

                self.hop = 15

        except SyntaxError as e:

            self.say(
                f"Oops! "
                f"{os.path.basename(path)} "
                f"line {e.lineno}: "
                f"{e.msg} 🙀",
                9000
            )

        except Exception:
            pass

    def play(self):

        self.say(
            "Catch me if you can! "
            "Move your mouse! 🏃‍♂️"
        )

        self.set_mode(
            "chase",
            12
        )


    def set_mode(self, m, secs=None):

        self.mode = m

        d = {
            "walk": (4, 10),
            "idle": (3, 7),
            "sleep": (3, 6),
            "slide": (1.5, 3),

            # NEW DANCE MODE
            "dance": (999999, 999999)

        }.get(m)

        self.mode_until = (
            time.time()
            +
            (
                secs
                if secs
                else
                random.uniform(*d)
                if d
                else
                0
            )
        )

        if m in (
            "walk",
            "slide",
            "dance"
        ):

            # Dance starts in a random direction
            if m == "dance":
                self.dir = random.choice(
                    [-1, 1]
                )
            else:
                self.dir = random.choice(
                    [-1, 1]
                )

    def on_press(self, e):

        self.press = (
            e.x_root,
            e.y_root,
            e.x,
            e.y
        )

        self.dragging = False

        if self.mode == "sleep":

            self.set_mode(
                "idle"
            )

            self.say(
                "Oh! You woke me up! 🥱🐧",
                3000
            )

            self.hop = 12


    def on_drag(self, e):

        px, py, ox, oy = self.press

        if (
            not self.dragging
            and
            abs(e.x_root - px)
            +
            abs(e.y_root - py)
            >
            5
        ):

            self.dragging = True

            self.mode = "drag"

            self.say(
                "Weeee! Put me down gently! 🙀",
                3000
            )

        if self.dragging:

            self.x = (
                e.x_root - ox
            )

            self.y = (
                e.y_root - oy
            )


    def on_release(self, e):

        if self.dragging:

            self.vy = 0

            self.mode = "fall"

        else:

            self.say(
                random.choice(POKES),
                3000
            )

            self.hop = 15


    def place(self):

        self.root.geometry(
            f"{W}x{H}+"
            f"{int(self.x)}+"
            f"{int(self.y)}"
        )


    def tick(self):

        self.t += 1

        now = time.time()

        m = self.mode


        if m == "walk":

            self.x += (
                self.dir * 2
            )

            if (
                self.x < 0
                or
                self.x > self.sw - W
            ):

                self.dir *= -1

                self.x = max(
                    0,
                    min(
                        self.x,
                        self.sw - W
                    )
                )

            if now > self.mode_until:

                self.set_mode(
                    "idle"
                )

        elif (
            m == "idle"
            and
            now > self.mode_until
        ):

            self.set_mode(
                random.choice([
                    "walk",
                    "walk",
                    "walk",
                    "walk",
                    "idle",
                    "idle",
                    "slide",
                    "sleep"
                ])
            )


        elif (
            m == "sleep"
            and
            now > self.mode_until
        ):

            self.set_mode(
                "idle"
            )

        elif m == "slide":

            self.x += (
                self.dir * 7
            )

            if (
                self.x < 0
                or
                self.x > self.sw - W
            ):

                self.dir *= -1

                self.x = max(
                    0,
                    min(
                        self.x,
                        self.sw - W
                    )
                )

            if now > self.mode_until:

                self.set_mode(
                    "idle"
                )

                self.say(
                    "Wheee! Belly slide! Again?! 🐧",
                    3000
                )


        elif m == "dance":

            # Move left and right while dancing
            self.x += (
                self.dir * 1.5
            )

            if (
                self.x < 0
                or
                self.x > self.sw - W
            ):

                self.dir *= -1

                self.x = max(
                    0,
                    min(
                        self.x,
                        self.sw - W
                    )
                )

            # If music somehow stopped,
            # immediately leave dance mode.
            if not self.music_playing:

                self.set_mode(
                    "idle"
                )


        # ================= CHASE =================

        elif m == "chase":

            d = (
                self.root.winfo_pointerx()
                -
                W // 2
                -
                self.x
            )

            self.dir = (
                1
                if d > 0
                else -1
            )

            self.x += max(
                -8,
                min(
                    8,
                    d
                )
            )

            if (
                abs(d) < 30
                and
                now -
                self.last_catch
                >
                3
            ):

                self.say(
                    "Gotcha! Tag, you're it! 🐾",
                    2500
                )

                self.hop = 15

                self.last_catch = now

            if now > self.mode_until:

                self.set_mode(
                    "idle"
                )

                self.say(
                    "Phew! That was fun! Again later? 😸"
                )


        # ================= FALL =================

        elif m == "fall":

            self.vy += 1.5

            self.y += self.vy

            if self.y >= self.ground:

                self.y = self.ground

                self.hop = 10

                self.set_mode(
                    "idle"
                )

                self.say(
                    "Landed on my feet! 😹",
                    3000
                )


        if (
            m != "drag"
            and
            m != "fall"
        ):

            self.y = self.ground


        # Eyes follow mouse

        px = (
            self.root.winfo_pointerx()
            -
            (
                self.x +
                W / 2
            )
        )

        py = (
            self.root.winfo_pointery()
            -
            (
                self.y +
                150
            )
        )

        self.look = (
            max(
                -1,
                min(
                    1,
                    px / 250
                )
            ),
            max(
                -1,
                min(
                    1,
                    py / 250
                )
            )
        )

        self.place()

        self.draw()

        self.root.after(
            50,
            self.tick
        )

    DARK = "#2f3b52"
    OUT = "#1c2436"
    ORG = "#ff9a3c"
    ORGO = "#d9701a"


    def draw(self):

        c = self.c
        cx = W // 2
        d = self.dir

        c.delete("pet")

        P = {
            "tags": "pet"
        }

        off = 0

        if self.hop > 0:

            off = -int(
                25 *
                math.sin(
                    math.pi *
                    self.hop /
                    15
                )
            )

            self.hop -= 1


        if self.mode == "slide":

            return self.draw_slide(
                cx,
                165 + 14,
                d
            )


        moving = self.mode in (
            "walk",
            "chase",
            "dance"
        )

        if self.mode == "dance":

            # Bigger side-to-side movement
            sway = int(
                12 *
                math.sin(
                    self.t / 2
                )
            )

            # Bounce to the beat
            bob = int(
                8 *
                abs(
                    math.sin(
                        self.t / 2
                    )
                )
            )

            # Feet move rapidly
            step = int(
                12 *
                math.sin(
                    self.t / 2
                )
            )

        else:

            # Normal movement
            sway = (
                int(
                    5 *
                    math.sin(
                        self.t / 3
                    )
                )
                if moving
                else
                0
            )

            if self.mode in (
                "idle",
                "sleep"
            ):

                bob = int(
                    2 *
                    math.sin(
                        self.t / 5
                    )
                )

            elif moving:

                bob = int(
                    3 *
                    abs(
                        math.sin(
                            self.t / 3
                        )
                    )
                )

            else:

                bob = 0

            step = (
                int(
                    6 *
                    math.sin(
                        self.t / 3
                    )
                )
                if moving
                else
                0
            )


        cy = (
            165 +
            off +
            bob
        )

        bx = cx + sway

        lf = max(
            0,
            step
        )

        rf = max(
            0,
            -step
        )

        c.create_oval(
            cx - 30,
            cy + 38 - lf,
            cx - 6,
            cy + 49 - lf,
            fill=self.ORG,
            outline=self.ORGO,
            **P
        )

        c.create_oval(
            cx + 6,
            cy + 38 - rf,
            cx + 30,
            cy + 49 - rf,
            fill=self.ORG,
            outline=self.ORGO,
            **P
        )

        if self.mode == "dance":

            swing = int(
                25 *
                math.sin(
                    self.t / 2
                )
            )

        elif self.hop > 0:

            swing = -24

        elif moving:

            swing = int(
                10 *
                math.sin(
                    self.t / 3
                )
            )

        else:

            swing = 0


        for sx in (-1, 1):

            tip = (
                cy +
                12 +
                swing
            )

            c.create_polygon(
                bx + sx * 38,
                cy - 18,

                bx + sx * 60,
                tip,

                bx + sx * 52,
                tip + 8,

                bx + sx * 38,
                cy + 8,

                smooth=True,

                fill=self.DARK,
                outline=self.OUT,
                width=2,

                **P
            )

        c.create_oval(
            bx - 43,
            cy - 44,
            bx + 43,
            cy + 44,

            fill=self.DARK,
            outline=self.OUT,
            width=2,

            **P
        )


        # Belly

        c.create_oval(
            bx - 30,
            cy - 18,
            bx + 30,
            cy + 41,

            fill="white",
            outline="",

            **P
        )

        asleep = (
            self.mode == "sleep"
        )

        blink = (
            self.t % 70
        ) < 3

        sad = (
            self.hunger >= 2
        )


        for sx in (-1, 1):

            ex = (
                bx +
                sx * 15 +
                d * 3
            )

            ey = (
                cy -
                14
            )


            if asleep or blink:

                c.create_arc(
                    ex - 8,
                    ey - 4,
                    ex + 8,
                    ey + 8,

                    start=200,
                    extent=140,

                    style="arc",
                    width=2,

                    outline="white",

                    **P
                )

            else:

                c.create_oval(
                    ex - 8,
                    ey - 9,
                    ex + 8,
                    ey + 9,

                    fill="white",
                    outline="",

                    **P
                )

                r = (
                    5
                    if sad
                    else
                    4
                )

                ox = int(
                    self.look[0] * 4
                )

                oy = int(
                    self.look[1] * 4
                )

                c.create_oval(
                    ex - r + ox,
                    ey - r + oy,
                    ex + r + ox,
                    ey + r + oy,

                    fill="#111",
                    outline="",

                    **P
                )

                c.create_oval(
                    ex - 2 + ox,
                    ey - 4 + oy,
                    ex + ox,
                    ey - 2 + oy,

                    fill="white",
                    outline="",

                    **P
                )


            if (
                sad
                and
                not asleep
            ):

                c.create_line(
                    ex - 7,
                    ey - 12 -
                    (
                        2
                        if sx == -1
                        else
                        0
                    ),

                    ex + 7,
                    ey - 12 -
                    (
                        2
                        if sx == 1
                        else
                        0
                    ),

                    fill="white",
                    width=2,

                    **P
                )

        for sx in (-1, 1):

            c.create_oval(
                bx + sx * 27 - 6 + d * 2,
                cy - 5,

                bx + sx * 27 + 6 + d * 2,
                cy + 3,

                fill="#ff9db6",
                outline="",

                stipple="gray50",

                **P
            )

        bk = (
            bx +
            d * 3
        )


        if time.time() < self.eating_until:

            o = (
                3 +
                int(
                    6 *
                    abs(
                        math.sin(
                            self.t / 2
                        )
                    )
                )
            )

            c.create_oval(
                bk - 6,
                cy - 2,
                bk + 6,
                cy + 5 + o,

                fill="#8b2e4a",
                outline="",

                **P
            )

            c.create_polygon(
                bk - 8,
                cy - 4,

                bk + 8,
                cy - 4,

                bk,
                cy + 5,

                fill=self.ORG,
                outline=self.ORGO,

                **P
            )

            c.create_polygon(
                bk - 5,
                cy + 5 + o,

                bk + 5,
                cy + 5 + o,

                bk,
                cy + 11 + o,

                fill=self.ORG,
                outline=self.ORGO,

                **P
            )

            c.create_text(
                bx,
                cy - 62 -
                int(
                    3 *
                    math.sin(
                        self.t / 2
                    )
                ),

                text=self.food_emoji,

                font=(
                    "Segoe UI Emoji",
                    16
                ),

                **P
            )

        else:

            c.create_polygon(
                bk - 8,
                cy - 4,

                bk + 8,
                cy - 4,

                bk,
                cy + 9,

                fill=self.ORG,
                outline=self.ORGO,
                width=1,

                **P
            )

            c.create_line(
                bk - 6,
                cy,

                bk + 6,
                cy,

                fill=self.ORGO,

                **P
            )


        if asleep:

            c.create_text(
                cx + 55,
                cy - 55 +
                int(
                    4 *
                    math.sin(
                        self.t / 6
                    )
                ),

                text="Z z z",

                font=(
                    "Segoe UI",
                    12,
                    "bold"
                ),

                fill="#8a8aff",

                **P
            )


        if self.mode == "dance":

            # Little music notes around Pebble
            notes = ["♪", "♫", "♬"]

            note = notes[
                (self.t // 8)
                % len(notes)
            ]

            c.create_text(
                bx - 65,
                cy - 55 +
                int(
                    8 *
                    math.sin(
                        self.t / 5
                    )
                ),

                text=note,

                font=(
                    "Segoe UI",
                    18,
                    "bold"
                ),

                fill="#ff8fab",

                **P
            )

            c.create_text(
                bx + 60,
                cy - 35 +
                int(
                    8 *
                    math.cos(
                        self.t / 5
                    )
                ),

                text=notes[
                    (self.t // 12 + 1)
                    % len(notes)
                ],

                font=(
                    "Segoe UI",
                    16,
                    "bold"
                ),

                fill="#9fd3ff",

                **P
            )

    def draw_slide(
        self,
        cx,
        cy,
        d
    ):

        c = self.c

        P = {
            "tags": "pet"
        }

        for i in range(3):

            c.create_line(
                cx -
                d *
                (70 + i * 8),

                cy -
                14 +
                i * 12,

                cx -
                d *
                (95 + i * 8),

                cy -
                14 +
                i * 12,

                fill="#9fd3ff",
                width=2,

                **P
            )


        c.create_oval(
            cx -
            d * 62 -
            10,

            cy + 2,

            cx -
            d * 62 +
            14,

            cy + 12,

            fill=self.ORG,
            outline=self.ORGO,

            **P
        )


        c.create_oval(
            cx - 52,
            cy - 24,
            cx + 52,
            cy + 24,

            fill=self.DARK,
            outline=self.OUT,
            width=2,

            **P
        )


        c.create_oval(
            cx - 44,
            cy + 6,
            cx + 44,
            cy + 24,

            fill="white",
            outline="",

            **P
        )


        wob = int(
            4 *
            math.sin(
                self.t
            )
        )


        c.create_polygon(
            cx - d * 4,
            cy - 14,

            cx - d * 40,
            cy - 34 + wob,

            cx - d * 28,
            cy - 8,

            smooth=True,

            fill=self.DARK,
            outline=self.OUT,
            width=2,

            **P
        )


        hx = (
            cx +
            d * 44
        )


        c.create_oval(
            hx - 17,
            cy - 22,
            hx + 17,
            cy + 14,

            fill=self.DARK,
            outline=self.OUT,
            width=2,

            **P
        )


        c.create_polygon(
            hx + d * 14,
            cy - 6,

            hx + d * 14,
            cy + 4,

            hx + d * 28,
            cy - 1,

            fill=self.ORG,
            outline=self.ORGO,

            **P
        )


        c.create_oval(
            hx + d * 3 - 6,
            cy - 14,

            hx + d * 3 + 6,
            cy - 2,

            fill="white",
            outline="",

            **P
        )


        c.create_oval(
            hx + d * 5 - 3,
            cy - 11,

            hx + d * 5 + 3,
            cy - 5,

            fill="#111",
            outline="",

            **P
        )


        c.create_oval(
            hx - 6,
            cy - 2,

            hx + 4,
            cy + 4,

            fill="#ff9db6",
            outline="",

            stipple="gray50",

            **P
        )

if __name__ == "__main__":

    if not PYCAW_AVAILABLE:

        print(
            "\n⚠️ pycaw is not installed.\n"
            "Music detection will not work.\n\n"
            "Install it with:\n"
            "pip install pycaw\n"
        )

    Pet().root.mainloop()
