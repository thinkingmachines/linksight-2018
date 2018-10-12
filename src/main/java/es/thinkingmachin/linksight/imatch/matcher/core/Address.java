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
//        if (locFields.length != 3) {
//            throw new IllegalArgumentException("Only 3 location fields are supported right now.");
//        }
//        Interlevel minLevel = null;
//        String[] terms = new String[Interlevel.indexed.length];
//        int ctr = 0;
//        for (int i = 0; i < Interlevel.indexed.length; i++) {
//            String value = csvRow.getField(locFields[i]);
//            value = (value.length() == 0) ? null : value;
//            if (value == null) continue;
//            minLevel = (minLevel == null) ? Interlevel.indexed[i] : minLevel;
//            terms[ctr] = value;
//            ctr++;
//        }
//        return new Address(Arrays.copyOf(terms, ctr), minLevel);
        throw new NotImplementedException();
    }

    public String getTerm(int index) {
        return getTerm(index, false);
    }

    public String getTerm(int index, boolean clean) {
//        if (terms == null || index >= terms.length) return null;
//        if (!clean) return terms[index];
//        if (modelCleanedTerms == null) throw new Error("Please clean the terms first.");
//        return modelCleanedTerms[index];
        throw new NotImplementedException();
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
