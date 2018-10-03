package es.thinkingmachin.linksight.imatch.matcher.core;

import es.thinkingmachin.linksight.imatch.matcher.filters.FirstLevelCandidatesFilter;
import com.google.common.base.Stopwatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.matchers.BasicMatcher;
import org.apache.commons.math3.stat.descriptive.rank.Percentile;
import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

public class MatchingJob {

    private final Reference reference;
    private final String csvPath;
    private final String[] locFields;
    public final ArrayList<ReferenceMatch> matchedRows = new ArrayList<>();
    private final BasicMatcher matcher;

    public MatchingJob(Reference reference, String csvPath, String[] locFields) {
        this.reference = reference;
        this.csvPath = csvPath;
        this.locFields = locFields;
        this.matcher = new BasicMatcher(reference);
    }

    public void start() throws IOException {
        System.out.println("Starting matching...");
        CsvParser csvParser = createCsvParser();
        CsvRow row;
        Stopwatch stopwatch = Stopwatch.createStarted();
        int i = 0;
        while ((row = csvParser.nextRow()) != null) {
            i++;
            Address address = Address.fromCsvRow(row, locFields);
            ReferenceMatch match = matcher.getTopMatch(address);
//            System.out.println("Candidate: "+address);
//            System.out.println("Match: "+match);
//            System.out.println("Matched? "+address.equals(match.address));
//            System.out.println("\n------------------------\n");
            matchedRows.add(match);
        }
        stopwatch.stop();
        long duration = stopwatch.elapsed(TimeUnit.MILLISECONDS);
        System.out.println("Matching took " + (duration/1000.0) + " sec at "+ (matchedRows.size()*1000.0/duration) +" rows/sec.");
//        System.out.println("Candidate gen: " +((double)BasicMatcher.METRIC_CANDIDATE_GEN_TOTAL)/BasicMatcher.METRIC_CANDIDATE_GEN_COUNT);
//        System.out.println("Top match: " + ((double)BasicMatcher.METRIC_TOP_MATCH_TOTAL)/BasicMatcher.METRIC_TOP_MATCH_COUNT);
//        System.out.println("First level gen: " + ((double) FirstLevelCandidatesFilter.METRIC_GENERATE_TOTAL)/FirstLevelCandidatesFilter.METRIC_GENERATE_COUNT);
//        System.out.println(BasicMatcher.METRIC_CANDIDATE_GEN_COUNT);
        printQuantiles("Candidate gen", BasicMatcher.metricCandidateGen);
        printQuantiles("Top match", BasicMatcher.metricTopMatch);
        printQuantiles("First level gen", FirstLevelCandidatesFilter.metricGen);
    }

    private void printQuantiles(String label, ArrayList<Long> list) {
        Percentile p25 = new Percentile(25);
        Percentile p50 = new Percentile(50);
        Percentile p75 = new Percentile(75);
        double[] dbls = list.stream().mapToDouble(Long::doubleValue).toArray();
        long max = list.stream().max(Long::compareTo).orElse(-1L);
        System.out.println(label+": (25%)"+p25.evaluate(dbls)+", (50%)"+p50.evaluate(dbls)+", (75%)"+p75.evaluate(dbls)+", (75%)"+p75.evaluate(dbls)+", (max)"+max);
    }

    private CsvParser createCsvParser() throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
