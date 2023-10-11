#ifndef DATABASE_H
#define DATABASE_H

#include <QDate>
#include <QDebug>
#include <QFile>
#include <QObject>
#include <QSql>
#include <QSqlDatabase>
#include <QSqlError>
#include <QSqlQuery>

#define DATABASE_HOSTNAME "ExampleDataBase"
#define DATABASE_NAME "maks.db"

#define TABLE_DOCTOR "doctor"
#define DOC_ID "id"
#define DOC_FIO "fio"
#define DOC_PROF "profession"


#define TABLE_CHILD "child"
#define CHILD_ID "id"
#define CHILD_FIO "fio"
#define CHILD_DATE "date"
#define CHILD_POL "pol"

#define TABLE_SERT "sertificate"
#define SERT_ID "id"
#define SERT_NUMBER "number"



class DataBase : public QObject
{
    Q_OBJECT
  public:
    explicit DataBase(QObject *parent = nullptr);
    ~DataBase();
    void connectToDataBase();
    bool inserIntoMainTable(const QVariantList &data);
    bool inserIntoDeviceTable(const QVariantList &data);

  private:
    QSqlDatabase db;

  private:
    bool openDataBase();
    bool restoreDataBase();
    void closeDataBase();
    bool createMainTable();
    bool createDeviceTable();
};

#endif   // DATABASE_H
