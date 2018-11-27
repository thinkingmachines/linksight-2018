package es.thinkingmachin.linksight.imatch.server.messaging;

import com.google.common.base.Throwables;
import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import spark.ResponseTransformer;

public class Response {
    public final Status status;
    public final String content;

    public Response(Status status, String content) {
        this.status = status;
        this.content = content;
    }

    public String toJson() {
        return new Gson().toJson(this);
    }

    public static Response createInProgress() {
        return new Response(Status.INPROGRESS, null);
    }

    public static Response createSuccess(String content) {
        return new Response(Status.DONE, content);
    }

    public static Response createFailed(Throwable e) {
        return new Response(Status.FAILED, Throwables.getStackTraceAsString(e));
    }

    public enum Status {
        @SerializedName("in_progress")
        INPROGRESS,
        @SerializedName("done")
        DONE,
        @SerializedName("failed")
        FAILED,
    }

    public static class SparkResponseTransformer implements ResponseTransformer {
        @Override
        public String render(Object model) throws Exception {
            Response res = (Response) model;
            if (res == null) throw new Exception("Not a valid response object");
            return res.toJson();
        }
    }
}