#include<stdio.h>

void greet(char *name){
	char buffer[16];
	sprintf(buffer, "Hi %s", name);
}

int main(){
	greet("Alice");
	return 0;
}
