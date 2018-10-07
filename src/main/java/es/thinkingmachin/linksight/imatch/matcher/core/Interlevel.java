package es.thinkingmachin.linksight.imatch.matcher.core;

public enum Interlevel {

    BARANGAY("bgy"),
    MUNICITY("municity"),
    PROVINCE("prov");

    public static final Interlevel[] indexed = Interlevel.values();
    public final String shortName;

    Interlevel(String shortName) {
        this.shortName = shortName;
    }

    public static Interlevel inferLevel(int numTerms) {
        return indexed[Math.max(indexed.length - numTerms, 0)];
    }
}
