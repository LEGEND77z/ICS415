public class Block {
    public float x, y, z;
    public boolean isActive;

    public Block(float x, float y, float z) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.isActive = true; // can be turned off if destroyed
    }
}
