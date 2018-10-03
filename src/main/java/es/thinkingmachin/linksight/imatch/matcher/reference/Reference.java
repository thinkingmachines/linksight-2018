package es.thinkingmachin.linksight.imatch.matcher.reference;

import com.google.common.base.Stopwatch;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import de.cxp.predict.PreDict;
import de.cxp.predict.api.PreDictSettings;
import de.cxp.predict.api.SuggestItem;
import de.cxp.predict.customizing.CommunityCustomization;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

public class Reference {

    public final PreDict predictModel;
    private final String csvPath;
    private final String[] locFields;
    private final String psgcField;
    private final String aliasField;
    public final ArrayList<ReferenceRow> rows = new ArrayList<>();

    public final HashMap<String, Set<ReferenceRow>> firstTermsCache = new HashMap<>();

    public Reference(String csvPath, String[] locFields, String psgcField, String aliasField) throws IOException {
        this.predictModel = createModel();
        this.csvPath = csvPath;
        this.locFields = locFields;
        this.psgcField = psgcField;
        this.aliasField = aliasField;
        init();
    }

    private void init() throws IOException {
        System.out.println("Building search index...");
        buildPredictIndex(csvPath);
    }

    private PreDict createModel() {
        PreDictSettings settings = new PreDictSettings();
        settings.accuracyLevel(PreDict.AccuracyLevel.maximum);
        CommunityCustomization custom = new CommunityCustomization(settings);
        return new PreDict(custom);
    }


    private void buildPredictIndex(String sourceCsv) throws IOException {
        Stopwatch stopwatch = Stopwatch.createStarted();
        File file = new File(sourceCsv);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        int i = 0;
        HashMap<Long, Address> allPsgc = new HashMap<>();
        try (CsvParser csvParser = csvReader.parse(file, StandardCharsets.UTF_8)) {
            CsvRow row;
            while ((row = csvParser.nextRow()) != null) {
                ReferenceRow referenceRow = ReferenceRow.fromCsvRow(row, locFields, psgcField, aliasField);
                addReferenceRow(referenceRow);
                allPsgc.putIfAbsent(referenceRow.psgc, referenceRow.stdAddress);
            }
        }
        for (Map.Entry<Long, Address> entry : allPsgc.entrySet()) {
            long psgc = entry.getKey();
            Address stdAddr = entry.getValue();
            if (stdAddr.minLevel == Interlevel.BARANGAY) {
                ReferenceRow extraRow = generateExtraReferenceRows(psgc, stdAddr);
                if (extraRow != null) addReferenceRow(extraRow);
            }
            addReferenceRow(new ReferenceRow(stdAddr, stdAddr, psgc));
        }
        stopwatch.stop();
        System.out.println("Done. Indexing took " + stopwatch.elapsed(TimeUnit.SECONDS) + " sec.\n");
    }

    private void addReferenceRow(ReferenceRow row) {
        // Add to list of es.thinkingmachin.linksight.imatch.matcher.reference rows
        rows.add(row);

        Address[] addresses = new Address[]{row.aliasAddress, row.stdAddress};
        for (Address addr : addresses) {
            // Index address terms
            for (String term : addr.terms) {
                predictModel.indexWord(term);
            }

            // Add address to first terms cache
            String firstTerm = addr.terms[0];
            String cleanTerm = predictModel.cleanIndexWord(firstTerm);

            if (!firstTermsCache.containsKey(cleanTerm)) {
                firstTermsCache.put(cleanTerm, new HashSet<>());
            }
            firstTermsCache.get(cleanTerm).add(row);
        }
    }

    private ReferenceRow generateExtraReferenceRows(long psgc, Address stdAddress){
        // Double second level -- e.g. Pangao-Ibaan,IBAAN,Batangas
        if (stdAddress.terms.length > 1) {
            String[] newTerms = stdAddress.terms.clone();
            newTerms[0] = newTerms[0] + " " + newTerms[1];
            Address newAddr = new Address(newTerms, stdAddress.minLevel);
            return new ReferenceRow(newAddr, stdAddress, psgc);
        }
        return null;
    }

    public Map<String, Double> getCandidatesDictionary(String searchTerm) {
        List<SuggestItem> suggestions = predictModel.lookup(searchTerm);
        return suggestions.stream()
                .collect(Collectors.toMap(s -> s.term, s -> s.proximity));
    }
}
