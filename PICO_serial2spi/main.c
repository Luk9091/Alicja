#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pico/stdio.h>
#include <pico/stdlib.h>

#include "led.h"

#include "spi_master.h"
#include "interface.h"

#include "util.h"




int atoli(char *str, size_t str_len, int32_t *list){
    int index = 0;
    int value = 0;
    int sign = 1;
    int base = 10;


    bool find = false;
    for (uint i = 0; i < str_len; i++){
        char c = str[i];
        if (c == 0) break;
        if (c >='0' && c <= '9'){
            find = true;
            if (i > 0 && str[i-1] == '-'){
                sign = -1;
            }
            if (c == '0' && str[i+1] == 'x'){
                base = 16;
                i++;
                continue;
            }

            value = value * base +  (c - '0');
        } else if (base == 16 && c >= 'a' && c <= 'f'){
            str[i] = c - 'a' + 'A';
            i--;
            continue;
        } else if (base == 16 && c >= 'A' && c <= 'F'){
            value = value * base +  (c - 'A' + 10);
        } else {
            if (find == true){
                list[index] = sign * value;
                sign = 1;
                value = 0;
                base = 10;
                index++;
            }
            find = false;
        }

    }
    if (find == true){
        list[index] = sign * value;
        index++;
    }
    return index;
}

int getLine(char *buffer){
    char c = 0;
    int index = 0;
    while (c != '\n' && c != '\r'){
        c = getchar();
        if (c == '\x08' || c == '\x7F'){
            putchar(0x08);
            putchar(' ');
            putchar(0x08);
            index--;
            continue;
        }
        putchar(c);
        if (c >= 'A' && c <= 'Z'){
            c = c -'A' + 'a';
        }
        buffer[index] = c;
        index++;
    }
    printf("\n\r");
    buffer[index] = 0;
    return index;
}


int readAndDisplay(uint16_t address, uint count){
    uint32_t *data = (uint32_t*)(malloc(count * sizeof(uint32_t)));
    if (data == NULL) return -1;

    SPI_master_read_multiple(address, count, data);

    for (uint i = 0; i < count; i++){
        printf("Read from:\t0x%- 4X: %u\n", address + i, data[i]);
    }

    free(data);
    return 0;
}

int fifoReadAndDisplay(uint16_t address, uint count){
    uint32_t *data = (uint32_t*)(malloc(count * sizeof(uint32_t)));
    if (data == NULL) return -1;

    SPI_master_read_multiple(address, count, data);


    for (uint i = 0; i < count; i++){
        printf("Read:\t0x%- 4X: %u\n", i, data[i]);
    }

    free(data);
    return 0;
}



int main(){
    stdio_init_all();
    LED_init();
    LED_on();
    printf("Run core 0\n");
    char readLine[128];




    SPI_master_init();
    int32_t setNum[128];
    while (1){
        int len = getLine(readLine);
        if (
            strncmp(readLine, "read", 4) == 0
        ){
            uint numOfParam = atoli(readLine, len, setNum);

            if (numOfParam == 1){
                setNum[1] = 1;
            }


            if (numOfParam >= 1 && setNum[0] >= 0 && setNum[1] > 0){
                readAndDisplay(setNum[0], setNum[1]);
                printf("OK\n");
            } else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "fread", 5) == 0){
            uint numOfParam = atoli(readLine, len, setNum);

            if (numOfParam == 1){
                setNum[1] = 1;
            }


            if (numOfParam >= 1 && setNum[0] >= 0 && setNum[1] > 0){
                fifoReadAndDisplay(setNum[0], setNum[1]);
                printf("OK\n");
            } else {
                printf("Syntax error\n");
            }

        }
        else if (
            strncmp(readLine, "write", 5) == 0 ||
            strncmp(readLine, "fwrite", 6) == 0
        ){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam >= 2){
                SPI_master_write_multiple(setNum[0], numOfParam-1, setNum + 1);
                printf("OK\n");
            } else {
                printf("Syntax error\n");
            }
        } 
        else if (strncmp(readLine, "ra", 2) == 0){
            RA_cmd();
        }
        else if (strncmp(readLine, "rf", 2) == 0){
            RF_cmd();
        }
        else if (strncmp(readLine, "rc", 2) == 0){
            RC_cmd();
        }
        else if (strncmp(readLine, "rs", 2) == 0){
            printf("Not implemented\n");
            // RF_cmd();
        }
        else if (strncmp(readLine, "rt", 2) == 0){
            RT_cmd();
        }
        else if (strncmp(readLine, "rz", 2) == 0){
            RZ_cmd();
        }
        else if (strncmp(readLine, "scl", 3) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SCL_cmd(setNum[0], setNum[1]);
                printf("OK");
            } 
            else {
                printf("Syntax error\n");
            }

        }
        else if (strncmp(readLine, "sct", 3) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SCT_cmd(setNum[0], setNum[1]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "sd", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SD_cmd(setNum[0], setNum[1]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "sl", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SL_cmd(setNum[0], setNum[1]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "so", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SO_cmd(setNum[0], setNum[1]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "sz", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 2){
                SZ_cmd(setNum[0], setNum[1]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "ss", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 1){
                SS_cmd(setNum[0]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "st", 2) == 0){
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam == 1){
                ST_cmd(setNum[0]);
                printf("OK");
            }
            else {
                printf("Syntax error\n");
            }
        }

        // else if (strncmp(readLine, "send", 4) == 0){
        //     int32_t setNum[128];
        //     int numOfParam = atoli(readLine, len, setNum);

        //     for (uint i = 0; i < numOfParam; i ++){
        //         SPI_master_send(setNum[i], i == numOfParam - 1);
        //         printf("Send data: 0x%hX\n", setNum[i]);
        //     }
        // }
        else {
            printf("Syntax error\n");
        }
        sleep_ms(250);
    }
}

