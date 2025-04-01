import GUI.image_viewer as img_viewer
from utils import Vector2D
from time import time
import tkinter as tk
from dataclasses import dataclass, field
from configInterface.initializer import settings



@dataclass
class SelectMarkerSizeOptions(img_viewer.ViewerSettings):
    def __init__(self):
        super().__init__()
        self.points: list[Vector2D] = []
        self.bubble_size: Vector2D = field(default_factory=Vector2D, init=False)


class EventHandler(img_viewer.EventHandler):
    time: float
    options: SelectMarkerSizeOptions

    def __init__(self, options: SelectMarkerSizeOptions, canvas: img_viewer.ImageCanvas, status_bar: img_viewer.StatusBar):
        super().__init__(options=options, canvas=canvas, status_bar=status_bar)

    def on_click(self, event):
        self.time = time()
        return

    def on_release(self, event):
        if time() - self.time < 0.2:
            self.add_point(self.options.mouse_position)
        else:
            print("Click too long, ignoring.")
    def on_right_click(self, event):
        if len(self.options.points) == 0:
            return
        self.options.points.pop()
        self.canvas.update_image()
        self.status_bar.update_button(len(self.options.points) >= 2)

    def add_point(self, point: Vector2D):
        if len(self.options.points) >= 2:
            return
        self.options.points.append(point)
        print(f"added point at {point.x}, {point.y}")
        self.canvas.update_image()
        self.status_bar.update_button(len(self.options.points) >= 2)

class StatusBar(img_viewer.StatusBar):
    def button_clicked(self):
        p1 = self.parent.options.points[0]
        p2 = self.parent.options.points[1]
        marker_width = abs(p1.x - p2.x)

class ImageCanvas(img_viewer.ImageCanvas):
    POINT_SIZE: int = 5
    options: SelectMarkerSizeOptions

    def draw_points(self):
        self.delete("point")
        for point in self.options.points:
            point *= self.options.scale_factor
            x, y = point.x, point.y
            self.create_oval(x - self.POINT_SIZE, y - self.POINT_SIZE, x + self.POINT_SIZE, y + self.POINT_SIZE, fill="red", tags="point")
        if len(self.options.points) == 2:
            self.draw_square()


    def draw_square(self):
        p1, p2 = self.options.points
        p1 *= self.options.scale_factor
        p2 *= self.options.scale_factor
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        self.create_rectangle(x1, y1, x2, y2, outline="red", tags="point")

    def update_image(self):
        super().update_image()
        self.draw_points()


class SelectMarkerSize(tk.Toplevel):
    def __init__(self, path_to_image: str):
        super().__init__()
        self.title("Ajustar Tamanho das Marcações")
        self.geometry("900x700")
        self.options = SelectMarkerSizeOptions()
        self.canvas = ImageCanvas(self, path_to_image, self.options)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.status_bar = img_viewer.StatusBar(self)
        self.event_handler = EventHandler(canvas=self.canvas, options=self.options, status_bar=self.status_bar)

