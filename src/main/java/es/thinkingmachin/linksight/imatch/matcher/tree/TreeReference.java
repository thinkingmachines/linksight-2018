package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.base.Stopwatch;
import com.google.common.collect.HashMultimap;
import com.google.common.collect.Ordering;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Psgc;
import es.thinkingmachin.linksight.imatch.matcher.core.Util;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.executor.ParallelExecutor;
import es.thinkingmachin.linksight.imatch.matcher.executor.SeriesExecutor;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.ListSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.CsvSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask;
import es.thinkingmachin.linksight.imatch.matcher.model.FuzzyStringMap;
import es.thinkingmachin.linksight.imatch.matcher.reference.PsgcRow;
import org.apache.commons.collections4.multiset.HashMultiSet;
import org.apache.commons.math3.util.Pair;

import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Set;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import static es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask.MatchesType.SINGLE;

/**
 * This class encapsulates the information about the reference address tree.
 * The contents of the tree is pulled from the PSGC dataset.
 * It also initializes the entrypoint for the reference tree and the
 * search indices of each node in the tree.
 */
public class TreeReference {

    public final AddressTreeNode root;
    public final AddressTreeNode entryPoint;

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
        this.entryPoint = AddressTreeNode.createRoot();
        initialize();
    }

    /**
     * Creates a PSGC tree and initializes the entrypoint, the root,
     * and the search indices for each node.
     * @throws IOException if psgc file is invalid
     */
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

        // Create entry point
        createEntryPoint();

        // Create search indices
        System.out.println("Creating search indices...");
        root.createSearchIndex();
        entryPoint.createSearchIndex();
        allNodes.values().forEach(AddressTreeNode::createSearchIndex);

        stopwatch.stop();
        System.out.println("Constructing tree reference took " + stopwatch.elapsed(TimeUnit.SECONDS) + " sec.");
    }

    /**
     * Creates an entry point to the reference address tree.
     * The entry point serves as a second root where its children
     * are all the provinces. The matching algorithm starts
     * searching at the entry point.
     */
    private void createEntryPoint() {
        for (AddressTreeNode node : allNodes.values()) {
            if (Psgc.getLevel(node.psgc) == 1) {    // Provinces
                entryPoint.addChild(node);
            }
        }
    }

    /**
     * Initializes an AddressTreeNode for a psgc row and adds it
     * to a map of all the nodes in the reference tree
     * @param row the psgc row
     */
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
