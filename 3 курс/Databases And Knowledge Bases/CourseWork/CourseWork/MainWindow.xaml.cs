// Views/MainWindow.xaml.cs (окончательная версия)
using CourseWork.Data;
using CourseWork.ViewModels;
using System.Windows;

namespace CourseWork.Views
{
    public partial class MainWindow : Window
    {
        private readonly DatabaseContext _dbContext;

        public MainWindow()
        {
            string connectionString = "Host=localhost;Username=postgres;Password=123;Database=db_coursework";
            _dbContext = new DatabaseContext(connectionString);

            var loginWindow = new LoginWindow(_dbContext);
            if (loginWindow.ShowDialog() != true)
            {
                Close();
                return;
            }

            InitializeComponent();

            if (DataContext is MainViewModel viewModel)
            {
                viewModel.Initialize(loginWindow.AuthenticatedUser);
            }
        }
    }
}