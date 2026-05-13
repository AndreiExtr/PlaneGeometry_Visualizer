# main.py
import tkinter as tk
from tkinter import messagebox
from coordinate_plane import CoordinatePlane
from point import Point
from line import Line
from triangle import Triangle
from circle import Circle
from shape import Shape
from rectangle import Rectangle

class GeometryApp:
    # ОСНОВНОЙ ИНТЕРФЕЙС
    def __init__(self, root):
        self.root = root
        self.root.title("Геометрический калькулятор")
        self.root.geometry("1100x600")
        
        # Рамка для левой панели (управление)
        left_frame = tk.Frame(root, bg='lightgray', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Рамка для правой панели (график)
        right_frame = tk.Frame(root, bg='white', relief=tk.SUNKEN, bd=2)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Координатная плоскость (фон и оси)
        self.plane = CoordinatePlane(right_frame, width=750, height=750, scale=30)
        
        self.create_control_panel(left_frame)
    
    # ПАНЕЛЬ
    def create_control_panel(self, parent):
        # Заголовок
        tk.Label(parent, text="📐 ГЕОМЕТРИЧЕСКИЙ\n    КАЛЬКУЛЯТОР", 
                font=('Arial', 14, 'bold'), bg='lightgray', 
                justify='center').pack(pady=10)
        
        tk.Frame(parent, height=2, bg='gray').pack(fill=tk.X, padx=10, pady=5)
        
        # Поле для ввода координат
        tk.Label(parent, text="Введите координаты:", 
                font=('Arial', 11, 'bold'), bg='lightgray').pack(pady=(10,5))
        
        tk.Label(parent, text="Треугольник: x1,y1 x2,y2 x3,y3", 
                font=('Arial', 9), bg='lightgray', fg='gray').pack()
        tk.Label(parent, text="Окружность (1 точка + радиус): x,y r", 
                font=('Arial', 9), bg='lightgray', fg='gray').pack()
        tk.Label(parent, text="Окружность (2 точки): x1,y1 x2,y2", 
                font=('Arial', 9), bg='lightgray', fg='gray').pack()
        tk.Label(parent, text="Прямоугольник: x1,y1 x2,y2 x3,y3 x4,y4", 
        font=('Arial', 9), bg='lightgray', fg='gray').pack()

        tk.Label(parent, text="Пример: 0,0 5  или  0,0 3,0", 
                font=('Arial', 8), bg='lightgray', fg='blue').pack()

        
        self.coords_entry = tk.Entry(parent, width=30, font=('Arial', 10))
        self.coords_entry.pack(pady=10)
        
        tk.Frame(parent, height=2, bg='gray').pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопки
        btn_frame = tk.Frame(parent, bg='lightgray')
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="ПОСТРОИТЬ", command=self.draw_shape,
                 bg='green', fg='white', font=('Arial', 11, 'bold'),
                 width=12, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="ОЧИСТИТЬ", command=self.clear_all,
                 bg='red', fg='white', font=('Arial', 11, 'bold'),
                 width=12, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Frame(parent, height=2, bg='gray').pack(fill=tk.X, padx=10, pady=10)
        
        # Рамка для результатов
        result_frame = tk.LabelFrame(parent, text="📊 РЕЗУЛЬТАТЫ", 
                                      bg='lightgray', font=('Arial', 11, 'bold'))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(result_frame, height=15, width=35, 
                                    font=('Courier', 10), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = tk.Scrollbar(result_frame, command=self.result_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scroll.set)
    
    # ПРИНИМЕТ И РАЗБИРАЕТ КООРДИНАТЫ ВВЕДЕННЫЕ В СТРОКЕ
    def parse_points(self, coords_str):
        points = []
        for pair in coords_str.split():
            if ',' in pair:
                parts = pair.split(',')
                try:
                    points.append(Point(float(parts[0]), float(parts[1])))
                except ValueError:
                    pass
        return points
    
    # ФАБРИЧНЫЙ МЕТОД: СОЗДЕТ ФИГУРУ ПО КООРДИНАТАМ (ПОЛИМОРФИЗМ)
    def create_figure(self, coords_str):
        parts = coords_str.split()
        
        # Окружность: центр + радиус
        if len(parts) == 2 and ',' in parts[0]:
            try:
                xy = parts[0].split(',')
                x = float(xy[0])
                y = float(xy[1])
                radius = float(parts[1])
                return Circle(Point(x, y), radius)
            except:
                pass
        
        points = self.parse_points(coords_str)
        count = len(points)
        
        if count == 2:
            # Окружность по двум точкам
            radius = Line(points[0], points[1]).length()
            return Circle(points[0], radius)
        elif count == 3:
            # Треугольник
            triangle = Triangle(points[0], points[1], points[2])
            # Проверка на вырожденность
            if triangle.is_degenerate() or triangle.area() == 0:
                return None
            return triangle
        
        elif count == 4:
            # Четырёхугольник (автоматическая сортировка точек)
            rect = Rectangle(points[0], points[1], points[2], points[3])
            if rect.is_degenerate():
                return None
            return rect
        
        return None
    
    # РИСУЕТ ФИГУРУ С ПОЛИМОРФИЗМОМ
    def draw_shape(self):
        coords_str = self.coords_entry.get().strip()
        if not coords_str:
            messagebox.showwarning("Ошибка", "Введите координаты!")
            return
        
        # СОЗДАЁТ ФИГУРУ (абстрактный тип Shape)
        figure = self.create_figure(coords_str)
        
        if figure is None:
            messagebox.showwarning("Ошибка", "Неверный формат или точки лежат на одной линии!\n\nТреугольник: 0,0 3,0 0,4\nОкружность (радиус): 0,0 5\nОкружность (2 точки): 0,0 3,0")
            return
        
        self.result_text.delete(1.0, tk.END)
        
        # ========== ПОЛИМОРФИЗМ ==========
        # Один и тот же код работает для ЛЮБОЙ фигуры!
        figure.draw(self.plane)           # ← разное поведение для Triangle и Circle
        self.result_text.insert(tk.END, figure.info())  # ← разное поведение
        

        points = self.parse_points(coords_str)
        if isinstance(figure, Circle) and len(points) == 2:
            self.result_text.insert(tk.END, f"\nТочка на окружности: ({points[1].x:.1f}, {points[1].y:.1f})")
    
    # ОЧИЩАЕТ ВСЕ
    def clear_all(self):
        self.plane.clear_all()
        self.result_text.delete(1.0, tk.END)
        self.coords_entry.delete(0, tk.END)

# ========== ЗАПУСК ==========

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)
    root.mainloop()