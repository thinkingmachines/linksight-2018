.. java:import:: com.google.common.base Throwables

.. java:import:: com.google.gson Gson

.. java:import:: com.google.gson.annotations SerializedName

Response
========

.. java:package:: es.thinkingmachin.linksight.imatch.server.messaging
   :noindex:

.. java:type:: public class Response

Fields
------
content
^^^^^^^

.. java:field:: public final String content
   :outertype: Response

status
^^^^^^

.. java:field:: public final Status status
   :outertype: Response

Constructors
------------
Response
^^^^^^^^

.. java:constructor:: public Response(Status status, String content)
   :outertype: Response

Methods
-------
createFailed
^^^^^^^^^^^^

.. java:method:: public static Response createFailed(Throwable e)
   :outertype: Response

createInProgress
^^^^^^^^^^^^^^^^

.. java:method:: public static Response createInProgress()
   :outertype: Response

createSuccess
^^^^^^^^^^^^^

.. java:method:: public static Response createSuccess(String content)
   :outertype: Response

toJson
^^^^^^

.. java:method:: public String toJson()
   :outertype: Response

