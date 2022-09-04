package query;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;
import lombok.extern.java.Log;
import model.Period;
import model.Ticker;
import query.tables.EarningsDataTable;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Log
public class EarningsStoredData implements Provider {

    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");

    @Override
    public EarningsDataTable getData(Ticker ticker, Period period) {
        String pathToCsv = createPath(ticker);
        Map<String, Double> records = new HashMap<>();
        try (CSVReader csvReader = new CSVReader(new FileReader(pathToCsv))) {
            String[] values = null;
            String[] dates = csvReader.readNext();
            int properColumnIndex = -1;

            for (int column = 1; column < dates.length; column++) {
                try {
                    Date recordDate = formatter.parse(dates[column]);
                    if (recordDate.after(period.getStartDate()) && recordDate.before(period.getEndDate())) {
                        properColumnIndex = column;
                    }
                } catch (ParseException e) {
                    throw new RuntimeException(e);
                }
            }
            while ((values = csvReader.readNext()) != null) {
                try {
                    records.put(values[0], Double.parseDouble(values[properColumnIndex]));
                } catch (NumberFormatException e) {
                    continue;
                }
            }
        } catch (IOException | CsvValidationException e) {
            throw new RuntimeException(e);
        }
        return new EarningsDataTable(records);
    }

    private static String createPath(Ticker symbol) {
        String workingDirectory = System.getProperty("user.dir");
        return workingDirectory + File.separator + ".." + File.separator + "examples" + File.separator
                + "data" + File.separator + "earnings" + File.separator + symbol.getDomain().getLabel()
                + File.separator + symbol.getName() + ".csv";
    }


}
