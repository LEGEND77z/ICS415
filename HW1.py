import numpy as np
from PIL import Image

# Image size
width, height = 500, 500

# Viewport and projection settings
viewport_size = 1
projection_plane_d = 1
background_color = (255, 255, 255)  # White background

# Define scene objects (spheres)
spheres = [
    {"center": np.array([0, -1, 3]), "radius": 1, "color": (255, 0, 0), "specular": 500},  # Red
    {"center": np.array([2, 0, 4]), "radius": 1, "color": (0, 0, 255), "specular": 500},  # Blue
    {"center": np.array([-2, 0, 4]), "radius": 1, "color": (0, 255, 0), "specular": 10},  # Green
    {"center": np.array([0, -5001, 0]), "radius": 5000, "color": (255, 255, 0), "specular": 1000},  # Yellow big
]

# Define lights
lights = [
    {"type": "ambient", "intensity": 0.2},
    {"type": "point", "intensity": 0.6, "position": np.array([2, 1, 0])},
    {"type": "directional", "intensity": 0.2, "direction": np.array([1, 4, 4])}
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
    """ Find intersection of a ray with a sphere """
    center = sphere["center"]
    radius = sphere["radius"]

    OC = origin - center
    a = np.dot(direction, direction)
    b = 2 * np.dot(OC, direction)
    c = np.dot(OC, OC) - radius ** 2

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return float("inf"), float("inf")  # No intersection
    t1 = (-b - np.sqrt(discriminant)) / (2 * a)
    t2 = (-b + np.sqrt(discriminant)) / (2 * a)
    return t1, t2  # Return both intersections


def compute_lighting(P, N, V, specular):
    """ Compute lighting intensity at point P """
    intensity = 0.0

    for light in lights:
        if light["type"] == "ambient":
            intensity += light["intensity"]
        else:
            if light["type"] == "point":
                L = light["position"] - P
            else:  # Directional light
                L = light["direction"]

            L = L / np.linalg.norm(L)  # Normalize light direction

            # Diffuse reflection
            n_dot_l = np.dot(N, L)
            if n_dot_l > 0:
                intensity += light["intensity"] * n_dot_l / (np.linalg.norm(N) * np.linalg.norm(L))

            # Specular reflection
            if specular != -1:
                R = 2 * N * np.dot(N, L) - L  # Reflection vector
                r_dot_v = np.dot(R, V)
                if r_dot_v > 0:
                    intensity += light["intensity"] * (r_dot_v / (np.linalg.norm(R) * np.linalg.norm(V))) ** specular

    return min(intensity, 1)  # Clamp intensity to max 1


def trace_ray(O, D, t_min, t_max):
    """ Find closest sphere hit by the ray """
    closest_t = float("inf")
    closest_sphere = None

    for sphere in spheres:
        t1, t2 = intersect_ray_sphere(O, D, sphere)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere is None:
        return background_color  # No intersection, return white

    # Compute intersection point and normal
    P = O + closest_t * D
    N = P - closest_sphere["center"]
    N = N / np.linalg.norm(N)  # Normalize normal vector
    V = -D  # View direction

    # Compute color based on lighting
    intensity = compute_lighting(P, N, V, closest_sphere["specular"])
    color = np.array(closest_sphere["color"]) * intensity
    return tuple(color.astype(int))


# Create a blank image
img = Image.new("RGB", (width, height), background_color)
pixels = img.load()

# Ray tracing loop
for x in range(width):
    for y in range(height):
        # Convert pixel coordinates to viewport
        viewport_x = (x - width / 2)
        viewport_y = -(y - height / 2)
        direction = canvas_to_viewport(viewport_x, viewport_y)
        direction = direction / np.linalg.norm(direction)  # Normalize direction

        # Trace ray
        pixels[x, y] = trace_ray(camera_position, direction, 1, float("inf"))

# Save and display
img.save("ray_traced_spheres.png")
img.show()
