using Avalonia.Controls;
using SafetySystem.ViewModels;
using System;

namespace SafetySystem.Views
{
    public partial class EmployeesWindow : Window
    {
        public EmployeesWindow()
        {
            InitializeComponent();
            DataContext = new EmployeesViewModel();
            Console.WriteLine($"DataContext set to: {DataContext?.GetType().Name}");
        }
    }
}