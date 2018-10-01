package scoring;

import core.Address;

public interface Scoring {
    public double getScore(Address address, Address candidate);
}
