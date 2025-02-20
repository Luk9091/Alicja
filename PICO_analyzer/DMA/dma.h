#ifndef __DMA_CONFIG_H__
#define __DMA_CONFIG_H__


#include <hardware/dma.h>
#define DATA_SIZE       (1024)
#define DATA_BIT_SIZE   10



bool DMA_PIOconfig(void *writeAddress, const volatile void *readAddress, uint dreq, uint *dmaOut_1, uint *dmaOut_2);
void DMA_setEnable(uint dmaChannel, bool enable);

bool DMA_clear();

uint dma_getCurrentIndex(uint dmaChannel);
// uint dma_getCurrentIndex(uint dmaChannel, uint *dataArray);

#endif // __DMA_CONFIG_H__