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

/**
 * This class encapsulates information about the CSV output file.
 * It facilitates appending and writing the original data, the matched
 * values, and the other statistics on a new csv file.
 */
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
    private String outputDir;

    public LinkSightCsvSink() {
        this("/volume/out/");
    }

    public LinkSightCsvSink(String outputDir) {
        this.outputDir = outputDir;
    }

    /**
     * Opens and starts the CSV writer
     * @throws IOException if file is invalid
     */
    @Override
    public void open() throws IOException {
        this.size = 0;
        Path tempDir = Paths.get(outputDir);
        tempDir.toFile().mkdirs();
        this.outputFile = Files.createTempFile(tempDir, "imatch-out-", ".csv").toFile();
        CsvWriter writer = new CsvWriter();
        this.csvAppender = writer.append(outputFile, StandardCharsets.UTF_8);
        csvAppender.appendLine(header);
    }

    /**
     * Closes the CSV writer
     * @return true if successful, false otherwise
     */
    @Override
    public boolean close() {
        try {
            csvAppender.close();
            return true;
        } catch (IOException | NullPointerException e) {
            return false;
        }
    }

    /**
     * Writes the original location with its matched fields,
     * together with the psgc, total score, match time, and match type
     * @param index         row number of the address
     * @param srcAddress    the source address in the input dataset
     * @param matchTime     the total matching time
     * @param match         the matched values
     * @throws IOException if output file is invalid
     */
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

    /**
     * @return the output file with the matched locations and psgc
     */
    public File getOutputFile() {
        return outputFile;
    }

    /**
     * @return the number of rows in the output file
     */
    @Override
    public int getSize() {
        return size;
    }

    /**
     * @return the path of the output file
     */
    @Override
    public String getName() {
        return "[CSV] "+outputFile.getAbsolutePath();
    }

    /**
     * Iterates over the original location fields and appends its values
     * @param address       an array of location names of an address by interlevel
     * @throws IOException if output file is invalid
     */
    private void writeAddressFields(String[] address) throws IOException {
        for (String term : address) {
            csvAppender.appendField(term);
        }
        for (int i = 0; i < 3 - address.length; i++) {
            csvAppender.appendField("");
        }
    }

}
