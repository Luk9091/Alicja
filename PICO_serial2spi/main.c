#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <pico/stdio.h>
#include <pico/stdlib.h>

#include "led.h"

#include "spi_master.h"

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
        buffer[index] = c;
        index++;
    }
    printf("\n\r");
    buffer[index] = 0;
    return index;
}




int main(){
    stdio_init_all();
    LED_init();
    LED_on();
    printf("Run core 0\n");
    char readLine[128];




    SPI_master_init();
    while (1){
        int len = getLine(readLine);
        if (strncmp(readLine, "read", 4) == 0){
            int32_t setNum[2];
            uint numOfParam = atoli(readLine, len, setNum);

            if (numOfParam == 1){
                setNum[1] = 1;
            }


            if (numOfParam >= 1){
                if (setNum[1] > 0){
                    for(uint i = 0; i < setNum[1]; i++){
                        uint data = SPI_master_read(setNum[0]+i);
                        printf("Read from:\t0x%- 4X: 0x%X\n", setNum[0] + i, data);
                    }
                } else {
                    setNum[1] = abs(setNum[1]);
                    for(uint i = 0; i < setNum[1]; i++){
                        int32_t data = SPI_master_read(setNum[0]);
                        printf("Read from:\t0x%- 4X: 0x%X\n", setNum[0], data);
                    }
                }
                printf("OK\n");
            } else {
                printf("Syntax error\n");
            }
        }
        else if (strncmp(readLine, "write", 5) == 0){
            int32_t setNum[128];
            int numOfParam = atoli(readLine, len, setNum);
            if (numOfParam >= 2){
                for (uint i = 0; i < numOfParam - 1; i++){
                    SPI_master_write(setNum[0] + i, setNum[i+1]);
                    sleep_ms(10);
                }
                printf("OK\n");
            } else {
                printf("Syntax error\n");
            }
        } 
        else if (strncmp(readLine, "send", 4) == 0){
            int32_t setNum[128];
            int numOfParam = atoli(readLine, len, setNum);

            for (uint i = 0; i < numOfParam; i ++){
                SPI_master_send(setNum[i], i == numOfParam - 1);
                printf("Send data: 0x%hX\n", setNum[i]);
            }
        }
        else {
            printf("Syntax error\n");
        }
        sleep_ms(250);
    }
}

