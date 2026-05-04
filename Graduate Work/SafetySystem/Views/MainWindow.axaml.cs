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
                "Единое рабочее пространство для наблюдения, регистрации и анализа событий.");
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
                "Добавляйте новые учетные записи для контроля доступа и мониторинга.");
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
                "Поток с камеры, детекция людей и события опасной зоны.");
        }

        private void OnRouteControlWindowClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new RouteControlWindow(),
                "Контроль точек",
                "Отслеживайте перемещения сотрудников и контрольные точки.");
        }

        private void OnDataAnalysisWindowClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new DataAnalysisWindow(),
                "Анализ данных",
                "Просматривайте события, динамику нарушений и аналитические данные.");
        }

        private void OnNotificationsClick(object? sender, RoutedEventArgs e)
        {
            ShowSection(
                new NotificationsView(),
                "Уведомления",
                "Оперативные сообщения, тревоги и служебные события системы.");
        }
    }
}
