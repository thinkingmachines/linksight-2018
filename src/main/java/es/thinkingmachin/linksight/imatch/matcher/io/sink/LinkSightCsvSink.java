package es.thinkingmachin.linksight.imatch.matcher.io.sink;

import de.siegmar.fastcsv.writer.CsvAppender;
import de.siegmar.fastcsv.writer.CsvWriter;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;

public class LinkSightCsvSink implements OutputSink {
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

    private CsvAppender csvAppender;
    private File outputFile;
    private int size;

    @Override
    public void open() throws IOException {
        this.size = 0;
        this.outputFile = Files.createTempFile("imatch-out-", ".tmp").toFile();
        CsvWriter writer = new CsvWriter();
        this.csvAppender = writer.append(outputFile, StandardCharsets.UTF_8);
        csvAppender.appendLine(header);
    }

    @Override
    public boolean close() {
        try {
            csvAppender.close();
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    @Override
    public void addMatch(long index, Address srcAddress, double matchTime, ReferenceMatch match) throws IOException {
        size++;

        // dataset_index
        csvAppender.appendField(Long.toString(index));

        // search_tuple
        csvAppender.appendField("");  // TODO: fix this

        // source_*
        writeAddressFields(srcAddress);

        // match_time
        csvAppender.appendField(String.format("%f", matchTime));

        if (match != null) {
            // matched_*
            throw new NotImplementedException();
//            writeAddressFields(match.referenceRow.aliasAddress);

            // code
//            csvAppender.appendField(Long.toString(match.referenceRow.psgc));

            // total_score
//            csvAppender.appendField(String.format("%f", match.score));

            // match_type
//            csvAppender.appendField(match.score == 1.0 ? "exact" : "near");
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

    public File getOutputFile() {
        return outputFile;
    }

    @Override
    public int getSize() {
        return size;
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
