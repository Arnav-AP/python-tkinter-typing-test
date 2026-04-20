from tkinter import *
import time
import random
import urllib.request
import words

"""Typing speed test GUI.

The app shows a randomly generated prompt, starts timing on the first
keystroke, and reports raw/net speed with accuracy at the end of a run.
"""

root=Tk()
root.title("Typing Test Application")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# UI color palette
BG_MAIN = "#0f172a"
BG_CARD = "#1e293b"
BG_SHADOW = "#020617"
TEXT_PRIMARY = "#e2e8f0"
ACCENT = "#38bdf8"
ERROR_COLOR = "#f87171"

root.configure(bg=BG_MAIN)

# Runtime state for an active typing session.
timer_started = False
time_left = 30
timer_over = False
start_time = None

def countdown():
    """Update the timer label every second and finish the test at zero."""
    global time_left, time_label, timer_over

    if time_left > 0:
        time_left -= 1
        time_label.config(text=f"Time Left: {time_left}")
        root.after(1000, countdown)
    else:
        time_label.config(text="Time's up!")
        timer_over = True
        evaluate_typing()


def evaluate_typing():
    """Compute and display speed/accuracy stats for the current attempt."""
    global txt_entry, start_time

    end_time = time.perf_counter()
    time_taken = end_time - start_time

    user_input = txt_entry.get("1.0", END).strip()
    target_text = random_text

    # Total typed characters (excluding trailing newline from Text widget).
    total = len(user_input)

    # Character-level correctness is position-sensitive.
    correct = 0
    for i in range(min(len(user_input), len(target_text))):
        if user_input[i] == target_text[i]:
            correct += 1

    errors = total - correct

    time_minutes = time_taken / 60 if time_taken > 0 else 1

    # Raw speed uses all typed characters regardless of mistakes.
    rcpm = total / time_minutes
    rwpm = (total / 5) / time_minutes

    # Net speed applies an error penalty.
    wpm = rwpm - (errors / time_minutes)
    cpm = wpm * 5

    accuracy = (correct / total) * 100 if total > 0 else 0

    result_label.config(
        text=(
            f"Raw WPM: {int(rwpm)} | Net WPM: {int(wpm)}\n"
            f"Raw CPM: {int(rcpm)} | Net CPM: {int(cpm)}\n"
            f"Accuracy: {int(accuracy)}% | Errors: {errors}"
        )
    )

    # Position the result card relative to the input area.
    y_pos = txt_entry.winfo_y() + 180
    result_shadow.place(x=30, y=y_pos + 5)
    result_bg.place(x=25, y=y_pos)
    result_label.place(x=40, y=y_pos + 15)

    restart_button.place(x=1260, y=y_pos + 15)

    txt_entry.config(state="disabled")


def restart_test():
    """Reset UI/state and prepare a fresh prompt without restarting the app."""
    global timer_started, timer_over, time_left, start_time, random_text

    timer_started = False
    timer_over = False
    time_left = 30
    start_time = None

    time_label.config(text="Time Left: 30")

    # Regenerate prompt and redraw the prompt canvas.
    random_text = words.generate_typing_text(word_list, num_words=30)
    canvas.delete("all")
    canvas.create_text(10, 10, anchor=NW, text=random_text, font=("Arial", 18), fill=TEXT_PRIMARY, width=1300)

    # Re-enable typing input and rebind first-keystroke start logic.
    txt_entry.config(state="normal")
    txt_entry.delete("1.0", END)
    txt_entry.focus_set()
    txt_entry.bind("<KeyPress>", lambda event: start_test(event, random_text, time_label))

    result_label.place_forget()
    result_bg.place_forget()
    result_shadow.place_forget()
    restart_button.place_forget()


def start_test(event, target_text, time_label):
    """Start timer on first keypress and auto-finish on exact prompt match."""
    global timer_started, start_time
    
    # Start the timer on the first key press only.
    if not timer_started and not timer_over:
        timer_started = True
        start_time = time.perf_counter()
        countdown()

    # Keep checking for completion while the timer is active.
    user_input = txt_entry.get("1.0", END).strip()
    if user_input == random_text and not timer_over:
        evaluate_typing()


# Prompt source data and initial prompt for the first run.
word_list = words.get_word_list()
random_text = words.generate_typing_text(word_list, num_words=30)

# Header and instructions.
welcome_label=Label(root, text="Welcome to the Typing Test Application",
                    font=("Impact", 24, "bold"),
                    bg=BG_MAIN, fg=TEXT_PRIMARY)
welcome_label.pack(side=TOP, padx=20, pady=20)

instructions_label=Label(root,
    text="Instructions: Type the given text as fast and accurately as you can.",
    font=("Arial", 14),
    bg=BG_MAIN, fg="#94a3b8")
instructions_label.pack(side=TOP, padx=20, pady=10)

text_label=Label(root, text="Press any key to type:",
                 font=("Impact", 16, "bold"),
                 bg=BG_MAIN, fg=TEXT_PRIMARY)
text_label.pack(side=TOP, anchor=W, padx=20, pady=10)

time_label=Label(root, text=f"Time Left: {time_left}",
                 font=("Impact", 20, "bold"),
                 fg=ERROR_COLOR, bg=BG_MAIN)
time_label.pack(side=TOP, anchor=E, padx=60, pady=10)

# Prompt display card.
shadow = Canvas(root, width=1350, height=160, bg=BG_SHADOW, highlightthickness=0)
shadow.place(x=40, y=260, anchor=NW)

canvas = Canvas(root, width=1350, height=150, bg=BG_CARD, highlightthickness=0)
canvas.place(x=30, y=250, anchor=NW)

canvas.create_text(10, 10, anchor=NW, text=random_text,
                   font=("Arial", 18), fill=TEXT_PRIMARY, width=1300)

# Typing input area.
txt_entry=Text(root, height=5, width=113,
               font=("Arial", 16),
               bg=BG_CARD, fg=TEXT_PRIMARY,
               insertbackground=TEXT_PRIMARY)
txt_entry.place(x=30, y=450)

txt_entry.focus_set()
txt_entry.bind("<KeyPress>", lambda event: start_test(event, random_text, time_label))


# Result card (hidden until test ends).
result_shadow = Canvas(root, width=500, height=120, bg=BG_SHADOW, highlightthickness=0)
result_shadow.place(x=30, y=560)

result_bg = Canvas(root, width=490, height=110, bg=BG_CARD, highlightthickness=0)
result_bg.place(x=25, y=555)

result_label = Label(
    root,
    text="",
    font=("Arial", 16, "bold"),
    bg=BG_CARD,
    fg=TEXT_PRIMARY,
    justify=LEFT
)

result_label.place(x=40, y=570)

result_label.place_forget()
result_bg.place_forget()
result_shadow.place_forget()


# Action to start a new run after results are shown.
restart_button = Button(
    root,
    text="Restart Test",
    font=("Arial", 14, "bold"),
    bg=ACCENT,
    fg="black",
    activebackground="#0284c7",
    command=restart_test
)

restart_button.place_forget()

root.mainloop()

