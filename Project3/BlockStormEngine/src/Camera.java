import org.joml.*;

import java.lang.Math;

import static org.lwjgl.glfw.GLFW.*;

public class Camera {
    public Vector3f position;
    public float pitch; // Up/down
    public float yaw;   // Left/right

    private final float speed = 0.1f;
    private final float sensitivity = 0.2f;

    public Camera(Vector3f startPos) {
        this.position = startPos;
        this.pitch = 0;
        this.yaw = -90; // Facing down -Z
    }

    public Matrix4f getViewMatrix() {
        Vector3f front = getFront();
        Vector3f target = new Vector3f(position).add(front);
        return new Matrix4f().lookAt(position, target, new Vector3f(0, 1, 0));
    }

    public Vector3f getFront() {
        Vector3f front = new Vector3f();
        front.x = (float) Math.cos(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        front.y = (float) Math.sin(Math.toRadians(pitch));
        front.z = (float) Math.sin(Math.toRadians(yaw)) * (float) Math.cos(Math.toRadians(pitch));
        return front.normalize();
    }

    public void move(long window) {
        Vector3f front = getFront();
        Vector3f right = front.cross(new Vector3f(0, 1, 0), new Vector3f()).normalize();

        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
            position.add(new Vector3f(front).mul(speed));
        }
        if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS) {
            position.sub(new Vector3f(front).mul(speed));
        }
        if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS) {
            position.sub(new Vector3f(right).mul(speed));
        }
        if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS) {
            position.add(new Vector3f(right).mul(speed));
        }
    }

    public void handleMouse(float dx, float dy) {
        yaw += dx * sensitivity;
        pitch -= dy * sensitivity;

        // Limit up/down angle
        pitch = Math.max(-89.0f, Math.min(89.0f, pitch));
    }
}
