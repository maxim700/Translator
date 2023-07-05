#include <stdio.h>

int main(void) {
	int a = 1;
	int b = 3;
	int maximum = 0;
	if ((a > b)) {
		maximum = a;
	} else if ((b > a)) {
		maximum = b;
	} else {
		for (int i=1; i<10; i+=5) {
			a += maximum;
		}
	}
}