package es.thinkingmachin.linksight.imatch.matcher.io.source;

import de.siegmar.fastcsv.reader.CsvParser;
import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;

import java.io.IOException;
import java.util.NoSuchElementException;

/**
 * This class encapsulates information about the CSV input data.
 * It contains the CSV parser which allows the user to loop through each row.
 */
public class CsvSource implements InputSource {

    private Dataset dataset;

    private CsvParser parser;
    private CsvRow nextRow;
    private int curCount;

    public CsvSource(Dataset dataset) {
        this.dataset = dataset;
    }

    /**
     * Opens and starts the CSV parser
     * @throws IOException if file is invalid
     */
    @Override
    public void open() throws IOException {
        curCount = 0;
        this.parser = dataset.getCsvParser();
        if (parser == null) throw new IOException("Cannot create CSV parser for dataset: "+dataset.csvPath);
        getNextRow();
    }

    /**
     * Closes the CSV parser
     * @return true if closing is successful
     */
    @Override
    public boolean close() {
        try {
            parser.close();
            return true;
        } catch (IOException | NullPointerException e) {
            return false;
        }
    }

    /**
     * @return true if the next row is not null
     */
    @Override
    public boolean hasNext() {
        return nextRow != null;
    }

    /**
     * Gets the next row and instantiates a new Address object
     * @return the created address object from the given row
     */
    @Override
    public Address next() {
        if (!hasNext()) throw new NoSuchElementException();
        Address address = Address.fromCsvRow(nextRow, dataset.locFields);
        getNextRow();
        return address;
    }

    /**
     * @return the filename of the CSV dataset
     */
    @Override
    public String getName() {
        return "[CSV] "+dataset.csvPath;
    }

    /**
     * Gets the next row in the CSV file
     */
    private void getNextRow() {
        try {
            this.nextRow = parser.nextRow();
            curCount++;
        } catch (IOException e) {
            this.nextRow = null;
        }
    }

    /**
     * @return the current count of rows passed
     */
    public int getCurrentCount() {
        return curCount;
    }
}
