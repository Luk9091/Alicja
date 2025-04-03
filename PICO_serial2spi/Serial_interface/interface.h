#ifndef __SERIAL_INTERFACE_H__
#define __SERIAL_INTERFACE_H__

#include <pico/stdio.h>


// TODO: RS -- read and analyze asm :C
// TODO: RT -- third line


void RA_cmd();
void RF_cmd();
void RC_cmd();
// void RS_cmd();
void RT_cmd();
void RZ_cmd();


void SCL_cmd(uint channel, uint32_t data);
void SCT_cmd(uint channel, uint32_t data);
void SD_cmd(uint channel, uint32_t data);
void SL_cmd(uint channel, uint32_t data);
void SO_cmd(uint channel, uint32_t data);
void SZ_cmd(uint channel, uint32_t data);
void SS_cmd(uint32_t data);
void ST_cmd(uint32_t data);




#endif