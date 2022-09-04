package query.tables;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;
import java.util.stream.Collectors;

@Data
@AllArgsConstructor
public class StockDataTable implements DataTable {
    List<List<String>> data;

    public static final int CLOSE_COLUMN = 4;
    public static final int VOLUME_COLUMN = 6;

    public List<Double> getClose() {
        return data.stream()
                .map(record -> Double.parseDouble(record.get(CLOSE_COLUMN)))
                .collect(Collectors.toList());
    }

    public List<Double> getVolume() {
        return data.stream()
                .map(record -> Double.parseDouble(record.get(VOLUME_COLUMN)))
                .collect(Collectors.toList());
    }



}
