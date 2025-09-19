import turtle

# Define constants for the clipping region
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

# Clipping window boundaries
x_min, y_min = -200, -200
x_max, y_max = 200, 200

def get_outcode(x, y):
    """Determine the region code for a point."""
    code = 0
    if x < x_min:    # to the left of clipping window
        code |= LEFT
    elif x > x_max:  # to the right of clipping window
        code |= RIGHT
    if y < y_min:    # below the clipping window
        code |= BOTTOM
    elif y > y_max:  # above the clipping window
        code |= TOP
    return code

def cohen_sutherland_line_clip(x0, y0, x1, y1):
    """Clip the line segment from (x0, y0) to (x1, y1) using Cohen-Sutherland algorithm."""
    outcode0 = get_outcode(x0, y0)
    outcode1 = get_outcode(x1, y1)
    accept = False

    while True:
        if not (outcode0 | outcode1):  # Both points inside
            accept = True
            break
        elif outcode0 & outcode1:  # Both points outside
            break
        else:  # Some portion of the line is within the clipping region
            # Choose one of the points outside
            if outcode0: 
                outcode_out = outcode0
            else:
                outcode_out = outcode1

            # Find the intersection point
            if outcode_out & TOP:  # Point is above the clipping window
                x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y = y_max
            elif outcode_out & BOTTOM:  # Point is below the clipping window
                x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y = y_min
            elif outcode_out & RIGHT:  # Point is to the right of the clipping window
                y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x = x_max
            elif outcode_out & LEFT:  # Point is to the left of the clipping window
                y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x = x_min

            # Replace outside point with intersection point
            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = get_outcode(x0, y0)
            else:
                x1, y1 = x, y
                outcode1 = get_outcode(x1, y1)

    if accept:  # Line accepted for drawing
        return (x0, y0, x1, y1)
    else:  # Line rejected
        return None

def draw_clipping_window():
    """Draw the clipping window."""
    turtle.penup()
    turtle.goto(x_min, y_min)
    turtle.pendown()
    turtle.goto(x_max, y_min)
    turtle.goto(x_max, y_max)
    turtle.goto(x_min, y_max)
    turtle.goto(x_min, y_min)

def get_user_lines():
    """Get lines from the user."""
    lines = []
    num_lines = int(input("Enter the number of lines you want to clip: "))
    for i in range(num_lines):
        print(f"Enter the coordinates for line {i + 1}:")
        x0 = float(input("x0: "))
        y0 = float(input("y0: "))
        x1 = float(input("x1: "))
        y1 = float(input("y1: "))
        lines.append((x0, y0, x1, y1))
    return lines

def main():
    # Get user-defined lines before starting Turtle
    lines = get_user_lines()
    
    # Start Turtle drawing
    turtle.speed(0)  # Fastest drawing speed
    draw_clipping_window()

    turtle.color("blue")
    for line in lines:
        x0, y0, x1, y1 = line
        clipped_line = cohen_sutherland_line_clip(x0, y0, x1, y1)
        if clipped_line:
            turtle.penup()
            turtle.goto(clipped_line[0], clipped_line[1])
            turtle.pendown()
            turtle.goto(clipped_line[2], clipped_line[3])

    turtle.done()

if __name__ == "__main__":
    main()
