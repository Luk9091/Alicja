#include "interface.h"

#include <pico/stdio.h>
#include <stdio.h>
#include "spi_master.h"


int fromU1ToInt(int data, uint8_t bitSize){
    int sign = 1;
    if (data & (1 << (bitSize - 1))){
        sign = -1;
        data = ~data;
    }
    return sign * (data & ((1 << bitSize) - 1));
}

void RA_cmd(){
    uint32_t adc[12*2];
    SPI_master_read_multiple(0x0D, 12 * 2, adc);
    for (uint i = 0; i < 12; i++){
        uint16_t adc_0 = adc[i*2];
        uint16_t adc_1 = adc[i*2 + 1];
        printf("\t%hu\t%hu\n", adc_0, adc_1);
    }
    printf("OK\n");
}


void RF_cmd(){
    uint32_t data[12 * 4];
    SPI_master_read_multiple(0x80, 12 * 4, data);


    for (uint i = 0; i < 12; i++){
        uint16_t threshold_raw  = data[i*4 + 0];
        int16_t shift_raw       = data[i*4 + 1];
        int16_t offset_raw      = data[i*4 + 2];
        uint16_t delay_raw      = data[i*4 + 3];

        float threshold = threshold_raw/100.f;
        float shift     = shift_raw/100.f;
        float offset    = offset_raw/100.f;
        float delay     = delay_raw/10.f;
        printf(
            "CH:\t%2u Treshold:\t%.2f Shift:\t%4.2f\tZero offs:\t%4.2f Delay:\t%4.3f\n",
            i, threshold, shift, offset, delay
        );
    }

    uint8_t trigger_level = SPI_master_read(0x0);// & 0x7F;
    uint16_t charge_level = SPI_master_read(0x3D);// & 0x7FF;
    printf("Trigger window: %i\n", trigger_level);
    printf("CFD sat. level: %i\n", charge_level);
}


void RC_cmd(){
    uint32_t lcal_raw[12];
    uint32_t time_raw[12];
    uint32_t rangeCorrection_raw[12 * 2];

    SPI_master_read_multiple(0xB0, 12, lcal_raw);
    SPI_master_read_multiple(0x01, 12, time_raw);
    SPI_master_read_multiple(0x25, 12*2, rangeCorrection_raw);


    for (uint i = 0; i < 12; i++){
        uint16_t lcal               = lcal_raw[i];
        uint16_t time               = time_raw[i];
        uint16_t rangeCorrection_0  = rangeCorrection_raw[i*2];
        uint16_t rangeCorrection_1  = rangeCorrection_raw[i*2 + 1];

        printf(
            "CH:\t%2i Lcal:\t%u TDC:\t-- Time shift:\t%u Range corr: %hu\t%hu\n",
            i, lcal, time, rangeCorrection_0, rangeCorrection_1
        );
    }
}

// void RS_cmd(){
//     uint16_t board_SN = SPI_master_read(0xBD);
//     uint32_t timestamp = SPI_master_read(0xF7);
//     printf("Board S/N: %04X Flash Timestamp: %X\n", board_SN, timestamp);

//     // !
//     // printf("External power source: ")

//     uint32_t temperature_raw = SPI_master_read(0xFC);
//     // printf("Temperature\t")
// }


void RT_cmd(){
    int16_t TDC_phase_1_2  = SPI_master_read(0x3E);
    int8_t  TDC_phase_3    = SPI_master_read(0x3F);

    printf("\t%hi\t%hi\t%hi\n", (int8_t)(TDC_phase_1_2), (int8_t)(TDC_phase_1_2 >> 8), (int8_t)(TDC_phase_3));
        

    uint32_t TDC_raw[12];
    SPI_master_read_multiple(0x40, 12, TDC_raw);

    for (uint i = 0; i < 12; i++){
        int8_t TDC_FPGA = (int8_t)(TDC_raw[i] >> 8);
        int8_t TDC_ASIC = (int8_t)(TDC_raw[i]);

        int16_t TDC = (int16_t)(TDC_FPGA << 7) + fromU1ToInt(TDC_ASIC, 6);

        printf("%02X%02X %6i  --\n", TDC_FPGA, TDC_ASIC, TDC);
    }
    printf("OK\n");
}

void RZ_cmd(){
    uint32_t baseline_raw[12 * 2];
    uint32_t sqrt_rms_raw[12 * 2];
    SPI_master_read_multiple(0x0D, 12 * 2, baseline_raw);
    SPI_master_read_multiple(0x4C, 12 * 2, sqrt_rms_raw);

    for(uint i = 0; i < 12; i++){
        uint16_t baseline_0 = baseline_raw[i*2];
        uint16_t baseline_1 = baseline_raw[i*2 + 1];
        uint16_t rms_0      = sqrt_rms_raw[i*2];
        uint16_t rms_1      = sqrt_rms_raw[i*2 + 1];
        printf(
            "\t%hu\t%hu\t%hu\t%hu\n",
            baseline_0, baseline_1, rms_0, rms_1
        );
    }
}


void SCL_cmd(uint channel, uint32_t value){
    SPI_master_write(0xB0 + channel, value);
}

void SCT_cmd(uint channel, uint32_t value){
    SPI_master_write(0x01 + channel, value);
}

void SD_cmd(uint channel, uint32_t value){
    SPI_master_write(0x83 + channel*4, value);
}

void SL_cmd(uint channel, uint32_t value){
    SPI_master_write(0x80 + channel*4, value);
}

void SO_cmd(uint channel, uint32_t value){
    SPI_master_write(0x82 + channel*4, value);
}

void SZ_cmd(uint channel, uint32_t value){
    SPI_master_write(0x81 + channel*4, value);
}


void SS_cmd(uint32_t value){
    SPI_master_write(0x3D, value);
}

void ST_cmd(uint32_t value){
    SPI_master_write(0x00, value);
}