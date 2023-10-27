from tkinter import *
import math
import os

# ---------------------------- CONSTANTS ------------------------------- #
LG = "#97bfe2"
BG = "#637687"
FONT_NAME = "Courier"
FIVE_MIN = 5
timer = None
clock_on = False
five_min_lapse = 0
seven_min_lapse = 0
message_notif = ""
beenIdle = True
# ---------------------------- TIMER RESET ------------------------------- #
def timer_restart():
    global clock_on
    if clock_on:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")
    else:
        pass
    clock_on = False
# ---------------------------- TIMER MECHANISM ------------------------------- #
def timer_start():
    global clock_on
    global five_min_lapse
    global seven_min_lapse

    minute_default = int(num_picker.get())

    cd_sec = minute_default * 60
    five_min_lapse = cd_sec
    if var1.get() == 1:

        seven_min_lapse = cd_sec
    if clock_on:
        window.after_cancel(timer)
        count_down(cd_sec)
    else:
        reset_button.config(state="active")
        count_down(cd_sec)
        clock_on = True
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
    ##troubleshooting
 #    os.system("""
 # #                osascript -e 'tell application "System Events" to do shell script "osascript -e 'tell application \"System Events\"
 # # display dialog (items of (name of (every process whose name contains \"sc\") as list) as string)
 # # end tell'
 # #    """)
    ##troubleshooting

#     os.system("""
#             osascript -e '
#             tell application "System Events" to tell process "timeLapse"
# 	perform action "AXRaise" of window "Countdown"
# end tell
#             '
#     """)

def count_down(count):
    global five_min_lapse
    global seven_min_lapse
    count_min = math.floor(count/60)
    count_sec = count % 60

#change
    if count == (five_min_lapse - 240) or count == (seven_min_lapse - 420) or count == 60:
        global message_notif
        #global sevenMinute
        #global fiveMinute
        global beenIdle

        minute_alert = math.floor(count / 60)
        if minute_alert > 1:
            s_string = "s"
        else:
            s_string = ""

        # message_notif will be sent regardless including at 60 seconds
        message_notif = f"{minute_alert} minute{s_string} remaining"
        #sevenMinute = ""
        #fiveMinute = ""
        beenIdle = True

        if var1.get() == 1 and count == (seven_min_lapse - 420):
            # notify("Timer",f" 7 minutes passed. {minute_alert} minute{s_string} remaining")
            #sevenMinute = "Tier down."
            message_notif = "Tier down. " + message_notif
            beenIdle = False
            if seven_min_lapse > 420:
                seven_min_lapse -= 420

        if count == (five_min_lapse - 240):
            if beenIdle:
                #fiveMinute = "Idle warning."
                message_notif = "Idle warning. " + message_notif
            # notify("Timer", f" Almost 5 minutes. {minute_alert} minute{s_string} remaining")
            if five_min_lapse >= 600:
                five_min_lapse -= 300
                # have method to reset idle warning and have manual button attached

        notify("Timer", message_notif)

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        timer_restart()
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Countdown")
window.config(padx=20, pady = 20, bg=LG)

canvas = Canvas(width=75, height=50, bg=LG, highlightthickness=0)
timer_text = canvas.create_text(30, 35, text="00:00", fill=BG, font=(FONT_NAME, 20, "bold"))
canvas.grid(column=1,row=1,)

timer_label = Label()
timer_label.grid(column=1,row=0)
timer_label.config(text="Timer", bg=LG, fg="white", font=(FONT_NAME, 25, "bold"))

start_button = Button(text="Start", highlightbackground=LG, command=timer_start)
start_button.grid(column=0,row=2)

reset_button = Button(text="Reset", highlightbackground=LG, command=timer_restart)
reset_button.grid(column=2,row=2)

pick_variable = StringVar()
pick_variable.set("5")
num_picker = Spinbox(master=window, width=5, from_=1, to=99, textvariable=pick_variable, justify=CENTER, bg=LG, fg="white", font=(FONT_NAME, 15, "bold"))
num_picker.grid(column=1, row=3,pady=5)

var1 = IntVar()
c1 = Checkbutton(window, text='7min',variable=var1, onvalue=1, offvalue=0, bg=LG)
c1.grid(column=0, row=3, pady=5)

window.mainloop()

