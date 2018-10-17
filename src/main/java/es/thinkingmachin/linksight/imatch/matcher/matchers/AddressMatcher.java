package es.thinkingmachin.linksight.imatch.matcher.matchers;

import de.siegmar.fastcsv.reader.CsvRow;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.util.List;

public interface AddressMatcher {

    ReferenceMatch getTopMatch(Address address, CsvRow row);

    List<ReferenceMatch> getTopMatches(Address address, int numMatches, CsvRow row);

}
