package es.thinkingmachin.linksight.imatch.main;

import es.thinkingmachin.linksight.imatch.matcher.dataset.TestDataset;
import es.thinkingmachin.linksight.imatch.matcher.eval.Evaluator;
import es.thinkingmachin.linksight.imatch.matcher.reference.ReferenceMatch;
import es.thinkingmachin.linksight.imatch.matcher.tree.TreeExplorer;
import es.thinkingmachin.linksight.imatch.server.Server;
import org.apache.commons.cli.*;

import java.io.IOException;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) throws Exception {
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
            default:
                throw new IllegalArgumentException("Unknown mode: " + runMode);
        }
    }

    private static CommandLine getCliArgs(String[] args) {
        Options options = new Options();
        options.addRequiredOption("m", "mode", true, "Run mode: 'server', 'test'")
                .addOption("i", "ipcaddr", true, "Path to the IPC address, should start with ipc://");
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

    private static void runTests() throws IOException {
        Server server = new Server(null);
        TreeExplorer treeExplorer = new TreeExplorer(server.reference);
        treeExplorer.launchRepl();
//        Server server = new Server(null);
//        TestDataset test = TestDataset.BuiltIn.IMAN_TEST;
//        ArrayList<ReferenceMatch> matches = server.matcher.getTopMatches(test);
//        Evaluator.evaluate(matches, test);
    }
}
