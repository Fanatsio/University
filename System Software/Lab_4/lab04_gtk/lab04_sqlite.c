#include <sqlite3.h>
#include <stdio.h>
#include "lab04_sqlite.h"

int callback(void *, int, char **, char **);
void sqlite_get_data(int flag)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char sql[512]; 
     sprintf(sql, "SELECT child.id, child.fio, child.date, child.pol, doctor.id, doctor.fio,  \
                  sertificate.id, \
                  sertificate.number \
              FROM \
                  ((child \
              INNER JOIN doctor ON child.id_doctor =  doctor.id) \
              INNER JOIN sertificate ON child.id_sert = sertificate.id) WHERE child.hidden != %d;", flag);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_insert(char *fio, char* date, char * pol, int doc_id, int sert_id)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "INSERT INTO child (fio, date, pol, id_doctor, id_sert, hidden) VALUES ('%s', '%s', '%s', %d, %d, %d);", fio, date, pol, doc_id, sert_id, 0);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_delete(int childid)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }

    char sql[256];
    sprintf(sql, "UPDATE child SET hidden = %d WHERE id = %d;", 1, childid);
    rc = sqlite3_exec(db, sql, callback, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to select data\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}

void sqlite_update(int childid, char*fio, char*date, char*pol, int doc_id, int sert_id)
{
    sqlite3 *db;
    char *err_msg = 0;
    int rc;
    if (SQLITE_OK != (rc = sqlite3_open(DB_FILE, &db)))
    {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
    }


    char sql_comp[255];
    sprintf(sql_comp, "UPDATE child SET fio = '%s', date = '%s', pol = '%s', id_doctor = %d, id_sert = %d WHERE id = %d;", fio, date, pol, doc_id, sert_id, childid);
    rc = sqlite3_exec(db, sql_comp, NULL, NULL, &err_msg);
    if (rc != SQLITE_OK)
    {
        fprintf(stderr, "Failed to update data in components\n");
        fprintf(stderr, "SQLite error: %s\n", err_msg);
        sqlite3_free(err_msg);
        sqlite3_close(db);
    }
    sqlite3_close(db);
}
