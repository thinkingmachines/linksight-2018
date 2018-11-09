.. java:import:: de.siegmar.fastcsv.reader CsvParser

.. java:import:: de.siegmar.fastcsv.reader CsvReader

.. java:import:: de.siegmar.fastcsv.reader CsvRow

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.core Address

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.dataset TestDataset

.. java:import:: es.thinkingmachin.linksight.imatch.matcher.reference ReferenceMatch

.. java:import:: java.io File

.. java:import:: java.io IOException

.. java:import:: java.nio.charset StandardCharsets

.. java:import:: java.util List

Evaluator
=========

.. java:package:: es.thinkingmachin.linksight.imatch.matcher.eval
   :noindex:

.. java:type:: public class Evaluator

   This class assesses the accuracy of the matching algorithm using test datasets.

Methods
-------
evaluate
^^^^^^^^

.. java:method:: public static void evaluate(List<ReferenceMatch> matchedAddresses, TestDataset testDataset) throws IOException
   :outertype: Evaluator

   Evaluates the accuracy of the matching algorithm using a test dataset. It compares the score of the matched value to benchmarks (0.95 and 1.00).

   :param matchedAddresses: a list of matched values
   :param testDataset: the test dataset used for evaluation
   :throws IOException: if file is invalid

