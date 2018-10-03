package es.thinkingmachin.linksight.imatch.matcher.filters;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceRow;

import java.util.List;

public abstract class CandidatesFilter {

    protected final Reference reference;

    public CandidatesFilter(Reference reference) {
        this.reference = reference;
    }

    public abstract List<ReferenceRow> generate(Address address);
}
