package es.thinkingmachin.linksight.imatch.matcher.core;

public class DatasetInfo {

    public final String csvPath;
    public final String[] locFields;
    public final String psgcField;
    public final String aliasField;

    public DatasetInfo(String csvPath, String[] locFields, String psgcField, String aliasField) {
        this.csvPath = csvPath;
        this.locFields = locFields;
        this.psgcField = psgcField;
        this.aliasField = aliasField;
    }
}
