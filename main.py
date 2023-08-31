import boto3
import PyPDF2
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog


class TexttoSpeech:
    def __init__(self, screen):

        self.ACCESS_KEY = os.environ.get("POLLY_ACCESS_KEY")
        self.SECRET_KEY = os.environ.get("POLLY_SECRET_KEY")
        self.REGION_NAME = "eu-central-1"
        screen.title("Text to Speech converter")
        screen.geometry("800x600")
        self.root = screen
        # Canvas and image
        self.photo_image = PhotoImage(file=r"C:\Users\zined\OneDrive\Desktop\background.png")
        self.pdf_photo = PhotoImage(file=r"C:\Users\zined\OneDrive\Desktop\pdf.png")
        self.text_photo = PhotoImage(file=r"C:\Users\zined\OneDrive\Desktop\text.png")
        self.canvas = tk.Canvas(width=800, height=600)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        self.voices = ["Joanna", "Matthew", "Ruben", "Joey", "Kendra", "Ivy", "Salli"]
        self.text = ""
        # Widgets
        self.write_field = None
        self.file = None
        self.dropdown_menu = None
        self.option_var = None
        self.file_entry = None
        # Labels
        self.welcome_label = None
        self.choice_label = None
        # Buttons
        self.button = None
        self.pdf_button = None
        self.convert_button = None
        self.upload_button = None
        self.write_button = None
        self.to_pdf = None
        self.to_text = None

    def clear_widget(self):
        # Clear widgets
        if self.file_entry is not None and self.write_field is not None:
            self.file_entry.destroy()
            self.dropdown_menu.destroy()
            self.write_field.destroy()
            self.button.destroy()

        elif self.file_entry is None:
            self.pdf_button.destroy()
            self.write_button.destroy()
        else:
            self.dropdown_menu.destroy()
            self.to_text.destroy()
            self.convert_button.destroy()
        # Clear canvas text and image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

    def pdf_page(self):
        self.clear_widget()
        # Text
        self.canvas.create_text(420, 80, text="PDF to Audio", font=("Arial", 25), fill="white")

        self.canvas.create_text(350, 160, text="Audio file name:", font=("Arial", 10), fill="white")

        self.canvas.create_text(340, 210, text="Voice type:", font=("Arial", 10), fill="white")

        self.canvas.create_text(340, 300, text="Upload a file:", font=("Arial", 10), fill="white")

        self.file_entry = tk.Entry(width=20)
        self.file_entry.place(x=400, y=150)
        # Voice drop menu
        self.option_var = tk.StringVar()
        self.option_var.set(self.voices[0])
        self.dropdown_menu = tk.OptionMenu(root, self.option_var, *self.voices)
        self.dropdown_menu.place(x=400, y=200)

        self.to_text = tk.Button(image=self.text_photo, width=40, relief="solid", command=self.text_page)
        self.to_text.place(x=650, y=60)

        self.upload_button = tk.Button(text="Upload", width=10, command=self.upload_file)
        self.upload_button.place(x=400, y=290)

        self.convert_button = tk.Button(text="Convert", relief="solid", bg="red", width=15, command=lambda:
                                        self.convert(self.text, self.option_var.get(), self.file_entry.get())
                                        )
        self.convert_button.place(x=350, y=350)

    def upload_file(self):
        self.file = tk.filedialog.askopenfilename()
        # Converting pft to text
        try:
            file_open = open(self.file, "rb")
            read_pdf = PyPDF2.PdfReader(file_open)
            self.text = ""
            for page in range(len(read_pdf.pages)):
                pages = read_pdf.pages[page]
                self.text += pages.extract_text()
        except FileNotFoundError:
            pass

    def text_page(self):
        self.clear_widget()
        if self.to_text is not None:
            self.to_text.destroy()

        self.canvas.create_text(420, 80, text="Text to Voice", font=("Arial", 25), fill="white")

        self.canvas.create_text(350, 150, text="Audio file name:", font=("Arial", 10), fill="white")

        self.canvas.create_text(340, 200, text="Voice type:", font=("Arial", 10), fill="white")

        self.canvas.create_text(320, 240, text="Write your Text down: ", font=("Arial", 10), fill="white")

        self.file_entry = tk.Entry(width=20)
        self.file_entry.place(x=400, y=145)

        # Voice dropmenu
        self.option_var = tk.StringVar()
        self.option_var.set(self.voices[0])
        self.dropdown_menu = tk.OptionMenu(root, self.option_var, *self.voices)
        self.dropdown_menu.place(x=400, y=180)
        # Text box
        self.write_field = tk.Text(wrap="word", font=("Arial", 10), height=17, width=100)
        self.write_field.place(x=50, y=260)
        # Butons
        self.to_pdf = tk.Button(image=self.pdf_photo, width=40, relief="solid", command=self.pdf_page)
        self.to_pdf.place(x=650, y=60)

        self.button = tk.Button(text="Convert", bg="blue", width=20, relief="solid", command=lambda:
                                self.convert(self.write_field.get(1.0, "end-1c"), self.option_var.get(),
                                             self.file_entry.get())
                                )
        self.button.place(x=350, y=555)

    def convert(self, text, voice, name):
        # checking if file name and text are correct
        if name == "":
            messagebox.showwarning("Error", "You file name is not valid. ")
        elif text == "":
            messagebox.showwarning("Error", "Your text field is empty/ Upload a file")
        else:
            # Converting to audio
            polly = boto3.client("polly", aws_access_key_id=self.ACCESS_KEY, aws_secret_access_key=self.SECRET_KEY,
                                 region_name=self.REGION_NAME)
            response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice)
            with open(name + ".mp3", "wb") as f:
                f.write(response["AudioStream"].read())
            messagebox.showinfo("Successful", "Your text is converted to audio")

    def create_gui(self):

        self.welcome_label = self.canvas.create_text(400, 150, text="Welcome to Text to Speech Converter",
                                                     font=("Arial", 25), fill="white")

        self.choice_label = self.canvas.create_text(400, 230, text="Do you want to write text or upload pdf file?",
                                                    font=("Arial", 15), fill="white")

        self.write_button = tk.Button(image=self.text_photo, text="Write", relief="solid", width=40, height=50,
                                      command=self.text_page)
        self.write_button.place(x=270, y=250)

        self.pdf_button = tk.Button(image=self.pdf_photo, text="Upload Pdf", width=40, height=50, relief="solid",
                                    command=self.pdf_page)
        self.pdf_button.place(x=450, y=250)


if __name__ == "__main__":
    root = tk.Tk()
    app = TexttoSpeech(root)
    app.create_gui()
    root.mainloop()
