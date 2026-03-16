using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;

namespace SafetySystem.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void OnRegisterWindowClick(object sender, RoutedEventArgs e)
        {
            var registerWindow = new RegisterWindow();
            registerWindow.Show();
        }

        private void OnEmployeesButtonClick(object? sender, RoutedEventArgs e)
        {
            var employeesWindow = new EmployeesWindow();
            employeesWindow.Show();
        }

        private void OnMonitorWindowClick(object sender, RoutedEventArgs e)
        {
            var monitorWindow = new MonitorWindow();
            monitorWindow.Show();
        }

        private void OnRouteControlWindowClick(object sender, RoutedEventArgs e)
        {
            var routeControlWindow = new RouteControlWindow();
            routeControlWindow.Show();
        }

        private void OnDataAnalysisWindowClick(object sender, RoutedEventArgs e)
        {
            var dataAnalysisWindow = new DataAnalysisWindow();
            dataAnalysisWindow.Show();
        }

        private void TitleBar_PointerPressed(object? sender, PointerPressedEventArgs e)
        {
            if (e.GetCurrentPoint(this).Properties.IsLeftButtonPressed)
                BeginMoveDrag(e);
        }
    }
}