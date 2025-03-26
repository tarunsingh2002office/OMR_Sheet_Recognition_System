import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

def detect_circles(image, dp=1.2, min_dist=20, param1=50, param2=30, min_radius=17, max_radius=17):
    """
    Detect circles in a grayscale image using HoughCircles.
    Returns a list of circles with (x, y, r) coordinates.
    """
    circles = cv2.HoughCircles(
        image, cv2.HOUGH_GRADIENT, dp, minDist=min_dist,
        param1=param1, param2=param2, minRadius=min_radius, maxRadius=max_radius
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return circles[0, :]
    else:
        return []

def main():
    st.title("Circle Detection in a Selected Region")
    
    # Step 1: Upload image
    uploaded_file = st.file_uploader("Upload a JPG image", type=["jpg", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Step 2: Ask for options a, b, c
        option = st.radio("Select an option", ("a", "b", "c"))
        
        if option == "a":
            st.write("Option A selected: Please draw a rectangle to select the region in the image.")
            # Step 3: Open image in Streamlit using drawable canvas
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=3,
                stroke_color="#FF0000",
                background_color="#eee",
                background_image=Image.fromarray(image_rgb),
                update_streamlit=True,
                height=image_rgb.shape[0],
                width=image_rgb.shape[1],
                drawing_mode="rect",
                key="canvas",
            )
            
            # Once the user draws a rectangle, process it
            if canvas_result.json_data is not None:
                objects = canvas_result.json_data.get("objects", [])
                if objects:
                    rect = objects[0]
                    left = int(rect.get("left", 0))
                    top = int(rect.get("top", 0))
                    width_rect = int(rect.get("width", 0))
                    height_rect = int(rect.get("height", 0))
                    
                    st.write(f"Selected region - Left: {left}, Top: {top}, Width: {width_rect}, Height: {height_rect}")
                    
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    selected_region = gray[top:top+height_rect, left:left+width_rect]
                    
                    circles = detect_circles(selected_region)
                    
                    output_image = image_rgb.copy()
                    circle_data = []
                    
                    if circles is not None and len(circles) > 0:  # Modified condition
                        for (x, y, r) in circles:
                            full_x = x + left
                            full_y = y + top
                            circle_data.append({"x": int(full_x), "y": int(full_y), "r": int(r)})
                            cv2.circle(output_image, (full_x, full_y), r, (0, 255, 0), 2)
                    
                    st.write("Detected circles (with coordinates in the full image):")
                    st.write(circle_data)
                    st.image(output_image, caption="Detected circles", use_column_width=True)
        else:
            st.write("Option b or c selected, nothing to do.")

if __name__ == '__main__':
    main()