package es.thinkingmachin.linksight.imatch.matcher.dataset;

public class TestDataset extends Dataset {

    public final String correctPsgcField;

    public TestDataset(String csvPath, String[] dirtyLocFields, String correctPsgcField) {
        super(csvPath, dirtyLocFields);
        this.correctPsgcField = correctPsgcField;
    }

    public static class BuiltIn {

        public static TestDataset FUZZY_200 = new TestDataset(
                "data/linksight-testing-file-fuzzy-200.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );

        public static TestDataset HAPPY_PATH = new TestDataset(
                "data/happy_path.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );

        public static TestDataset IMAN_TEST = new TestDataset(
                "data/iman-test.csv",
                new String[]{"source_brgy", "source_municity", "source_prov"},
                "expected_psgc"

        );
    }
}
