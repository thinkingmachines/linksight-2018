package es.thinkingmachin.linksight.imatch.matcher.dataset;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * This class encapsulates the information about the psgc dataset.
 * It includes the path to where the CSV file is located, and the
 * headers for the psgc, location, isOriginal, and interlevel columns.
 */
public class PsgcDataset {

    public final String csvPath;
    public final String codeField;
    public final String termField;
    public final String isOrigField;
    public final String levelField;

    public PsgcDataset(String csvPath, String termField, String isOrigField, String codeField, String levelField) {
        this.csvPath = csvPath;
        this.termField = termField;
        this.isOrigField = isOrigField;
        this.codeField = codeField;
        this.levelField = levelField;
    }

    /**
     * Instantiates a CSV reader and returns a CSV parser.
     *
     * @return a new CSV parser
     */
    public CsvParser getCsvParser() {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        try {
            return csvReader.parse(file, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException("PSGC dataset: " + csvPath + " not found");
        }
    }
}
