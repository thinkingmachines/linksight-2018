package es.thinkingmachin.linksight.imatch.main;

import es.thinkingmachin.linksight.imatch.server.Server;
import org.apache.commons.cli.*;

import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        CommandLine cli = getCliArgs(args);
        if (cli == null) return;

        String runMode = cli.getOptionValue("mode");
        String ipcAddr = cli.getOptionValue("ipcaddr", "ipc:///tmp/ipchello");

        if (runMode.equals("server")) {
            runServer(ipcAddr);
        } else if (runMode.equals("test")) {
            runTests();
        } else {
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

    private static void runTests() {
        System.out.println("Tests!");
    }
}
