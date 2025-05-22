using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using Dapper;
using Microsoft.Data.Sqlite;
using SafetySystem.Models;

namespace SafetySystem.Services
{
    public class DatabaseService
    {
        private static readonly string _dbPath = "safetysystem.db";
        private static DatabaseService? _instance;

        public static DatabaseService Instance
        {
            get => _instance ??= new DatabaseService();
        }

        private DatabaseService()
        {
            if (!File.Exists(_dbPath))
            {
                InitializeDatabase();
            }
        }

        private void InitializeDatabase()
        {
            try
            {
                using var connection = GetConnection();
                connection.Open();
                var tableExists = connection.ExecuteScalar<int>("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Employees'") > 0;
                if (!tableExists)
                {
                    connection.Execute(@"
                        CREATE TABLE Employees (
                            Id INTEGER PRIMARY KEY AUTOINCREMENT,
                            EmployeeId TEXT NOT NULL,
                            RfidTag TEXT NOT NULL,
                            Name TEXT NOT NULL,
                            PhotoPath TEXT
                        );
                    ");
                    Console.WriteLine("Employees table created.");
                }
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error initializing database: {ex.Message}");
                throw;
            }
        }

        private static IDbConnection GetConnection()
        {
            var fullPath = Path.GetFullPath(_dbPath);
            Console.WriteLine($"Opening database at: {fullPath}");
            return new SqliteConnection($"Data Source={fullPath}");
        }

        public void AddEmployee(Employee employee)
        {
            if (employee == null)
                throw new ArgumentNullException(nameof(employee));
            if (string.IsNullOrEmpty(employee.EmployeeId) || string.IsNullOrEmpty(employee.RfidTag) || string.IsNullOrEmpty(employee.Name))
                throw new ArgumentException("EmployeeId, RfidTag, and Name cannot be null or empty.");

            try
            {
                using var connection = GetConnection();
                connection.Open();
                connection.Execute(@"
                    INSERT INTO Employees (EmployeeId, RfidTag, Name, PhotoPath)
                    VALUES @EmployeeId, @RfidTag, @Name, @PhotoPath)
                ", employee);
                Console.WriteLine("Employee added successfully.");
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error adding employee: {ex.Message}");
                throw;
            }
        }

        public List<Employee> GetEmployees()
        {
            try
            {
                using var connection = GetConnection();
                connection.Open();
                var employees = connection.Query<Employee>("SELECT * FROM Employees").AsList();
                Console.WriteLine($"DataBase {employees.Count} employees");
                return employees;
            }
            catch (SqliteException ex)
            {
                Console.WriteLine($"Error retrieving employees: {ex.Message}");
                return new List<Employee>();
            }
        }
    }
}