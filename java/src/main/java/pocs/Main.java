package pocs;

import model.Period;
import model.measures.AllIterationsTimeMeasurement;
import model.measures.OneIterationTimeMeasurement;
import model.measures.TickerTimeMeasurement;
import query.EarningsStoredData;
import query.Provider;
import query.ShareOutstandingStoredData;
import query.StockStoredData;
import query.tables.EarningsDataTable;
import query.tables.SharesOutstandingDataTable;
import query.tables.StockDataTable;

import java.util.List;

public class Main {

    public static void main(String[] args) {
        Period period = MarketIndicators.createPeriod();

        Provider stockDataProvider = new StockStoredData();
        Provider earningsDataProvider = new EarningsStoredData();
        Provider sharesOutstandingProvider = new ShareOutstandingStoredData();

        AllIterationsTimeMeasurement allIterationsTimeMeasurement = new AllIterationsTimeMeasurement();

        System.out.println("Market measures across " + period.getStartDate() + " - " + period.getEndDate() + " time period:");

        for (int i = 0; i < 100; i++) {
            OneIterationTimeMeasurement oneIterationMeasurementsSet = new OneIterationTimeMeasurement();
            Tickers.itCompanies.forEach(ticker -> {
                long startTime = System.nanoTime();

                StockDataTable stockData = (StockDataTable) stockDataProvider.getData(ticker, period);
                EarningsDataTable financials = (EarningsDataTable) earningsDataProvider.getData(ticker, period);
                SharesOutstandingDataTable sharesOutstanding = (SharesOutstandingDataTable) sharesOutstandingProvider.getData(ticker, period);
                long timeAfterDataCollected = System.nanoTime();

                Double eps = MarketIndicators.calculateEPS(financials, sharesOutstanding);
                List<Double> pb = MarketIndicators.calculatePB(stockData, financials, sharesOutstanding);
                List<Double> pe = MarketIndicators.calculatePE(stockData, financials, sharesOutstanding);
                long timeAfterCalculations = System.nanoTime();
//                MarketIndicators.printIndicators(ticker, eps, pb, pe);

                TickerTimeMeasurement timeMeasurement = new TickerTimeMeasurement(startTime, timeAfterDataCollected, timeAfterCalculations);
                oneIterationMeasurementsSet.addMeasurement(timeMeasurement);
//                timeMeasurement.printTimeMeasurement();
            });

            allIterationsTimeMeasurement.addIteration(oneIterationMeasurementsSet);
            oneIterationMeasurementsSet.printAverageTimeMeasurement(i);
        }

        System.out.println("Average data collection time: " + allIterationsTimeMeasurement.calculateDataCollectionAverage()
                + " | Average calculations time: " + allIterationsTimeMeasurement.calculateCalculationsAverage());
    }
}
