#include "lph8836.h"

unsigned char fonts [5] = {0x3E, 0x50, 0x0A, 0x50, 0x3E};

unsigned char LCD_init_array[105] =
{  
0x00, 0x00, 0x01, 0x07, 0x00, 0x00, 0x02, 0x04, 0x00, 0x04, 0x00, 0x00,
0x0C, 0x00, 0x01, 0x0D, 0x06, 0x16, 0x1E, 0x10, 0x10, 0x03, 0x00, 0x0C,
0x0E, 0x2D, 0x1F, 0x0D, 0x06, 0x16, 0x01, 0x02, 0x15, 0x0F, 0x00, 0x00,
0x0B, 0x00, 0x00, 0x11, 0x00, 0x00, 0x06, 0x00, 0x00, 0x05, 0x00, 0x30,
0x14, 0xAF, 0x00, 0x15, 0x00, 0x00, 0x16, 0x83, 0x00, 0x17, 0xAF, 0x00,
0x20, 0x00, 0x00, 0x30, 0x00, 0x00, 0x31, 0x04, 0x00, 0x32, 0x02, 0x07,
0x33, 0x07, 0x00, 0x34, 0x00, 0x05, 0x35, 0x07, 0x03, 0x36, 0x07, 0x07,
0x37, 0x00, 0x07, 0x3A, 0x12, 0x00, 0x3B, 0x00, 0x09, 0x07, 0x00, 0x05,
0x07, 0x00, 0x25, 0x07, 0x00, 0x27, 0x07, 0x00, 0x37
};

unsigned char lph_rect_coord[6][3] = {
                                      0x74,0x00,0x16,
  									  0x76,131,0, // X2 X1 
                                      0x74,0x00,0x17, 
                                      0x76,18,10, // Y2 Y1 
                                      0x74,0x00,0x21,
                                      0x76,10,0,  // Y2 X1 
                                     };  


hitachi::hitachi (spi_drv hIo_drv)
	:spi_send(hIo_drv), h_fontbg(0x00),
	l_fontbg(0x00), h_fontcl(0xFF), l_fontcl(0xFF)
{ 
//GPIO_InitTypeDef		GPIO_InitStructure;
//
//	GPIO_InitStructure.GPIO_Pin   = GPIO_Pin_3;
//	GPIO_InitStructure.GPIO_Mode  = GPIO_Mode_Out_PP;
//	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
//	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	cs_hi
}
  
//==============================================================================

void hitachi::lph_spi_com (char lph_com)
{
	cs_lo
		spi_send(0x74);
		spi_send(0x00);
		spi_send(lph_com);
	cs_hi  
}

void hitachi::lph_spi_dat (char lph_dat_h, char lph_dat_l)
{
	cs_lo
		spi_send(0x76);
		spi_send(lph_dat_h);
		spi_send(lph_dat_l);
	cs_hi  
}


void hitachi::init()
{
unsigned char i;

	for(i = 0; i < 105; i+=3) 
	{
		lph_spi_com(LCD_init_array[i]);                 
		lph_spi_dat(LCD_init_array[i + 1], LCD_init_array[i + 2]);                 
	};   
} 
//==============================================================================
void hitachi::get_rect(char x1, char y1, char x2, char y2, char lph_or)
{
unsigned char i=0;

	lph_spi_com (0x05);
	lph_spi_dat	(0x00, lph_or);

	if (lph_or == 0x28)
	{
		lph_rect_coord[1][1] = 131 - y1;
		lph_rect_coord[1][2] = 131 - y2;
		lph_rect_coord[3][1] = x2;
		lph_rect_coord[3][2] = x1;
		lph_rect_coord[5][1] = x2;
		lph_rect_coord[5][2] = 131 - y2;
	}
	else
	{
		lph_rect_coord[1][1] = x2;
		lph_rect_coord[1][2] = x1;
		lph_rect_coord[3][1] = y2;
		lph_rect_coord[3][2] = y1;
		lph_rect_coord[5][1] = x1;
		lph_rect_coord[5][2] = y1;
	}
		  
	for(i = 0; i < 6; i++)
	{
		cs_lo
	
		spi_send (lph_rect_coord[i][0]);
		spi_send (lph_rect_coord[i][1]);
		spi_send (lph_rect_coord[i][2]);

		cs_hi
	};     
	
	lph_spi_com(0x22);

}

void hitachi::fill_rect(char hRGB, char lRGB)
{
int i;
	cs_lo
	spi_send (0x76);

	for(i = 0; i < 23232; i++)
	{
		spi_send (hRGB);
		spi_send (lRGB);
	}
	cs_hi
}

void hitachi::fill_rect_(char hRGB, char lRGB, int size)
{
int i;
	cs_lo
	spi_send (0x76);

	for(i = 0; i < size; i++)
	{
		spi_send (hRGB);
		spi_send (lRGB);
	}
	cs_hi
}

int  hitachi::fill_bitmap (unsigned char *lph_bmp_pic, int w)
{
	if((w > 0) && (lph_bmp_pic != 0))
	{
		int lph_bmp_j;
		
		cs_lo 
	
		spi_send (0x76);
    	for(lph_bmp_j = 0; lph_bmp_j < w; lph_bmp_j++)
			spi_send (lph_bmp_pic[lph_bmp_j]);
        
		cs_hi
		return 0;
	}
	else
		return 1;
}

void hitachi::set_point (char x1, char y1, char hRGB, char lRGB)
{
	get_rect(x1, y1, x1 + 1, y1 + 1, 0x30);
	lph_spi_dat(hRGB, lRGB);
}

void hitachi::put_char (char x, char y, char ch, char lph_or)
{
//	get_rect(0, 0, 5, 8, lph_or_0);
// 
//	cs_lo
//		spi_send (0x76);
//		spi_send (0xFF);
//		spi_send (0xFF);
//	cs_hi   
//
//	cs_lo
//		spi_send (0x76);
//		spi_send (0xFF);
//		spi_send (0xFF);
//	cs_hi   

}	 
