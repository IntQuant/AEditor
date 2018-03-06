#define F_CPU 20000000

#include <avr/io.h> //standard include for ATMega16
#include <util/delay.h>

#define sbi(x,y) x |= _BV(y) //set bit - using bitwise OR operator 
#define cbi(x,y) x &= ~(_BV(y)) //clear bit - using bitwise AND operator
#define tbi(x,y) x ^= _BV(y) //toggle bit - using bitwise XOR operator
#define is_high(x,y) (x & _BV(y) == _BV(y)) //check if the y'th bit of register 'x' is high ... test if its AND with 1 is 1

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

int main(void) { 
set_pin_mode(10, true);
for (;;) {}
}