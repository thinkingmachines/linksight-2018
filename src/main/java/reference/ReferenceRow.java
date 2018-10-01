package reference;

import core.Address;
import core.Interlevel;
import de.siegmar.fastcsv.reader.CsvRow;

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

    public static ReferenceRow fromCsvRow(CsvRow csvRow, String[] stdLocFields, String psgcField, String aliasField) {
        // Extract PSGC
        long psgc = Long.parseLong(csvRow.getField(psgcField));

        // Extract canonicalized address
        Address stdAddress = Address.fromCsvRow(csvRow, stdLocFields);

        // Extract alias address
        String aliasValue = csvRow.getField(aliasField);
        String[] alias = aliasValue.split(",");
        alias = Arrays.copyOf(alias, alias.length-1);
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
