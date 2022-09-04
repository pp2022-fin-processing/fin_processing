package model;

import lombok.Getter;

@Getter
public enum Domain {

    INDEX("indices"),
    INDEXED_COMPANY("indexed-companies"),
    IT_COMPANY("IT"),
    NON_INDEXED_COMPANY("non-indexed-companies"),
    CURRENCY("currencies");
    private final String label;

    private Domain(String label) {
        this.label = label;
    }
}
