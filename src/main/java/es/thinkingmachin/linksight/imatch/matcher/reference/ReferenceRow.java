package es.thinkingmachin.linksight.imatch.matcher.reference;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.dataset.ReferenceDataset;
import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;
import de.siegmar.fastcsv.reader.CsvRow;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Objects;

public class ReferenceRow {

    public final long psgc;
    public final Address aliasAddress;
    public final Address stdAddress;

    public ReferenceRow(Address aliasAddress, Address stdAddress, long psgc) {
        this.aliasAddress = aliasAddress;
        this.stdAddress = stdAddress;
        this.psgc = psgc;
    }

    public static ReferenceRow fromCsvRow(CsvRow csvRow, ReferenceDataset referenceDataset) {
        return fromCsvRow(csvRow, referenceDataset.locFields, referenceDataset.psgcField, referenceDataset.aliasField);
    }

    public static ReferenceRow fromCsvRow(CsvRow csvRow, String[] stdLocFields, String psgcField, String aliasField) {
        // Extract PSGC
        long psgc = Long.parseLong(csvRow.getField(psgcField));

        // Extract canonicalized address
        Address stdAddress = Address.fromCsvRow(csvRow, stdLocFields);

        // Extract alias address
        String aliasValue = csvRow.getField(aliasField);
        String[] alias = aliasValue.split(",");
        alias = Arrays.copyOf(alias, alias.length-1);

        // Special cases
        if (stdAddress.terms.length != alias.length) {
            String lastTerm = alias[alias.length-1];
            String middleTerm = alias[alias.length-2];
            if ((lastTerm.equals("national capital region ncr")
                    || lastTerm.equals("ncr")
                    || lastTerm.equals("national capital region")
                    || lastTerm.equals("metro manila")
                    || lastTerm.equals("metropolitan manila")) && middleTerm.equals("manila")) {
                // TODO: optimize!
                // Remove middle term
                ArrayList<String> temp = new ArrayList<>(Arrays.asList(alias));
                temp.remove(temp.size() - 2);
                alias = temp.toArray(new String[]{});
            }
        }

        if (stdAddress.terms.length != alias.length) {
            assert false: "Unequal: "+stdAddress+" and "+Arrays.toString(alias);
        }

        Interlevel level = Interlevel.inferLevel(alias.length);
        Address aliasAddress = new Address(alias, level);

        // Construct object
        return new ReferenceRow(aliasAddress, stdAddress, psgc);
    }

    @Override
    public String toString() {
        return aliasAddress.toString() + " PSGC: " + psgc;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ReferenceRow that = (ReferenceRow) o;
        return psgc == that.psgc &&
                Objects.equals(aliasAddress, that.aliasAddress) &&
                Objects.equals(stdAddress, that.stdAddress);
    }

    @Override
    public int hashCode() {
        return Objects.hash(psgc, aliasAddress, stdAddress);
    }
}
