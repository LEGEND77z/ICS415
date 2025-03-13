import math
import random
import concurrent.futures
import numpy as np
from PIL import Image

# -----------------------------------------------------
# Vector utilities (Vec3)
# -----------------------------------------------------
class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.x * t.x, self.y * t.y, self.z * t.z)
        else:
            return Vec3(self.x * t, self.y * t, self.z * t)
    __rmul__ = __mul__

    def __truediv__(self, t):
        return Vec3(self.x / t, self.y / t, self.z / t)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        return self / self.length()

# -----------------------------------------------------
# Ray class
# -----------------------------------------------------
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def at(self, t):
        return self.origin + self.direction * t

# -----------------------------------------------------
# Material system
# -----------------------------------------------------
def reflect(v, n):
    return v - n * (2 * v.dot(n))

def refract(uv, n, etai_over_etat):
    cos_theta = min((-uv).dot(n), 1.0)
    r_out_perp = etai_over_etat * (uv + n * cos_theta)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.dot(r_out_perp))) * n
    return r_out_perp + r_out_parallel

def schlick(cosine, ref_idx):
    r0 = (1 - ref_idx) / (1 + ref_idx)
    r0 = r0 * r0
    return r0 + (1 - r0) * ((1 - cosine) ** 5)

class Material:
    def scatter(self, ray_in, hit_record):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in, hit_record):
        scatter_direction = hit_record.normal + random_unit_vector()
        if near_zero(scatter_direction):
            scatter_direction = hit_record.normal
        scattered = Ray(hit_record.p, scatter_direction)
        attenuation = self.albedo
        return (True, scattered, attenuation)

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, ray_in, hit_record):
        reflected = reflect(ray_in.direction.normalize(), hit_record.normal)
        scattered = Ray(hit_record.p, reflected + self.fuzz * random_in_unit_sphere())
        attenuation = self.albedo
        return (scattered.direction.dot(hit_record.normal) > 0, scattered, attenuation)

class Dielectric(Material):
    def __init__(self, index_of_refraction):
        self.ir = index_of_refraction

    def scatter(self, ray_in, hit_record):
        attenuation = Vec3(1.0, 1.0, 1.0)
        ref_ratio = (1.0 / self.ir) if hit_record.front_face else self.ir
        unit_direction = ray_in.direction.normalize()
        cos_theta = min((-unit_direction).dot(hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
        cannot_refract = ref_ratio * sin_theta > 1.0
        if cannot_refract or schlick(cos_theta, ref_ratio) > random.random():
            direction = reflect(unit_direction, hit_record.normal)
        else:
            direction = refract(unit_direction, hit_record.normal, ref_ratio)
        scattered = Ray(hit_record.p, direction)
        return (True, scattered, attenuation)

# -----------------------------------------------------
# Helper functions for random directions
# -----------------------------------------------------
def random_in_unit_sphere():
    while True:
        p = Vec3(random.random()*2 - 1, random.random()*2 - 1, random.random()*2 - 1)
        if p.dot(p) < 1.0:
            return p

def random_unit_vector():
    a = 2 * math.pi * random.random()
    z = random.random()*2 - 1
    r = math.sqrt(1 - z*z)
    return Vec3(r * math.cos(a), r * math.sin(a), z)

def near_zero(v):
    s = 1e-8
    return (abs(v.x) < s) and (abs(v.y) < s) and (abs(v.z) < s)

# -----------------------------------------------------
# Sphere and HitRecord
# -----------------------------------------------------
class HitRecord:
    def __init__(self):
        self.p = None
        self.normal = None
        self.t = 0
        self.front_face = True
        self.material = None

    def set_face_normal(self, ray, outward_normal):
        self.front_face = ray.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else outward_normal * -1

class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, ray, t_min, t_max, rec):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        half_b = oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False
        sqrt_d = math.sqrt(discriminant)
        root = (-half_b - sqrt_d) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrt_d) / a
            if root < t_min or root > t_max:
                return False
        rec.t = root
        rec.p = ray.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(ray, outward_normal)
        rec.material = self.material
        return True

# -----------------------------------------------------
# Hittable list
# -----------------------------------------------------
class HittableList:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def hit(self, ray, t_min, t_max, rec):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max
        for obj in self.objects:
            if obj.hit(ray, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material
        return hit_anything

# -----------------------------------------------------
# Camera
# -----------------------------------------------------
def random_in_unit_disk():
    while True:
        p = Vec3(random.random()*2 - 1, random.random()*2 - 1, 0)
        if p.dot(p) < 1:
            return p

class Camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist):
        theta = math.radians(vfov)
        h = math.tan(theta/2)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self.w = (lookfrom - lookat).normalize()
        self.u = vup.cross(self.w).normalize()
        self.v = self.w.cross(self.u)

        self.origin = lookfrom
        self.horizontal = self.u * (viewport_width * focus_dist)
        self.vertical = self.v * (viewport_height * focus_dist)
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - self.w * focus_dist
        self.lens_radius = aperture / 2

    def get_ray(self, s, t):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x + self.v * rd.y
        return Ray(
            self.origin + offset,
            (self.lower_left_corner + self.horizontal * s + self.vertical * t - self.origin - offset)
        )

# -----------------------------------------------------
# Ray color function (recursive)
# -----------------------------------------------------
def ray_color(ray, world, depth):
    if depth <= 0:
        return Vec3(0, 0, 0)
    rec = HitRecord()
    if world.hit(ray, 0.001, math.inf, rec):
        scattered_ok, scattered, attenuation = rec.material.scatter(ray, rec)
        if scattered_ok:
            return attenuation * ray_color(scattered, world, depth - 1)
        return Vec3(0, 0, 0)
    else:
        unit_direction = ray.direction.normalize()
        t = 0.5 * (unit_direction.y + 1.0)
        return (Vec3(1.0, 1.0, 1.0) * (1.0 - t)) + (Vec3(0.5, 0.7, 1.0) * t)

# -----------------------------------------------------
# Scene generation
# -----------------------------------------------------
def random_scene():
    world = HittableList()

    # Ground
    ground_material = Lambertian(Vec3(0.5, 0.5, 0.5))
    world.add(Sphere(Vec3(0, -1000, 0), 1000, ground_material))

    # Random small spheres
    for a in range(-11, 12):
        for b in range(-11, 12):
            choose_mat = random.random()
            center = Vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if (center - Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = Vec3(random.random() * random.random(),
                                  random.random() * random.random(),
                                  random.random() * random.random())
                    world.add(Sphere(center, 0.2, Lambertian(albedo)))
                elif choose_mat < 0.95:
                    albedo = Vec3(random.uniform(0.5, 1),
                                  random.uniform(0.5, 1),
                                  random.uniform(0.5, 1))
                    fuzz = random.uniform(0, 0.5)
                    world.add(Sphere(center, 0.2, Metal(albedo, fuzz)))
                else:
                    world.add(Sphere(center, 0.2, Dielectric(1.5)))

    # Three main spheres
    world.add(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))
    world.add(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))))
    world.add(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))

    return world

# -----------------------------------------------------
# Process a single scanline (row) – for multiprocessing
# -----------------------------------------------------
def process_scanline(j, image_width, image_height, samples_per_pixel, max_depth, cam, world):
    row = []
    for i in range(image_width):
        pixel_color = Vec3(0, 0, 0)
        for s in range(samples_per_pixel):
            u = (i + random.random()) / (image_width - 1)
            v = (j + random.random()) / (image_height - 1)
            r = cam.get_ray(u, v)
            pixel_color += ray_color(r, world, max_depth)
        scale = 1.0 / samples_per_pixel
        r_val = math.sqrt(scale * pixel_color.x)
        g_val = math.sqrt(scale * pixel_color.y)
        b_val = math.sqrt(scale * pixel_color.z)
        ir = int(255.999 * clamp(r_val, 0.0, 0.999))
        ig = int(255.999 * clamp(g_val, 0.0, 0.999))
        ib = int(255.999 * clamp(b_val, 0.0, 0.999))
        row.append((ir, ig, ib))
    return j, row

def clamp(x, min_val, max_val):
    return max(min(x, max_val), min_val)

# -----------------------------------------------------
# Main rendering (with multiprocessing and countdown)
# -----------------------------------------------------
def main():
    # Image settings
    aspect_ratio = 3.0 / 2.0
    image_width = 600
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 50

    # World and Camera
    world = random_scene()
    lookfrom = Vec3(13, 2, 3)
    lookat = Vec3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1
    vfov = 20.0
    cam = Camera(lookfrom, lookat, vup, vfov, aspect_ratio, aperture, dist_to_focus)

    # Create image buffer as a NumPy array
    img_array = np.zeros((image_height, image_width, 3), dtype=np.uint8)
    total_scanlines = image_height
    remaining = total_scanlines

    print("Rendering with multiprocessing (countdown in remaining scanlines)...")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_scanline, j, image_width, image_height,
                                     samples_per_pixel, max_depth, cam, world)
                   for j in range(image_height)]
        for future in concurrent.futures.as_completed(futures):
            j, row = future.result()
            img_array[image_height - 1 - j, :] = row
            remaining -= 1
            print(f"Remaining scanlines: {remaining:3d}", end='\r')

    img = Image.fromarray(img_array, 'RGB')
    img.save("final_scene.png")
    print("\nDone! Saved to final_scene.png")

if __name__ == "__main__":
    random.seed(42)
    main()
