package es.thinkingmachin.linksight.imatch.matcher.io.source;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;

import java.io.IOException;
import java.util.NoSuchElementException;

public class CsvSource implements InputSource {

    private Dataset dataset;

    private CsvParser parser;
    private CsvRow nextRow;
    private int curCount;

    public CsvSource(Dataset dataset) {
        this.dataset = dataset;
    }

    @Override
    public void open() throws IOException {
        curCount = 0;
        this.parser = dataset.getCsvParser();
        getNextRow();
    }

    @Override
    public boolean close() {
        try {
            parser.close();
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    @Override
    public boolean hasNext() {
        return nextRow != null;
    }

    @Override
    public Address next() {
        if (!hasNext()) throw new NoSuchElementException();
        Address address = Address.fromCsvRow(nextRow, dataset.locFields);
        getNextRow();
        return address;
    }

    @Override
    public String getName() {
        return "[CSV] "+dataset.csvPath;
    }

    private void getNextRow() {
        try {
            this.nextRow = parser.nextRow();
            curCount++;
        } catch (IOException e) {
            this.nextRow = null;
        }
    }

    public int getCurrentCount() {
        return curCount;
    }
}
