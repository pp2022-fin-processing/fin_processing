package model.measures;

import java.util.ArrayList;
import java.util.List;

public class AllIterationsTimeMeasurement {

    List<OneIterationTimeMeasurement> allIterations;

    public AllIterationsTimeMeasurement() {
        this.allIterations = new ArrayList<>();
    }

    public void addIteration(OneIterationTimeMeasurement oneIteration) {
        this.allIterations.add(oneIteration);
    }

    public double calculateDataCollectionAverage() {
        return this.allIterations.stream()
                .mapToDouble(OneIterationTimeMeasurement::calculateAverageDataCollectionTime)
                .average().orElse(Double.NaN);
    }

    public double calculateCalculationsAverage() {
        return this.allIterations.stream()
                .mapToDouble(OneIterationTimeMeasurement::calculateAverageCalculationsTime)
                .average().orElse(Double.NaN);
    }
}
