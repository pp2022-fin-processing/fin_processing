package query;

import model.Period;
import model.Ticker;
import query.tables.DataTable;

public interface Provider {

    DataTable getData(Ticker symbol, Period period);

}
