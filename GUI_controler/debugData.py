debugAns = {
    "RS" : [
        "Board S/N: C802 Flash Timestamp: 852AD92B",
        "External power source: OK",
        "Temperature\t38.3 NORMAL",
        "Board power ON, OK",
        "Clock source PRIMARY, PLL LOCKED",
        "FPGA ready",
        "Clock system OK",
        "Last reset from SPI command",
        "GBT link ON,\tno errors"
    ],

    "RF" : [
    "CH:\t0 Treshold:\t 1.00 Shift:\t0.15 Zero offs:\t2.23 Delay\t9.112",
    "CH:\t1 Treshold:\t 2.00 Shift:\t0.00 Zero offs:\t2.20 Delay\t9.935",
    "CH:\t2 Treshold:\t 3.00 Shift:\t1.40 Zero offs:\t2.24 Delay\t10.560",
    "CH:\t3 Treshold:\t 4.00 Shift:\t0.25 Zero offs:\t1.82 Delay\t10.518",
    "CH:\t4 Treshold:\t 5.00 Shift:\t0.70 Zero offs:\t2.00 Delay\t9.803",
    "CH:\t5 Treshold:\t 6.00 Shift:\t0.20 Zero offs:\t3.11 Delay\t10.303",
    "CH:\t6 Treshold:\t 7.00 Shift:\t0.00 Zero offs:\t2.75 Delay\t11.098",
    "CH:\t7 Treshold:\t 8.00 Shift:\t0.50 Zero offs:\t3.47 Delay\t9.529",
    "CH:\t8 Treshold:\t 9.00 Shift:\t0.50 Zero offs:\t2.22 Delay\t10.105",
    "CH:\t9 Treshold:\t 10.00 Shift:\t1.20 Zero offs:\t3.37 Delay\t9.698",
    "CH:\t 10 Treshold:\t11.00 Shift:\t0.70 Zero offs:\t2.59 Delay\t10.191",
    "CH:\t 11 Treshold:\t12.00 Shift:\t0.10 Zero offs:\t1.37 Delay\t9.108",
    "Trigger window:  153",
    "CFD sat. level: 4095"
    ],

    "RA" : [
    "    0     0",
    "    0   100",
    "    0 65535",
    "    0 65520",
    "    0     0",
    "    0     0",
    "    0     0",
    "    0     0",
    "    0     0",
    "    0     0",
    "    0     0",
    "    0     0",
    "OK",
    ],

    "RT" : [
    "    -3      5     11",
    "1749   1481     13",
    "0000      0     15",
    "0C0D    781      4",
    "041B    283      5",
    "0979    633     16",
    "1141   1089     13",
    "0000      0     14",
    "007F     -1      9",
    "193F   1599      7",
    "0033     51     11",
    "007F     -1     18",
    "003F     63     20",
    "",
    "ok",
    ],

    "RZ" : [
    "    42    36     1     1",
    "    35    45     1     1",
    "    82    33     2     1",
    "    35    48     1     1",
    "    70    51     1     1",
    "    53    47     1     1",
    "    37    93     0     0",
    "    37   102     1     0",
    "    68    53     1     2",
    "    50    69     1     1",
    "    83    40     1     1",
    "    34    63     2     2",
    "OK",
    ],

    "RC" : [
    "CH:    0 Lcal: 2190 TDC:     1 Time shift:   979 Range corr: 2048  2048",
    "CH:    1 Lcal: 2240 TDC:     2 Time shift:   958 Range corr: 2048  2048",
    "CH:    2 Lcal: 2200 TDC:     3 Time shift:   930 Range corr: 2048  2048",
    "CH:    3 Lcal: 2420 TDC:     4 Time shift:   932 Range corr: 2048  2048",
    "CH:    4 Lcal: 2500 TDC:     5 Time shift:   980 Range corr: 2048  2048",
    "CH:    5 Lcal: 2365 TDC:     6 Time shift:  1022 Range corr: 2048  2048",
    "CH:    6 Lcal: 2780 TDC:     7 Time shift:   915 Range corr: 2048  2048",
    "CH:    7 Lcal: 2420 TDC:     8 Time shift:  1021 Range corr: 2048  2048",
    "CH:    8 Lcal: 2225 TDC:     9 Time shift:  1020 Range corr: 2048  2048",
    "CH:    9 Lcal: 2490 TDC:    10 Time shift:  1048 Range corr: 2048  2048",
    "CH:   10 Lcal: 2190 TDC:    11 Time shift:   969 Range corr: 2048  2048",
    "CH:   11 Lcal: 2300 TDC:    12 Time shift:   968 Range corr: 2048  2048",
    ],
}





def debugData(data: str) -> tuple[int, list[str]]:
    data = data.upper()
    try:
        return len(debugAns[data]), debugAns[data]
    except IndexError:
        return 0, ""