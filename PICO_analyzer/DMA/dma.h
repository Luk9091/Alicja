#ifndef __DMA_CONFIG_H__
#define __DMA_CONFIG_H__


#include <hardware/dma.h>
#define DATA_SIZE       (1024*8)



uint DMA_PIOconfig(volatile void *writeData, const volatile void *readData, uint dreq);
void DMA_setEnable(uint dmaChannel, bool enable);


#endif // __DMA_CONFIG_H__