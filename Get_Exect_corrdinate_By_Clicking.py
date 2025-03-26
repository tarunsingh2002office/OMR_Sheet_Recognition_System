import cv2
import numpy as np

# Global variables for zoom and pan
scale = 1.0  # Zoom scale
dx, dy = 0, 0  # Pan offsets
image = None  # Global image reference

# Function to capture mouse click coordinates
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
        # Adjust coordinates based on zoom and pan
        adjusted_x = int((x - dx) / scale)
        adjusted_y = int((y - dy) / scale)
        print(f"Coordinates: ({adjusted_x}, {adjusted_y})")

# Function to update zoom and pan
def update_display(val):
    global scale, dx, dy, image

    # Get zoom level from trackbar
    scale = cv2.getTrackbarPos('Zoom', 'Image') / 10.0
    if scale < 0.1:
        scale = 0.1  # Avoid zero or negative zoom

    # Get pan offsets from trackbars
    dx = cv2.getTrackbarPos('Pan X', 'Image') - 100
    dy = cv2.getTrackbarPos('Pan Y', 'Image') - 100

    # Resize and display the image
    h, w = image.shape[:2]
    resized = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

    # Create a canvas to fit the panned view
    canvas = 255 * np.ones((h, w, 3), dtype=np.uint8)
    canvas_y, canvas_x = canvas.shape[:2]
    resized_h, resized_w = resized.shape[:2]

    # Get overlay coordinates
    y_start = max(-dy, 0)
    x_start = max(-dx, 0)
    y_end = min(canvas_y - dy, resized_h)
    x_end = min(canvas_x - dx, resized_w)

    canvas[max(dy, 0):max(dy, 0) + (y_end - y_start), max(dx, 0):max(dx, 0) + (x_end - x_start)] = \
        resized[y_start:y_end, x_start:x_end]

    # Display the updated canvas
    cv2.imshow('Image', canvas)

# Load the image
image_path = r"C:\Users\USER\Desktop\Tarun_Sing_Projects\OMR_Index_Complete_Template\files\batch_1\1.jpg"  # Replace with your image file path
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found.")
else:
    # Create a window
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

    # Create trackbars for zoom and pan
    cv2.createTrackbar('Zoom', 'Image', 10, 30, update_display)  # Zoom range 0.1x to 3.0x
    cv2.createTrackbar('Pan X', 'Image', 100, 200, update_display)  # Pan X range -100 to +100
    cv2.createTrackbar('Pan Y', 'Image', 100, 200, update_display)  # Pan Y range -100 to +100

    # Set the mouse callback function to get coordinates
    cv2.setMouseCallback('Image', get_coordinates)

    # Initialize the display
    update_display(0)

    # Wait until a key is pressed
    cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()
