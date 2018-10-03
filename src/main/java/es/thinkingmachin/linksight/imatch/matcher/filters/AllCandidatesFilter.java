package es.thinkingmachin.linksight.imatch.matcher.filters;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceRow;

import java.util.List;

public class AllCandidatesFilter extends CandidatesFilter {

    public AllCandidatesFilter(Reference reference) {
        super(reference);
    }

    @Override
    public List<ReferenceRow> generate(Address address) {
        return reference.rows;
    }
}
