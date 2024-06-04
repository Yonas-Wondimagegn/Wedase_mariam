import tkinter as tk
from tkinter import ttk
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import pygame
import os

class Wedase_Mariam_App:
    def __init__(self, master, pdf_path, voice_folder):
        self.master = master
        self.master.title("Wedase Mariam")

        try:
            self.pdf_document = fitz.open(pdf_path)
        except FileNotFoundError:
            print("PDF file not found.")
            self.master.destroy()
            return

        self.current_page = 0
        self.voice_folder = voice_folder
        
        self.canvas = tk.Canvas(self.master, width=800, height=1000)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        
        self.display_page()

        self.master.bind("<Left>", self.prev_page)
        self.master.bind("<Right>", self.next_page)

        self.voice_button = ttk.Button(self.master, text="Voice", command=self.play_voice)
        self.voice_button.grid(row=0, column=0, sticky="ew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def display_page(self):
        page = self.pdf_document.load_page(self.current_page)
        pixmap = page.get_pixmap()
        pil_img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        img = ImageTk.PhotoImage(pil_img)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        image_width = pixmap.width
        image_height = pixmap.height
        x_offset = (canvas_width - image_width) / 2
        y_offset = (canvas_height - image_height) / 2
        self.canvas.create_image(x_offset, y_offset, anchor="nw", image=img)
        self.canvas.image = img

    def prev_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.canvas.delete("all")
            self.display_page()

    def next_page(self, event):
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.canvas.delete("all")
            self.display_page()



    def play_voice(self):
        print("Contents of voices folder:", os.listdir(self.voice_folder))

        voice_file = os.path.join(self.voice_folder, f"page_{self.current_page + 1}.mp3")
        print("Attempting to play:", voice_file)  
        if os.path.exists(voice_file):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(voice_file)
                pygame.mixer.music.play()
                print("Playing voice file:", voice_file) 
            except pygame.error as e:
                print("Error playing voice file:", e)
        else:
            print("Voice file not found:", voice_file)


def main():
    root = tk.Tk()
    app = Wedase_Mariam_App(root, "wedasemariam.pdf", "voices")
    root.mainloop()

if __name__ == "__main__":
    main()
