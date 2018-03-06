#define F_CPU 20000000

#include <avr/io.h>
#include <util/delay.h>

#define sbi(x,y) x |= _BV(y)
#define cbi(x,y) x &= ~(_BV(y))
#define tbi(x,y) x ^= _BV(y)
#define is_high(x,y) (x & _BV(y) == _BV(y))

void set_pin_mode(int ind, bool value) {
	int tv = ind / 8;
	if (value) {
		if (tv==0) {
			sbi(DDRD, ind-(tv * 8));
		}
		if (tv==1) {
			sbi(DDRB, ind-(tv * 8));
		}
/*		if (tv==2) {
			sbi(DDRC, ind-(tv * 8));
		}
		if (tv==3) {
			sbi(DDRD, ind-(tv * 8));
		}
*/	}
	else {
		if (tv==0) {
			cbi(DDRD, ind-(tv * 8));
		}
		if (tv==1) {
			cbi(DDRB, ind-(tv * 8));
		}
/*		if (tv==2) {
			cbi(DDRC, ind-(tv * 8));
		}
		if (tv==3) {
			cbi(DDRD, ind-(tv * 8));
		}
*/	}
}

void set_pin(int ind, bool value) {
	int tv = ind / 8;
	if (value) {
		if (tv==0) {
			sbi(PORTD, ind-(tv * 8));
		}
		if (tv==1) {
			sbi(PORTB, ind-(tv * 8));
		}
/*		if (tv==2) {
			sbi(PORTC, ind-(tv * 8));
		}
		if (tv==3) {
			sbi(PORTD, ind-(tv * 8));
		}
*/	} else {
		if (tv==0) {
			cbi(PORTD, ind-(tv * 8));
		}
		if (tv==1) {
			cbi(PORTB, ind-(tv * 8));
		}
/*		if (tv==2) {
			cbi(PORTC, ind-(tv * 8));
		}
		if (tv==3) {
			cbi(PORTD, ind-(tv * 8));
		}
*/	}
}


bool test_pin(int ind) {
	int tv = ind / 8;
	if (tv==0) {
		return is_high(PIND, ind-(tv * 8));
	}
	if (tv==1) {
		return is_high(PINB, ind-(tv * 8));
	}
}

