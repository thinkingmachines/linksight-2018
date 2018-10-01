package core;

import de.siegmar.fastcsv.reader.CsvRow;
import reference.Reference;

import java.util.Arrays;
import java.util.Objects;

public class Address {
    public final String[] terms;
    public final Interlevel minLevel;
    private String[] modelCleanedTerms;

    public Address(String[] terms, Interlevel minLevel) {
        this.terms = terms;
        this.minLevel = minLevel;
    }

    public void cleanTerms(Reference reference) {
        if (modelCleanedTerms != null) return;
        modelCleanedTerms = new String[terms.length];
        for (int i = 0; i < terms.length; i++) {
            modelCleanedTerms[i] = reference.predictModel.cleanIndexWord(terms[i]);
        }
    }

    public static Address fromCsvRow(CsvRow csvRow, String[] locFields) {
        if (locFields.length != 3) {
            throw new IllegalArgumentException("Only 3 location fields are supported right now.");
        }
        Interlevel minLevel = null;
        String[] terms = new String[Interlevel.indexed.length];
        int ctr = 0;
        for (int i = 0; i < Interlevel.indexed.length; i++) {
            String value = csvRow.getField(locFields[i]);
            value = (value.length() == 0) ? null : value;
            Interlevel level = Interlevel.indexed[i];
            if (value == null) continue;
            minLevel = (minLevel == null) ? level : minLevel;
            terms[ctr] = value;
            ctr++;
        }
        return new Address(Arrays.copyOf(terms, ctr), minLevel);
    }

    public String getTerm(int index) {
        return getTerm(index, false);
    }

    public String getTerm(int index, boolean clean) {
        if (terms == null || index >= terms.length) return null;
        if (!clean) return terms[index];
        if (modelCleanedTerms == null) throw new Error("Please clean the terms first.");
        return modelCleanedTerms[index];
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Address address = (Address) o;
        return Arrays.equals(terms, address.terms) &&
                minLevel == address.minLevel &&
                Arrays.equals(modelCleanedTerms, address.modelCleanedTerms);
    }

    @Override
    public int hashCode() {
        int result = Objects.hash(minLevel);
        result = 31 * result + Arrays.hashCode(terms);
        result = 31 * result + Arrays.hashCode(modelCleanedTerms);
        return result;
    }

    @Override
    public String toString() {
        return "[" + String.join(",", terms) + "] Level: "+minLevel;
    }
}
