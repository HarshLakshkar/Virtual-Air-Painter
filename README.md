# Virtual Air-Painter using OpenCV
Virtual Air-Painter is an interactive application that allows users to create digital art by simply using hand gestures in the air. Using OpenCV and MediaPipe, this project leverages hand gesture recognition and computer vision to offer an innovative painting experience, eliminating the need for physical input devices like a mouse or stylus. Users can draw in the air, controlling brush sizes and styles through real-time gesture detection.

# Features:
Real-Time Hand Gesture Detection: Tracks and recognizes hand movements to create smooth and intuitive drawings.
Gesture-to-Action Mapping: Converts specific hand gestures into drawing commands (e.g., pointing for drawing, pinching for changing brush size).
Customizable Brushes: Users can switch between different brush styles and adjust the size for more precise control.
Interactive Painting Canvas: The virtual painting canvas responds dynamically to hand gestures in the air, offering a seamless drawing experience.

# Technologies Used:
OpenCV: For real-time computer vision, capturing and processing video input.
MediaPipe: For hand tracking and gesture recognition.
Python: The core programming language for implementing the logic and functionality.
Numpy: Used for mathematical operations on image data.

# How It Works:
The application uses a webcam to capture video input.
MediaPipe is employed to detect and track the user's hand in the video stream.
The hand's movements are mapped to actions, such as drawing, changing brush sizes, or erasing, based on the gestures.
The drawing is displayed in real-time on the screen, providing an immersive virtual painting experience.

# Installation:
Clone the repository:
git clone [https://github.com/HarshLakshkar/Virtual-Air-Painting.git]

# Install the required dependencies:

pip install opencv-python mediapipe numpy

# Run the application:
python air_painter.py

# Future Improvements:
Add support for multiple brush colors and textures.
Integrate voice commands for more intuitive controls.
Optimize for mobile or other platforms (e.g., VR/AR).
