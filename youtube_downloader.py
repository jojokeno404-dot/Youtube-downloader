from tkinter import ttk
import threading

import yt_dlp

from pytube import YouTube
import tkinter as tk
from tkinter import messagebox, filedialog
import os

#helper function#
def run_in_thread(func):
    threading.Thread(target=func, daemon=True).start()


#progress hook function#
def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').replace('%', '').strip()
        try:
            progress_var.set(float(percent))
            window.update_idletasks()
        except:
            pass

    elif d['status'] == 'finished':
        progress_var.set(100)


# ----------------------------
# Download Functions
# ----------------------------

def download_video():
    try:
        url = url_entry.get()
        save_path = filedialog.askdirectory()

        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook],

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))




def download_audio():
    try:
        url = url_entry.get()
        save_path = filedialog.askdirectory()

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Audio downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))




def download_video_only():
    try:
        url = url_entry.get()
        save_path = filedialog.askdirectory()

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
            'noplaylist': True,
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", "Video-only download completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))




# ----------------------------
# GUI Window
# ----------------------------

window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("400x300")
window.resizable(False, False)

# ----------------------------
# Widgets
# ----------------------------

title_label = tk.Label(window, text="Jakababa Video Downloader",
                       font=("Arial", 16, "bold"))
title_label.pack(pady=10)

url_label = tk.Label(window, text="Enter YouTube Video URL:")
url_label.pack()

url_entry = tk.Entry(window, width=45)
url_entry.pack(pady=5)

progress_var = tk.DoubleVar()

progress_bar = ttk.Progressbar(
    window,
    variable=progress_var,
    maximum=100,
    length=300,
    mode='determinate'
)
progress_bar.pack(pady=10)

video_btn = tk.Button(window, text="Download Video (MP4)",
                      width=30, command=download_video)
video_btn.config(command=lambda: run_in_thread(download_video))
video_btn.pack(pady=5)

audio_btn = tk.Button(window, text="Download Audio Only (MP3)",
                      width=30, command=download_audio)
audio_btn.config(command=lambda: run_in_thread(download_audio))
audio_btn.pack(pady=5)

video_only_btn = tk.Button(window, text="Download Video Only (No Audio)",
                           width=30, command=download_video_only)
video_only_btn.config(command=lambda: run_in_thread(download_video_only))
video_only_btn.pack(pady=5)

exit_btn = tk.Button(window, text="Exit", width=30,
                     command=window.destroy)
exit_btn.pack(pady=10)

# ----------------------------
# Run Application
# ----------------------------

window.mainloop()

