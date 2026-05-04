using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using Dapper;
using Microsoft.Data.Sqlite;
using SafetySystem.Models;

namespace SafetySystem.Services
{
    public class DatabaseService
    {
        private static DatabaseService? _instance;
        private static readonly object _initializationLock = new();
        private static readonly HashSet<string> _initializedDatabasePaths = [];

        public static DatabaseService Instance
        {
            get => _instance ??= new DatabaseService();
        }

        private DatabaseService()
        {
            EnsureDatabaseInitialized();
        }

        private static string EnsureDatabaseInitialized()
        {
            var dbPath = ResolveDatabasePath();

            if (_initializedDatabasePaths.Contains(dbPath))
            {
                return dbPath;
            }

            lock (_initializationLock)
            {
                if (_initializedDatabasePaths.Contains(dbPath))
                {
                    return dbPath;
                }

                InitializeDatabase(dbPath);
                _initializedDatabasePaths.Add(dbPath);
            }

            return dbPath;
        }

        private static void InitializeDatabase(string dbPath)
        {
            try
            {
                using var connection = CreateConnection(dbPath);
                connection.Open();
                connection.Execute(@"
                    CREATE TABLE IF NOT EXISTS Employees (
                        Id INTEGER PRIMARY KEY AUTOINCREMENT,
                        EmployeeId TEXT NOT NULL,
                        RfidTag TEXT NOT NULL,
                        Name TEXT NOT NULL,
                        PhotoPath TEXT
                    );
                ");

                var employeesCount = connection.ExecuteScalar<int>("SELECT COUNT(*) FROM Employees");
                if (employeesCount == 0)
                {
                    connection.Execute(@"
                        INSERT INTO Employees (EmployeeId, RfidTag, Name, PhotoPath)
                        VALUES
                            ('EMP-001', 'RFID-1001', 'Иванов Иван Иванович', 'Assets\\employee-1.jpg'),
                            ('EMP-002', 'RFID-1002', 'Петров Петр Сергеевич', 'Assets\\employee-2.jpg'),
                            ('EMP-003', 'RFID-1003', 'Сидорова Анна Викторовна', 'Assets\\employee-3.jpg');
                    ");
                    Console.WriteLine("Sample employees added.");
                }
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error initializing database: {ex.Message}");
                throw;
            }
        }

        private static IDbConnection CreateConnection(string dbPath)
        {
            Console.WriteLine($"Opening database at: {dbPath}");
            return new SqliteConnection($"Data Source={dbPath}");
        }

        private static string ResolveDatabasePath()
        {
            var configuredPath = AppSettingsService.Load().DatabasePath;
            return Path.GetFullPath(configuredPath);
        }

        public static void AddEmployee(Employee employee)
        {
            var dbPath = EnsureDatabaseInitialized();
            ArgumentNullException.ThrowIfNull(employee);
            if (string.IsNullOrEmpty(employee.EmployeeId) || string.IsNullOrEmpty(employee.RfidTag) || string.IsNullOrEmpty(employee.Name))
                throw new ArgumentException("EmployeeId, RfidTag, and Name cannot be null or empty.");

            try
            {
                using var connection = CreateConnection(dbPath);
                connection.Open();
                connection.Execute(@"
                    INSERT INTO Employees (EmployeeId, RfidTag, Name, PhotoPath)
                    VALUES (@EmployeeId, @RfidTag, @Name, @PhotoPath)
                ", employee);
                Console.WriteLine("Employee added successfully.");
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error adding employee: {ex.Message}");
                throw;
            }
        }

        public static List<Employee> GetEmployees()
        {
            var dbPath = EnsureDatabaseInitialized();
            try
            {
                using var connection = CreateConnection(dbPath);
                connection.Open();
                var employees = connection.Query<Employee>("SELECT * FROM Employees").AsList();
                Console.WriteLine($"DataBase {employees.Count} employees");
                return employees;
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error retrieving employees: {ex.Message}");
                return [];
            }
        }
    }
}
