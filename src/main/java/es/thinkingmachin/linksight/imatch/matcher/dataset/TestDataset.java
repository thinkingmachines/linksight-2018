package es.thinkingmachin.linksight.imatch.matcher.dataset;

public class TestDataset extends Dataset {

    public final String correctPsgcField;
    public final String name;

    public TestDataset(String name, String csvPath, String[] dirtyLocFields, String correctPsgcField) {
        super(csvPath, dirtyLocFields);
        this.name = name;
        this.correctPsgcField = correctPsgcField;
    }

    public boolean hasCorrectField() {
        return correctPsgcField != null;
    }

    public static class BuiltIn {

        public static TestDataset FUZZY_200 = new TestDataset(
                "FUZZY_200",
                "data/linksight-testing-file-fuzzy-200.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );

        public static TestDataset HAPPY_PATH = new TestDataset(
                "HAPPY_PATH",
                "data/happy_path.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );

        public static TestDataset IMAN_TEST = new TestDataset(
                "IMAN_TEST",
                "data/iman-test.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );

        public static TestDataset SSS_CLEAN = new TestDataset(
                "SSS_TEST",
                "data/sss_clean2.csv",
                new String[]{"Barangay", "Municities", "Province"},
                null
        );
    }
}
