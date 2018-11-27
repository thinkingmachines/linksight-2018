package es.thinkingmachin.linksight.imatch.matcher.core;

public class Util {
    /**
     * Splits a term based on the defined delimiter.
     * @param term the location name being split
     * @return list of terms split
     */
    public static String[] splitTerm(String term) {
        String splitRegex = "[\\s@()&.?$+-]+";
        return term.split(splitRegex);
    }
}
