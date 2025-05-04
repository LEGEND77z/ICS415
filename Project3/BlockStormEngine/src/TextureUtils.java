import org.lwjgl.stb.STBImage;
import java.nio.ByteBuffer;
import java.nio.IntBuffer;
import static org.lwjgl.opengl.GL11.*;
import static org.lwjgl.opengl.GL13.*;
import static org.lwjgl.opengl.GL30.*;
import org.lwjgl.system.MemoryStack;

public class TextureUtils {
    public static int loadTexture(String path) {
        int width, height;
        ByteBuffer image;

        IntBuffer w = MemoryStack.stackMallocInt(1);
        IntBuffer h = MemoryStack.stackMallocInt(1);
        IntBuffer channels = MemoryStack.stackMallocInt(1);

        STBImage.stbi_set_flip_vertically_on_load(true);
        image = STBImage.stbi_load(path, w, h, channels, 4);
        if (image == null) {
            throw new RuntimeException("Failed to load image: " + STBImage.stbi_failure_reason());
        }

        width = w.get(0);
        height = h.get(0);

        int textureID = glGenTextures();
        glBindTexture(GL_TEXTURE_2D, textureID);
        // keep the WRAP lines if you already added them
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

// 🔸 use nearest-neighbour for both min and mag:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

        // ✅ Add these lines RIGHT HERE after glBindTexture:
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);

        // Load texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                GL_RGBA, GL_UNSIGNED_BYTE, image);
        glGenerateMipmap(GL_TEXTURE_2D);

        STBImage.stbi_image_free(image);
        return textureID;
    }
}
