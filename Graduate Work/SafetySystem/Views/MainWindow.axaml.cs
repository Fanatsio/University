using Avalonia.Controls;
using SafetySystem.Views;

namespace SafetySystem.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void OnRegisterWindowClick(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            var registerWindow = new RegisterWindow();
            registerWindow.Show();
        }

        private void OnEmployeesButtonClick(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            var employeesWindow = new EmployeesWindow();
            employeesWindow.Show();
        }

        private void OnMonitorWindowClick(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            var monitorWindow = new MonitorWindow();
            monitorWindow.Show();
        }

        private void OnRouteControlWindowClick(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            var routeControlWindow = new RouteControlWindow();
            routeControlWindow.Show();
        }

        private void OnDataAnalysisWindowClick(object sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            var dataAnalysisWindow = new DataAnalysisWindow();
            dataAnalysisWindow.Show();
        }
    }
}