import streamlit as st
from PIL import Image
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Function to detect circles and draw them on the image
def detect_and_draw_circles(original_image, roi_coords):
    x1, y1, x2, y2 = roi_coords
    roi = original_image[y1:y2, x1:x2]
    
    # Convert ROI to grayscale and blur
    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Detect circles using Hough Circle Transform
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=20,
        param1=50,
        param2=30,
        minRadius=0,
        maxRadius=0
    )
    
    detected_circles = []
    output_image = original_image.copy()
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # Convert ROI coordinates to original image coordinates
            x, y, r = circle
            x_orig = x1 + x
            y_orig = y1 + y
            
            detected_circles.append((x_orig, y_orig, r))
            cv2.circle(output_image, (x_orig, y_orig), r, (0, 255, 0), 2)
    
    return detected_circles, output_image

# Streamlit app
st.title("Circle Detection App")

# Step 1: Image upload
uploaded_file = st.file_uploader("Upload a JPG image", type=["jpg"])

if uploaded_file is not None:
    # Load and prepare image
    image_pil = Image.open(uploaded_file)
    original_image = np.array(image_pil)
    orig_height, orig_width = original_image.shape[:2]
    
    # Step 2: Options selection
    option = st.selectbox("Select option", ["a", "b", "c"])
    
    if option == "a":
        # Step 3-4: ROI selection with scaled canvas
        display_width = 800
        scaling_factor = display_width / orig_width
        display_height = int(orig_height * scaling_factor)
        
        st.markdown("### Draw a rectangle to select region")
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.2)",
            stroke_width=2,
            stroke_color="#FF0000",
            background_image=image_pil.resize((display_width, display_height)),
            drawing_mode="rect",
            height=display_height,
            width=display_width,
            key="canvas"
        )
        
        # Process canvas results
        if canvas_result.json_data is not None:
            if len(canvas_result.json_data["objects"]) > 0:
                rect = canvas_result.json_data["objects"][0]
                
                # Convert coordinates to original scale
                left = rect["left"] / scaling_factor
                top = rect["top"] / scaling_factor
                width = rect["width"] / scaling_factor
                height = rect["height"] / scaling_factor
                
                x1, y1 = int(left), int(top)
                x2, y2 = int(left + width), int(top + height)
                
                # Validate coordinates
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(orig_width, x2), min(orig_height, y2)
                
                if x1 >= x2 or y1 >= y2:
                    st.error("Invalid region selected!")
                else:
                    # Step 5-7: Detect circles and process
                    circles, output_image = detect_and_draw_circles(original_image, (x1, y1, x2, y2))
                    
                    if circles:
                        st.success("Detected Circles (x, y, radius):")
                        for i, (x, y, r) in enumerate(circles, 1):
                            st.write(f"{i}. X: {x}, Y: {y}, Radius: {r}")
                        
                        # Step 7: Show output image
                        st.image(Image.fromarray(output_image), 
                                caption="Detected Circles", 
                                use_column_width=True)
                    else:
                        st.warning("No circles found in selected region!")
    else:
        st.info("Selected option b/c - No action required")
else:
    st.write("Please upload an image to begin")