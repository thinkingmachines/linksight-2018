package es.thinkingmachin.linksight.imatch.matcher.model;

import com.google.common.collect.HashMultimap;
import de.cxp.predict.PreDict;
import de.cxp.predict.api.PreDictSettings;
import de.cxp.predict.api.SuggestItem;
import de.cxp.predict.customizing.CommunityCustomization;
import org.apache.commons.math3.util.Pair;

import java.util.*;
import java.util.stream.Collectors;

public class FuzzyStringMap<T> {

    private final PreDict preDict;
    private final HashMultimap<String, T> strMultiMap;

    public FuzzyStringMap() {
        this.preDict = createPredictModel();
        this.strMultiMap = HashMultimap.create();
    }

    private PreDict createPredictModel() {
        PreDictSettings settings = new PreDictSettings();
        settings.accuracyLevel(PreDict.AccuracyLevel.fast);
        CommunityCustomization custom = new CommunityCustomization(settings);
        return new PreDict(custom);
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
}
