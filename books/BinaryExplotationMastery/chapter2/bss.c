#include<stdio.h>

int count; //stored in .bss, defaults to 0

int main(){
	count += 5;
	printf("Count is %d\n", count);
	return 0;
}
