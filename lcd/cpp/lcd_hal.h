#ifndef __lcd_hal__
#define __lcd_hal__

#include "STM32F10x.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"
#include "stm32f10x_spi.h"

#include "lph8836.h"

unsigned char lcd_spi_send (unsigned char data);
void lcd_spi_init (void);
 
#endif
