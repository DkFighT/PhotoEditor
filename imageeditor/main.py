import customtkinter as ct, ctypes, os, PIL, random
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
size_xy = [0, 0, 100, 100]

class CropWindow(ct.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f'{round(screensize[0]*0.5)}x{round(screensize[1]*0.5)}+200+200')
        self.title('Crop')
        self.bind('<Escape>', lambda x: self.destroy())
        self.overrideredirect(1)

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # left panel
        self.left_panel = ct.CTkFrame(self, width=200, corner_radius=10)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.left_panel.grid_rowconfigure(8, weight=1)

        # work panel
        self.field = ct.CTkFrame(self, fg_color='transparent', bg_color='transparent', width=700, corner_radius=10)
        self.field.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=10)
        self.field.grid_rowconfigure(1, weight=1)

        self.imageFrame = ct.CTkLabel(self.field, text='')
        self.imageFrame.place(anchor="c", relx=.5, rely=.5)

        self.left = ct.CTkLabel(self.left_panel, text='Left', text_color='#ffffff', bg_color='transparent')
        self.left.grid(row=0, column=0, sticky="ew", pady=10)
        self.left_btn = ct.CTkSlider(self.left_panel, from_=0, to=80, command=self.left_func)
        self.left_btn.grid(row=1, column=0, sticky="ew", padx=10)
        self.left_btn.set(size_xy[0])

        self.top = ct.CTkLabel(self.left_panel, text='Top', text_color='#ffffff', bg_color='transparent')
        self.top.grid(row=2, column=0, sticky="ew", pady=10)
        self.top_btn = ct.CTkSlider(self.left_panel, from_=0, to=80, command=self.top_func)
        self.top_btn.grid(row=3, column=0, sticky="ew", padx=10)
        self.top_btn.set(size_xy[1])
        
        self.right = ct.CTkLabel(self.left_panel, text='Right', text_color='#ffffff', bg_color='transparent')
        self.right.grid(row=4, column=0, sticky="ew", pady=10)
        self.right_btn = ct.CTkSlider(self.left_panel, from_=20, to=100, command=self.right_func)
        self.right_btn.grid(row=5, column=0, sticky="ew", padx=10)
        self.right_btn.set(size_xy[2])

        self.bottom = ct.CTkLabel(self.left_panel, text='Bottom', text_color='#ffffff', bg_color='transparent')
        self.bottom.grid(row=6, column=0, sticky="ew", pady=10)
        self.bottom_btn = ct.CTkSlider(self.left_panel, from_=20, to=100, command=self.bottom_func)
        self.bottom_btn.grid(row=7, column=0, sticky="ew", padx=10)
        self.bottom_btn.set(size_xy[3])

        # ok button
        self.ok_btn = ct.CTkButton(self.left_panel, command=self.ok_func, text='Ok')
        self.ok_btn.grid(row=8, column=0, sticky="ews", pady=10, padx=10)

        self.image = None

    def left_func(self, value):
        size_xy[0] = value
        self.update_func()
    def top_func(self, value):
        size_xy[1] = value
        self.update_func()
    def right_func(self, value):
        size_xy[2] = value
        self.update_func()
    def bottom_func(self, value):
        size_xy[3] = value
        self.update_func()

    def create_image(self, image):
        self.image = image
        self.tatras = ImageTk.PhotoImage(self.image) # Вставляем изображение
        self.imageFrame.configure(image=self.tatras)
        self.update_func()

    def ok_func(self):
        app.update_func()
        self.destroy()
    
    def update_func(self):
        croped = self.image.crop((round(self.image.size[0] * (size_xy[0] / 100)), round(self.image.size[1] * (size_xy[1] / 100)), round(self.image.size[0] * (size_xy[2] / 100)), round(self.image.size[1] * (size_xy[3] / 100))))
        self.tatras = ImageTk.PhotoImage(croped) # Вставляем изображение
        self.imageFrame.configure(image=self.tatras)

    def __del__(self):
        print('New window closed')

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

        # left panel
        self.left_panel = ct.CTkFrame(self, width=200, corner_radius=10, fg_color='transparent')
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.left_panel.grid_rowconfigure(0, weight=1)

        # work panel
        self.field = ct.CTkFrame(self, fg_color='transparent', bg_color='transparent', width=700, corner_radius=10)
        self.field.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=10)
        self.field.grid_rowconfigure(1, weight=1)
        self.settings_panel = ct.CTkFrame(self.field, fg_color='transparent', bg_color='transparent', width=700, corner_radius=0)
        self.settings_panel.grid(row=0, column=0, sticky='ew', pady=(10, 10))
        self.settings_panel.grid_columnconfigure(5, weight=1)
        self.image_frame = ct.CTkFrame(self.field, fg_color='transparent', bg_color='transparent', width=700, corner_radius=0)
        self.image_frame.grid(row=1, column=0, sticky='news')
        self.edit_image = ct.CTkLabel(self.image_frame, text='', corner_radius=10)

        # tabs
        self.tabview = ct.CTkTabview(self.left_panel, width=150)
        self.tabview.grid(row=0, column=0, sticky='news')
        self.tab1 = self.tabview.add('WhiteBalance')
        self.tab2 = self.tabview.add('Shade')
        self.tab1.grid_rowconfigure(0, weight=1)
        self.tab2.grid_rowconfigure(0, weight=1)

        # scroll frame for tab1
        self.scroll_frame1 = ct.CTkScrollableFrame(self.tab1, bg_color='transparent', fg_color='transparent', scrollbar_fg_color='transparent')
        self.scroll_frame1.grid(row=0, column=0, padx=0, sticky="news")

        # scroll frame for tab2
        self.scroll_frame2 = ct.CTkScrollableFrame(self.tab2, bg_color='transparent', fg_color='transparent', scrollbar_fg_color='transparent')
        self.scroll_frame2.grid(row=0, column=0, padx=0, sticky="news")
        
        # control buttons
        self.zoom = ct.CTkLabel(self.scroll_frame1, text='Zoom', text_color='#ffffff', bg_color='transparent')
        self.zoom.grid(row=0, column=0, sticky="ew", pady=10)
        self.zoom_btn = ct.CTkSlider(self.scroll_frame1, from_=0, to=200, command=self.zoom_func)
        self.zoom_btn.grid(row=1, column=0, sticky="ew")

        self.rotate_lbl = ct.CTkLabel(self.scroll_frame1, text='Rotate', text_color='#ffffff', bg_color='transparent')
        self.rotate_lbl.grid(row=2, column=0, sticky="ew", pady=10)
        self.rotate_btn = ct.CTkSlider(self.scroll_frame1, from_=-180, to=180, command=self.rotate_func)
        self.rotate_btn.grid(row=3, column=0, sticky="ew")

        self.white_balance_lbl = ct.CTkLabel(self.scroll_frame1, text='White Balance', text_color='#ffffff', bg_color='transparent')
        self.white_balance_lbl.grid(row=4, column=0, sticky="ew", pady=10)
        self.white_balance_btn = ct.CTkSlider(self.scroll_frame1, from_=-100, to=100, command=self.wh_balance_func)
        self.white_balance_btn.grid(row=5, column=0, sticky="ew")

        self.shade_lbl = ct.CTkLabel(self.scroll_frame1, text='Shade', text_color='#ffffff', bg_color='transparent')
        self.shade_lbl.grid(row=6, column=0, sticky="ew", pady=10)
        self.shade_btn = ct.CTkSlider(self.scroll_frame1, from_=-100, to=100, command=self.shade_func)
        self.shade_btn.grid(row=7, column=0, sticky="ew")

        self.red_lbl = ct.CTkLabel(self.scroll_frame2, text='Saturation', text_color='#ffffff', bg_color='transparent')
        self.red_lbl.grid(row=0, column=0, sticky="ew", pady=10)
        self.red_btn = ct.CTkSlider(self.scroll_frame2, from_=0, to=200, command=self.enchance_func)
        self.red_btn.grid(row=1, column=0, sticky="ew")

        self.green_lbl = ct.CTkLabel(self.scroll_frame2, text='Contrast', text_color='#ffffff', bg_color='transparent')
        self.green_lbl.grid(row=2, column=0, sticky="ew", pady=10)
        self.green_btn = ct.CTkSlider(self.scroll_frame2, from_=0, to=200, command=self.contrast_func)
        self.green_btn.grid(row=3, column=0, sticky="ew")

        self.blue_lbl = ct.CTkLabel(self.scroll_frame2, text='Brightness', text_color='#ffffff', bg_color='transparent')
        self.blue_lbl.grid(row=4, column=0, sticky="ew", pady=10)
        self.blue_btn = ct.CTkSlider(self.scroll_frame2, from_=0, to=200, command=self.brightness_func)
        self.blue_btn.grid(row=5, column=0, sticky="ew")

        self.sharp_lbl = ct.CTkLabel(self.scroll_frame2, text='Sharpness', text_color='#ffffff', bg_color='transparent')
        self.sharp_lbl.grid(row=6, column=0, sticky="ew", pady=10)
        self.sharp_btn = ct.CTkSlider(self.scroll_frame2, from_=0, to=200, command=self.sharpness_func)
        self.sharp_btn.grid(row=7, column=0, sticky="ew")

        self.winiet_lbl = ct.CTkLabel(self.scroll_frame2, text='Winiet', text_color='#ffffff', bg_color='transparent')
        self.winiet_lbl.grid(row=8, column=0, sticky="ew", pady=10)
        self.winiet_btn = ct.CTkSlider(self.scroll_frame2, from_=-100, to=100, command=self.winiet_func)
        self.winiet_btn.grid(row=9, column=0, sticky="ew")
        self.winiet_btn.set(0)

        self.noise_lbl = ct.CTkLabel(self.scroll_frame2, text='Noise', text_color='#ffffff', bg_color='transparent')
        self.noise_lbl.grid(row=10, column=0, sticky="ew", pady=10)
        self.noise_btn = ct.CTkSlider(self.scroll_frame2, from_=0, to=1000, command=self.noise_func)
        self.noise_btn.grid(row=11, column=0, sticky="ew")
        self.noise_btn.set(0)

        # save button
        self.save_btn = ct.CTkButton(self.left_panel, command=self.save_image_func, text='Save')
        self.save_btn.grid(row=1, column=0, sticky="ews", pady=(10, 0))

        # reset button
        self.reset_btn = ct.CTkButton(self.settings_panel, command=self.reset_func, text='Reset')
        self.reset_btn.grid(row=0, column=0, padx=5)

        # new image
        self.new_image_btn = ct.CTkButton(self.settings_panel, command=self.add_new_img, text='Add New Image')
        self.new_image_btn.grid(row=0, column=1, padx=5)

        # crop image button
        self.crop_btn = ct.CTkButton(self.settings_panel, command=self.crop_func, text='Crop')
        self.crop_btn.grid(row=0, column=2, padx=5)

        # field for photo download
        self.add_photo = ct.CTkButton(self.field, command=self.add_img, text='Upload Image')
        self.add_photo.place(anchor="c", relx=.5, rely=.5)

        self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value, self.white_balance, self.shade, self.winiet, self.noise = 100, 0, 100, 100, 100, 100, 0, 0, 0, 0
        self.window = None
        self.new_img = None

    def add_img(self):
        self.filenamee = askopenfilename()
        if (self.filenamee):
            size_xy = [0, 0, 100, 100]
            self.fixed_width = self.field.winfo_width()
            self.img = Image.open(self.filenamee)
            self.image_name = self.img.filename
            self.img = self.img.convert('RGB')
            width_percent = (self.fixed_width / self.img.size[0])
            new_width = round(self.img.size[0] * width_percent)
            new_height = round(self.img.size[1] * width_percent)
            self.new_img = self.img.resize((new_width, new_height))
            if (self.add_photo):
                self.add_photo.destroy()
                self.add_photo = None
            self.tatras = ImageTk.PhotoImage(self.new_img) # Вставляем изображение
            self.edit_image.place(anchor="c", relx=.5, rely=.5)
            self.edit_image.configure(image=self.tatras)
        else:
            pass

    def zoom_func(self, value):
        self.zoom_value = value
        self.update_func()

    def rotate_func(self, value):
        self.rotate_value = value
        self.update_func()

    def enchance_func(self, value):
        self.ench_value = value
        self.update_func()

    def contrast_func(self, value):
        self.contr_value = value
        self.update_func()

    def brightness_func(self, value):
        self.bright_value = value
        self.update_func()

    def sharpness_func(self, value):
        self.sharp_value = value
        self.update_func()
    
    def wh_balance_func(self, value):
        self.white_balance = value
        self.update_func()
    
    def shade_func(self, value):
        self.shade = value
        self.update_func()

    def winiet_func(self, value):
        self.winiet = value
        self.update_func()
    
    def noise_func(self, value):
        self.noise = value
        self.update_func()
    
    def wb_func(self, sharpness):
        r, g, b = sharpness.split()
        if self.white_balance > 0:
            r = r.point(lambda p: p * ((self.white_balance + 100) / 100) )
            g = g.point(lambda p: p * ((self.white_balance + 100) / 100) )
        elif self.white_balance == 0:
            pass
        elif self.white_balance < 0:
            b = b.point(lambda p: p * (((self.white_balance - 100) * -1) / 100) )
        return Image.merge("RGB", (r, g, b))
    
    def shade_edit_func(self, wb_img):
        r, g, b = wb_img.split()
        if self.shade > 0:
            r = r.point(lambda p: p * ((self.shade + 100) / 100) )
            b = b.point(lambda p: p * ((self.shade + 100) / 100) )
        elif self.shade == 0:
            return wb_img
        elif self.shade < 0:
            g = g.point(lambda p: p * (((self.shade - 100) * -1) / 100) )
        return Image.merge("RGB", (r, g, b))

    def create_winiet(self, shade_img):
        mask = Image.new('L', shade_img.size, 0)
        d = ImageDraw.Draw(mask)
        if (self.winiet > 0):
            indent = self.winiet * 5
            rect = Image.new('RGB', shade_img.size, (0, 0, 0))
            size = (round(shade_img.size[0]/2) * -1 + indent, round(shade_img.size[1]/2) * -1 + indent, shade_img.size[0] + round(shade_img.size[0]/2) - indent, shade_img.size[1] + round(shade_img.size[1]/2) - indent)
            d.ellipse(size, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(50))
            rect = rect.filter(ImageFilter.GaussianBlur(50))
            img = Image.composite(shade_img, rect, mask)
            return img
        elif (self.winiet == 0):
            return shade_img
        else:
            indent = self.winiet * -5
            rect = Image.new('RGB', shade_img.size, (255, 255, 255))
            size = (round(shade_img.size[0]/2) * -1 + indent, round(shade_img.size[1]/2) * -1 + indent, shade_img.size[0] + round(shade_img.size[0]/2) - indent, shade_img.size[1] + round(shade_img.size[1]/2) - indent)
            d.ellipse(size, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(50))
            rect = rect.filter(ImageFilter.GaussianBlur(50))
            img = Image.composite(shade_img, rect, mask)
            return img

    def create_noise(self, winiet_img):
        if (self.noise != 0):
            for i in range( round(winiet_img.size[0]*winiet_img.size[1] / (1001 - self.noise) ) ):
                winiet_img.putpixel(
                    (random.randint(0, winiet_img.size[0]-1), random.randint(0, winiet_img.size[1]-1)),
                    (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                )
            return winiet_img
        else:
            return winiet_img

    def add_new_img(self):
        self.add_img()
        self.reset_func()

    def reset_func(self):
        self.zoom_value, self.rotate_value, self.ench_value, self.contr_value, self.bright_value, self.sharp_value, self.white_balance, self.shade, self.winiet, self.noise = 100, 0, 100, 100, 100, 100, 0, 0, 0, 0
        self.zoom_btn.set(self.zoom_value)
        self.rotate_btn.set(self.rotate_value)
        self.red_btn.set(self.ench_value)
        self.green_btn.set(self.contr_value)
        self.blue_btn.set(self.bright_value)
        self.sharp_btn.set(self.sharp_value)
        self.white_balance_btn.set(self.white_balance)
        self.shade_btn.set(self.shade)
        self.winiet_btn.set(self.winiet)
        self.noise_btn.set(self.noise)
        size_xy = [0, 0, 100, 100]
        self.update_func()
    
    def crop_func(self):
        if (self.new_img):
            if self.window is None or not self.window.winfo_exists():
                self.window = CropWindow(self)
                self.window.create_image(self.new_img)
            else:
                self.window.focus()
            self.update_func()

    def update_func(self):
        new_resize_img = self.new_img.resize((round(self.new_img.size[0] * (self.zoom_value / 100)), round(self.new_img.size[1] * (self.zoom_value / 100))))
        editable_image = new_resize_img.rotate(self.rotate_value)
        saturation = ImageEnhance.Color(editable_image).enhance(self.ench_value / 100)
        contrast = ImageEnhance.Contrast(saturation).enhance(self.contr_value / 100)
        brightness = ImageEnhance.Brightness(contrast).enhance(self.bright_value / 100)
        sharpness = ImageEnhance.Sharpness(brightness).enhance(self.sharp_value / 100)

        wb_img = self.wb_func(sharpness)
        shade_img = self.shade_edit_func(wb_img)
            
        noise_img  = self.create_noise(shade_img)
        winiet_img = self.create_winiet(noise_img)

        croped = winiet_img.crop((round(winiet_img.size[0] * (size_xy[0] / 100)), round(winiet_img.size[1] * (size_xy[1] / 100)), round(winiet_img.size[0] * (size_xy[2] / 100)), round(winiet_img.size[1] * (size_xy[3] / 100))))

        self.end_img = croped
        self.tatras = ImageTk.PhotoImage(self.end_img)
        self.edit_image.configure(image=self.tatras)

    def save_image_func(self):
        if(self.end_img):
            foldername = askdirectory()
            editable_image = self.img.rotate(self.rotate_value)
            saturation = ImageEnhance.Color(editable_image).enhance(self.ench_value / 100)
            contrast = ImageEnhance.Contrast(saturation).enhance(self.contr_value / 100)
            brightness = ImageEnhance.Brightness(contrast).enhance(self.bright_value / 100)
            sharpness = ImageEnhance.Sharpness(brightness).enhance(self.sharp_value / 100)

            wb_img = self.wb_func(sharpness)
            shade_img = self.shade_edit_func(wb_img)

            noise_img  = self.create_noise(shade_img)
            winiet_img = self.create_winiet(noise_img)
            croped = winiet_img.crop((round(winiet_img.size[0] * (size_xy[0] / 100)), round(winiet_img.size[1] * (size_xy[1] / 100)), round(winiet_img.size[0] * (size_xy[2] / 100)), round(winiet_img.size[1] * (size_xy[3] / 100))))


            save_edit_img = croped
            save_edit_img.save(f'{foldername}/{(((self.image_name).split("/"))[::-1])[0].split(".")[0]}.png', 'png', quality=100)

    def __del__(self):
        print('destroed!')

if __name__ == '__main__':
    ct.set_appearance_mode('System')
    ct.set_default_color_theme('blue')

    app = App()
    app.mainloop()