package es.thinkingmachin.linksight.imatch.matcher.core;

/**
 * This class serves as a utility class for the psgc field.
 * It allows the program to get the parent psgc and the level
 * where the psgc is located.
 */
public class Psgc {

    public static final long NONE = -1;
    private static long[] levels = new long[]{10000000, 100000, 1000, 1};

    /**
     * Computes for the parent psgc of the given psgc.
     * @param psgc the psgc being processed
     * @return the parent psgc
     */
    public static long getParent(long psgc) {
        int level = getLevel(psgc);
        if (level == 0) return NONE;
        long parent = levels[level - 1];
        return (psgc / parent) * parent;
    }

    /**
     * Computes for the level the current psgc is in.
     * @param psgc the psgc being processed
     * @return the level where the psgc belongs
     */
    public static int getLevel(long psgc) {
        for (int i = 0; i < levels.length; i++) {
            if (psgc % levels[i] == 0) return i;
        }
        throw new Error("Bad PSGC: "+psgc);
    }

    /**
     * Computes for the level the current psgc is in.
     * @param psgc the psgc being processed in string format
     * @return the level where the psgc belongs
     */
    public static int getLevel(String psgc) {
        return getLevel(Long.parseLong(psgc));
    }
}
