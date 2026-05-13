# rectangle.py
from shape import Shape
from line import Line
from point import Point
import math

class Rectangle(Shape):
    # ПРЯМОУГОЛЬНИК ПО 4 ТОЧКАМ (АВТОМАТИЧЕСКАЯ СОРТИРОВКА)
    def __init__(self, p1, p2, p3, p4):
        self.points = self._order_points([p1, p2, p3, p4])
        self.p1, self.p2, self.p3, self.p4 = self.points
    
    # УПОРЯДОЧИВАЕТ 4 ТОЧКИ ДЛЯ ПРАВИЛЬНОГО РИСОВАНИЯ (ПО ЧАСОВОЙ СТРЕЛКЕ)
    def _order_points(self, points):
        # Находит центр
        cx = sum(p.x for p in points) / 4
        cy = sum(p.y for p in points) / 4
        
        # Сортирует по углу относительно центра
        def get_angle(point):
            return math.atan2(point.y - cy, point.x - cx)
        
        sorted_points = sorted(points, key=get_angle)
        return sorted_points
    
    def is_degenerate(self):
        a, b, c, d = self.sides()
        # Если периметр почти равен сумме двух диагоналей (точки на одной линии)
        if self.perimeter() < 0.0001:
            return True
        
        # Проверка на 3 точки на одной линии (площадь треугольника = 0)
        if abs(Line(self.p1, self.p2).length() + Line(self.p2, self.p3).length() - Line(self.p1, self.p3).length()) < 0.0001:
            return True
        if abs(Line(self.p2, self.p3).length() + Line(self.p3, self.p4).length() - Line(self.p2, self.p4).length()) < 0.0001:
            return True
        if abs(Line(self.p3, self.p4).length() + Line(self.p4, self.p1).length() - Line(self.p3, self.p1).length()) < 0.0001:
            return True
        if abs(Line(self.p4, self.p1).length() + Line(self.p1, self.p2).length() - Line(self.p4, self.p2).length()) < 0.0001:
            return True
        
        return False
    
    def sides(self):
        a = Line(self.p1, self.p2).length()
        b = Line(self.p2, self.p3).length()
        c = Line(self.p3, self.p4).length()
        d = Line(self.p4, self.p1).length()
        return (a, b, c, d)
    
    def diagonals(self):
        d1 = Line(self.p1, self.p3).length()
        d2 = Line(self.p2, self.p4).length()
        return (d1, d2)
    
    def perimeter(self):
        return sum(self.sides())
    
    # ПЛОЩАДЬ ЧЕРЕЗ ФОРМУЛУ ГАУССА
    def area(self):
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
        s1, s2, s3, s4 = sides[0], sides[1], sides[2], sides[3]
        
        # Ромб (все стороны равны)
        if abs(a - b) < 0.0001 and abs(b - c) < 0.0001 and abs(c - d) < 0.0001:
            if abs(d1 - d2) < 0.0001:
                return "квадрат"
            else:
                return "ромб"
        
        # Прямоугольник (противоположные стороны равны, диагонали равны)
        if abs(a - c) < 0.0001 and abs(b - d) < 0.0001:
            if abs(d1 - d2) < 0.0001:
                return "прямоугольник"
            else:
                return "параллелограмм"
        
        # Параллелограмм (противоположные стороны равны)
        if abs(a - c) < 0.0001 and abs(b - d) < 0.0001:
            return "параллелограмм"
        
        # Трапеция (одна пара сторон параллельна)
        # Упрощённая проверка: отношение длин сторон
        if abs(a - c) < 0.0001 or abs(b - d) < 0.0001:
            return "равнобокая трапеция"
        
        return "произвольный четырёхугольник"
    
    def draw(self, plane):
        plane.clear_all()
        
        pts = []
        for p in self.points:
            x, y = plane.world_to_screen(p.x, p.y)
            pts.extend([x, y])
            plane.canvas.create_oval(x-4, y-4, x+4, y+4, fill='red', tags='figure')
            plane.canvas.create_text(x+10, y-10, 
                                     text=f'({p.x:.1f}, {p.y:.1f})',
                                     font=('Arial', 8), tags='figure')
        
        plane.canvas.create_polygon(pts, outline='purple', fill='', width=2, tags='figure')
        
        cx = sum(p.x for p in self.points) / 4
        cy = sum(p.y for p in self.points) / 4
        sx, sy = plane.world_to_screen(cx, cy)
        
        plane.canvas.create_text(sx, sy, 
                                 text=f'P={self.perimeter():.2f}\nS={self.area():.2f}',
                                 font=('Arial', 9), fill='darkviolet', tags='figure')
    
    def info(self):
        return f"ЧЕТЫРЁХУГОЛЬНИК\nТип: {self.quadrilateral_type()}\nПериметр: {self.perimeter():.3f}\nПлощадь: {self.area():.3f}"