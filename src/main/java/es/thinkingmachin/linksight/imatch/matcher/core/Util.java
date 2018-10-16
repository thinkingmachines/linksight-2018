package es.thinkingmachin.linksight.imatch.matcher.core;

public class Util {
    public static String[] splitTerm(String term) {
        String splitRegex = "[\\s@&.?$+-]+";
        return term.split(splitRegex);
    }
}
