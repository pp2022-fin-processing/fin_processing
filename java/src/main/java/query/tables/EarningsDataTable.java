package query.tables;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Map;

@Data
@AllArgsConstructor
public class EarningsDataTable implements DataTable {
    Map<String, Double> data;


    public static final String NET_INCOME_COLUMN_NAME = "netIncome";
    public static final String NET_TOTAL_ASSETS_COLUMN_NAME = "totalAssets";
    public static final String NET_TOTAL_LIABILITY_COLUMN_NAME = "totalLiab";

    public Double getNetIncome() {
        return data.get(NET_INCOME_COLUMN_NAME);
    }

    public Double getTotalAssets() {
        return data.get(NET_TOTAL_ASSETS_COLUMN_NAME);
    }

    public Double getTotalLiability() {
        return data.get(NET_TOTAL_LIABILITY_COLUMN_NAME);
    }
}
