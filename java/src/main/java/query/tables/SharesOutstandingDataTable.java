package query.tables;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class SharesOutstandingDataTable implements DataTable {
    Double data;

    public Double getSharesOutstanding() {
        return data;
    }
}
