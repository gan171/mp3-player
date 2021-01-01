from pygame import mixer
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
import time
import threading

mixer.init()

root = Tk()
statusbar = Label(root, text="No music Playing Currently", relief=GROOVE, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)


# about us
def about_us():
    tkinter.messagebox.showinfo("About Mp", "Tere Bhai ka music player. tkinter python op ")


playlist = []


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


index = 0


def add_to_playlist(filename):
    global index
    filename = os.path.basename(filename)
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


# menu and submenu
menubar = Menu(root)
# sub menu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="file", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="Instruction")
submenu.add_command(label="About Us", command=about_us)
root.config(menu=menubar)
root.title("music player")
root.iconbitmap(r'mp ico.ico')

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30)
playlistbox = Listbox(leftframe)
playlistbox.pack()
add_img = PhotoImage(file="plus.png")
del_img = PhotoImage(file="delete.png")
add_btn = Button(leftframe, image=add_img, command=browse_file)
del_btn = Button(leftframe, image=del_img)
add_btn.pack(side=LEFT)
del_btn.pack(side=LEFT)

Rightframe = Frame(root)
Rightframe.pack()
topframe = Frame(Rightframe)
topframe.pack()
intro_text = Label(topframe, text="Aaj Gaane Tera Bhai Bajayega")
intro_text.pack(pady=0)
length_label = Label(topframe, text="Total length --:--")
length_label.pack(pady=5)
current_time = Label(topframe, text="Current time --:--", relief=GROOVE)
current_time.pack()


def show_details():
    file_data = os.path.splitext(filename_path)
    if file_data[1] == ".mp3":
        audio = MP3(filename_path)
        music_length = audio.info.length
    else:

        a = mixer.Sound(filename_path)
        music_length = a.get_length()

    mins, sec = divmod(music_length, 60)
    mins = round(mins)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(mins, sec)
    length_label['text'] = "Total length" + "-" + timeformat
    t1 = threading.Thread(target=current_det, args=(music_length,))
    t1.start()


def current_det(t):
    x = 0
    while x <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, sec = divmod(x, 60)
            mins = round(mins)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(mins, sec)
            current_time['text'] = "Current time" + "-" + timeformat
            time.sleep(1)
            x += 1


# noinspection PyBroadException
def pl_btn():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "music is unpaused" + "-" + os.path.basename(filename_path)
        paused = False
    else:
        try:
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_song = playlist[selected_song]
            mixer.music.load(play_song)
            mixer.music.play()
            statusbar['text'] = "music is playing" + "-" + os.path.basename(filename_path)
            show_details(play_song)
        except:
            tkinter.messagebox.showerror("ERROR", "Please Load a Music First!")


def st_btn():
    mixer.music.stop()
    statusbar['text'] = "Music  Stopped "


def rp_btn():
    mixer.music.rewind()
    statusbar['text'] = "Replaying music" + "-" + os.path.basename(filename_path)


muted = False


def vol_btn():
    global muted
    if muted:
        mixer.music.set_volume(0.50)
        vol_btn.configure(image=vol_img)
        scale.set(50)
        muted = False
        statusbar['text'] = "Music unmuted!" + "-" + os.path.basename(filename_path)

    else:
        mixer.music.set_volume(0)
        vol_btn.configure(image=mute_img)
        scale.set(0)
        muted = True
        statusbar['text'] = "Music muted!"


paused = False


def ps_btn():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music Paused,to unpause hit the play button"


def vol_ctrl(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


middleframe = Frame(Rightframe)
middleframe.pack(padx=10, pady=10)
play_img = PhotoImage(file='play.png')
play_btn = Button(middleframe, image=play_img, command=pl_btn)
stop_img = PhotoImage(file='stop.png')
stop_btn = Button(middleframe, image=stop_img, command=st_btn)
pause_img = PhotoImage(file='pause.png')
pause_btn = Button(middleframe, image=pause_img, command=ps_btn)
bottomframe = Frame(Rightframe)
bottomframe.pack(padx=10, pady=10)
rewind_img = PhotoImage(file='replay (1).png')
rewind_btn = Button(bottomframe, image=rewind_img, command=rp_btn)
mute_img = PhotoImage(file='mute.png')
vol_img = PhotoImage(file='speaker.png')
vol_btn = Button(bottomframe, image=vol_img, command=vol_btn)
scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=vol_ctrl)

scale.set(50)  # slider start from 50
vol_ctrl(50)
play_btn.grid(row=0, column=0, padx=10)
pause_btn.grid(row=0, column=1, padx=10)
stop_btn.grid(row=0, column=2, padx=10)
rewind_btn.grid(row=0, column=0, padx=0)
vol_btn.grid(row=0, column=1, padx=20)
scale.grid(row=0, column=2, pady=20)


def close():
    st_btn()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
