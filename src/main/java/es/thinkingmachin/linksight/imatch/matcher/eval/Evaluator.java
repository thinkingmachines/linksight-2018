package es.thinkingmachin.linksight.imatch.matcher.eval;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;
import de.siegmar.fastcsv.reader.CsvRow;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class Evaluator {
    public static void evaluate(List<ReferenceMatch> matchedAddresses, String testCsvPath, String[] testCorrectCols) throws IOException {
        CsvParser csvParser = createCsvParser(testCsvPath);
        CsvRow row;
        int i = -1;
        int countCorrect = 0;
        int countTotal = 0;
        while ((row = csvParser.nextRow()) != null) {
            i++;
            String match_type = row.getField("expected_match_type");
            long correct_psgc = Long.parseLong(row.getField("expected_psgc"));
//            if (!match_type.equalsIgnoreCase("Ambiguous")) continue;
            Address correct = Address.fromCsvRow(row, testCorrectCols);
            if (i >= matchedAddresses.size()) break;
            ReferenceMatch match = matchedAddresses.get(i);
            if (match != null && match.referenceRow.psgc == correct_psgc) {
                countCorrect++;
            } else {
                //Wrong
//                if (match == null) {
//                    System.out.println("Raw: " + Address.fromCsvRow(row, new String[]{"source_brgy", "source_municity", "source_prov"}));
//                    System.out.println("Correct: " + correct);
//                    System.out.println("Matched: "+ match);
//                    System.out.println();
//                }
            }

            countTotal++;
        }
        System.out.println("Correct: " + countCorrect);
        System.out.println("Total: " + countTotal);
        System.out.println("% correct: " + (countCorrect * 100.0 / countTotal));

        if (matchedAddresses.size() != countTotal) {
            throw new Error("Size mismatch! " + matchedAddresses.size() + " matched vs " + countTotal + " correct");
        }
    }


    private static CsvParser createCsvParser(String csvPath) throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
