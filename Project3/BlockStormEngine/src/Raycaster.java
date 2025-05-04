import org.joml.*;

import java.lang.Math;
import java.util.List;

/** Simple voxel ray-cast. Returns the first block hit and which face was entered. */
public class Raycaster {

    /** A hit result:   block … the block that was hit
     *                  normal … the outward normal of the face (±1,0,0 …) */
    public record Hit(Block block, Vector3i normal) {}

    public static Hit castRay(Camera cam,
                              List<Block> blocks,
                              float maxDist,
                              float step)
    {
        Vector3f origin = new Vector3f(cam.position);
        Vector3f dir    = cam.getFront().normalize();

        // keep previous sample so we can see which axis changed first
        Vector3f prev = new Vector3f(origin);

        for (float t = 0; t < maxDist; t += step) {
            Vector3f p = new Vector3f(dir).mul(t).add(origin);

            for (Block b : blocks) {
                if (!b.isActive) continue;
                if (inside(p, b)) {

                    // which axis did we cross between prev and p?
                    Vector3f delta = new Vector3f(p).sub(prev);
                    int nx = Math.abs(delta.x) > Math.abs(delta.y) && Math.abs(delta.x) > Math.abs(delta.z)
                            ? (delta.x > 0 ? 1 : -1) : 0;
                    int ny = (nx == 0 && Math.abs(delta.y) > Math.abs(delta.z))
                            ? (delta.y > 0 ? 1 : -1) : 0;
                    int nz = (nx == 0 && ny == 0)
                            ? (delta.z > 0 ? 1 : -1) : 0;

                    return new Hit(b, new Vector3i(nx, ny, nz));
                }
            }
            prev.set(p);
        }
        return null;
    }

    private static boolean inside(Vector3f p, Block b) {
        return p.x > b.x-0.5f && p.x < b.x+0.5f &&
                p.y > b.y-0.5f && p.y < b.y+0.5f &&
                p.z > b.z-0.5f && p.z < b.z+0.5f;
    }
}
