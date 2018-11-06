package es.thinkingmachin.linksight.imatch.matcher.dataset;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * This class encapsulates the information about the dataset file
 * uploaded by the user. It includes the path to where the CSV file
 * is located and the fields (barangay, municity, province) specified
 * by the user that are included in the dataset.
 */
public class Dataset {

    public final String csvPath;
    public final String[] locFields;

    public Dataset(String csvPath, String[] locFields) {
        this.csvPath = csvPath;
        this.locFields = locFields;
    }

    /**
     * Instantiates a CSV reader and returns a CSV parser.
     * @return a new CSV parser
     * @throws IOException
     */
    public CsvParser getCsvParser() throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
