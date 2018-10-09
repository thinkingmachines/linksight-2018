package es.thinkingmachin.linksight.imatch.matcher.io;

import de.siegmar.fastcsv.writer.CsvAppender;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.IOException;

public class CsvOutput {
    private static String[] header = {
            "dataset_index",
            "search_tuple",
            "source_province",
            "source_city_municipality",
            "source_barangay",
            "match_time",
            "matched_province",
            "matched_city_municipality",
            "matched_barangay",
            "code",
            "total_score",
            "match_type"
    };

    private final CsvAppender csvAppender;

    public CsvOutput(CsvAppender csvAppender) {
        this.csvAppender = csvAppender;
    }

    public void writeHeaderRow() throws IOException {
        csvAppender.appendLine(header);
    }

    public void writeRow(int index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException {
        // dataset_index
        csvAppender.appendField(Integer.toString(index));

        // search_tuple
        csvAppender.appendField("");  // TODO: fix this

        // source_*
        writeAddressFields(srcAddress);

        // match_time
        csvAppender.appendField(String.format("%f", matchTime));

        if (match != null) {
            // matched_*
            writeAddressFields(match.referenceRow.aliasAddress);

            // code
            csvAppender.appendField(Long.toString(match.referenceRow.psgc));

            // total_score
            csvAppender.appendField(String.format("%f", match.score));

            // match_type
            csvAppender.appendField(match.score == 1.0 ? "exact" : "near");
        } else {
            // no matched_*, code
            for (int i = 0; i < 4; i++) {
                csvAppender.appendField("");
            }

            // no total_score
            csvAppender.appendField("0.0");

            // no match_type
            csvAppender.appendField("no_match");
        }
        csvAppender.endLine();
    }

    private void writeAddressFields(Address address) throws IOException {
        for (int i = address.terms.length - 1; i >= 0; i--) {
            csvAppender.appendField(address.terms[i]);
        }
        for (int i = 0; i < 3 - address.terms.length; i++) {
            csvAppender.appendField("");
        }
    }

}
