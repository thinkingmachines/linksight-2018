package es.thinkingmachin.linksight.imatch.matcher.dataset;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class Dataset {

    public final String csvPath;
    public final String[] locFields;

    public Dataset(String csvPath, String[] locFields) {
        this.csvPath = csvPath;
        this.locFields = locFields;
    }

    public CsvParser getCsvParser() throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
