using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace SafetySystem.Models
{
    public class Employee : INotifyPropertyChanged
    {
        private int _id;
        private string? _employeeId;
        private string? _rfidTag;
        private string? _name;
        private string? _photoPath;

        public int Id
        {
            get => _id;
            set { _id = value; OnPropertyChanged(); }
        }

        public string? EmployeeId
        {
            get => _employeeId;
            set { _employeeId = value; OnPropertyChanged(); }
        }

        public string? RfidTag
        {
            get => _rfidTag;
            set { _rfidTag = value; OnPropertyChanged(); }
        }

        public string? Name
        {
            get => _name;
            set { _name = value; OnPropertyChanged(); }
        }

        public string? PhotoPath
        {
            get => _photoPath;
            set { _photoPath = value; OnPropertyChanged(); }
        }

        public void Validate()
        {
            if (string.IsNullOrEmpty(EmployeeId)) throw new ArgumentException("EmployeeId cannot be null or empty.");
            if (string.IsNullOrEmpty(RfidTag)) throw new ArgumentException("RfidTag cannot be null or empty.");
            if (string.IsNullOrEmpty(Name)) throw new ArgumentException("Name cannot be null or empty.");
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged([CallerMemberName] string? propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}