import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from dataclasses import dataclass, field
from utils import Vector2D

@dataclass
class ViewerSettings:
    min_scale: float = 0.2
    max_scale: float = 4.0
    scale_factor: float = 1.0
    mouse_position: Vector2D = field(default_factory=Vector2D(0, 0))


class ImageCanvas(tk.Canvas):
    def __init__(self, parent, image_path: str, options: ViewerSettings):
        super().__init__(parent, bg="black", scrollregion=(0, 0, 0, 0))
        self.parent = parent
        self.image_path = image_path
        self.image = None
        self.tk_image = None
        self.img_width = 0
        self.img_height = 0
        self.options = options

        self.load_image()

        self.x_scroll = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
        self.y_scroll = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        self.configure(xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)

        self.x_scroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.y_scroll.pack(fill=tk.Y, side=tk.RIGHT)

    def load_image(self):
        """Loads and displays the image on the canvas."""
        self.image = Image.open(self.image_path)
        self.img_width, self.img_height = self.image.size
        self.update_image()

    def update_image(self):
        """Updates the displayed image based on the scale factor."""
        scale = max(self.options.min_scale, min(self.options.scale_factor, self.options.max_scale))
        resized_image = self.image.resize(
            (int(self.img_width * scale), int(self.img_height * scale)),
            Image.Resampling.NEAREST
        )
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.delete("image")
        self.create_image(0, 0, anchor=tk.NW, image=self.tk_image, tags="image")
        self.config(scrollregion=(0, 0, resized_image.width, resized_image.height))

class StatusBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side=tk.BOTTOM, fill=tk.X)

        # Configure grid layout
        self.columnconfigure(0, weight=1)  # Label expands
        self.columnconfigure(1, weight=0)  # Button stays on the right

        self.label = ttk.Label(self, text="Mouse: (---, ---)", anchor=tk.W)
        self.label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.confirm_btn = ttk.Button(self, text="Confirmar", command=self.button_clicked, state=tk.DISABLED)
        self.confirm_btn.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    def button_clicked(self):
        """Button click event handler."""
        print("Button clicked!")
        self.destroy()

    def update_label(self, text: str):
        """Updates the status bar with new text."""
        self.label.config(text=text)

    def update_button(self, condition: bool):
        """Enables or disables the confirm button based on a condition."""
        self.confirm_btn.config(state=tk.NORMAL if condition else tk.DISABLED)

class EventHandler:
    def __init__(self, canvas: ImageCanvas, status_bar: StatusBar ,options: ViewerSettings):
        self.canvas = canvas
        self.options = options
        self.status_bar = status_bar
        self.bind_events()

    def bind_events(self):
        """Binds mouse events for interactivity."""
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.on_zoom)  # Windows & macOS
        self.canvas.bind("<Control-MouseWheel>", self.on_zoom)  # macOS with Control key
        self.canvas.bind("<Button-4>", self.on_zoom_in)  # Linux Scroll Up
        self.canvas.bind("<Button-5>", self.on_zoom_out)  # Linux Scroll Down
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def on_right_click(self, event):
        pass

    def on_click(self, event):
        pass

    def on_release(self, event):
        pass

    def on_mouse_move(self, event):
        """Updates the status bar with the current image pixel coordinates."""
        x = self.canvas.canvasx(event.x) / self.options.scale_factor
        y = self.canvas.canvasy(event.y) / self.options.scale_factor
        if 0 <= x < self.canvas.img_width and 0 <= y < self.canvas.img_height:
            self.options.mouse_position = Vector2D(x, y)
            self.status_bar.update_label(f"Mouse: ({int(x)}, {int(y)})")
        else:
            self.status_bar.update_label("Mouse: (---, ---)")

    def on_press(self, event):
        """Stores the initial click position for panning."""
        self.canvas.scan_mark(event.x, event.y)

    def on_drag(self, event):
        """Handles panning by dragging the mouse."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def on_zoom(self, event):
        """Handles zooming in and out with the mouse wheel."""
        if event.delta > 0:
            self.options.scale_factor *= 1.1
        else:
            self.options.scale_factor *= 0.9
        self.options.scale_factor = max(self.options.min_scale, min(self.options.scale_factor, self.options.max_scale))
        self.canvas.update_image()

    def on_zoom_in(self, event):
        """Handles zooming in (Linux scroll up)."""
        self.options.scale_factor *= 1.1
        self.options.scale_factor = min(self.options.scale_factor, self.options.max_scale)
        self.canvas.update_image()

    def on_zoom_out(self, event):
        """Handles zooming out (Linux scroll down)."""
        self.options.scale_factor *= 0.9
        self.options.scale_factor = max(self.options.scale_factor, self.options.min_scale)
        self.canvas.update_image()




class SideBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side=tk.LEFT, fill=tk.Y)

        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)


class ImageViewer(tk.Toplevel):
    def __init__(self, path_to_image: str):
        super().__init__()
        self.title("Image Viewer with Pixel Coordinates")
        self.geometry("900x700")
        self.path_to_image = path_to_image

    def initialize(self):
        """Initializes the image viewer with the given image."""
        self.options = ViewerSettings()
        self.canvas = ImageCanvas(self, self.path_to_image, self.options)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.event_handler = EventHandler(self.canvas, self.options)
        self.status_bar = StatusBar(self)
    def update_status(self, text: str):
        """Updates the status bar with new text."""
        self.status_bar.update_label(text)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = ImageViewer("singlecreepers.png")
    app.mainloop()
