package es.thinkingmachin.linksight.imatch.matcher.core;

import de.siegmar.fastcsv.reader.CsvRow;

import java.util.Arrays;

/**
 * This class stores the array of location terms in an object,
 * together with its corresponding row number.
 */
public class Address {
    public final String[] terms;
    public final long rowNum;

    public Address(String[] terms, long rowNum) {
        this.terms = terms;
        this.rowNum = rowNum;
    }

    /**
     * Parses the CSV row to convert to an Address object.
     * @param csvRow    the CSV row being processed
     * @param locFields the location fields (barangay, municity, province)
     * @return a new instance of an Address object
     */
    public static Address fromCsvRow(CsvRow csvRow, String[] locFields) {
        if (locFields.length != 3) {
            throw new IllegalArgumentException("Only 3 location fields are supported right now.");
        }
        String[] terms = new String[locFields.length];
        int ctr = 0;
        for (String locField : locFields) {
            String value = csvRow.getField(locField);
            if (value == null || value.length() == 0) continue;
            terms[ctr] = value;
            ctr++;
        }
        return new Address(Arrays.copyOf(terms, ctr), csvRow.getOriginalLineNumber());
    }

    /**
     * Checks if two address objects are equal by comparing its terms.
     * @param o the object being compared
     * @return true if the two objects are equal, false otherwise
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Address address = (Address) o;
        return Arrays.equals(terms, address.terms);
    }

    /**
     * @return a hashcode value for the object using the hashcode of the array of terms
     */
    @Override
    public int hashCode() {
        int result = Arrays.hashCode(terms);
        result = 31 * result;
        return result;
    }

    /**
     * @return a string representation of the array of terms
     */
    @Override
    public String toString() {
        return Arrays.toString(terms);
    }
}
