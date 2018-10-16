package es.thinkingmachin.linksight.imatch.matcher.core;

public class Psgc {

    public static final long NONE = -1;
    private static long[] levels = new long[]{10000000, 100000, 1000, 1};

    public static long getParent(long psgc) {
        int level = getLevel(psgc);
        if (level == 0) return NONE;
        long parent = levels[level - 1];
        return (psgc / parent) * parent;
    }

    public static int getLevel(long psgc) {
        for (int i = 0; i < levels.length; i++) {
            if (psgc % levels[i] == 0) return i;
        }
        throw new Error("Bad PSGC: "+psgc);
    }

    public static int getLevel(String psgc) {
        return getLevel(Long.parseLong(psgc));
    }
}
