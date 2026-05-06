# circle.py
from shape import Shape
from line import Line 
import math

class Circle(Shape): # ← Circle НАСЛЕДУЕТ Shape
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    
    @classmethod
    def from_two_points(cls, center, point_on_circle):
        radius = Line(center, point_on_circle).length()
        return cls(center, radius)
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def circumference(self):
        return self.perimeter()
    
    def draw(self, plane):
        plane.clear_all()
        
        cx, cy = plane.world_to_screen(self.center.x, self.center.y)
        r_pixel = self.radius * plane.scale
        
        plane.canvas.create_oval(cx - r_pixel, cy - r_pixel,
                                 cx + r_pixel, cy + r_pixel,
                                 outline='orange', fill='', width=2, tags='figure')
        
        plane.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill='red', tags='figure')
        plane.canvas.create_text(cx+10, cy-10, 
                                 text=f'({self.center.x:.1f}, {self.center.y:.1f})',
                                 font=('Arial', 8), tags='figure')
        
        plane.canvas.create_text(cx, cy - r_pixel - 10,
                                 text=f'R={self.radius:.2f}',
                                 font=('Arial', 9), fill='darkorange', tags='figure')
        
        plane.canvas.create_text(cx, cy + r_pixel + 20,
                                 text=f'C={self.circumference():.2f}\nS={self.area():.2f}',
                                 font=('Arial', 9), fill='darkorange', tags='figure')
    
    def draw_with_point(self, plane, point_on_circle):
        plane.clear_all()
        
        cx, cy = plane.world_to_screen(self.center.x, self.center.y)
        r_pixel = self.radius * plane.scale
        
        plane.canvas.create_oval(cx - r_pixel, cy - r_pixel,
                                 cx + r_pixel, cy + r_pixel,
                                 outline='orange', fill='', width=2, tags='figure')
        
        plane.canvas.create_oval(cx-4, cy-4, cx+4, cy+4, fill='red', tags='figure')
        plane.canvas.create_text(cx+10, cy-10, 
                                 text=f'({self.center.x:.1f}, {self.center.y:.1f})',
                                 font=('Arial', 8), tags='figure')
        
        x2, y2 = plane.world_to_screen(point_on_circle.x, point_on_circle.y)
        plane.canvas.create_oval(x2-4, y2-4, x2+4, y2+4, fill='blue', tags='figure')
        plane.canvas.create_text(x2+10, y2-10, 
                                 text=f'({point_on_circle.x:.1f}, {point_on_circle.y:.1f})',
                                 font=('Arial', 8), tags='figure')
        
        plane.canvas.create_line(cx, cy, x2, y2, fill='gray', width=1, dash=(5,5), tags='figure')
        
        plane.canvas.create_text(cx, cy - r_pixel - 10,
                                 text=f'R={self.radius:.2f}',
                                 font=('Arial', 9), fill='darkorange', tags='figure')
        
        plane.canvas.create_text(cx, cy + r_pixel + 20,
                                 text=f'C={self.circumference():.2f}\nS={self.area():.2f}',
                                 font=('Arial', 9), fill='darkorange', tags='figure')
    
    def info(self):
        return f"ОКРУЖНОСТЬ / КРУГ\nРадиус: {self.radius:.3f}\nДиаметр: {self.radius*2:.3f}\nДлина окружности: {self.circumference():.3f}\nПлощадь круга: {self.area():.3f}"