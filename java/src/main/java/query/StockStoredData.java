package query;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;
import lombok.extern.java.Log;
import model.Period;
import model.Ticker;
import query.tables.StockDataTable;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.LogRecord;

@Log
public class StockStoredData implements Provider {

    SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");

    @Override
    public StockDataTable getData(Ticker ticker, Period period) {
        String pathToCsv = createPath(ticker);
        List<List<String>> records = new ArrayList<>();
        try (CSVReader csvReader = new CSVReader(new FileReader(pathToCsv))) {
            String[] values;
            csvReader.skip(1);
            while ((values = csvReader.readNext()) != null) {
                Date recordDate = formatter.parse(values[0]);
                if (period.getStartDate().after(recordDate)) {
                    continue;
                } else if (period.getEndDate().before(recordDate)) {
                    break;
                } else {
                    records.add(Arrays.asList(values));
                }
            }
        } catch (CsvValidationException | IOException e) {
            throw new RuntimeException(e);
        } catch (ParseException e) {
            log.log(new LogRecord(Level.SEVERE, "Improper date format in stored .csv file: " + pathToCsv));
            throw new RuntimeException(e);
        }
        return new StockDataTable(records);
    }

    private static String createPath(Ticker symbol) {
        String workingDirectory = System.getProperty("user.dir");
        return workingDirectory + File.separator + ".." + File.separator + "examples" + File.separator
                + "data" + File.separator + "shares" + File.separator + symbol.getDomain().getLabel()
                + File.separator + symbol.getName() + ".csv";
    }


}
