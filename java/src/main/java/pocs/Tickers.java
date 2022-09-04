package pocs;

import model.Ticker;

import java.util.Arrays;
import java.util.List;

import static model.Domain.*;

public class Tickers {

    public static final List<Ticker> indices = Arrays.asList(
            new Ticker("S&P500", "^GSPC", INDEX),
            new Ticker("nasdaq", "^IXIC", INDEX)
    );

    public static final  List<Ticker> itCompanies = Arrays.asList(
            new Ticker("amazon", "amzn", IT_COMPANY),
            new Ticker("apple", "aapl", IT_COMPANY),
            new Ticker("google", "goog", IT_COMPANY),
            new Ticker("microsoft", "msft", IT_COMPANY),
            new Ticker("facebook", "ft", IT_COMPANY),
            new Ticker("adobe", "adbe", IT_COMPANY),
//            new Ticker("accenture", "acn", IT_COMPANY),
            new Ticker("akamai", "akam", IT_COMPANY),
            new Ticker("activision", "atvi", IT_COMPANY),
            new Ticker("autodesk", "adsk", IT_COMPANY),
            new Ticker("nvidia", "nvda", IT_COMPANY),
            new Ticker("intel", "intc", IT_COMPANY)
//            new Ticker("at&t", "t", IT_COMPANY)
//            new Ticker("tmobile", "tmus", IT_COMPANY)
    );

    public static final  List<Ticker> indexedCompanies = Arrays.asList(
            new Ticker("Apple Inc", "AAPL", INDEXED_COMPANY),
            new Ticker("Microsoft Corporation", "MSFT", INDEXED_COMPANY),
            new Ticker("Amazon.com Inc", "AMZN", INDEXED_COMPANY),
            new Ticker("Tesla Inc", "TSLA", INDEXED_COMPANY),
            new Ticker("NVIDIA Corporation", "NVDA", INDEXED_COMPANY),
            new Ticker("BorgWagner Inc", "BWA", INDEXED_COMPANY),
            new Ticker("Invesco Ltd", "IVZ", INDEXED_COMPANY),
            new Ticker("Under Armour Inc. Class A", "UA", INDEXED_COMPANY)
    );

    public static final  List<Ticker> nonIndexdCompanies = Arrays.asList(
            new Ticker("KGHM Polska Miedz S.A.", "KGHPF", NON_INDEXED_COMPANY),
            new Ticker("Ferrexpo plc", "FXPO.L", NON_INDEXED_COMPANY)
    );
}
