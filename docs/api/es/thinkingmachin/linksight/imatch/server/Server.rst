.. java:import:: com.google.common.base Throwables

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset Dataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset PsgcDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree.matcher TreeAddressMatcher

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.tree TreeReference

.. java:import:: es.thinkingmachin.linksight.imatch.server.jobs LinkSightCsvMatchingJob

.. java:import:: es.thinkingmachin.linksight.imatch.server.jobs Job

.. java:import:: es.thinkingmachin.linksight.imatch.server.messaging Request

.. java:import:: es.thinkingmachin.linksight.imatch.server.messaging Response

.. java:import:: io.reactivex BackpressureStrategy

.. java:import:: io.reactivex.disposables Disposable

.. java:import:: io.reactivex.schedulers Schedulers

.. java:import:: io.reactivex.subjects PublishSubject

.. java:import:: org.zeromq ZMQ

.. java:import:: sun.reflect.generics.reflectiveObjects NotImplementedException

.. java:import:: java.io IOException

.. java:import:: java.nio.charset Charset

.. java:import:: java.util.concurrent ConcurrentHashMap

Server
======

.. java:package:: es.thinkingmachin.linksight.imatch.server
   :noindex:

.. java:type:: public class Server

Fields
------
addressMatcher
^^^^^^^^^^^^^^

.. java:field:: public TreeAddressMatcher addressMatcher
   :outertype: Server

reference
^^^^^^^^^

.. java:field:: public TreeReference reference
   :outertype: Server

Constructors
------------
Server
^^^^^^

.. java:constructor:: public Server(String port) throws IOException
   :outertype: Server

Methods
-------
start
^^^^^

.. java:method:: public void start()
   :outertype: Server

