#!/usr/bin/env python
# coding: utf-8

# In[39]:


# Import necessary libraries
import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter.messagebox 

# Define a class for the Seam Carving App
class Seam:
    def __init__(self, root):
        # Initialize the Tkinter root window
        self.root = root
        self.root.title("Masters in Software Engineering Seam Carving App")

        # Initialize variables
        self.input_image = None
        self.output_image = None
        self.num_seams_var = tk.StringVar()
        self.num_seams_var.set("20")
        self.paused = False

        # Create widgets for the UI
        self.image_frame = tk.Frame(root, width=600, height=400, bg='ivory')
        self.image_label = tk.Label(self.image_frame)
        self.load_button = tk.Button(root, text="Select Image", command=self.load_image, bg='turquoise')
        self.num_seams_label = tk.Label(root, text="Enter Number of Seams:")
        self.num_seams_entry = tk.Entry(root, textvariable=self.num_seams_var)
        self.run_button = tk.Button(root, text="Perform Seam Carving", command=self.run_seam_carving, bg='turquoise')
        self.pause_button = tk.Button(root, text="Pause algorithm ", command=self.pause_seam_carving, bg='turquoise')
        self.resume_button = tk.Button(root, text="Resume Algorithm", command=self.resume_seam_carving,bg='turquoise')
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image, bg='turquoise')
        self.exit_button = tk.Button(root, text="Close Program", command=root.destroy, bg='turquoise')

        # Create a label for the hint
        self.hint_label = tk.Label(root, text="Enter number of seams")
        
        # Grid layout for widgets
        self.image_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.load_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.num_seams_label.grid(row=1, column=1, padx=10, pady=10)
        self.num_seams_entry.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        self.run_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        self.pause_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.resume_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.save_button.grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        self.exit_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Set resizing behavior for columns and rows
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(1, weight=1)

    # Method to load an image from the file system
    def load_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            # Read the selected image using OpenCV
            self.input_image = cv2.imread(file_path)
            # Display the loaded image
            self.display_the_image(self.input_image)

    # Method to display an image in the UI
    def display_the_image(self, image):
        if image is not None:
            #where we Convert the image from BGR to RGB
            #BGR "BLACK, GREEN, RED"
            #RGB "RED, GREE, BLUE"
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #where we Convert the image to a PIL Image
            image = Image.fromarray(image)
            # Create a PhotoImage from the PIL Image
            photo = ImageTk.PhotoImage(image=image)
            # Configure the image label to display the PhotoImage
            self.image_label.config(image=photo)
            self.image_label.image = photo
            # Pack the image label to fill the available space
            self.image_label.pack(fill="both", expand=True)

    # Method to perform seam carving based on user input
    def run_seam_carving(self):
        if self.input_image is not None:
            try:
                # Get the number of seams from the entry widget
                num_seams = int(self.num_seams_var.get())
                # Reset paused state
                self.paused = False
                # Perform seam carving on the input image
                self.output_image = self.seam_carving(self.input_image, num_seams)
                # Display the output image
                self.display_the_image(self.output_image)
            except ValueError:
                 tkinter.messagebox.showinfo("Error"," Please enter a valid integer for the number of seams.")
               

    # Method to save the output image
    def save_image(self):
        if self.output_image is not None:
            # Open a file dialog to select the save location and file name
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                # Save the original color image using PIL
                output_pil_image = Image.fromarray(cv2.cvtColor(self.output_image, cv2.COLOR_BGR2RGB))
                output_pil_image.save(file_path)
                # root window title and dimension 
                
            tkinter.messagebox.showinfo("Seamed Image saved Successfully", {file_path})
            

    # Method to calculate energy map of an image
    def energy_map(self, image):
        # where we Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # where we Calculate the gradient using Sobel operators
        dx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        dy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        # where we Calculate the gradient magnitude
        gradient_magnitude = np.sqrt(dx**2 + dy**2)
        return gradient_magnitude

    # Method to calculate cumulative energy map
    def cumulative_energy_map(self, energy_map):
        height, width = energy_map.shape
        #where we Initialize an array for the cumulative energy map
        cumulative_map = np.zeros_like(energy_map)

        #where we Calculate the cumulative energy map
        cumulative_map[0, :] = energy_map[0, :]
        for i in range(1, height):
            for j in range(width):
                if j == 0:
                    cumulative_map[i, j] = energy_map[i, j] + min(cumulative_map[i - 1, j], cumulative_map[i - 1, j + 1])
                elif j == width - 1:
                    cumulative_map[i, j] = energy_map[i, j] + min(cumulative_map[i - 1, j - 1], cumulative_map[i - 1, j])
                else:
                    cumulative_map[i, j] = energy_map[i, j] + min(cumulative_map[i - 1, j - 1], cumulative_map[i - 1, j], cumulative_map[i - 1, j + 1])

        return cumulative_map

    # Method to find the vertical seam with the minimum cumulative energy
    def find_vertical_seam(self, cumulative_map):
        height, width = cumulative_map.shape
        #where we Initialize an array for the vertical seam
        seam = np.zeros(height, dtype=np.int64)

        #where we Find the minimum index in the bottom row of the cumulative map
        min_index = np.argmin(cumulative_map[height - 1, :])
        seam[height - 1] = min_index

        # where we Trace the vertical seam from bottom to top
        for i in range(height - 2, -1, -1):
            if min_index == 0:
                min_index = np.argmin(cumulative_map[i, min_index:min_index + 2])
            elif min_index == width - 1:
                min_index = np.argmin(cumulative_map[i, min_index - 1:min_index + 1]) + min_index - 1
            else:
                min_index = np.argmin(cumulative_map[i, min_index - 1:min_index + 2]) + min_index - 1

            seam[i] = min_index

        return seam

    # Method to remove a vertical seam from the image
    def remove_vertical_seam(self, image, seam):
        height, width, _ = image.shape
        # Create a new image with one less column
        new_image = np.zeros((height, width - 1, 3), dtype=np.uint8)

        # Remove the pixels corresponding to the seam
        for i in range(height):
            new_image[i, :, :] = np.delete(image[i, :, :], seam[i], axis=0)

        return new_image

    # Method to perform seam carving on the image
    def seam_carving(self, image, num_seams):
        for _ in range(num_seams):
            # Check if paused
            while self.paused:
                self.root.update()

            # Calculate the energy map of the current image
            energy_map_image = self.energy_map(image)
            # Calculate the cumulative energy map
            cumulative_map = self.cumulative_energy_map(energy_map_image)
            # Find the vertical seam with the minimum cumulative energy
            seam = self.find_vertical_seam(cumulative_map)

            # Create a display image with the same color as the original
            display_the_image = np.copy(image)

            # Highlight the seam in red for visualization
            for i in range(image.shape[0]):
                display_the_image[i, seam[i], :] = [0, 0, 255]  # Mark the seam in red

            # Display the image with the highlighted seam
            self.display_the_image(display_the_image)
            # Update the Tkinter window to show the changes
            self.root.update()

            # Remove the vertical seam from the image
            image = self.remove_vertical_seam(image, seam)

        return image

    # Method to pause seam carving
    def pause_seam_carving(self):
        self.paused = True

    # Method to resume seam carving
    def resume_seam_carving(self):
        self.paused = False


# Main entry point
if __name__ == "__main__":
    # Create the Tkinter root window
    root = tk.Tk()
    # Create an instance of the SeamCarvingApp class
    app = Seam(root)
    # Start the Tkinter event loop
    root.mainloop()


# In[ ]:





# In[ ]:




