package es.thinkingmachin.linksight.imatch.matcher.model;

import com.google.common.collect.HashMultimap;
import de.cxp.predict.PreDict;
import de.cxp.predict.api.PreDictSettings;
import de.cxp.predict.api.SuggestItem;
import de.cxp.predict.customizing.CommunityCustomization;
import de.cxp.predict.customizing.PreDictCustomizing;
import org.apache.commons.math3.util.Pair;

import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * This class encapsulates information about the PreDict model.
 * It consists of the PreDict model, the multi map of nodes and its values,
 * and the customization settings for the PreDict model.
 * @param <T>
 */
public class FuzzyStringMap<T> {

    public final PreDict preDict;
    private final HashMultimap<String, T> strMultiMap;
    public PreDictCustomizing customization;

    public FuzzyStringMap() {
        this.preDict = createPredictModel();
        this.strMultiMap = HashMultimap.create();
    }

    /**
     * Creates the PreDict model and sets its accuracy and customization settings
     * @return the PreDict model
     */
    private PreDict createPredictModel() {
        PreDictSettings settings = new PreDictSettings();
        settings.accuracyLevel(PreDict.AccuracyLevel.fast);
        customization = new PredictCustomization(settings);
        return new PreDict(customization);
    }

    /**
     * Creates a key using the specified PreDict customization settings
     * and adds the key-value pair to the multimap.
     * @param key
     * @param value
     */
    public void put(String key, T value) {
        key = preDict.cleanIndexWord(key);
        strMultiMap.put(key, value);
        preDict.indexWord(key);
    }

    public Set<T> getExact(String key) {
        key = preDict.cleanIndexWord(key);
        return strMultiMap.get(key);
    }

    /**
     * Searches the key using the predict model and returns a list of suggestions.
     * Each key of the suggested items is looked up in the multi map, getting its
     * values. Each value, together with the computed proximity in PreDict is added
     * to a list called fuzzyPairs.
     * @param key the subphrase to be searched using the PreDict model
     * @return a set of values of the suggested items during the search and their corresponding proximity
     */
    public Set<Pair<T, Double>> getFuzzy(String key) {
        List<SuggestItem> suggestions = preDict.lookup(key);
        Set<Pair<T, Double>> fuzzyPairs = new HashSet<>();
        for (SuggestItem s : suggestions) {
            Set<T> values = strMultiMap.get(s.term);
            for (T value : values) {
                fuzzyPairs.add(new Pair<>(value, s.proximity));
            }
        }
        return fuzzyPairs;
    }

    private static class PredictCustomization extends CommunityCustomization {

        private static final Pattern removePattern = Pattern.compile("[^\\p{L}\\p{N}\\p{Z}]");

        PredictCustomization(PreDictSettings settings) {
            super(settings);
        }

        @Override
        public String cleanIndexWord(String word) {
            return cleanWord(word);
        }

        @Override
        public String cleanSearchWord(String searchWord) {
            return cleanWord(searchWord);
        }

        public String cleanWord(String word) {
            word = removePattern.matcher(word)
                    .replaceAll("")
                    .toLowerCase()
                    .replaceAll("ñ", "n")
                    .replaceAll("barangay|bgy", "bgy")
                    .replaceAll("occidental", "occ")
                    .replaceAll("poblacion", "pob")
                    .replaceAll("not a province|capital|\\(|\\)|city of|city", "")
                    .replaceAll("\\s+", " ");
            return word;
        }
    }
}
