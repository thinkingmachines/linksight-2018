package es.thinkingmachin.linksight.imatch.main;

import es.thinkingmachin.linksight.imatch.matcher.dataset.Dataset;
import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.executor.ParallelExecutor;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.LinkSightCsvSink;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.ListSink;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.OutputSink;
import es.thinkingmachin.linksight.imatch.matcher.io.source.CsvSource;
import es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask;
import es.thinkingmachin.linksight.imatch.matcher.executor.SeriesExecutor;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeExplorer;
import es.thinkingmachin.linksight.imatch.server.Server;
import org.apache.commons.cli.*;

import java.io.IOException;

import static es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset.BuiltIn.*;
import static es.thinkingmachin.linksight.imatch.matcher.matching.DatasetMatchingTask.MatchesType.SINGLE;

public class Main {

    private static final int DEFAULT_PORT = 8686;

    /**
     * The main method. Allows user to choose between different modes:
     * server, test, explorer, and manual.
     *
     * @param args the command line arguments
     * @throws Throwable if mode value is invalid.
     */
    public static void main(String[] args) throws Throwable {
        CommandLine cli = getCliArgs(args);
        if (cli == null) return;

        String runMode = cli.getOptionValue("mode");
        String port = cli.getOptionValue("port", String.valueOf(DEFAULT_PORT));
        String fields = cli.getOptionValue("fields");
        String dataset = cli.getOptionValue("dataset");

        switch (runMode) {
            case "server":
                runServer(port);
                break;
            case "test":
                runTests();
                break;
            case "explorer":
                runExplorer();
                break;
            case "manual":
                runManual(fields, dataset);
                break;
            default:
                throw new IllegalArgumentException("Unknown mode: " + runMode);
        }
    }

    /**
     * Gets command line arguments and passes it as command line options.
     *
     * @param args the command line arguments
     * @return the list of atomic option and value tokens
     */
    private static CommandLine getCliArgs(String[] args) {
        Options options = new Options();
        options.addRequiredOption("m", "mode", true, "Run mode: 'server', 'test', 'explorer', 'manual'")
                .addOption("p", "port", true, "[Server Mode] Port to listen on. Default: " + DEFAULT_PORT)
                .addOption("d", "dataset", true, "[Manual Mode] Path to the dataset to match")
                .addOption("f", "fields", true, "[Manual Mode] Comma-separated names of location fields to be used for matching");
        CommandLineParser parser = new DefaultParser();
        try {
            return parser.parse(options, args);
        } catch (ParseException e) {
            new HelpFormatter().printHelp("imatch -m server [-p port]", options);
            return null;
        }
    }

    /**
     * Runs the server.
     *
     * @param port the server port specified in the command line
     */
    private static void runServer(String port) {
        try {
            Server mainServer = new Server(Integer.parseInt(port));
            mainServer.start();
        } catch (IOException | NumberFormatException e) {
            System.out.println(e.getMessage());
        }
    }

    /**
     * Runs the test cases set by the program.
     *
     * @throws Throwable
     */
    private static void runTests() throws Throwable {
        Server server = new Server(null);
        TestDataset[] tests = new TestDataset[]{SSS_CLEAN, HAPPY_PATH, FUZZY_200};
        for (TestDataset test : tests) {
            System.out.println("┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄");
            System.out.println("Test dataset: " + test.name);
            CsvSource source = new CsvSource(test);
            ListSink sink = new ListSink();
            Executor executor = new SeriesExecutor();
            DatasetMatchingTask task = new DatasetMatchingTask(source, sink, executor, server.addressMatcher, SINGLE);
            task.run();
            Evaluator.evaluate(sink.getMatches(), test);
            System.out.println();
        }
    }

    /**
     * Runs the explorer mode of the program.
     * Allows the user to explore and run queries on the Address Tree built by the program.
     *
     * @throws IOException if psgc dataset is invalid
     */
    private static void runExplorer() throws IOException {
        Server server = new Server(null);
        TreeExplorer treeExplorer = new TreeExplorer(server.reference);
        treeExplorer.launchRepl();
    }

    /**
     * Runs the program with the fields provided by the user.
     *
     * @param fields      the fields (barangay, municity, province) included in the dataset
     * @param datasetPath the path of the dataset file
     * @throws Throwable
     */
    private static void runManual(String fields, String datasetPath) throws Throwable {
        if (datasetPath == null || fields == null) {
            System.out.println("Usage: imatch -m manual -d /path/to/input.csv -f bgy,municity,province");
            return;
        }
        Dataset input = new Dataset(datasetPath, fields.split(","));
        Server server = new Server(null);
        CsvSource source = new CsvSource(input);
        LinkSightCsvSink sink = new LinkSightCsvSink();
        Executor executor = new SeriesExecutor();
        DatasetMatchingTask task = new DatasetMatchingTask(source, sink, executor, server.addressMatcher, SINGLE);
        task.run();
        task.matchingStats.printStats();
    }
}
