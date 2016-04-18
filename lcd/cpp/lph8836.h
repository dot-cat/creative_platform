//=====================LCD LPH8836 Hitachi Driver By FIOS=======================
//===========================Version 1 =========================================
//=========================MCU: ATMEL AT91SAMXXXXX==============================
#ifndef __lph8836_h__
#define __lph8836_h__

#include "stm32f10x_gpio.h"				  //
#include "stm32f10x.h"
										  // HAL
#define cs_lo	GPIOA->BRR  = 1 << 4;	  //
#define cs_hi	GPIOA->BSRR = 1 << 4;	  //

#define  lph_or_90  0x28
#define  lph_or_0   0x30

class hitachi 
{
private:
	typedef unsigned char(*spi_drv)(unsigned char data_byte);

	spi_drv		spi_send; 

	char h_fontbg;
	char l_fontbg;
	char h_fontcl;
	char l_fontcl;
	
	void lph_spi_com (char lph_com);
	void lph_spi_dat (char lph_dat_h, char lph_dat_l);

public:  
  
	hitachi (spi_drv hIo_drv);
    
    
	void init    ();
	void get_rect    (char x1, char y1, char x2, char y2, char lph_or);
	void fill_rect   (char hRGB, char lRGB);
	void fill_rect_  (char hRGB, char lRGB, int size);
	int  fill_bitmap (unsigned char *lph_bmp_pic, int w);
	void set_point 	 (char x1, char y1, char hRGB, char lRGB);
	void put_char  	 (char x, char y, char ch, char lph_or);
};

#endif

















/*void print_char (char x, char y, char txt)
{
  int lph_i, lph_j;
  char lph_tmp, lph_tmp1;
 
  get_rect (x , y, x + 4, y + 7);
   
   lph_Pio -> PIO_CODR |= lph_cs;
   spi_send (0x76);
   
   for (lph_i = 0; lph_i < 8; lph_i ++)
   {
     lph_tmp = ascii_tab[txt][lph_i];
     for (lph_j = 0; lph_j < 5; lph_j++)
     {
       lph_tmp1 = lph_tmp | 0xEF;
       if (lph_tmp1 == 0xEF )
       {
        spi_send(h_fontbg);
        spi_send(l_fontbg);
       }
       else
       {
        spi_send(h_fontcl);
        spi_send(h_fontcl);
       }
       lph_tmp = lph_tmp << 1;
     }
   }
   lph_Pio -> PIO_SODR |= lph_cs;
} 
*/
