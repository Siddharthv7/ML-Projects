import tkinter as tk
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model('traffic_classifier.h5')

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predict_traffic(model, img_path):
    img_array = load_and_preprocess_image(img_path)
    prediction = model.predict(img_array)
    return 'T' if prediction[0][0] > 0.5 else 'N'

# Function to draw the lanes and update their colors based on traffic conditions
def deslane(lane_statuses):
    # Initialize the main window
    root = tk.Tk()
    root.title("City Road Map")
    canvas = tk.Canvas(root, width=800, height=800, bg="grey")
    canvas.pack()

    # Function to draw a road (lane) with given coordinates and color
    def draw_road(x1, y1, x2, y2, color):
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    # Determine the colors for each lane based on traffic status
    colors = ["#e8776d" if status == 'T' else "#79db45" for status in lane_statuses]

    # Horizontal Lanes (4 Lanes)
    for i in range(4):
        draw_road(50, 150 + i * 100, 750, 200 + i * 100, colors[i])   # Draw lanes
        canvas.create_text(400, 130 + i * 100, text=f"Lane {i + 1}", fill="black", font=('Arial', 12, 'bold'))

    # Vertical Lanes (4 Lanes)
    for i in range(4):
        draw_road(150 + i * 150, 50, 200 + i * 150, 750, colors[i + 4])   # Draw lanes
        canvas.create_text(130 + i * 150, 400, text=f"Lane {i + 5}", fill="black", font=('Arial', 12, 'bold'), angle=90)

    root.mainloop()

# Example usage
if __name__ == "__main__":
    # List of image paths corresponding to each lane
    lane_image_paths = [
        'img1.jpg',
        'img2.jpg',
        'img3.jpg',
        'img4.jpg',
        'img5.jpg',
        'img6.jpg',
        'img7.jpg',
        'img8.jpg',
    ]

    # Predict traffic for each lane
    lane_statuses = [predict_traffic(model, img_path) for img_path in lane_image_paths]

    # Draw the lanes based on predicted traffic conditions
    deslane(lane_statuses)
