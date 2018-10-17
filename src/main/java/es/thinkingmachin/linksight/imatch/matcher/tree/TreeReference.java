package es.thinkingmachin.linksight.imatch.matcher.tree;

import com.google.common.base.Stopwatch;
import com.google.common.collect.HashMultimap;
import com.google.common.collect.Ordering;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Psgc;
import es.thinkingmachin.linksight.imatch.matcher.core.Util;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;
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

        // Generate extra aliases
//        createExtraAliases();

        // Create search indices
        System.out.println("Creating search indices...");
        root.createSearchIndex();
        entryPoint.createSearchIndex();
        allNodes.values().forEach(AddressTreeNode::createSearchIndex);

        stopwatch.stop();
        System.out.println("Constructing tree reference took " + stopwatch.elapsed(TimeUnit.SECONDS) + " sec.\n");
    }

    private void createEntryPoint() {
        for (AddressTreeNode node : allNodes.values()) {
            if (Psgc.getLevel(node.psgc) == 1) {    // Provinces
                entryPoint.addChild(node);
            }
        }
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

    private void createExtraAliases() {
        HashMultimap<String, String> small = HashMultimap.create();
        for (AddressTreeNode node : allNodes.values()) {
            for (String alias : node.aliases) {
                // Debug
                String[] words = Util.splitTerm(alias);
                for (String word : words) {
                    if (word.length() <= 3) {
                        small.put(word, alias);
//                        System.out.println("Alias: " + alias + ", word: " + word);
                    }
                }
            }
//            HashMultimap<String, AddressTreeNode> possibleAliases = HashMultimap.create();
//            for (AddressTreeNode child : node.children) {
//                for (String alias : child.aliases) {
//                    String[] words = Util.splitTerm(alias);
//                    if (words.length == 1) continue;
//                    for (String word : words) {
//                        if (word.length() > 3) {
//                            possibleAliases.put(word, child);
//                        }
//                    }
//                }
//            }
//            for (String alias : possibleAliases.keySet()) {
//                Set<AddressTreeNode> nodes = possibleAliases.get(alias);
//                if (nodes.size() == 1) {
//                    AddressTreeNode child = nodes.iterator().next();
//                    System.out.println("Unique alias: "+alias+" from "+child.getOrigTerm());
//                }
//            }
        }
        List<Pair<String, Set<String>>> counts = small.keySet().stream()
                .map(item -> new Pair<>(item, small.get(item)))
                .sorted(Comparator.comparingInt(p -> -p.getValue().size()))
                .collect(Collectors.toList());
        for (Pair<String, Set<String>> p : counts) {
            System.out.print(p.getKey()+" ("+p.getValue().size()+"): ");
            Ordering.natural()
                    .greatestOf(p.getValue(), 5)
                    .forEach(s -> System.out.print(s+" | "));
            System.out.println();
        }
    }
}
