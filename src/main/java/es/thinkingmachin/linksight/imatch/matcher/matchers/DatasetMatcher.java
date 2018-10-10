package es.thinkingmachin.linksight.imatch.matcher.matchers;

import com.google.common.base.Stopwatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import de.siegmar.fastcsv.writer.CsvAppender;
import de.siegmar.fastcsv.writer.CsvWriter;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.io.CsvOutput;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class DatasetMatcher {

    private final AddressMatcher addressMatcher;

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
        long duration = stopwatch.elapsed(TimeUnit.MILLISECONDS);
        System.out.println("Matching took " + (duration/1000.0) + " sec at "+ (matchedRows.size()*1000.0/duration) +" rows/sec.");
        return matchedRows;
    }

    public File getPossibleMatches(Dataset dataset) throws IOException {
        File outputFile = Files.createTempFile("imatch-out-", ".tmp").toFile();

        System.out.println("Starting matching...");
        Stopwatch stopwatch = Stopwatch.createStarted();

        CsvParser parser = dataset.getCsvParser();
        CsvWriter writer = new CsvWriter();
        CsvRow row;

        int i;
        try (CsvAppender csvAppender = writer.append(outputFile, StandardCharsets.UTF_8)) {
            CsvOutput csv = new CsvOutput(csvAppender);
            csv.writeHeaderRow();
            for (i = 0; (row = parser.nextRow()) != null; i++) {
                Address address = Address.fromCsvRow(row, dataset.locFields);
                if (address.terms.length == 0) continue; // Ignore blank rows
                long startTime = System.nanoTime();
                List<ReferenceMatch> matches = addressMatcher.getTopMatches(address, 4);
                double matchTime = (System.nanoTime() - startTime) / 1e9;
                for (ReferenceMatch match : matches) {
                    csv.writeRow(i, address, matchTime, match);
                }
            }
        }

        stopwatch.stop();
        long duration = stopwatch.elapsed(TimeUnit.MILLISECONDS);
        System.out.println("Matching took " + (duration/1000.0) + " sec at "+ (i*1000.0/duration) +" rows/sec.");
        return outputFile;
    }
}
