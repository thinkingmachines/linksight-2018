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

public class FuzzyStringMap<T> {

    public final PreDict preDict;
    private final HashMultimap<String, T> strMultiMap;
    public PreDictCustomizing customization;

    public FuzzyStringMap() {
        this.preDict = createPredictModel();
        this.strMultiMap = HashMultimap.create();
    }

    private PreDict createPredictModel() {
        PreDictSettings settings = new PreDictSettings();
        settings.accuracyLevel(PreDict.AccuracyLevel.fast);
        customization = new PredictCustomization(settings);
        return new PreDict(customization);
    }

    public void put(String key, T value) {
        key = preDict.cleanIndexWord(key);
        strMultiMap.put(key, value);
        preDict.indexWord(key);
    }

    public Set<T> getExact(String key) {
        key = preDict.cleanIndexWord(key);
        return strMultiMap.get(key);
    }

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
                    .replaceAll("poblacion", "pob")
                    .replaceAll("not a province|capital|\\(|\\)|city of|city", "")
                    .replaceAll("\\s+", " ");
            return word;
        }
    }
}
