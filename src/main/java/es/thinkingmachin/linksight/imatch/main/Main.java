package es.thinkingmachin.linksight.imatch.main;

import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.executor.Executor;
import es.thinkingmachin.linksight.imatch.matcher.executor.ParallelExecutor;
import es.thinkingmachin.linksight.imatch.matcher.io.sink.ListSink;
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

    public static void main(String[] args) throws Throwable {
        CommandLine cli = getCliArgs(args);
        if (cli == null) return;

        String runMode = cli.getOptionValue("mode");
        String ipcAddr = cli.getOptionValue("ipcaddr", "ipc:///tmp/ipchello");

        switch (runMode) {
            case "server":
                runServer(ipcAddr);
                break;
            case "test":
                runTests();
                break;
            case "explorer":
                runExplorer();
                break;
            default:
                throw new IllegalArgumentException("Unknown mode: " + runMode);
        }
    }

    private static CommandLine getCliArgs(String[] args) {
        Options options = new Options();
        options.addRequiredOption("m", "mode", true, "Run mode: 'server', 'test', 'explorer'")
                .addOption("i", "ipcaddr", true, "Path to the IPC address, should execute with ipc://");
        CommandLineParser parser = new DefaultParser();
        try {
            return parser.parse(options, args);
        } catch (ParseException e) {
            new HelpFormatter().printHelp("imatch -m server [-i ipc://addr]", options);
            return null;
        }
    }

    private static void runServer(String ipcAddr) {
        try {
            Server mainServer = new Server(ipcAddr);
            mainServer.start();
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }

    private static void runTests() throws Throwable {
        Server server = new Server(null);
//        TestDataset[] tests = new TestDataset[]{FUZZY_200, HAPPY_PATH, IMAN_TEST, SSS_CLEAN};
        TestDataset[] tests = new TestDataset[]{SSS_CLEAN, HAPPY_PATH, FUZZY_200};
        for (TestDataset test : tests) {
            System.out.println("Test dataset: "+test.name);
            CsvSource source = new CsvSource(test);
            ListSink sink = new ListSink();
            Executor executor = new ParallelExecutor();
            executor = new SeriesExecutor();
            DatasetMatchingTask task = new DatasetMatchingTask(source, sink, executor, server.addressMatcher, SINGLE);
            task.run();
            Evaluator.evaluate(sink.getMatches(), test);
            System.out.println();
        }
    }

    private static void runExplorer() throws IOException {
        Server server = new Server(null);
        TreeExplorer treeExplorer = new TreeExplorer(server.reference);
        treeExplorer.launchRepl();
    }
}
