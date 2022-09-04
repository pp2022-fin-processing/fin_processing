package model;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Date;

@Data
@AllArgsConstructor
public class Period {
    Date startDate;
    Date endDate;
    String interval;
}
