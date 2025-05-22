// Views/LoginWindow.xaml.cs
using CourseWork.Data;
using CourseWork.Models;
using System.Windows;

namespace CourseWork.Views
{
    public partial class LoginWindow : Window
    {
        private readonly DatabaseContext _dbContext;
        public User AuthenticatedUser { get; private set; } // Добавляем свойство для передачи пользователя

        public LoginWindow(DatabaseContext dbContext)
        {
            InitializeComponent();
            _dbContext = dbContext;
        }

        private async void LoginButton_Click(object sender, RoutedEventArgs e)
        {
            string username = UsernameTextBox.Text;
            string password = PasswordBox.Password;

            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
            {
                MessageBox.Show("Введите логин и пароль.", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var user = await _dbContext.AuthenticateUserAsync(username, password);
            if (user != null)
            {
                AuthenticatedUser = user; // Сохраняем пользователя
                DialogResult = true;
                Close();
            }
            else
            {
                MessageBox.Show("Неверный логин или пароль.", "Ошибка входа", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}