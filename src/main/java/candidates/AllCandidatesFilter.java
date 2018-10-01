package candidates;

import core.Address;
import reference.Reference;
import reference.ReferenceRow;

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
