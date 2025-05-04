import java.util.ArrayList;
import java.util.List;

public class World {
    private final List<Block> blocks = new ArrayList<>();

    public World(int width, int height, int depth) {
        generateFlatWorld(width, height, depth);
    }

    private void generateFlatWorld(int width, int height, int depth) {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                for (int z = 0; z < depth; z++) {
                    blocks.add(new Block(x, y, z));
                }
            }
        }
    }

    public List<Block> getBlocks() {
        return blocks;
    }
}
