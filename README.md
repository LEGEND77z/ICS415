#Ray Tracing from Scratch
Overview
This project is a simple ray tracer built using Python and Pillow (PIL). It simulates how light interacts with objects (spheres) in a 3D space and renders a 2D image.
#Features
✔️ Implements basic ray tracing
✔️ Renders spheres in 3D space
✔️ Uses Python & NumPy for calculations
✔️ Generates an image as output
#Installation & Setup
**Prerequisites**
Make sure you have Python 3.x installed. You also need the following libraries:

Pillow (for image creation)
NumPy (for mathematical calculations)
Installation Steps
Clone the repository
git clone https://github.com/LEGEND77z/ICS415
cd HW1
#Install dependencies
pip install -r requirements.txt
Run the script
python HW1.py
The output image will be saved as ray_traced_spheres.png.
How It Works
The script simulates rays from a camera towards objects (spheres).
If a ray hits a sphere, the pixel is colored accordingly.
If no sphere is hit, the pixel is white (background).
#Example Output
![ray_traced_spheres](https://github.com/user-attachments/assets/49d63b80-ab8a-47e9-b58f-d92ef90bd2fd)


