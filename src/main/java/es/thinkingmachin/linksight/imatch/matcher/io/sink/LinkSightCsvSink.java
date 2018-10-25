package es.thinkingmachin.linksight.imatch.matcher.io.sink;

import de.siegmar.fastcsv.writer.CsvAppender;
import de.siegmar.fastcsv.writer.CsvWriter;
import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

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
        Path tempDir = Paths.get("/volume/out/");
        tempDir.toFile().mkdirs();
        this.outputFile = Files.createTempFile(tempDir, "imatch-out-", ".csv").toFile();
        CsvWriter writer = new CsvWriter();
        this.csvAppender = writer.append(outputFile, StandardCharsets.UTF_8);
        csvAppender.appendLine(header);
    }

    @Override
    public boolean close() {
        try {
            csvAppender.close();
            return true;
        } catch (IOException | NullPointerException e) {
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
        writeAddressFields(srcAddress.terms);

        // match_time
        csvAppender.appendField(String.format("%f", matchTime));

        if (match != null) {
            // matched_*

            writeAddressFields(match.match.address);

            // code
            csvAppender.appendField(match.match.psgc);

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

    public File getOutputFile() {
        return outputFile;
    }

    @Override
    public int getSize() {
        return size;
    }

    @Override
    public String getName() {
        return "[CSV] "+outputFile.getAbsolutePath();
    }

    private void writeAddressFields(String[] address) throws IOException {
        for (String term : address) {
            csvAppender.appendField(term);
        }
        for (int i = 0; i < 3 - address.length; i++) {
            csvAppender.appendField("");
        }
    }

}
