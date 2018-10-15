package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.base.Stopwatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Psgc;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;
import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;
import es.thinkingmachin.linksight.imatch.matcher.reference.PsgcRow;

import java.io.IOException;
import java.util.HashMap;
import java.util.concurrent.TimeUnit;

public class TreeReference {

    public final AddressTreeNode root;

    private final PsgcDataset[] psgcDatasets;
    private final HashMap<Long, AddressTreeNode> allNodes = new HashMap<>();

    public static PsgcDataset DEFAULT_PSGC_DATASET = new PsgcDataset(
            "data/clean-psgc.csv",
            "location",
            "original",
            "code",
            "interlevel"
    );

    public static PsgcDataset EXTRA_PSGC_DATASET = new PsgcDataset(
            "data/extra-psgc.csv",
            "location",
            "original",
            "code",
            "interlevel"
    );

    public TreeReference(PsgcDataset[] psgcDatasets) throws IOException {
        this.psgcDatasets = psgcDatasets;
        this.root = AddressTreeNode.createRoot();
        initialize();
    }

    private void initialize() throws IOException {
        Stopwatch stopwatch = Stopwatch.createStarted();

        // Create PSGC tree
        System.out.println("Creating tree...");
        for (PsgcDataset psgcDataset : psgcDatasets) {
            try (CsvParser csvParser = psgcDataset.getCsvParser()) {
                CsvRow row;
                while ((row = csvParser.nextRow()) != null) {
                    addPsgcRow(PsgcRow.fromCsvRow(row, psgcDataset));
                }
            }
        }

        // Create search indices
        System.out.println("Creating search indices...");
        root.createSearchIndex();
        allNodes.values().forEach(AddressTreeNode::createSearchIndex);

        stopwatch.stop();
        System.out.println("Constructing tree reference took " + stopwatch.elapsed(TimeUnit.SECONDS) + " sec.\n");
    }

    private void addPsgcRow(PsgcRow row) {
        if (!allNodes.containsKey(row.psgc)) {  // Add new node
            long parentPsgc = Psgc.getParent(row.psgc);
            AddressTreeNode parentNode = (parentPsgc == Psgc.NONE) ? root : allNodes.get(parentPsgc);
            AddressTreeNode node = new AddressTreeNode(row.psgcStr, parentNode);
            allNodes.put(row.psgc, node);
            parentNode.addChild(node);
        }
        allNodes.get(row.psgc).addAlias(row.location, row.isOriginal);
    }
}
