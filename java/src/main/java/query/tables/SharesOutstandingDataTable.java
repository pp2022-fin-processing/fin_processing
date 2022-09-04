package query.tables;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class SharesOutstandingDataTable implements DataTable {
    Double data;

    public static final String NET_INCOME_COLUMN_NAME = "netIncome";

    public Double getSharesOutstanding() {
        return data;
    }
}
