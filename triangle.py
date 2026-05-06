# triangle.py
from shape import Shape
from line import Line 
import math

class Triangle(Shape):  # ← Triangle НАСЛЕДУЕТ Shape
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_degenerate(self):
        return self.area() == 0
    
    def sides(self):
        ab = Line(self.a, self.b).length()
        bc = Line(self.b, self.c).length()
        ca = Line(self.c, self.a).length()
        return (ab, bc, ca)
    
    def perimeter(self):
        return sum(self.sides())
    
    def area(self):
        ab, bc, ca = self.sides()
        s = self.perimeter() / 2
        under_root = s * (s - ab) * (s - bc) * (s - ca)
        if under_root < 0:
            return 0
        return math.sqrt(under_root)
    
    def triangle_type(self):

        a, b, c = self.sides()
        
        # Сортируем стороны для удобства
        sides = sorted([a, b, c])
        s1, s2, s3 = sides[0], sides[1], sides[2]
        
        # Равносторонний
        if abs(a - b) < 0.0001 and abs(b - c) < 0.0001:
            return "равносторонний"
        
        # Равнобедренный
        if abs(a - b) < 0.0001 or abs(b - c) < 0.0001 or abs(a - c) < 0.0001:
            return "равнобедренный"
        
        # Прямоугольный (теорема Пифагора)
        if abs(s1**2 + s2**2 - s3**2) < 0.0001:
            return "прямоугольный"
        
        # Остроугольный / Тупоугольный
        if s1**2 + s2**2 > s3**2:
            return "остроугольный"
        else:
            return "тупоугольный"
    
    def draw(self, plane):
        plane.clear_all()
        
        pts = []
        for p in [self.a, self.b, self.c]:
            x, y = plane.world_to_screen(p.x, p.y)
            pts.extend([x, y])
            plane.canvas.create_oval(x-4, y-4, x+4, y+4, fill='red', tags='figure')
            plane.canvas.create_text(x+10, y-10, 
                                     text=f'({p.x:.1f}, {p.y:.1f})',
                                     font=('Arial', 8), tags='figure')
        
        plane.canvas.create_polygon(pts, outline='green', fill='', width=2, tags='figure')
        
        cx = (self.a.x + self.b.x + self.c.x) / 3
        cy = (self.a.y + self.b.y + self.c.y) / 3
        sx, sy = plane.world_to_screen(cx, cy)
        plane.canvas.create_text(sx, sy, 
                                 text=f'P={self.perimeter():.2f}\nS={self.area():.2f}',
                                 font=('Arial', 9), fill='darkgreen', tags='figure')
    
    def info(self):
        return f"ТРЕУГОЛЬНИК\nТип: {self.triangle_type()}\nПериметр: {self.perimeter():.3f}\nПлощадь: {self.area():.3f}"