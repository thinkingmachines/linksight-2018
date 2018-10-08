package es.thinkingmachin.linksight.imatch.matcher.model;

import de.cxp.predict.PreDict;
import de.cxp.predict.api.PreDictSettings;
import de.cxp.predict.api.SuggestItem;
import de.cxp.predict.customizing.CommunityCustomization;
import org.apache.commons.math3.util.Pair;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class FuzzyStringMap<T> {

    private final PreDict preDict;
    private final Map<String, T> strMap;

    private static int badCounts = 0;

    public FuzzyStringMap() {
        this.preDict = createPredictModel();
        this.strMap = new HashMap<>();
    }

    private PreDict createPredictModel() {
        PreDictSettings settings = new PreDictSettings();
        settings.accuracyLevel(PreDict.AccuracyLevel.fast);
        CommunityCustomization custom = new CommunityCustomization(settings);
        return new PreDict(custom);
    }

    public void put(String key, T value) {
        key = preDict.cleanIndexWord(key);
        if (strMap.containsKey(key) && strMap.get(key) != value) {
            System.out.println("WARNING: More than once instance of key '" + key + "' was added. Ignoring.");
            badCounts++;
            System.out.println("Alias Bad: " + badCounts);
        }
        strMap.putIfAbsent(key, value);
        preDict.indexWord(key);
    }

    public T getExact(String key) {
        key = preDict.cleanIndexWord(key);
        return strMap.get(key);
    }

    public List<Pair<T, Double>> getFuzzy(String key) {
        List<SuggestItem> suggestions = preDict.lookup(key);
        return suggestions.stream()
                .map(s -> new Pair<>(strMap.get(s.term), s.proximity))
                .collect(Collectors.toList());
    }

    public void addKeyAlias(String key, String alias) {
        put(alias, getExact(key));
    }
}
