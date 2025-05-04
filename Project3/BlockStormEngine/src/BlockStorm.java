import org.joml.*;
import org.lwjgl.BufferUtils;
import org.lwjgl.glfw.*;
import org.lwjgl.opengl.*;

import java.lang.Math;
import java.nio.*;
import java.util.List;

import static org.lwjgl.glfw.Callbacks.*;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL15.*;
import static org.lwjgl.opengl.GL20.*;
import static org.lwjgl.opengl.GL30.*;
import static org.lwjgl.system.MemoryUtil.*;

public class BlockStorm {
    private long window;
    private int vaoID, vboID;
    private int shaderProgram;
    private int textureID;

    private World world;
    private Camera camera;
    private int transformLoc;

    private boolean leftClicked = false;
    private boolean rightClicked = false;
    private double lastMouseX, lastMouseY;
    private boolean firstMouse = true;

    private Matrix4f projectionMatrix;
    private Matrix4f viewMatrix;

    private final float[] cubeVertices = {
            // x, y, z      u, v
            // Back
            -0.5f, -0.5f, -0.5f, 0f, 0.33f,  0.5f, -0.5f, -0.5f, 1f, 0.33f,  0.5f,  0.5f, -0.5f, 1f, 0.66f,
            0.5f,  0.5f, -0.5f, 1f, 0.66f, -0.5f,  0.5f, -0.5f, 0f, 0.66f, -0.5f, -0.5f, -0.5f, 0f, 0.33f,
            // Front
            -0.5f, -0.5f,  0.5f, 0f, 0.33f,  0.5f, -0.5f,  0.5f, 1f, 0.33f,  0.5f,  0.5f,  0.5f, 1f, 0.66f,
            0.5f,  0.5f,  0.5f, 1f, 0.66f, -0.5f,  0.5f,  0.5f, 0f, 0.66f, -0.5f, -0.5f,  0.5f, 0f, 0.33f,
            // Left
            -0.5f,  0.5f,  0.5f, 0f, 0.66f, -0.5f,  0.5f, -0.5f, 1f, 0.66f, -0.5f, -0.5f, -0.5f, 1f, 0.33f,
            -0.5f, -0.5f, -0.5f, 1f, 0.33f, -0.5f, -0.5f,  0.5f, 0f, 0.33f, -0.5f,  0.5f,  0.5f, 0f, 0.66f,
            // Right
            0.5f,  0.5f,  0.5f, 0f, 0.66f,  0.5f,  0.5f, -0.5f, 1f, 0.66f,  0.5f, -0.5f, -0.5f, 1f, 0.33f,
            0.5f, -0.5f, -0.5f, 1f, 0.33f,  0.5f, -0.5f,  0.5f, 0f, 0.33f,  0.5f,  0.5f,  0.5f, 0f, 0.66f,
            // Bottom
            -0.5f, -0.5f, -0.5f, 0f, 0.00f,  0.5f, -0.5f, -0.5f, 1f, 0.00f,  0.5f, -0.5f,  0.5f, 1f, 0.33f,
            0.5f, -0.5f,  0.5f, 1f, 0.33f, -0.5f, -0.5f,  0.5f, 0f, 0.33f, -0.5f, -0.5f, -0.5f, 0f, 0.00f,
            // Top
            -0.5f,  0.5f, -0.5f, 0f, 1.00f,  0.5f,  0.5f, -0.5f, 1f, 1.00f,  0.5f,  0.5f,  0.5f, 1f, 0.66f,
            0.5f,  0.5f,  0.5f, 1f, 0.66f, -0.5f,  0.5f,  0.5f, 0f, 0.66f, -0.5f,  0.5f, -0.5f, 0f, 1.00f
    };

    public void run() {
        init();
        loop();
        cleanup();
    }

    private void init() {
        glfwInit();
        window = glfwCreateWindow(800, 600, "BlockStorm 3D Textured", NULL, NULL);
        glfwMakeContextCurrent(window);
        glfwSwapInterval(1);
        glfwShowWindow(window);
        GL.createCapabilities();

        vaoID = glGenVertexArrays();
        glBindVertexArray(vaoID);

        vboID = glGenBuffers();
        glBindBuffer(GL_ARRAY_BUFFER, vboID);
        FloatBuffer buffer = BufferUtils.createFloatBuffer(cubeVertices.length);
        buffer.put(cubeVertices).flip();
        glBufferData(GL_ARRAY_BUFFER, buffer, GL_STATIC_DRAW);

        int stride = 5 * Float.BYTES;
        glVertexAttribPointer(0, 3, GL_FLOAT, false, stride, 0);
        glEnableVertexAttribArray(0);
        glVertexAttribPointer(1, 2, GL_FLOAT, false, stride, 3 * Float.BYTES);
        glEnableVertexAttribArray(1);

        glEnable(GL_DEPTH_TEST);

        shaderProgram = ShaderUtils.createShader("shaders/vertexShader.glsl", "shaders/fragmentShader.glsl");
        transformLoc = glGetUniformLocation(shaderProgram, "transform");

        textureID = TextureUtils.loadTexture("textures/block_atlas.png");
        glBindTexture(GL_TEXTURE_2D, textureID);

        world = new World(10, 1, 10);
        camera = new Camera(new Vector3f(5, 5, 20));

        projectionMatrix = new Matrix4f().perspective((float) Math.toRadians(70), 800f / 600f, 0.1f, 100f);

        // Mouse
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
        glfwSetCursorPosCallback(window, (win, xpos, ypos) -> {
            if (firstMouse) {
                lastMouseX = xpos;
                lastMouseY = ypos;
                firstMouse = false;
            }
            float dx = (float) (xpos - lastMouseX);
            float dy = (float) (ypos - lastMouseY);
            lastMouseX = xpos;
            lastMouseY = ypos;
            camera.handleMouse(dx, dy);
        });

        glfwSetMouseButtonCallback(window, (w, button, action, mods) -> {
            if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) leftClicked = true;
            if (button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS) rightClicked = true;
        });
    }

    private void loop() {
        while (!glfwWindowShouldClose(window)) {
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            glClearColor(0.5f, 0.75f, 1.0f, 1.0f);

            glUseProgram(shaderProgram);
            glBindVertexArray(vaoID);
            glBindTexture(GL_TEXTURE_2D, textureID);

            camera.move(window);
            if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
                glfwSetWindowShouldClose(window, true);
            }

            viewMatrix = camera.getViewMatrix();
            Matrix4f vp = new Matrix4f();
            projectionMatrix.mul(viewMatrix, vp);

            Raycaster.Hit hit = Raycaster.castRay(camera, world.getBlocks(), 5f, 0.05f);
            Block target = hit == null ? null : hit.block();

            // Break
            if (leftClicked && target != null) {
                target.isActive = false;
                leftClicked = false;
            }

            // Place
            if (rightClicked && hit != null) {
                Block b = hit.block();
                Vector3i n = hit.normal();

                // 🧠 Round to match destroy logic
                int bx = Math.round(b.x);
                int by = Math.round(b.y);
                int bz = Math.round(b.z);

                int nx = bx + n.x;
                int ny = by + n.y;
                int nz = bz + n.z;

                boolean occupied = world.getBlocks().stream()
                        .anyMatch(q -> q.x == nx && q.y == ny && q.z == nz);

                if (!occupied) world.getBlocks().add(new Block(nx, ny, nz));
                rightClicked = false;
            }

            // Draw
            for (Block b : world.getBlocks()) {
                if (!b.isActive) continue;
                Matrix4f model = new Matrix4f().translate(b.x, b.y, b.z);
                Matrix4f transform = new Matrix4f(vp).mul(model);
                FloatBuffer fb = BufferUtils.createFloatBuffer(16);
                transform.get(fb);
                glUniformMatrix4fv(transformLoc, false, fb);
                glDrawArrays(GL_TRIANGLES, 0, 36);
            }

            glfwSwapBuffers(window);
            glfwPollEvents();
        }
    }

    private void cleanup() {
        glDeleteVertexArrays(vaoID);
        glDeleteBuffers(vboID);
        glfwTerminate();
    }

    public static void main(String[] args) {
        new BlockStorm().run();
    }
}
