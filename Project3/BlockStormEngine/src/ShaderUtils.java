import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import static org.lwjgl.opengl.GL20.*;

public class ShaderUtils {
    public static int createShader(String vertexPath, String fragmentPath) {
        String vertexCode = readFile(vertexPath);
        String fragmentCode = readFile(fragmentPath);

        int vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, vertexCode);
        glCompileShader(vertexShader);
        checkCompileErrors(vertexShader, "VERTEX");

        int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, fragmentCode);
        glCompileShader(fragmentShader);
        checkCompileErrors(fragmentShader, "FRAGMENT");

        int shaderProgram = glCreateProgram();
        glAttachShader(shaderProgram, vertexShader);
        glAttachShader(shaderProgram, fragmentShader);
        glLinkProgram(shaderProgram);
        checkCompileErrors(shaderProgram, "PROGRAM");

        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);

        return shaderProgram;
    }

    private static String readFile(String path) {
        try {
            return new String(Files.readAllBytes(Paths.get(path)));
        } catch (IOException e) {
            throw new RuntimeException("Failed to load shader file: " + path);
        }
    }

    private static void checkCompileErrors(int shader, String type) {
        if (type.equals("PROGRAM")) {
            if (glGetProgrami(shader, GL_LINK_STATUS) == GL_FALSE) {
                throw new RuntimeException("Shader Program linking failed:\n" + glGetProgramInfoLog(shader));
            }
        } else {
            if (glGetShaderi(shader, GL_COMPILE_STATUS) == GL_FALSE) {
                throw new RuntimeException(type + " Shader compilation failed:\n" + glGetShaderInfoLog(shader));
            }
        }
    }
}
