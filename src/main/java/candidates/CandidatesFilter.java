package candidates;

import core.Address;
import reference.Reference;
import reference.ReferenceRow;

import java.util.List;

public abstract class CandidatesFilter {

    protected final Reference reference;

    public CandidatesFilter(Reference reference) {
        this.reference = reference;
    }

    public abstract List<ReferenceRow> generate(Address address);
}
