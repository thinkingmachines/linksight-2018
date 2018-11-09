package es.thinkingmachin.linksight.imatch.matcher.io.sink;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

/**
 * This class encapsulates information about the list of matched values.
 * It adds the matched values to a list.
 */
public class ListSink implements OutputSink {

    private LinkedList<ReferenceMatch> matches;

    /**
     * Initialize the list of matches.
     * @throws IOException if file is invalid
     */
    @Override
    public void open() throws IOException {
        matches = new LinkedList<>();
    }

    /**
     * Adds the match to the list.
     * @param index
     * @param srcAddress
     * @param matchTime
     * @param match
     * @throws IOException if file is invalid
     */
    @Override
    public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException {
        matches.add(match);
    }

    @Override
    public boolean close() {
        return true;
    }

    /**
     * @return the total number of matches in the list
     */
    @Override
    public int getSize() {
        return matches.size();
    }

    /**
     * @return a string stating the number of matches in the list
     */
    @Override
    public String getName() {
        return "[list] size: "+matches.size();
    }

    /**
     * @return the list of matched locations
     */
    public List<ReferenceMatch> getMatches() {
        return matches;
    }

}
