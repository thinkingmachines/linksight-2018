package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.base.Stopwatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.dataset.ReferenceDataset;
import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceRow;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

public class TreeReference {

    private final ReferenceDataset referenceDataset;
    public final AddressTreeNode root;

    public TreeReference(ReferenceDataset referenceDataset) throws IOException {
        this.referenceDataset = referenceDataset;
        this.root = new AddressTreeNode(null, null);
        startIndexing();
    }

    private void startIndexing() throws IOException {
        Stopwatch stopwatch = Stopwatch.createStarted();
        File file = new File(referenceDataset.csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        try (CsvParser csvParser = csvReader.parse(file, StandardCharsets.UTF_8)) {
            CsvRow row;
            while ((row = csvParser.nextRow()) != null) {
                ReferenceRow referenceRow = ReferenceRow.fromCsvRow(row, referenceDataset);
                addReferenceRow(referenceRow);
            }
        }
        stopwatch.stop();
        System.out.println("Done. Indexing took " + stopwatch.elapsed(TimeUnit.SECONDS) + " sec.\n");
    }

    private void addReferenceRow(ReferenceRow row) {
        assert row.aliasAddress.terms.length == row.stdAddress.terms.length: "Unequal alias and std address: "+row.aliasAddress+" and "+row.stdAddress;
        int numTerms = row.aliasAddress.terms.length;

        AddressTreeNode currentNode = root;
        for (int i = numTerms - 1; i >= 0; i--) {
            assert numTerms <= 3: row.aliasAddress + " does not have <= 3 terms";
            Interlevel level = Interlevel.indexed[Interlevel.values().length - numTerms + i];
            String aliasTerm = row.aliasAddress.getTerm(i);
            String stdTerm = row.stdAddress.getTerm(i);
            assert stdTerm != null: "Std term is null: "+row.stdAddress;
            currentNode.addChild(level, stdTerm, aliasTerm);
            currentNode = currentNode.getChild(stdTerm);
            if (i == 0) currentNode.setReferenceRow(row);
        }
    }


}
