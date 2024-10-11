# -*- coding: utf-8 -*-
from tkinter import Tk, filedialog, Button, Label, StringVar, OptionMenu
from video_processor import process_video

class VideoHeatmapApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Motion Detection and Heatmap Generator")

        self.video_label = Label(self.root, text="No video selected")
        self.video_label.pack()

        Button(self.root, text="Upload Video", command=self.upload_video).pack()

        self.start_time_var = StringVar(value="0")
        self.end_time_var = StringVar(value="10")
        self.color_palette_var = StringVar(value="hot")

        Label(self.root, text="Start Time (seconds):").pack()
        OptionMenu(self.root, self.start_time_var, "0", "5", "10", "15", "20").pack()

        Label(self.root, text="End Time (seconds):").pack()
        OptionMenu(self.root, self.end_time_var, "10", "15", "20", "25", "30").pack()

        Label(self.root, text="Color Palette:").pack()
        OptionMenu(self.root, self.color_palette_var, "hot", "cool", "plasma").pack()

        Button(self.root, text="Create Heatmap", command=self.create_heatmap).pack()

    def upload_video(self):
        video_path = filedialog.askopenfilename(title="Select Video File", 
                                                 filetypes=[("Video Files", "*.*")])
        self.video_label.config(text=video_path)

    def create_heatmap(self):
        video_path = self.video_label.cget("text")
        start_time = float(self.start_time_var.get())
        end_time = float(self.end_time_var.get())
        color_palette = self.color_palette_var.get()
        
        process_video(video_path, start_time, end_time, color_palette)

    def run(self):
        self.root.mainloop()
