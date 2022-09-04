package model;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Ticker {
    String name;
    String symbol;
    Domain domain;
}
