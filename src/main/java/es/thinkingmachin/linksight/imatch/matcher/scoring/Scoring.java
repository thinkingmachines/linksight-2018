package es.thinkingmachin.linksight.imatch.matcher.scoring;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;

public interface Scoring {
    public double getScore(Address address, Address candidate);
}
