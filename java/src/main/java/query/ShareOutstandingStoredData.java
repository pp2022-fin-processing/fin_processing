package query;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;
import lombok.extern.java.Log;
import model.Period;
import model.Ticker;
import query.tables.SharesOutstandingDataTable;

import javax.swing.text.DateFormatter;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;
import java.util.Date;

@Log
public class ShareOutstandingStoredData implements Provider {
    SimpleDateFormat formatter = new SimpleDateFormat("yyyy");

    @Override
    public SharesOutstandingDataTable getData(Ticker ticker, Period period) {
        String pathToCsv = createPath(ticker);
        Double value = null;
        try (CSVReader csvReader = new CSVReader(new FileReader(pathToCsv))) {
            String[] values = null;
            csvReader.skip(1);
            while ((values = csvReader.readNext()) != null) {
                try {
                    Calendar recordDate = Calendar.getInstance();
                    recordDate.setTime(formatter.parse(values[0]));
                    LocalDate periodDate = period.getStartDate().toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
                    if (recordDate.get(Calendar.YEAR) == periodDate.getYear()) {
                        value = Double.parseDouble(values[1]);
                    }
                } catch (NumberFormatException e) {
                    continue;
                }
            }

        } catch (IOException | CsvValidationException | ParseException e) {
            throw new RuntimeException(e);
        }
        return new SharesOutstandingDataTable(value);
    }

    private static String createPath(Ticker symbol) {
        String workingDirectory = System.getProperty("user.dir");
        return workingDirectory + File.separator + ".." + File.separator + "examples" + File.separator
                + "data" + File.separator + "earnings" + File.separator + symbol.getDomain().getLabel() + "-shares-outstanding"
                + File.separator + symbol.getName() + ".csv";
    }


}
