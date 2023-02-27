from tkinter import *
from tkinter import ttk
import simpleaudio as sa
import soundfile as sf

def play_music():
    global IS_PLAYING
    # Reset the progress bar
    progress_check.set(0)
    currentLabel.config(text='0:00')
    IS_PLAYING = True
    play_obj = PLAYLIST[CURRENT_SONG][0].play()
    TRACK_LIST[CURRENT_SONG].config(state=ACTIVE)
    window.after(1000, current_time)
    progress.start(1000)

def stop_music():
    global IS_PLAYING
    IS_PLAYING = False
    sa.stop_all()
    progress.stop()

# Return the duration of a song in 0:00 format
def duration(song_length):
    minutes = song_length // 60
    seconds = song_length % 60
    if seconds < 10:
        return f'{minutes}:0{seconds}'
    else:
        return f'{minutes}:{seconds}'

# Keep track of the current time of the song
def current_time():
    global IS_PLAYING
    if IS_PLAYING:
        current = progress_check.get()
        minutes = current // 60
        seconds = current % 60
        if seconds < 10:
            currentLabel.config(text=f'{minutes}:0{seconds}')
        else:
            currentLabel.config(text=f'{minutes}:{seconds}')

    window.after(1000, current_time)

def skip_music(skip):
    global CURRENT_SONG

    # Advance the track forward
    if skip == '>>' and CURRENT_SONG <= len(PLAYLIST) - 2:
        # Stop the current playback and progress bar
        stop_music()
        # Un-highlight the previous track in the track list
        TRACK_LIST[CURRENT_SONG].config(state=DISABLED)
        CURRENT_SONG += 1
        # Play the new song, highlight its name, and set/start the new progress bar
        progress.config(maximum=PLAYLIST[CURRENT_SONG][1])
        durationLabel.config(text=duration(PLAYLIST[CURRENT_SONG][1]))
        play_music()

    # Advance the track backwards
    elif skip == '<<' and CURRENT_SONG > 0:
        stop_music()
        TRACK_LIST[CURRENT_SONG].config(state=DISABLED)
        CURRENT_SONG -= 1
        progress.config(maximum=PLAYLIST[CURRENT_SONG][1])
        durationLabel.config(text=duration(PLAYLIST[CURRENT_SONG][1]))
        play_music()

# Initialize GUI
window = Tk()
window.title('Music Player')
window.geometry('490x320')

# Import Songs
sleepy_tea = sa.WaveObject.from_wave_file('music_player/CHON - Homey - 01 - Sleepy Tea.wav')
waterslide = sa.WaveObject.from_wave_file('music_player/CHON - Homey - 02 - Waterslide.wav')
berry_streets = sa.WaveObject.from_wave_file('music_player/CHON - Homey - 03 - Berry Streets.wav')
no_signal = sa.WaveObject.from_wave_file('music_player/CHON - Homey - 04 - No Signal.wav')
checkpoint = sa.WaveObject.from_wave_file('music_player/CHON - Homey - 05 - Checkpoint.wav')

# Import the songs again using soundfile in order to collect their time data
sleepy_tea_info = sf.SoundFile('music_player/CHON - Homey - 01 - Sleepy Tea.wav')
waterslide_info = sf.SoundFile('music_player/CHON - Homey - 02 - Waterslide.wav')
berry_streets_info = sf.SoundFile('music_player/CHON - Homey - 03 - Berry Streets.wav')
no_signal_info = sf.SoundFile('music_player/CHON - Homey - 04 - No Signal.wav')
checkpoint_info = sf.SoundFile('music_player/CHON - Homey - 05 - Checkpoint.wav')

# Assign each song duration to an int variable. Duration = (Samples/Sample Rate)
sleepy_tea_time = int((sleepy_tea_info.frames / sleepy_tea_info.samplerate))
waterslide_time = int((waterslide_info.frames / waterslide_info.samplerate))
berry_streets_time = int((berry_streets_info.frames / berry_streets_info.samplerate))
no_signal_time = int((no_signal_info.frames / no_signal_info.samplerate))
checkpoint_time = int((checkpoint_info.frames / checkpoint_info.samplerate))

# [0] is the track for playback. [1] is the length of the song
PLAYLIST = [(sleepy_tea, sleepy_tea_time),
            (waterslide, waterslide_time),
            (berry_streets, berry_streets_time),
            (no_signal, no_signal_time), 
            (checkpoint, checkpoint_time),
            ]
CURRENT_SONG = 0
IS_PLAYING = False

#################### Tkinter widget setup ####################

titleLabel = Label(window, text='Snotify', font=('Helvetica', 40), width=20)
titleLabel.grid(row=0, column=0, columnspan=4)

# Track List Frame
trackFrame = LabelFrame(window, text='Track List')
trackFrame.grid(row=1, column=0, padx=50, pady=20, columnspan=4, ipadx=150, ipady=5)

Track1 = Label(trackFrame, text='Sleepy Tea', state=DISABLED)
Track2 = Label(trackFrame, text='Waterslide', state=DISABLED)
Track3 = Label(trackFrame, text='Berry Streets', state=DISABLED)
Track4 = Label(trackFrame, text='No Signal', state=DISABLED)
Track5 = Label(trackFrame, text='Checkpoint', state=DISABLED)

Track1.pack()
Track2.pack()
Track3.pack()
Track4.pack()
Track5.pack()

# Progress bar
progress_check = IntVar()
progress = ttk.Progressbar(window, orient=HORIZONTAL, maximum=waterslide_time,
                           length=300, mode='determinate', variable=progress_check)
progress.grid(row=2, column=1, pady=10, columnspan=2)

durationLabel = Label(window, text='3:05')
durationLabel.grid(row=2, column=3, sticky='w')

currentLabel = Label(window, text='0:00')
currentLabel.grid(row=2, column=0, sticky='e')

# List of song labels in the tracklist frame in order to better manipulate them
TRACK_LIST = [Track1, Track2, Track3, Track4, Track5]

# Create Buttons
playButton = Button(window, text='Play', command=play_music)
stopButton = Button(window, text='Stop', command=stop_music)
nextButton = Button(window, text='>>', command=lambda: skip_music('>>'))
previousButton = Button(window, text='<<', command=lambda: skip_music('<<'))

playButton.grid(row=3, column=1)
stopButton.grid(row=3, column=2)
nextButton.grid(row=3, column=3)
previousButton.grid(row=3, column=0)


window.mainloop()
