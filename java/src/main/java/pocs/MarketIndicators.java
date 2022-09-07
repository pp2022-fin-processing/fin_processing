package pocs;

import model.Period;
import model.Ticker;
import query.tables.EarningsDataTable;
import query.tables.SharesOutstandingDataTable;
import query.tables.StockDataTable;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.stream.Collectors;

public class MarketIndicators {


    public static Double calculateEPS(EarningsDataTable financials, SharesOutstandingDataTable sharesOutstanding) {
        return financials.getNetIncome() / sharesOutstanding.getSharesOutstanding();
    }

    public static List<Double> calculatePB(StockDataTable stockData, EarningsDataTable financials,
                                           SharesOutstandingDataTable sharesOutstanding) {
        return stockData.getClose().stream()
                .map(closeShare -> closeShare /
                        ((financials.getTotalAssets() - financials.getTotalLiability()) / sharesOutstanding.getSharesOutstanding()))
                .collect(Collectors.toList());

    }

    public static List<Double> calculatePE(StockDataTable stockData, EarningsDataTable financials,
                                           SharesOutstandingDataTable sharesOutstanding) {
        return stockData.getClose().stream()
                .map(closeShare -> closeShare / calculateEPS(financials, sharesOutstanding))
                .collect(Collectors.toList());
    }

    public static Period createPeriod() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        try {
            return new Period(formatter.parse("2021-09-28"), formatter.parse("2021-12-31"), "1d");
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }

    public static void printIndicators(Ticker ticker, Double eps, List<Double> pb, List<Double> pe) {
        System.out.println("Ticker: " + ticker.getName());
        System.out.println("EPS: " + eps);
        System.out.println("P/B: " + pb);
        System.out.println("P/E: " + pe);
    }
}
