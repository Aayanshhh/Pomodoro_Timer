from tkinter import *
import math
from tkinter import messagebox
from tkinter import ttk

# Constants
PINK = "#e2989c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer_id = None
paused = False
pause_time = 0


# Timer Mechanism
def start_timer():
    global reps
    global paused
    global pause_time

    paused = False
    pause_time = 0

    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        timer.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer.config(text="Break", fg=PINK)
    else:
        count_down(work_sec)
        timer.config(text="Work", fg=GREEN)


def reset_timer():
    global reps
    global paused
    global pause_time

    if timer_id:
        window.after_cancel(timer_id)

    reps = 0
    paused = False
    pause_time = 0
    timer.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    progress_bar['value'] = 0
    check_marks.config(text="")


def count_down(count):
    global timer_id
    global pause_time

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    else:
        count_sec = f"{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    progress_bar['value'] = ((WORK_MIN * 60 - count) / (WORK_MIN * 60)) * 100

    if count > 0:
        timer_id = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


def pause_timer():
    global paused
    global pause_time
    if not paused:
        if timer_id:
            window.after_cancel(timer_id)
        paused = True
        current_time = canvas.itemcget(timer_text, "text")
        time_parts = current_time.split(":")
        pause_time = int(time_parts[0]) * 60 + int(time_parts[1])
        pause_button.config(text="Resume")
    else:
        paused = False
        count_down(pause_time)
        pause_button.config(text="Pause")


def open_settings():
    settings_window = Toplevel(window)
    settings_window.title("Settings")
    settings_window.config(bg=YELLOW, padx=20, pady=20)

    Label(settings_window, text="Work Duration (minutes):", bg=YELLOW).grid(row=0, column=0, pady=5)
    Label(settings_window, text="Short Break Duration (minutes):", bg=YELLOW).grid(row=1, column=0, pady=5)
    Label(settings_window, text="Long Break Duration (minutes):", bg=YELLOW).grid(row=2, column=0, pady=5)

    work_entry = Entry(settings_window)
    work_entry.insert(0, WORK_MIN)
    work_entry.grid(row=0, column=1, pady=5)

    short_break_entry = Entry(settings_window)
    short_break_entry.insert(0, SHORT_BREAK_MIN)
    short_break_entry.grid(row=1, column=1, pady=5)

    long_break_entry = Entry(settings_window)
    long_break_entry.insert(0, LONG_BREAK_MIN)
    long_break_entry.grid(row=2, column=1, pady=5)

    def save_settings():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
        try:
            WORK_MIN = int(work_entry.get())
            SHORT_BREAK_MIN = int(short_break_entry.get())
            LONG_BREAK_MIN = int(long_break_entry.get())
            settings_window.destroy()
        except ValueError:
            messagebox.showerror(title="Invalid Input", message="Please enter valid integer values.")

    save_button = Button(settings_window, text="Save", command=save_settings)
    save_button.grid(row=3, column=0, columnspan=2, pady=20)


# UI Setup
window = Tk()
window.title("Pomodoro")
window.config(bg=YELLOW, padx=100, pady=50)

timer = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 35, "bold"), bg=YELLOW)
timer.grid(row=0, column=1)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

style = ttk.Style()
style.configure("TButton", font=(FONT_NAME, 12, "bold"), background=YELLOW, foreground=GREEN, padding=10)
style.map("TButton", background=[('active', PINK)])

start_button = ttk.Button(text="Start", command=start_timer, style="TButton")
start_button.grid(row=2, column=0, padx=5, pady=10)

pause_button = ttk.Button(text="Pause", command=pause_timer, style="TButton")
pause_button.grid(row=2, column=1, padx=5, pady=10)

reset_button = ttk.Button(text="Reset", command=reset_timer, style="TButton")
reset_button.grid(row=2, column=2, padx=5, pady=10)

settings_button = ttk.Button(text="Settings", command=open_settings, style="TButton")
settings_button.grid(row=3, column=1, pady=20)

check_marks = Label(text="", fg=GREEN, bg=YELLOW)
check_marks.grid(row=4, column=1)

progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=200, mode='determinate')
progress_bar.grid(row=5, column=1, pady=20)

window.mainloop()
