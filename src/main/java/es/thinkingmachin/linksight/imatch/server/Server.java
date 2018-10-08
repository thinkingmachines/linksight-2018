package es.thinkingmachin.linksight.imatch.server;

import de.siegmar.fastcsv.writer.CsvAppender;
import de.siegmar.fastcsv.writer.CsvWriter;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.ReferenceDataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.matchers.DatasetMatcher;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeAddressMatcher;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeReference;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.LinkedList;
import java.util.List;

public class Server {

    // Reference
    private static ReferenceDataset referenceDataset = new ReferenceDataset(
            "data/psgc-locations.csv",
            new String[]{"bgy", "municity", "prov"},
            "code",
            "candidate_terms"
    );

    private static Dataset dataset = new Dataset(
            "data/lgu201.csv",
            new String[]{"LOCATION", "citymun_m", "province_m"}
    );

    public static void main(String[] args) throws Exception {
        TreeReference reference = new TreeReference(referenceDataset);
        DatasetMatcher matcher = new DatasetMatcher(new TreeAddressMatcher(reference));

        List<ReferenceMatch> matches = matcher.getTopMatches(dataset);
        int allCount = 0;
        int nullCount = 0;
        for (ReferenceMatch match : matches) {
            if (match == null) nullCount++;
            allCount++;
        }
        System.out.println("All count: "+allCount);
        System.out.println("Null count: "+nullCount);
        writeOutput(matches, "output/lgu201.csv");
    }

    private static void writeOutput(List<ReferenceMatch> matches, String filePath) throws IOException {
        File file = new File(filePath);
        CsvWriter csvWriter = new CsvWriter();

        try (CsvAppender csvAppender = csvWriter.append(file, StandardCharsets.UTF_8)) {
            // Header
            csvAppender.appendLine("brgy", "municity", "prov", "score");
            // Values
            for (ReferenceMatch match: matches) {
                String[] terms;
                if (match == null) {
                    terms = new String[0];
                } else {
                    assert match.referenceRow != null;
                    assert match.referenceRow.stdAddress != null;
                    terms = match.referenceRow.stdAddress.terms;
                }
                assert terms.length <= 3;
                for (int i = 0; i < 3 - terms.length; i++) {
                    csvAppender.appendField("");
                }
                for (String term : terms) {
                    csvAppender.appendField(term);
                }
                if (match != null) {
                    csvAppender.appendField(String.format("%.2f", match.score));
                } else {
                    csvAppender.appendField("");
                }
                csvAppender.endLine();
            }
        }
    }
}
