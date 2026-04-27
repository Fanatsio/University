using Avalonia.Controls;
using Avalonia.Interactivity;

namespace SafetySystem.Views
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            ShowHome();
        }

        private void ShowSection(Control view, string title, string subtitle)
        {
            SectionTitleText.Text = title;
            SectionSubtitleText.Text = subtitle;
            MainContentHost.Content = view;
        }

        private void ShowHome()
        {
            ShowSection(
                new DashboardView(),
                "Главная",
                "Контролируйте систему и переключайтесь между разделами.");
        }

        private void ShowEmployees()
        {
            ShowSection(
                new EmployeesWindow(),
                "Список сотрудников",
                "Актуальный реестр сотрудников доступен прямо в основном рабочем окне.");
        }

        private void OnHomeClick(object? sender, RoutedEventArgs e)
        {
            ShowHome();
        }

        private void OnRegisterWindowClick(object? sender, RoutedEventArgs e)
        {
            var registerView = new RegisterWindow();
            registerView.EmployeeSaved += (_, _) => ShowEmployees();

            ShowSection(
                registerView,
                "Регистрация сотрудников",
                "Добавляйте новых сотрудников.");
        }

        private void OnEmployeesButtonClick(object? sender, RoutedEventArgs e)
        {
            ShowEmployees();
        }

        private void OnMonitorWindowClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new MonitorWindow(),
                "Мониторинг",
                "Поток с камеры и события опасной зоны.");
        }

        private void OnRouteControlWindowClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new RouteControlWindow(),
                "Контроль точек",
                "Отслеживайте перемещения и контрольные точки.");
        }

        private void OnDataAnalysisWindowClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new DataAnalysisWindow(),
                "Анализ данных",
                "Просматривайте события и аналитические данные.");
        }

        private void OnNotificationsClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new NotificationsView(),
                "Уведомления",
                "Оперативные сообщения и тревоги.");
        }
    }
}
