package es.thinkingmachin.linksight.imatch.matcher.dataset;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvReader;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

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

    public CsvParser getCsvParser() throws IOException {
        File file = new File(csvPath);
        CsvReader csvReader = new CsvReader();
        csvReader.setContainsHeader(true);
        return csvReader.parse(file, StandardCharsets.UTF_8);
    }
}
