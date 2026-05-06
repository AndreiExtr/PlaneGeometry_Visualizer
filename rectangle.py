# rectangle.py
from shape import Shape
from line import Line
from point import Point
import math

class Rectangle(Shape):

    # ПРЯМОУГОЛЬНИК ПО 4 ТОЧКАМ
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.points = [p1, p2, p3, p4]
    
    # ВОЗВРАЩАЕТ ДЛИНЫ ВСЕХ 4 СТОРОН
    def sides(self):
        a = Line(self.p1, self.p2).length()
        b = Line(self.p2, self.p3).length()
        c = Line(self.p3, self.p4).length()
        d = Line(self.p4, self.p1).length()
        return (a, b, c, d)
    
    # ВОЗВРАЩАЕТ ДЛИНЫ ДИАГОНАЛЕЙ
    def diagonals(self):
        d1 = Line(self.p1, self.p3).length()
        d2 = Line(self.p2, self.p4).length()
        return (d1, d2)
    
    def perimeter(self):
        return sum(self.sides())
    
    # ПЛОЩАДЬ ЧЕРЕЗ ДИАГОНАЛИ И УГОЛ
    def area(self):
        # Используется формулу Гаусса 
        x = [p.x for p in self.points]
        y = [p.y for p in self.points]
        
        sum1 = 0
        sum2 = 0
        for i in range(4):
            sum1 += x[i] * y[(i + 1) % 4]
            sum2 += y[i] * x[(i + 1) % 4]
        
        return abs(sum1 - sum2) / 2
    
    def quadrilateral_type(self):
        a, b, c, d = self.sides()
        d1, d2 = self.diagonals()
        
        # Сортирует стороны для удобства
        sides = sorted([a, b, c, d])
        
        # Проверка на квадрат (все стороны равны И диагонали равны И углы 90°)
        if abs(a - b) < 0.0001 and abs(b - c) < 0.0001 and abs(c - d) < 0.0001:
            # Проверяем диагонали (у квадрата они равны)
            if abs(d1 - d2) < 0.0001:
                return "квадрат"
            else:
                return "ромб"
        
        # Проверка на прямоугольник (противоположные стороны равны, диагонали равны)
        if abs(a - c) < 0.0001 and abs(b - d) < 0.0001:
            if abs(d1 - d2) < 0.0001:
                # Проверяем, есть ли прямые углы (теорема Пифагора)
                if abs(a**2 + b**2 - d1**2) < 0.0001:
                    return "прямоугольник"
                else:
                    return "параллелограмм"
        
        # Проверка на параллелограмм (противоположные стороны равны)
        if abs(a - c) < 0.0001 and abs(b - d) < 0.0001:
            return "параллелограмм"
        
        # Проверка на равнобокую трапецию
        if abs(a - c) < 0.0001 or abs(b - d) < 0.0001:
            return "равнобокая трапеция"
        
        # Проверка на трапецию (хотя бы одна пара параллельных сторон)
        # Упрощённо: если одна пара сторон почти равна
        if abs(a - c) < 0.0001 or abs(b - d) < 0.0001:
            return "трапеция"
        
        return "произвольный четырёхугольник"
    
    def draw(self, plane):
        plane.clear_all()
        
        # Рисует точки и подписи
        pts = []
        for p in self.points:
            x, y = plane.world_to_screen(p.x, p.y)
            pts.extend([x, y])
            plane.canvas.create_oval(x-4, y-4, x+4, y+4, fill='red', tags='figure')
            plane.canvas.create_text(x+10, y-10, 
                                     text=f'({p.x:.1f}, {p.y:.1f})',
                                     font=('Arial', 8), tags='figure')
        
        # Рисует многоугольник
        plane.canvas.create_polygon(pts, outline='purple', fill='', width=2, tags='figure')
        
        # Центр для отображения информации
        cx = sum(p.x for p in self.points) / 4
        cy = sum(p.y for p in self.points) / 4
        sx, sy = plane.world_to_screen(cx, cy)
        
        plane.canvas.create_text(sx, sy, 
                                 text=f'P={self.perimeter():.2f}\nS={self.area():.2f}',
                                 font=('Arial', 9), fill='darkviolet', tags='figure')
    
    def info(self):
        return f"ЧЕТЫРЁХУГОЛЬНИК\nТип: {self.quadrilateral_type()}\nПериметр: {self.perimeter():.3f}\nПлощадь: {self.area():.3f}"