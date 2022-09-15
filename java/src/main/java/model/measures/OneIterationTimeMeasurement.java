package model.measures;

import java.util.ArrayList;
import java.util.List;
import static model.measures.TickerTimeMeasurement.*;
public class OneIterationTimeMeasurement {
    List<TickerTimeMeasurement> timeMeasures;

    public OneIterationTimeMeasurement() {
        this.timeMeasures = new ArrayList<>();
    }

    public void addMeasurement(TickerTimeMeasurement timeMeasurement) {
        this.timeMeasures.add(timeMeasurement);
    }

    public double calculateTotalDataCollectionTime() {
        return this.timeMeasures.stream()
                .mapToDouble(TickerTimeMeasurement::getDataCollectionTime)
                .sum() / NANOSECONDS_IN_MILISECOND;
    }

    public double calculateTotalCalculationsTime() {
        return this.timeMeasures.stream()
                .mapToDouble(TickerTimeMeasurement::getCalculationsTime)
                .sum() / NANOSECONDS_IN_MILISECOND;
    }

    public double calculateAverageDataCollectionTime() {
        return this.timeMeasures.stream()
                .mapToDouble(TickerTimeMeasurement::getDataCollectionTime)
                .average().orElse(Double.NaN) /NANOSECONDS_IN_MILISECOND;
    }

    public double calculateAverageCalculationsTime() {
        return this.timeMeasures.stream()
                .mapToDouble(TickerTimeMeasurement::getCalculationsTime)
                .average().orElse(Double.NaN) / NANOSECONDS_IN_MILISECOND;
    }

    public void printAverageTimeMeasurement(int i) {
        System.out.println("Iteration " + i + ": Average data collection time: " + calculateAverageDataCollectionTime() +
                "[ms] | Average calculations time: " + calculateAverageCalculationsTime() + "[ms]");
    }

    public void printTotalTimeMeasurement(int i) {
        System.out.println("Iteration " + i + ": Total data collection time: " + calculateTotalDataCollectionTime() +
                "[ms] | Total calculations time: " + calculateTotalCalculationsTime() + "[ms]");
    }

}
