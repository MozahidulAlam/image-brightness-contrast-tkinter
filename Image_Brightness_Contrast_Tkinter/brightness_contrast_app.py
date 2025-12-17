# Import tkinter for GUI creation
import tkinter as tk

# Import dialogs and message boxes from tkinter
from tkinter import filedialog, messagebox

# Import Pillow modules for image handling inside Tkinter
from PIL import Image, ImageTk

# Import OpenCV for image processing
import cv2

# Import NumPy for numerical operations on images
import numpy as np


# Create a class for the Image Editor Application
class ImageEditorApp:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Image Brightness & Contrast Adjustment")
        self.root.geometry("900x600")

        # Store original image (unchanged)
        self.original_image = None

        # Store processed (modified) image
        self.processed_image = None

        # ---------------- BUTTON SECTION ----------------
        # Create a frame to hold buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # Button to load image
        tk.Button(
            btn_frame,
            text="Load Image",
            command=self.load_image,
            width=15
        ).grid(row=0, column=0, padx=5)

        # Button to save image
        tk.Button(
            btn_frame,
            text="Save Image",
            command=self.save_image,
            width=15
        ).grid(row=0, column=1, padx=5)

        # ---------------- SLIDER SECTION ----------------
        # Create a frame to hold sliders
        slider_frame = tk.Frame(root)
        slider_frame.pack(pady=10)

        # Brightness label
        tk.Label(slider_frame, text="Brightness").grid(row=0, column=0)

        # Brightness slider
        self.brightness_slider = tk.Scale(
            slider_frame,
            from_=-100,          # Minimum brightness
            to=100,              # Maximum brightness
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_image  # Call update_image on change
        )
        self.brightness_slider.set(0)  # Default brightness
        self.brightness_slider.grid(row=0, column=1, padx=10)

        # Contrast label
        tk.Label(slider_frame, text="Contrast").grid(row=1, column=0)

        # Contrast slider
        self.contrast_slider = tk.Scale(
            slider_frame,
            from_=10,            # Low contrast
            to=300,              # High contrast
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_image
        )
        self.contrast_slider.set(100)  # Default contrast (1.0)
        self.contrast_slider.grid(row=1, column=1, padx=10)

        # ---------------- IMAGE DISPLAY ----------------
        # Label to display image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=20)

    # ---------------- LOAD IMAGE FUNCTION ----------------
    def load_image(self):
        # Open file dialog to choose image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )

        # If no file selected, exit function
        if not file_path:
            return

        # Read image using OpenCV
        image = cv2.imread(file_path)

        # Convert BGR (OpenCV default) to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Store original image
        self.original_image = image

        # Copy image for processing
        self.processed_image = image.copy()

        # Display image
        self.show_image(self.processed_image)

    # ---------------- UPDATE IMAGE FUNCTION ----------------
    def update_image(self, event=None):
        # If image not loaded, do nothing
        if self.original_image is None:
            return

        # Get brightness value from slider
        brightness = self.brightness_slider.get()

        # Get contrast value and scale it
        contrast = self.contrast_slider.get() / 100.0

        # Convert image to float for calculations
        img = self.original_image.astype(np.float32)

        # Apply brightness and contrast formula
        # New Image = (Original Image × Contrast) + Brightness
        img = img * contrast + brightness

        # Clip values to valid range [0, 255]
        img = np.clip(img, 0, 255)

        # Convert back to unsigned 8-bit integer
        img = img.astype(np.uint8)

        # Save processed image
        self.processed_image = img

        # Display updated image
        self.show_image(self.processed_image)

    # ---------------- DISPLAY IMAGE FUNCTION ----------------
    def show_image(self, img):
        # Convert NumPy array to PIL image
        img_pil = Image.fromarray(img)

        # Resize image for GUI display
        img_pil = img_pil.resize((500, 350))

        # Convert PIL image to Tkinter format
        img_tk = ImageTk.PhotoImage(img_pil)

        # Update image label
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk  # Prevent garbage collection

    # ---------------- SAVE IMAGE FUNCTION ----------------
    def save_image(self):
        # If no image exists, show error
        if self.processed_image is None:
            messagebox.showerror("Error", "No image to save")
            return

        # Open save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )

        # Save image if path is selected
        if file_path:
            # Convert RGB back to BGR for OpenCV
            img_bgr = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)

            # Write image to disk
            cv2.imwrite(file_path, img_bgr)

            # Show success message
            messagebox.showinfo("Success", "Image saved successfully!")


# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    # Create main Tkinter window
    root = tk.Tk()

    # Create app object
    app = ImageEditorApp(root)

    # Start Tkinter event loop
    root.mainloop()
