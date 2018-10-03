package es.thinkingmachin.linksight.imatch.matcher.filters;

import com.google.common.base.Stopwatch;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.Reference;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceRow;
import de.cxp.predict.api.SuggestItem;

import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

public class FirstLevelCandidatesFilter extends CandidatesFilter {

    public static ArrayList<Long> metricGen = new ArrayList<>(2000);

    public FirstLevelCandidatesFilter(Reference reference) {
        super(reference);
    }

    @Override
    public List<ReferenceRow> generate(Address address) {
        Stopwatch stopwatch = Stopwatch.createStarted();
        List<SuggestItem> suggestions = reference.predictModel.lookup(address.terms[0]);
        stopwatch.stop();
        long duration = stopwatch.elapsed(TimeUnit.MICROSECONDS);
        metricGen.add(duration);

        return suggestions.stream()
                .map(s -> reference.firstTermsCache.get(s.term))
                .filter(Objects::nonNull)
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }
}
