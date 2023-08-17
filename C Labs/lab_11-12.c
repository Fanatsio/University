#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int Number = 4;

struct studlist{
    char surname[15]; //Фамилия
    char name[15]; //Имя
    char group[15]; //Группа
    int exam1; //Первый экзамен
    int exam2; //Второй экзамен
    int exam3; //третий экзамен
    double gpa; //grade point average(Средний балл)
}*list;

void gpa(struct studlist *list){
    for (int i = 0; i < Number; i++)
        list[i].gpa = (list[i].exam1 + list[i].exam2 + list[i].exam3) / 3.0;
}

void getgpa(struct studlist *list){
    for (int i = 0; i < Number; i++)
        if (list[i].gpa >= 4.5)
        {
            printf("%d)", i + 1);
            printf("%-*s\t", 15, list[i].surname);
            printf("%-*s\t", 15, list[i].name);
            printf("%-*s\t", 15, list[i].group);
            printf("%4d ", list[i].exam1);
            printf("%4d ", list[i].exam2);
            printf("%4d    ", list[i].exam3);
            printf("%4lf\n", list[i].gpa);
        }
}

void insert1(struct studlist *list){
    int in;
    for (;;) {
        Number++;
        list = realloc(list, 100 * sizeof(struct studlist));
        if (NULL == list){
            printf("Error");
            exit(1);
        }
        
        char *data_input = (char *)malloc(sizeof(char));
        
        gets(data_input);
        
        printf("Enter surname -> ");
        gets(data_input);
        strncpy(list[Number - 1].surname, data_input, 15);
        
        printf("Enter name -> ");
        gets(data_input);
        strncpy(list[Number - 1].name, data_input, 15);
        
        printf("Enter group -> ");
        gets(data_input);
        strncpy(list[Number - 1].group, data_input, 15);
        
        printf("Enter exam1 -> ");
        scanf("%d", &list[Number - 1].exam1);;
        
        printf("Enter exam2 -> ");
        scanf("%d", &list[Number - 1].exam2);
        
        printf("Enter exam3 -> ");
        scanf("%d", &list[Number - 1].exam3);
        
        printf("add more string ?\nEnter‚Yes - 1 / No - 2\n");
        scanf("%d", &in);
        
        free(data_input);
        
        if (in == 1)
          continue;
        else
          break;
    }
    printf("---------------\n");
    output(list);
}

void delete2(struct studlist *list){
    int n;
    printf("Enter string number -> ");
    scanf("%d", &n);
    
    for (int i = n - 1; i < Number; i++)
        list[i] = list[i + 1];
            
    Number--;
    list = realloc(list, 100 * sizeof(struct studlist));
    if (NULL == list){
        printf("Error");
        exit(1);
    }
    printf("---------------\n");
    output(list);
}

void output(struct studlist *list){
    gpa(list);
    for (int i = 0; i < Number; i++)
    {
        printf("%d) ", i + 1);
        printf("%-*s\t", 15, list[i].surname);
        printf("%-*s\t", 15, list[i].name);
        printf("%-*s\t", 15, list[i].group);
        printf("%4d ", list[i].exam1);
        printf("%4d ", list[i].exam2);
        printf("%4d    ", list[i].exam3);
        printf("%4f\n", list[i].gpa);
    }
}

void load4(FILE *fp, struct studlist *list){
    fp = fopen("text.txt", "r");
    if (fp == NULL)
    {
        printf("ERROR\n");
        exit(1);
    }
    
    char str[255];
    char num[255];
    char *istr;

    for (int i = 0; ; i++){
        if (i == Number)
            break;
        fgets(str, 256, fp);
        
        istr = strtok(str, "|");
        Number = atoi(istr);
            
        istr = strtok(NULL, "|");
        sprintf(list[i].surname, "%s", istr);
            
        istr = strtok(NULL, "|");
        sprintf(list[i].name, "%s", istr);
            
        istr = strtok(NULL, "|");
        sprintf(list[i].group, "%s", istr);
            
        istr = strtok(NULL, "|");
        list[i].exam1 = atoi(istr);
            
        istr = strtok(NULL, "|");
        list[i].exam2 = atoi(istr);
            
        istr = strtok(NULL, "|");
        list[i].exam3 = atoi(istr);
            
        istr = strtok(NULL, "|");
        list[i].gpa = atoi(istr);
    }
    
    printf("Number = %d\n", Number);
    output(list);
    fclose(fp);
}

void save3(FILE *fp, struct studlist *list){
    fp = fopen("text.txt", "w");
    if (fp == NULL)
    {
        printf("ERROR\n");
        exit(1);
    }
    
    for (int i = 0; i < Number; i++)
        fprintf(fp, "%d|%s|%s|%s|%d|%d|%d|%lf\n", Number, list[i].surname, list[i].name, list[i].group, list[i].exam1, list[i].exam2, list[i].exam3, list[i].gpa);
        

    fclose(fp);
}

int main(){
    int l;
    FILE *fp = NULL;
    
    struct studlist *list = (struct studlist *)malloc(100 * sizeof(struct studlist));
    if (NULL == list)
    {
        printf("Error");
        exit(1);
    }
    
    strncpy(list[0].surname, "Rechuk", 15);
    strncpy(list[0].name, "Dmitrii", 15);
    strncpy(list[0].group, "606-11", 15);
    list[0].exam1 = 5;
    list[0].exam2 = 4;
    list[0].exam3 = 5;

    strncpy(list[1].surname, "Koplova", 15);
    strncpy(list[1].name, "Anna", 15);
    strncpy(list[1].group, "111-11", 15);
    list[1].exam1 = 5;
    list[1].exam2 = 5;
    list[1].exam3 = 5;

    strncpy(list[2].surname, "Shelkov", 15);
    strncpy(list[2].name, "Egor", 15);
    strncpy(list[2].group, "222-11", 15);
    list[2].exam1 = 4;
    list[2].exam2 = 4;
    list[2].exam3 = 5;

    strncpy(list[3].surname, "Komorov", 15);
    strncpy(list[3].name, "Maxim", 15);
    strncpy(list[3].group, "333-11", 15);
    list[3].exam1 = 4;
    list[3].exam2 = 4;
    list[3].exam3 = 4;
    
    for (;;)
    {
        printf("---------------\n");
        printf("Menu\n 1-add\n 2-delete\n 3-save\n 4-load\n 5-print\n 6-gpa\n 7-exit \n");
        printf("---------------\n");
        scanf("%d", &l);
        printf("---------------\n");
        fflush(stdin);

        switch (l)
        {
            case 1:
                insert1(list);
                break;
            case 2:
                delete2(list);
                break;
            case 3:
                save3(fp, list);
                break;
            case 4:
                load4(fp, list);
                break;
            case 5:
                output(list);
                break;
            case 6:
                getgpa(list);
                break;
            case 7:
                return 0;
            default:
                printf("You entered an incorrect value");
        }
    }
    
    free(list);
    
    return 0;
}