#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void unique(char s[], int c[])
{
    bool unique;
    int l = strlen(s);
    int min_i = 0, min_j = 0;
    for (int i = 0; i < l; i ++) 
        for (int j = i; j < l; j ++) 
        {
            for (int k = 0; k < 255; k++) 
            {
                c[k] = 0;
                unique = true;
            }
            for (int k = i; k <= j; k++) 
            {
                c[s[k]]++;
                if (c[s[k]] > 1) 
                {
                    unique = false;
                    break;
                }
            }
            if (unique && (j - i >= min_j - min_i)) 
            {
                min_i = i;
                min_j = j;
            }
        }
    for (int i = min_i; i <= min_j; i++)
        printf("%c", s[i]);
}

int main() 
{
    char *s = (char *)malloc(sizeof(char));
    printf("Enter -> ");
    scanf("%s", s);
    int *c = (int *)malloc(sizeof(int));
    unique(s, c);
}