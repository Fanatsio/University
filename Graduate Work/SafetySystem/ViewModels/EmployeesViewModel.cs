using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using SafetySystem.Models;
using SafetySystem.Services;

namespace SafetySystem.ViewModels
{
    public class EmployeesViewModel : INotifyPropertyChanged
    {
        private bool _noDataMessageVisible;
        private ObservableCollection<Employee> _employees = [];

        public bool NoDataMessageVisible
        {
            get => _noDataMessageVisible;
            set
            {
                _noDataMessageVisible = value;
                OnPropertyChanged(nameof(NoDataMessageVisible));
            }
        }

        public ObservableCollection<Employee> Employees
        {
            get => _employees;
            set
            {
                _employees = value;
                OnPropertyChanged(nameof(Employees));
                NoDataMessageVisible = _employees == null || _employees.Count == 0;
            }
        }

        public EmployeesViewModel()
        {
            LoadEmployees();
        }

        private void LoadEmployees()
        {
            try
            {
                var employees = DatabaseService.Instance.GetEmployees();
                Console.WriteLine($"ViewModel {employees.Count} employees");
                Employees.Clear(); // Очищаем старую коллекцию
                foreach (var employee in employees)
                {
                    Employees.Add(employee); // Добавляем элементы в существующую коллекцию
                }
                // Добавьте отладочный вывод
                foreach (var emp in Employees)
                {
                    Console.WriteLine($"Employee: {emp.Name}, RFID: {emp.RfidTag}, Photo: {emp.PhotoPath}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error loading employees: {ex.Message}");
                Employees.Clear();
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}