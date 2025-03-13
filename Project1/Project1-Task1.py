import numpy as np
from PIL import Image

# Image size
width, height = 500, 500

# Viewport size and projection plane distance
viewport_size = 1
projection_plane_d = 1

# Scene definition (spheres)
spheres = [
    {"center": np.array([0, -1, 3]), "radius": 1, "color": (255, 0, 0)},  # Red Sphere
    {"center": np.array([2, 0, 4]), "radius": 1, "color": (0, 0, 255)},  # Blue Sphere
    {"center": np.array([-2, 0, 4]), "radius": 1, "color": (0, 255, 0)},  # Green Sphere
]

# Camera position
camera_position = np.array([0, 0, 0])

def canvas_to_viewport(x, y):
    """ Convert canvas coordinates to viewport coordinates """
    return np.array([
        x * viewport_size / width,
        y * viewport_size / height,
        projection_plane_d
    ])

def intersect_ray_sphere(origin, direction, sphere):
    """ Check if a ray intersects a sphere """
    center = sphere["center"]
    radius = sphere["radius"]

    OC = origin - center
    a = np.dot(direction, direction)
    b = 2 * np.dot(OC, direction)
    c = np.dot(OC, OC) - radius**2

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return float("inf")  # No intersection
    return (-b - np.sqrt(discriminant)) / (2*a)  # Closest intersection

# Create a blank image
img = Image.new("RGB", (width, height), "white")
pixels = img.load()

# Ray tracing loop
for x in range(width):
    for y in range(height):
        # Convert pixel coordinates to viewport
        viewport_x = (x - width/2)
        viewport_y = -(y - height/2)
        direction = canvas_to_viewport(viewport_x, viewport_y)
        direction = direction / np.linalg.norm(direction)  # Normalize

        closest_t = float("inf")
        pixel_color = (255, 255, 255)

        # Check intersection with each sphere
        for sphere in spheres:
            t = intersect_ray_sphere(camera_position, direction, sphere)
            if t < closest_t:
                closest_t = t
                pixel_color = sphere["color"]  # Set color of closest sphere

        # Draw the pixel
        pixels[x, y] = pixel_color

# Save and display
img.save("ray_traced_spheresTask1.png")
img.show()
