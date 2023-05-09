import customtkinter as ct, ctypes, os, PIL
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, Frame, BOTH, NW
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

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
        self.controls.grid_rowconfigure(12, weight=1)
        # control buttons
        self.zoom = ct.CTkLabel(self.controls, text='Zoom', text_color='#ffffff', bg_color='transparent')
        self.zoom.grid(row=0, column=0, sticky="ew", pady=10)
        self.zoom_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.zoom_func)
        self.zoom_btn.grid(row=1, column=0, sticky="ew", padx=10)

        self.rotate_lbl = ct.CTkLabel(self.controls, text='Rotate', text_color='#ffffff', bg_color='transparent')
        self.rotate_lbl.grid(row=2, column=0, sticky="ew", pady=10)
        self.rotate_btn = ct.CTkSlider(self.controls, from_=-180, to=180, command=self.rotate_func)
        self.rotate_btn.grid(row=3, column=0, sticky="ew", padx=10)

        self.red_lbl = ct.CTkLabel(self.controls, text='Saturation', text_color='#ffffff', bg_color='transparent')
        self.red_lbl.grid(row=4, column=0, sticky="ew", pady=10)
        self.red_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.enchance_func)
        self.red_btn.grid(row=5, column=0, sticky="ew", padx=10)

        self.green_lbl = ct.CTkLabel(self.controls, text='Contrast', text_color='#ffffff', bg_color='transparent')
        self.green_lbl.grid(row=6, column=0, sticky="ew", pady=10)
        self.green_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.contrast_func)
        self.green_btn.grid(row=7, column=0, sticky="ew", padx=10)

        self.blue_lbl = ct.CTkLabel(self.controls, text='Brightness', text_color='#ffffff', bg_color='transparent')
        self.blue_lbl.grid(row=8, column=0, sticky="ew", pady=10)
        self.blue_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.brightness_func)
        self.blue_btn.grid(row=9, column=0, sticky="ew", padx=10)

        self.sharp_lbl = ct.CTkLabel(self.controls, text='Sharpness', text_color='#ffffff', bg_color='transparent')
        self.sharp_lbl.grid(row=10, column=0, sticky="ew", pady=10)
        self.sharp_btn = ct.CTkSlider(self.controls, from_=0, to=200, command=self.sharpness_func)
        self.sharp_btn.grid(row=11, column=0, sticky="ew", padx=10)

        # save button
        self.save_btn = ct.CTkButton(self.controls, command=self.save_image_func, text='Save')
        self.save_btn.grid(row=12, column=0, sticky="ews", padx=10, pady=10)

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
            self.new_img = self.new_img.convert('RGB')
            self.add_photo.destroy()
            self.tatras = ImageTk.PhotoImage(self.new_img) # Вставляем изображение
            self.edit_image.place(anchor="c", relx=.5, rely=.5)
            self.edit_image.configure(image=self.tatras)
            self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value = 100, 0, 100, 100, 100, 100
        else:
            pass

    def zoom_func(self, value):
        self.zoom_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def rotate_func(self, value):
        self.rotate_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def enchance_func(self, value):
        self.ench_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def contrast_func(self, value):
        self.contr_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def brightness_func(self, value):
        self.bright_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def sharpness_func(self, value):
        self.sharp_value = value
        self.update_func(self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value)

    def update_func(self, zoom_val, rotate_val, ench_val, contr_val, bright_val, sharp_val):
        new_resize_img = self.new_img.resize((round(self.new_img.size[0] * (zoom_val / 100)), round(self.new_img.size[1] * (zoom_val / 100))))
        editable_image = new_resize_img.rotate(rotate_val)
        saturation = ImageEnhance.Color(editable_image).enhance(ench_val / 100)
        contrast = ImageEnhance.Contrast(saturation).enhance(contr_val / 100)
        brightness = ImageEnhance.Brightness(contrast).enhance(bright_val / 100)
        sharpness = ImageEnhance.Sharpness(brightness).enhance(sharp_val / 100)

        self.end_img = sharpness
        self.tatras = ImageTk.PhotoImage(self.end_img)
        self.edit_image.configure(image=self.tatras)

    def save_image_func(self):
        if(self.end_img):
            x, y = self.end_img.size[0], self.end_img.size[1]
            self.end_img.resize((self.img.size[0], self.img.size[1]))
            self.end_img.save('some.png', 'png', quality=100)
            self.end_img.resize((x, y))

    def __del__(self):
        print('destroed!')


ct.set_appearance_mode('System')
ct.set_default_color_theme('blue')

app = App()
app.mainloop()