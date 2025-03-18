from GUI.top_level_window import TopLevelWindow
from tkinter import ttk, filedialog
import tkinter as tk
from GUI.functions import set_page_size
from PIL import Image, ImageTk
from GUI.widget_builder import WidgetBuilder
import time


class ScannerConfig(WidgetBuilder):
    def __init__(self):
        super().__init__()
        self.sheet_template_path: str = None
        self.title("Configuração")
        self.default()


    def default(self) -> None:
        self.create_label(text="Selecionar Modelo do Gabarito", row=0)
        self.create_button(0, "Selecionar", button_command=self.get_template)
        self.create_label_and_button(row=1, button_text="Ajustar", label_text="Ajustar tamanho da marcação", button_command=...)
        self.create_button(button_text="Fechar", button_command=self.destroy, row=2)


    def get_template(self):
        self.sheet_template_path = filedialog.askopenfilename()
        set_page_size(self.sheet_template_path)


class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Viewer with Pixel Coordinates")
        self.geometry("900x700")

        # UI Controls
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, pady=5)

        self.load_button = ttk.Button(self.control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.zoom_in_button = ttk.Button(self.control_frame, text="Zoom In", command=lambda: self.zoom(1.1))
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = ttk.Button(self.control_frame, text="Zoom Out", command=lambda: self.zoom(0.9))
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(self.control_frame, text="Reset View", command=self.reset_view)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Label(self, text="Mouse: (---, ---)", anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.confirm_button = ttk.Button(self.control_frame, text="Confirm", command=self.confirm_selection, state=tk.DISABLED)
        self.confirm_button.pack(side=tk.LEFT, padx=5)

        # Canvas for Image Display
        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Image data
        self.image = None
        self.tk_image = None
        self.zoom_factor = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.start_x, self.start_y = 0, 0
        self.start_time = 0  # Track click time

        self.circles = []  # Store circles (only 2 at max)
        self.square_id = None  # Store square ID

        # Bindings
        self.canvas.bind("<MouseWheel>", self.mouse_zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)
        self.canvas.bind("<ButtonRelease-1>", self.place_circle)
        self.canvas.bind("<Button-3>", self.remove_circle)  # Right-click removes circles
        self.canvas.bind("<Motion>", self.update_mouse_coordinates)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not file_path:
            return

        self.image = Image.open(file_path)
        self.original_width, self.original_height = self.image.size
        self.zoom_factor = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.circles.clear()
        self.display_image()

    def display_image(self):
        """ Displays the image on the canvas at the current zoom level """
        if not self.image:
            return

        new_size = (int(self.original_width * self.zoom_factor), int(self.original_height * self.zoom_factor))
        resized_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)

        self.canvas.delete("all")
        self.img_x = self.canvas.winfo_width() // 2 + self.offset_x
        self.img_y = self.canvas.winfo_height() // 2 + self.offset_y

        self.image_id = self.canvas.create_image(self.img_x, self.img_y, image=self.tk_image, anchor=tk.CENTER)
        self.redraw_circles()

    def zoom(self, factor):
        """ Zooms while keeping position centered """
        if not self.image:
            return

        old_zoom = self.zoom_factor
        self.zoom_factor *= factor

        self.offset_x -= (self.offset_x * (self.zoom_factor - old_zoom))
        self.offset_y -= (self.offset_y * (self.zoom_factor - old_zoom))

        self.display_image()

    def mouse_zoom(self, event):
        """ Handles zooming with mouse scroll, supporting Linux """
        if event.delta > 0 or event.num == 4:  # Scroll Up
            self.zoom(1.1)
        elif event.delta < 0 or event.num == 5:  # Scroll Down
            self.zoom(0.9)

    def reset_view(self):
        """ Resets the zoom and panning """
        self.zoom_factor = 1.0
        self.offset_x, self.offset_y = 0, 0
        self.display_image()

    def start_pan(self, event):
        """ Starts panning & records click time """
        self.start_x, self.start_y = event.x, event.y
        self.start_time = time.time()  # Record time when button is pressed

    def pan(self, event):
        """ Moves the image while tracking true offset values """
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.offset_x += dx
        self.offset_y += dy
        self.start_x, self.start_y = event.x, event.y

        self.display_image()

    def place_circle(self, event):
        """ Places a circle on left-click **ONLY** if it was a quick tap """
        if not self.image:
            return

        elapsed_time = time.time() - self.start_time  # Check how long the button was held
        if elapsed_time > 0.2:  # If held longer than 0.2s, ignore it
            return

        if len(self.circles) >= 2:
            return  # Limit to 2 circles

        # Convert canvas coordinates to image pixel coordinates
        image_x = (event.x - self.img_x + (self.original_width / 2)) / self.zoom_factor
        image_y = (event.y - self.img_y + (self.original_height / 2)) / self.zoom_factor

        image_x = int(max(0, min(self.original_width - 1, image_x)))
        image_y = int(max(0, min(self.original_height - 1, image_y)))

        self.circles.append((image_x, image_y))
        print(f"Circle at Image Pixels: ({image_x}, {image_y})")

        self.redraw_circles()

    def remove_circle(self, event):
        """ Removes the last placed circle on right-click """
        if not self.circles:
            return

        self.circles.pop()
        self.redraw_circles()

    def redraw_circles(self):
        """ Redraws circles and square """
        self.canvas.delete("circle", "square")

        for x, y in self.circles:
            canvas_x = self.img_x - (self.original_width / 2) + (x * self.zoom_factor)
            canvas_y = self.img_y - (self.original_height / 2) + (y * self.zoom_factor)
            self.canvas.create_oval(canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5, outline="red", width=2, tags="circle")

        if len(self.circles) == 2:
            self.draw_square()

        self.update_confirm_button()

    def draw_square(self):
        """ Draws a square using the two placed circles """
        if len(self.circles) != 2:
            return

        x1, y1 = self.circles[0]
        x2, y2 = self.circles[1]

        self.canvas.create_rectangle(
            self.img_x - (self.original_width / 2) + (x1 * self.zoom_factor),
            self.img_y - (self.original_height / 2) + (y1 * self.zoom_factor),
            self.img_x - (self.original_width / 2) + (x2 * self.zoom_factor),
            self.img_y - (self.original_height / 2) + (y2 * self.zoom_factor),
            outline="blue", width=2, tags="square"
        )

    def update_confirm_button(self):
        """ Enables confirm button only when 2 circles are present """
        self.confirm_button.config(state=tk.NORMAL if len(self.circles) == 2 else tk.DISABLED)

    def confirm_selection(self):
        """ Prints the confirmed square coordinates """
        print(f"Confirmed Square: {self.circles[0]} -> {self.circles[1]}")

    def update_mouse_coordinates(self, event):
        """ Updates the status bar with mouse coordinates in image pixels """
        if not self.image:
            self.status_bar.config(text="Mouse: (---, ---)")
            return

        image_x = (event.x - self.img_x + (self.original_width / 2)) / self.zoom_factor
        image_y = (event.y - self.img_y + (self.original_height / 2)) / self.zoom_factor

        if 0 <= image_x < self.original_width and 0 <= image_y < self.original_height:
            self.status_bar.config(text=f"Mouse: ({int(image_x)}, {int(image_y)})")
        else:
            self.status_bar.config(text="Mouse: Outside Image")