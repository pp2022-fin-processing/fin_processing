package pocs;

import model.Period;
import query.EarningsStoredData;
import query.Provider;
import query.ShareOutstandingStoredData;
import query.StockStoredData;
import query.tables.EarningsDataTable;
import query.tables.SharesOutstandingDataTable;
import query.tables.StockDataTable;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.stream.Collectors;

public class MarketIndicators {
    public static void main(String[] args) {


        Period period = createPeriod();

        System.out.println("Market measures across " + period.getStartDate() + " - " + period.getEndDate() + "time period:");

        Provider stockDataProvider = new StockStoredData();
        Provider earningsDataProvider = new EarningsStoredData();
        Provider sharesOutstandingProvider = new ShareOutstandingStoredData();

        Tickers.itCompanies.forEach(ticker -> {
            StockDataTable stockData = (StockDataTable) stockDataProvider.getData(ticker, period);
            EarningsDataTable financials = (EarningsDataTable) earningsDataProvider.getData(ticker, period);
            SharesOutstandingDataTable sharesOutstanding = (SharesOutstandingDataTable) sharesOutstandingProvider.getData(ticker, period);
            System.out.println("Ticker: " + ticker.getName());
            System.out.println("EPS: " + calculateEPS(financials, sharesOutstanding));
            System.out.println("P/B: " + calculatePB(stockData, financials, sharesOutstanding));
            System.out.println("P/E: " + calculatePE(stockData, financials, sharesOutstanding));
        });

    }

    private static Double calculateEPS(EarningsDataTable financials, SharesOutstandingDataTable sharesOutstanding) {
        return financials.getNetIncome() / sharesOutstanding.getSharesOutstanding();
    }

    private static List<Double> calculatePB(StockDataTable stockData, EarningsDataTable financials,
                                            SharesOutstandingDataTable sharesOutstanding) {
        return stockData.getClose().stream()
                .map(closeShare -> closeShare /
                        ((financials.getTotalAssets() - financials.getTotalLiability()) / sharesOutstanding.getSharesOutstanding()))
                .collect(Collectors.toList());

    }

    private static List<Double> calculatePE(StockDataTable stockData, EarningsDataTable financials,
                                            SharesOutstandingDataTable sharesOutstanding) {
        return stockData.getClose().stream()
                .map(closeShare -> closeShare / calculateEPS(financials, sharesOutstanding))
                .collect(Collectors.toList());
    }

    private static Period createPeriod() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        try {
            return new Period(formatter.parse("2021-09-28"), formatter.parse("2021-12-31"), "1d");
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }


}
