package es.thinkingmachin.linksight.imatch.matcher.core;

import de.siegmar.fastcsv.reader.CsvRow;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.Arrays;

public class Address {
    public final String[] terms;

    public Address(String[] terms) {
        this.terms = terms;
    }

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
        return new Address(Arrays.copyOf(terms, ctr));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Address address = (Address) o;
        return Arrays.equals(terms, address.terms);
    }

    @Override
    public int hashCode() {
        int result = Arrays.hashCode(terms);
        result = 31 * result;
        return result;
    }

    @Override
    public String toString() {
        return Arrays.toString(terms);
    }
}
