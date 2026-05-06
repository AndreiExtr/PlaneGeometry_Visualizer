# coordinate_plane.py
import tkinter as tk

class CoordinatePlane:
    
    def __init__(self, root, width=600, height=600, scale=30):
        self.root = root
        self.width = width
        self.height = height
        self.scale = scale  # 1 единица = scale пикселей
        
        # Холст для рисования
        self.canvas = tk.Canvas(root, width=width, height=height, bg='white')
        self.canvas.pack()
        
        # Центр координат
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Рисуем фон
        self.draw_grid()
        self.draw_axes()
    
    # КЛЕТЧАТЫЙ ФОН (от центра)
    def draw_grid(self):
        # Вертикальные линии (от центра влево и вправо)
        # Влево от центра
        x = self.center_x
        while x >= 0:
            self.canvas.create_line(x, 0, x, self.height, fill='#d0d0d0', tags='grid')
            x -= self.scale
        # Вправо от центра
        x = self.center_x + self.scale
        while x <= self.width:
            self.canvas.create_line(x, 0, x, self.height, fill='#d0d0d0', tags='grid')
            x += self.scale
        
        # Горизонтальные линии (от центра вверх и вниз)
        # Вверх от центра
        y = self.center_y
        while y >= 0:
            self.canvas.create_line(0, y, self.width, y, fill='#d0d0d0', tags='grid')
            y -= self.scale
        # Вниз от центра
        y = self.center_y + self.scale
        while y <= self.height:
            self.canvas.create_line(0, y, self.width, y, fill='#d0d0d0', tags='grid')
            y += self.scale
    
    # КООРДИНАТНЫЕ ОСИ X И Y
    def draw_axes(self):
        # Ось X
        self.canvas.create_line(0, self.center_y, self.width, self.center_y,
                               fill='black', width=2, tags='axis')
        # Ось Y
        self.canvas.create_line(self.center_x, 0, self.center_x, self.height,
                               fill='black', width=2, tags='axis')
        
        # Стрелка X
        self.canvas.create_polygon(self.width - 10, self.center_y - 5,
                                   self.width, self.center_y,
                                   self.width - 10, self.center_y + 5,
                                   fill='black', tags='axis')
        # Стрелка Y
        self.canvas.create_polygon(self.center_x - 5, 10,
                                   self.center_x, 0,
                                   self.center_x + 5, 10,
                                   fill='black', tags='axis')
        
        # Подписи X и Y
        self.canvas.create_text(self.width - 20, self.center_y - 10,
                               text='X', font=('Arial', 12, 'bold'), tags='axis')
        self.canvas.create_text(self.center_x + 15, 15,
                               text='Y', font=('Arial', 12, 'bold'), tags='axis')
        
        # Ноль
        self.canvas.create_text(self.center_x - 15, self.center_y + 15,
                               text='0', font=('Arial', 10, 'bold'), tags='axis')
        
        # Деления на оси X
        i = 1
        # Вправо
        x_pixel = self.center_x + self.scale
        while x_pixel <= self.width:
            self.canvas.create_text(x_pixel, self.center_y + 15,
                                   text=str(i), font=('Arial', 8), tags='axis')
            x_pixel += self.scale
            i += 1
        
        i = -1
        # Влево
        x_pixel = self.center_x - self.scale
        while x_pixel >= 0:
            self.canvas.create_text(x_pixel, self.center_y + 15,
                                   text=str(i), font=('Arial', 8), tags='axis')
            x_pixel -= self.scale
            i -= 1
        
        # Деления на оси Y
        i = 1
        # Вверх
        y_pixel = self.center_y - self.scale
        while y_pixel >= 0:
            self.canvas.create_text(self.center_x - 15, y_pixel,
                                   text=str(i), font=('Arial', 8), tags='axis')
            y_pixel -= self.scale
            i += 1
        
        i = -1
        # Вниз
        y_pixel = self.center_y + self.scale
        while y_pixel <= self.height:
            self.canvas.create_text(self.center_x - 15, y_pixel,
                                   text=str(i), font=('Arial', 8), tags='axis')
            y_pixel += self.scale
            i -= 1
    
    # ПЕРЕВОД МИРОВЫХ КООРДИНАТ В ЭКРАННЫЕ
    def world_to_screen(self, x, y):
        screen_x = self.center_x + x * self.scale
        screen_y = self.center_y - y * self.scale
        return screen_x, screen_y
    
    # ПЕРЕВОД ЭКРАННЫХ КООРДИНАТ В МИРОВЫЕ
    def screen_to_world(self, px, py):
        world_x = (px - self.center_x) / self.scale
        world_y = (self.center_y - py) / self.scale
        return world_x, world_y
    
    def clear_all(self):
        self.canvas.delete('all')
        self.draw_grid()
        self.draw_axes()