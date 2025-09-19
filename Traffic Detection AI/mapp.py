import tkinter as tk

# Function to draw the lanes and update their colors based on traffic conditions
def deslane(lane1_status, lane2_status, lane3_status, lane4_status,
            lane5_status, lane6_status, lane7_status, lane8_status):
    # Initialize the main window
    root = tk.Tk()
    root.title("City Road Map")
    canvas = tk.Canvas(root, width=800, height=800, bg="grey")
    canvas.pack()

    # Function to draw a road (lane) with given coordinates and color
    def draw_road(x1, y1, x2, y2, color):
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    # Determine the colors for each lane based on traffic status ('T' for Traffic, 'N' for No Traffic)
    color1 = "#e8776d" if lane1_status == 'T' else "#79db45"
    color2 = "#e8776d" if lane2_status == 'T' else "#79db45"
    color3 = "#e8776d" if lane3_status == 'T' else "#79db45"
    color4 = "#e8776d" if lane4_status == 'T' else "#79db45"
    color5 = "#e8776d" if lane5_status == 'T' else "#79db45"
    color6 = "#e8776d" if lane6_status == 'T' else "#79db45"
    color7 = "#e8776d" if lane7_status == 'T' else "#79db45"
    color8 = "#e8776d" if lane8_status == 'T' else "#79db45"

    # Horizontal Lanes (4 Lanes)
    draw_road(50, 150, 750, 200, color1)   # Lane 1 (Top-most horizontal lane)
    canvas.create_text(400, 130, text="Lane 1", fill="black", font=('Arial', 12, 'bold'))

    draw_road(50, 250, 750, 300, color2)   # Lane 2
    canvas.create_text(400, 230, text="Lane 2", fill="black", font=('Arial', 12, 'bold'))

    draw_road(50, 350, 750, 400, color3)   # Lane 3
    canvas.create_text(400, 330, text="Lane 3", fill="black", font=('Arial', 12, 'bold'))

    draw_road(50, 450, 750, 500, color4)   # Lane 4 (Bottom-most horizontal lane)
    canvas.create_text(400, 430, text="Lane 4", fill="black", font=('Arial', 12, 'bold'))

    # Vertical Lanes (4 Lanes)
    draw_road(150, 50, 200, 750, color5)   # Lane 5 (Left-most vertical lane)
    canvas.create_text(130, 400, text="Lane 5", fill="black", font=('Arial', 12, 'bold'), angle=90)

    draw_road(300, 50, 350, 750, color6)   # Lane 6
    canvas.create_text(280, 400, text="Lane 6", fill="black", font=('Arial', 12, 'bold'), angle=90)

    draw_road(450, 50, 500, 750, color7)   # Lane 7
    canvas.create_text(430, 400, text="Lane 7", fill="black", font=('Arial', 12, 'bold'), angle=90)

    draw_road(600, 50, 650, 750, color8)   # Lane 8 (Right-most vertical lane)
    canvas.create_text(580, 400, text="Lane 8", fill="black", font=('Arial', 12, 'bold'), angle=90)

    root.mainloop()

# Example usage:
if __name__ == "__main__":
    # Traffic conditions for lanes: 'T' for traffic, 'N' for no traffic
    deslane('T', 'N', 'T', 'N', 'N', 'T', 'T', 'N')  
    # Lanes 1, 3, 6, and 7 have traffic, others have no traffic
