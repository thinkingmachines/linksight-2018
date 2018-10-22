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

public class Evaluator {
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

    private static void printStat(String name, int count, int total) {
        System.out.println(String.format("\t%s: %d (%.3f%%)", name, count, count*100.0/total));
    }

    private static CsvParser createCsvParser(String csvPath) throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
