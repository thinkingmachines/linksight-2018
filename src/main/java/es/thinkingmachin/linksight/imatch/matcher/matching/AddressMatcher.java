package es.thinkingmachin.linksight.imatch.matcher.matching;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.util.List;

/**
 * This class serves as the interface for getting the top matches for matching algorithms.
 */
public interface AddressMatcher {

    List<ReferenceMatch> getTopMatches(Address address, int numMatches);

}
