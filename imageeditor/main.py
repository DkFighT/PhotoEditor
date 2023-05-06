import customtkinter as ct, ctypes, os, PIL
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH, NW
from PIL import Image, ImageTk, ImageFilter

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class App(ct.CTk):
    def __init__(self):
        super().__init__()

        # self.resizable(False, False)
        self.geometry(f'{round(screensize[0]*0.5)}x{round(screensize[1]*0.5)}')
        self.title('PhotoEditor')
        self.bind('<Escape>', lambda x: self.destroy())

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # control panel
        self.controls = ct.CTkFrame(self, width=200, corner_radius=10)
        self.controls.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.controls.grid_rowconfigure(10, weight=1)
        # control buttons
        self.zoom = ct.CTkLabel(self.controls, text='Zoom', text_color='#ffffff', bg_color='transparent')
        self.zoom.grid(row=0, column=0, sticky="ew", pady=10)
        self.zoom_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.zoom_func)
        self.zoom_btn.grid(row=1, column=0, sticky="ew", padx=10)

        self.rotate_lbl = ct.CTkLabel(self.controls, text='Rotate', text_color='#ffffff', bg_color='transparent')
        self.rotate_lbl.grid(row=2, column=0, sticky="ew", pady=10)
        self.rotate_btn = ct.CTkSlider(self.controls, from_=-180, to=180, command=self.rotate_func)
        self.rotate_btn.grid(row=3, column=0, sticky="ew", padx=10)

        self.red_lbl = ct.CTkLabel(self.controls, text='Red', text_color='#ffffff', bg_color='transparent')
        self.red_lbl.grid(row=4, column=0, sticky="ew", pady=10)
        self.red_btn = ct.CTkSlider(self.controls, from_=0, to=255, command=self.red_func)
        self.red_btn.grid(row=5, column=0, sticky="ew", padx=10)

        self.green_lbl = ct.CTkLabel(self.controls, text='Green', text_color='#ffffff', bg_color='transparent')
        self.green_lbl.grid(row=6, column=0, sticky="ew", pady=10)
        self.green_btn = ct.CTkSlider(self.controls, from_=0, to=255, command=self.green_func)
        self.green_btn.grid(row=7, column=0, sticky="ew", padx=10)

        self.blue_lbl = ct.CTkLabel(self.controls, text='Blue', text_color='#ffffff', bg_color='transparent')
        self.blue_lbl.grid(row=8, column=0, sticky="ew", pady=10)
        self.blue_btn = ct.CTkSlider(self.controls, from_=0, to=255, command=self.blue_func)
        self.blue_btn.grid(row=9, column=0, sticky="ew", padx=10)

        # save button
        self.save_btn = ct.CTkButton(self.controls, command=self.save_image_func, text='Save')
        self.save_btn.grid(row=10, column=0, sticky="ews", padx=10, pady=10)

        # work panel
        self.field = ct.CTkFrame(self, fg_color='transparent', bg_color='transparent', width=700, corner_radius=10)
        self.field.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.edit_image = ct.CTkLabel(self.field, text='', corner_radius=10)

        # field for photo download
        self.add_photo = ct.CTkButton(self.field, command=self.add_img, text='Upload Image')
        self.add_photo.place(anchor="c", relx=.5, rely=.5)

    def add_img(self):
        self.filename = askopenfilename()
        if (self.filename):
            self.fixed_width = self.field.winfo_width()
            self.img = Image.open(self.filename)
            width_percent = (self.fixed_width / self.img.size[0])
            new_width = round(self.img.size[0] * width_percent)
            new_height = round(self.img.size[1] * width_percent)
            self.new_img = self.img.resize((new_width, new_height))
            self.new_resize_img = self.new_img
            self.editable_image = None
            self.add_photo.destroy()
            self.tatras = ImageTk.PhotoImage(self.new_img) # Вставляем изображение
            self.edit_image.place(anchor="c", relx=.5, rely=.5)
            self.edit_image.configure(image=self.tatras)
        else:
            pass

    def zoom_func(self, value):
        self.new_resize_img = self.new_img.resize((round(self.new_img.size[0] * (value / 100)), round(self.new_img.size[1] * (value / 100))))
        self.tatras = ImageTk.PhotoImage(self.new_resize_img)
        self.edit_image.configure(image=self.tatras)
    
    def rotate_func(self, value):
        self.editable_image = self.new_resize_img.rotate(value)
        self.tatras = ImageTk.PhotoImage(self.editable_image)
        self.edit_image.configure(image=self.tatras)

    def red_func(self, value):
        pass

    def green_func(self, value):
        pass

    def blue_func(self, value):
        pass

    def save_image_func(self):
        if(self.editable_image):
            x, y = self.editable_image.size[0], self.editable_image.size[1]
            self.editable_image.resize((self.img.size[0], self.img.size[1]))
            self.editable_image.save('some.png', 'png')
            self.editable_image.resize((x, y))

    def __del__(self):
        print('destroed!')


ct.set_appearance_mode('System')
ct.set_default_color_theme('blue')

app = App()
app.mainloop()