package es.thinkingmachin.linksight.imatch.matcher.eval;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * This class assesses the accuracy of the matching algorithm using test datasets.
 */
public class Evaluator {
    /**
     * Evaluates the accuracy of the matching algorithm using a test dataset.
     * It compares the score of the matched value to benchmarks (0.95 and 1.00).
     * @param matchedAddresses  a list of matched values
     * @param testDataset       the test dataset used for evaluation
     * @throws IOException if file is invalid
     */
    public static void evaluate(List<ReferenceMatch> matchedAddresses, TestDataset testDataset) throws IOException {
        CsvParser csvParser = createCsvParser(testDataset.csvPath);
        CsvRow row;
        int countCorrect = 0;
        int countTotal = 0;
        int countNull = 0;
        int countScore095 = 0;
        int countScore100 = 0;
        int countBgyLevel = 0;
        for (int i = 0; (row = csvParser.nextRow()) != null; i++) {
            if (i >= matchedAddresses.size()) throw new Error("Size mismatch!");
            ReferenceMatch match = matchedAddresses.get(i);

            countTotal++;
            if (match == null) {
                // No match at all
                countNull++;
                System.out.println("Null match: (row " + row.getOriginalLineNumber() + ")");
                System.out.println("\tRaw: " + Address.fromCsvRow(row, testDataset.locFields));
                System.out.println();
            } else {
                if (match.score >= 0.95) countScore095++;
                if (match.score == 1) countScore100++;
                if (match.match.address.length == 3) countBgyLevel++;

                if (testDataset.hasCorrectField()) {
                    // Correct answer provided
                    long correct_psgc = Long.parseLong(row.getField(testDataset.correctPsgcField));
                    if (Long.parseLong(match.match.psgc) == correct_psgc) {
                        // Correct answer
                        countCorrect++;
                    } else {
                        // Wrong answer
                        System.out.println("Wrong match: (row " + row.getOriginalLineNumber() + ")");
                        System.out.println("\tRaw: " + Address.fromCsvRow(row, testDataset.locFields));
                        System.out.println("\tMatched: " + match);
                        System.out.println("\tCorrect PSGC: " + correct_psgc);
                        System.out.println();
                    }
                }
            }
        }

        System.out.println("Evaluation:");
        System.out.println("\tTotal: " + countTotal);
        printStat("Correct", countCorrect, countTotal);
        printStat("Null", countNull, countTotal);
        printStat("Score >= 0.95", countScore095, countTotal);
        printStat("Score == 1.00", countScore100, countTotal);
        printStat("Brgy Level", countBgyLevel, countTotal);
    }

    /**
     * Prints the statistics of the evaluation
     * @param name  the statistic title
     * @param count the total number of scores hitting the benchmark
     * @param total the total number of scores
     */
    private static void printStat(String name, int count, int total) {
        System.out.println(String.format("\t%s: %d (%.3f%%)", name, count, count*100.0/total));
    }

    /**
     * Creates a csv reader for the test dataset and parses it
     * @param csvPath the path of the test dataset
     * @return the csv parser for the test dataset
     * @throws IOException if file is invalid
     */
    private static CsvParser createCsvParser(String csvPath) throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
