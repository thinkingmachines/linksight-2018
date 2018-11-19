package es.thinkingmachin.linksight.imatch.server.messaging;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import com.google.gson.annotations.SerializedName;

public class Request {
    public String id;
    public String csvPath;
    public String outputDir;
    public String[] columns;

    public static Request fromJson(String json) {
        try {
            return new Gson().fromJson(json, Request.class);
        } catch (JsonSyntaxException e) {
            return null;
        }
    }
}
