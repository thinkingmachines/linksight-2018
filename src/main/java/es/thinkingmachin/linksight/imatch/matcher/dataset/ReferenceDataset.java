package es.thinkingmachin.linksight.imatch.matcher.dataset;

public class ReferenceDataset extends Dataset{

    public final String psgcField;
    public final String aliasField;

    public ReferenceDataset(String csvPath, String[] locFields, String psgcField, String aliasField) {
        super(csvPath, locFields);
        this.psgcField = psgcField;
        this.aliasField = aliasField;
    }


}
