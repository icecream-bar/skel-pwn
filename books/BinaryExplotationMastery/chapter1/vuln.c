#include <stdio.h>
#include <string.h>

void vulnerable_function(){
	char buffer[32];

	printf("Enter some text: ");
	gets(buffer);//deliberately unsafe

	printf("You entered: %s\n", buffer);
}

int main(){
	vulnerable_function();
	return 0;
}
