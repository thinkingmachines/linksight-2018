package es.thinkingmachin.linksight.imatch.main;

import es.thinkingmachin.linksight.imatch.server.Server;

import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        // TODO: parse args, i.e. run type, ipc path
        String runType = "server";
        String ipcPath = "ipc:///tmp/ipchello";
        // TODO: fix
        if (runType.equals("server")) {
            try {
                Server mainServer = new Server(ipcPath);
                mainServer.start();
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
        }
    }
}
