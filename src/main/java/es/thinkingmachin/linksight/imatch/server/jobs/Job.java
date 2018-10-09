package es.thinkingmachin.linksight.imatch.server.jobs;

import es.thinkingmachin.linksight.imatch.server.messaging.Response;

public abstract class Job {

    public final String id;

    public Job(String id) {
        this.id = id;
    }

    public abstract Response run();
}
