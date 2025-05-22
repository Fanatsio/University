#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

#define END 27

int mygetch() {
    struct termios oldt, newt;
    int c;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    c = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return c;
}

int main(){
    int a;
    while (mygetch() != END){
        int res = scanf("%d", &a);
        if(res)
            printf("Вещественное число\n");
        else
            printf("Не число\n");
        if (mygetch() == END)
            break;
    }
    return 0;
}
