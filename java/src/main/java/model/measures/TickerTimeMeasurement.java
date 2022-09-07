package model.measures;

import lombok.Getter;

@Getter
public class TickerTimeMeasurement {
    private long dataCollectionTime;
    private long calculationsTime;
    static final long NANOSECONDS_IN_MILISECOND = (long) 10e6;

    public TickerTimeMeasurement(long startTime, long timeAfterDataCollected, long timeAfterCalculations) {
        this.dataCollectionTime = timeAfterDataCollected - startTime;
        this.calculationsTime = timeAfterCalculations - timeAfterDataCollected;
    }

    public double getDataCollectionTimeInMs() {
        return (double) this.dataCollectionTime / NANOSECONDS_IN_MILISECOND;
    }

    public double getCalculationsTimeInMs() {
        return (double) this.calculationsTime / NANOSECONDS_IN_MILISECOND;
    }

    public void printTimeMeasurement() {
        System.out.println("Data collection time: " + getDataCollectionTimeInMs() + "[ms]");
        System.out.println("Calculations time: " + getCalculationsTimeInMs() + "[ms]");
        System.out.println();
    }

}
