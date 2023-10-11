#ifndef LAB04_SQLITE_H
#define LAB04_SQLITE_H

#define DB_FILE "maks.db"

void sqlite_insert(char *fio, char* date, char * pol, int doc_id, int sert_id);
void sqlite_delete(int);
void sqlite_get_data(int);
void sqlite_update(int childid, char*fio, char*date, char*pol, int doc_id, int sert_id);

#endif
