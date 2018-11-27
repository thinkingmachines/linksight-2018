.. java:import:: com.google.gson Gson

.. java:import:: com.google.gson JsonSyntaxException

.. java:import:: com.google.gson.annotations SerializedName

Request
=======

.. java:package:: es.thinkingmachin.linksight.imatch.server.messaging
   :noindex:

.. java:type:: public class Request

Fields
------
columns
^^^^^^^

.. java:field:: public String[] columns
   :outertype: Request

csvPath
^^^^^^^

.. java:field:: public String csvPath
   :outertype: Request

id
^^

.. java:field:: public String id
   :outertype: Request

type
^^^^

.. java:field:: public Type type
   :outertype: Request

Methods
-------
fromJson
^^^^^^^^

.. java:method:: public static Request fromJson(String json)
   :outertype: Request

