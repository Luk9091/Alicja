#ifndef __DMA_CONFIG_H__
#define __DMA_CONFIG_H__


#include <hardware/dma.h>
#define DATA_SIZE       (1024)
#define DATA_BIT_SIZE   10



uint DMA_PIOconfig(volatile void *writeData, const volatile void *readData, uint dreq);
void DMA_setEnable(uint dmaChannel, bool enable);

uint dma_getCurrentIndex(uint dmaChannel);
// uint dma_getCurrentIndex(uint dmaChannel, uint *dataArray);

#endif // __DMA_CONFIG_H__