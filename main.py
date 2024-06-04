import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import speech_recognition as sr
import fitz
from PIL import Image, ImageTk
import pygame

class Wedase_Mariam_App:
    def __init__(self, master, pdf_path, voice_folder):
        self.master = master
        self.master.title("Wedase Mariam")

        # to load wedase mariam
        try:
            self.pdf_document = fitz.open(pdf_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "PDF file not found.")
            self.master.destroy()
            return

        self.voice_folder = voice_folder
        self.playing = False
        self.paused = False

        # for pdf canvas
        self.canvas = tk.Canvas(self.master, width=800, height=1000)
        self.canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # voice button
        self.voice_button = ttk.Button(self.master, text="Play", command=self.toggle_voice)
        self.voice_button.grid(row=0, column=0, sticky="ew")

        # text button
        self.text_button = ttk.Button(self.master, text="Text", command=self.search_text)
        self.text_button.grid(row=0, column=1, sticky="ew")

        # search button
        self.search_button = ttk.Button(self.master, text="Search", command=self.search_page_voice)
        self.search_button.grid(row=0, column=2, sticky="ew")

        # restart button
        self.restart_button = ttk.Button(self.master, text="Restart", command=self.restart_voice)
        self.restart_button.grid(row=0, column=3, sticky="ew")

        # for selecting page(manual)
        self.master.bind("<Left>", self.prev_page)
        self.master.bind("<Right>", self.next_page)


        # first page
        self.current_page = 0
        self.display_page()

    def display_page(self):

        # load page
        page = self.pdf_document.load_page(self.current_page)
        pixmap = page.get_pixmap()
        pil_img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        img = ImageTk.PhotoImage(pil_img)

        # displaying
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
            self.display_page()

    def next_page(self, event):
        if self.current_page < len(self.pdf_document) - 1:
            self.current_page += 1
            self.display_page()

    def toggle_voice(self):
        if not self.playing:
            self.play_voice()
            self.voice_button.config(text="Pause")
        else:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.voice_button.config(text="Pause")
            else:
                pygame.mixer.music.pause()
                self.paused = True
                self.voice_button.config(text="Resume")

    def restart_voice(self):
        pygame.mixer.music.stop()
        self.play_voice()

    def play_voice(self):
        print("voices folder:", os.listdir(self.voice_folder))

        voice_file = os.path.join(self.voice_folder, f"page_{self.current_page + 1}.mp3")
        print("Attempting to play:", voice_file)  
        if os.path.exists(voice_file):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(voice_file)
                pygame.mixer.music.play()
                print("Playing voice file:", voice_file) 
                self.playing = True
            except pygame.error as e:
                print("Error playing voice file:", e)
        else:
            print("Voice file not found:", voice_file)

    def search_text(self):
        text_to_search = simpledialog.askstring("Search Text", "Enter the text to search:")
        if text_to_search is None:
            return

        # search for the text in the document
        for idx, page in enumerate(self.pdf_document):
            page_text = page.get_text()
            if text_to_search in page_text:
                print(f"Text '{text_to_search}' found on page {idx + 1}")
                self.current_page = idx
                self.display_page()
                return

        print("Text not found in the document.")

    def search_page_voice(self):
        # starting recognizer
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Speak the text you want to search for:")
            audio = recognizer.listen(source)

        try:
            # from convrtt audio to text
            search_text = recognizer.recognize_google(audio, language="am-ET")

            # search for the text in the document
            for idx, page in enumerate(self.pdf_document):
                page_text = page.get_text()
                if search_text in page_text:
                    print(f"Text '{search_text}' found on page {idx + 1}")
                    self.current_page = idx
                    self.display_page()
                    return

            print(f"Text '{search_text}' not found in the document.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except ValueError:
            print("Could not convert audio to text.")

def main():
    root = tk.Tk()
    app = Wedase_Mariam_App(root, "wedasemariam.pdf", "voices")
    root.mainloop()


print("Thanks for using our bot")

if __name__ == "__main__":
    main()
