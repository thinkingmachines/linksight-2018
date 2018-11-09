package es.thinkingmachin.linksight.imatch.matcher.reference;

import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.dataset.PsgcDataset;

/**
 * This class encapsulates the information about each row in the PSGC dataset.
 * It includes the psgc, location name, its interlevel, its line number in the
 * CSV file, and the row in string format.
 */
public class PsgcRow {
    public final long psgc;
    public final String psgcStr;
    public final String location;
    public final String interlevel;
    public final boolean isOriginal;
    public final long csvLineNo;
    public final String rowString;

    private PsgcRow(long psgc, String location, String interlevel, boolean isOriginal, long csvLineNo, String rowString) {
        this.psgc = psgc;
        this.psgcStr = Long.toString(psgc);
        this.location = location;
        this.interlevel = interlevel;
        this.isOriginal = isOriginal;
        this.csvLineNo = csvLineNo;
        this.rowString = rowString;
    }

    /**
     * Creates a new instance of a PSGC row based on the PSGC dataset
     * @param row       a row from the psgc dataset
     * @param dataset   the psgc dataset object
     * @return  an object containing data about each row in the psgc dataset
     */
    public static PsgcRow fromCsvRow(CsvRow row, PsgcDataset dataset) {
        long psgc = Long.parseLong(row.getField(dataset.codeField));
        String location = row.getField(dataset.termField);
        String interlevel = row.getField(dataset.levelField);
        boolean isOriginal;
        switch (row.getField(dataset.isOrigField)) {
            case "True":
                isOriginal = true;
                break;
            case "False":
                isOriginal = false;
                break;
            default:
                throw new Error("Unknown value for boolean: " + row.getField(dataset.isOrigField));
        }
        return new PsgcRow(psgc, location, interlevel, isOriginal, row.getOriginalLineNumber(), row.toString());
    }
}
