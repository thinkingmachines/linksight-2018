package es.thinkingmachin.linksight.imatch.matcher.scoring;

import es.thinkingmachin.linksight.imatch.matcher.core.Address;
import es.thinkingmachin.linksight.imatch.matcher.core.Interlevel;

public abstract class WeightedScoring implements Scoring {

    // Weighted average es.thinkingmachin.linksight.imatch.matcher.scoring
    private final double firstItemRatioWeight = 6;
    private final double otherItemsRatioWeight = 4;

    // Other scores
    private final double adminLevelMismatchPenalty = 0.8;

    public abstract double getSimilarity(String search, String candidate);

    public abstract double getAbsenceScore();

    @Override
    public double getScore(Address search, Address candidate) {
        return getScore(search, candidate, false);
    }

    public double getScore(Address search, Address candidate, boolean verbose) {
//        Address searchDebug = new Address(new String[]{"Poblacion (Carmen)", "CARMEN", "Agusan del Norte"}, Interlevel.BARANGAY);

//        if (search.equals(searchDebug)) {
//            verbose = true;
//            System.out.println("-----------");
//            System.out.println(search);
//        }

        double adminLevelScore = (search.minLevel == candidate.minLevel) ? 1 : adminLevelMismatchPenalty;
        double totalWeight = 0;
        double totalScore = 0;
        for (int i = 0; i < Interlevel.values().length; i++) {
            double itemWeight = (i == 0) ? firstItemRatioWeight : otherItemsRatioWeight;
            String searchTerm = search.getTerm(i);
            String candidateTerm = candidate.getTerm(i, true);
            if (searchTerm == null && candidateTerm == null) {
                // If both terms absent, ignore
            } else if (searchTerm == null || candidateTerm == null) {
                totalScore += getAbsenceScore() * itemWeight;
                totalWeight += itemWeight;
            } else {
                totalScore += getSimilarity(searchTerm, candidateTerm) * itemWeight;
                totalWeight += itemWeight;
            }
        }
        if (verbose) {
            System.out.println("Total score: "+totalScore);
            System.out.println("Total weight: "+totalWeight);
//            throw new Error("");
        }
        double score = (totalScore / totalWeight) * adminLevelScore;
//        if (verbose && search.equals(searchDebug)) {
//            System.out.println(candidate+" score: "+score);
////            throw new Error("score: "+score);
//        }
        return score;
    }
}
