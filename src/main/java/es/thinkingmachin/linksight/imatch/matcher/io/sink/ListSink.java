package es.thinkingmachin.linksight.imatch.matcher.io.sink;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

public class ListSink implements OutputSink {

    private LinkedList<ReferenceMatch> matches;

    @Override
    public void open() throws IOException {
        matches = new LinkedList<>();
    }

    @Override
    public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException {
        matches.add(match);
    }

    @Override
    public boolean close() {
        return true;
    }

    @Override
    public int getSize() {
        return matches.size();
    }

    @Override
    public String getName() {
        return "[list] size: "+matches.size();
    }

    public List<ReferenceMatch> getMatches() {
        return matches;
    }

}
