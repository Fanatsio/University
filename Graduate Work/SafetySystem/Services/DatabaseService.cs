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
        private static readonly string _dbPath = "safetysystem.db";
        private static DatabaseService? _instance;
        private static readonly object _initializationLock = new();
        private static bool _isInitialized;

        public static DatabaseService Instance
        {
            get => _instance ??= new DatabaseService();
        }

        private DatabaseService()
        {
            EnsureDatabaseInitialized();
        }

        private static void EnsureDatabaseInitialized()
        {
            if (_isInitialized)
            {
                return;
            }

            lock (_initializationLock)
            {
                if (_isInitialized)
                {
                    return;
                }

                InitializeDatabase();
                _isInitialized = true;
            }
        }

        private static void InitializeDatabase()
        {
            try
            {
                using var connection = Connection;
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

        private static IDbConnection Connection
        {
            get
            {
                var fullPath = Path.GetFullPath(_dbPath);
                Console.WriteLine($"Opening database at: {fullPath}");
                return new SqliteConnection($"Data Source={fullPath}");
            }
        }

        public static void AddEmployee(Employee employee)
        {
            EnsureDatabaseInitialized();
            ArgumentNullException.ThrowIfNull(employee);
            if (string.IsNullOrEmpty(employee.EmployeeId) || string.IsNullOrEmpty(employee.RfidTag) || string.IsNullOrEmpty(employee.Name))
                throw new ArgumentException("EmployeeId, RfidTag, and Name cannot be null or empty.");

            try
            {
                using var connection = Connection;
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
            EnsureDatabaseInitialized();
            try
            {
                using var connection = Connection;
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
