package es.thinkingmachin.linksight.imatch.matcher.matchers;

import com.google.common.base.Stopwatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

public class DatasetMatcher {

    private AddressMatcher addressMatcher;

    public DatasetMatcher(AddressMatcher addressMatcher) {
        this.addressMatcher = addressMatcher;
    }

    public ArrayList<ReferenceMatch> getTopMatches(Dataset dataset) throws IOException {
        System.out.println("Starting matching...");

        ArrayList<ReferenceMatch> matchedRows = new ArrayList<>();
        Stopwatch stopwatch = Stopwatch.createStarted();

        CsvParser parser = dataset.getCsvParser();
        CsvRow row;
        while ((row = parser.nextRow()) != null) {
            Address address = Address.fromCsvRow(row, dataset.locFields);
            ReferenceMatch match = addressMatcher.getTopMatch(address);
            matchedRows.add(match);
        }

        stopwatch.stop();
        System.out.println("Done. Matching took " + stopwatch.elapsed(TimeUnit.MILLISECONDS) + " msec.\n");
        return matchedRows;
    }
}
