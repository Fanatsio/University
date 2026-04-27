using Avalonia.Controls;
using SafetySystem.ViewModels;

namespace SafetySystem.Views
{
    public partial class EmployeesWindow : UserControl
    {
        public EmployeesWindow()
        {
            InitializeComponent();
            DataContext = new EmployeesViewModel();
        }
    }
}
