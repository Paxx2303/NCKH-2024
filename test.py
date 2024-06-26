import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import PIL
from GUI import cvhelpers as cvHelp
import mediapipe as mp

import cv2

class Page1(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.controller = controller

        # Chèn ảnh background cho trang 1
        image = Image.open(r"page1.png")  # Đường dẫn đến tệp ảnh của bạn
        image = image.resize((320, 570), PIL.Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        background_label = ttk.Label(self, image=photo)
        background_label.image = photo
        background_label.place(relwidth=1, relheight=1)
        next_button = ttk.Button(self, text="Start", command=self.go_to_page2)
        next_button.pack(side = "bottom")

    def go_to_page2(self):
        self.controller.show_frame(Page2)

class Page2(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.controller = controller

        # Chèn ảnh background cho trang 2
        image = Image.open(r"page2.png")  # Đường dẫn đến tệp ảnh của bạn
        image = image.resize((320, 570), PIL.Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        background_label = ttk.Label(self, image=photo)
        background_label.image = photo
        background_label.place(relwidth=1, relheight=1)

        image1 = Image.open(r"setting.png")
        image1 = image1.resize((30, 30), PIL.Image.Resampling.LANCZOS)
        photo1 = ImageTk.PhotoImage(image1)

        next_button = ttk.Button(self, image=photo1, command=self.go_to_page3)
        next_button.image = photo1
        next_button.place(relx=0.95, rely=0.03, anchor="ne")

        image2 = Image.open(r"sound.png")
        image2 = image2.resize((33, 28), PIL.Image.Resampling.LANCZOS)
        photo2 = ImageTk.PhotoImage(image2)

        next_button2 = ttk.Button(self, image=photo2)
        next_button2.image = photo2
        next_button2.place(relx=0.2, rely=0.033, anchor="ne")

        back_button = ttk.Button(self, text="Back", command=self.go_to_page1)
        back_button.pack(side = "bottom")




    def go_to_page3(self):
        self.controller.show_frame(Page3)

    def go_to_page1(self):
        self.controller.show_frame(Page1)

class Page3(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.controller = controller

        # Chèn ảnh background cho trang 3
        image = Image.open("page2.png")  # Đường dẫn đến tệp ảnh của bạn
        image = image.resize((320, 570), PIL.Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        background_label = ttk.Label(self, image=photo)
        background_label.image = photo
        background_label.place(relwidth=1, relheight=1)


        # Load ảnh và lưu trữ chúng trong các thuộc tính của lớp
        self.image1 = Image.open("menu.png")
        self.image1 = self.image1.resize((100, 35), PIL.Image.Resampling.LANCZOS)
        self.photo1 = ImageTk.PhotoImage(self.image1)

        self.image2 = Image.open("instruction.png")
        self.image2 = self.image2.resize((170, 35), PIL.Image.Resampling.LANCZOS)
        self.photo2 = ImageTk.PhotoImage(self.image2)

        self.image3 = Image.open("about us.png")
        self.image3 = self.image3.resize((170, 35), PIL.Image.Resampling.LANCZOS)
        self.photo3 = ImageTk.PhotoImage(self.image3)

        self.image4 = Image.open("help.png")
        self.image4 = self.image4.resize((170, 35), PIL.Image.Resampling.LANCZOS)
        self.photo4 = ImageTk.PhotoImage(self.image4)


        # Sử dụng hình ảnh đã lưu trữ trong các thuộc tính
        label1 = ttk.Label(self, image=self.photo1)
        label2 = ttk.Label(self, image=self.photo2)
        label3 = ttk.Label(self, image=self.photo3)
        label4 = ttk.Label(self, image=self.photo4)


        # Tạo các nút menu

        self.image111 = Image.open("mui_ten.png")
        self.image111 = self.image111.resize((25, 25), PIL.Image.Resampling.LANCZOS)
        self.photo111 = ImageTk.PhotoImage(self.image111)

        button1 = ttk.Button(self, image=self.photo111)
        button2 = ttk.Button(self, image=self.photo111)
        button3 = ttk.Button(self, image=self.photo111)

        # Đặt các nút menu vào grid layout

        button1.grid(row=2, column=0, padx=60, pady=(70,10), sticky="e")
        button2.grid(row=3, column=0, padx=60, pady=10, sticky="e")
        button3.grid(row=4, column=0, padx=60, pady=10, sticky="e")

        # Đặt các nút vào grid layout
        label1.grid(row=1, column=0, padx=120, pady=(70,10))
        label2.grid(row=2, column=0, padx=50, pady=(70,10), sticky="w")
        label3.grid(row=3, column=0, padx=50, pady=0, sticky="w")
        label4.grid(row=4, column=0, padx=50, pady=0, sticky="w")

        back_button = ttk.Button(self, text="Back", command=self.go_to_page2)
        back_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(180,10))

    def go_to_page2(self):
        self.controller.show_frame(Page2)


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Multi-page Application")
        self.geometry("320x570")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Page1, Page2, Page3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = MainApplication()
app.mainloop()
