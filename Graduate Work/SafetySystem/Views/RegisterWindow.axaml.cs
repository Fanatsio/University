using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media;
using Avalonia.Platform.Storage;
using SafetySystem.Models;
using SafetySystem.Services;
using System;

namespace SafetySystem.Views
{
    public partial class RegisterWindow : UserControl
    {
        private string? _photoPath;

        public event EventHandler? EmployeeSaved;

        public RegisterWindow()
        {
            InitializeComponent();
        }

        private async void OnChoosePhotoClick(object? sender, RoutedEventArgs e)
        {
            var storageProvider = TopLevel.GetTopLevel(this)?.StorageProvider;
            if (storageProvider is null)
            {
                SetStatus("Не удалось открыть диалог выбора файла.", Brushes.Orange);
                return;
            }

            var files = await storageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
            {
                Title = "Выберите фотографию",
                AllowMultiple = false,
                FileTypeFilter =
                [
                    new FilePickerFileType("Изображения")
                    {
                        Patterns = ["*.jpg", "*.jpeg", "*.png"]
                    }
                ]
            });

            if (files.Count == 0)
            {
                return;
            }

            _photoPath = files[0].Path.LocalPath;
            PhotoPathText.Text = _photoPath;
            SetStatus("Фотография выбрана и готова к сохранению.", Brushes.LightGreen);
        }

        private void OnSaveEmployeeClick(object? sender, RoutedEventArgs e)
        {
            var employee = new Employee
            {
                EmployeeId = EmployeeIdTextBox.Text,
                Name = NameTextBox.Text,
                RfidTag = RfidTagTextBox.Text,
                PhotoPath = _photoPath
            };

            try
            {
                DatabaseService.AddEmployee(employee);
                ClearForm();
                SetStatus("Сотрудник успешно добавлен. Открываю список сотрудников.", Brushes.LightGreen);
                EmployeeSaved?.Invoke(this, EventArgs.Empty);
            }
            catch (Exception ex)
            {
                SetStatus($"Ошибка при добавлении сотрудника: {ex.Message}", Brushes.OrangeRed);
            }
        }

        private void ClearForm()
        {
            EmployeeIdTextBox.Text = string.Empty;
            NameTextBox.Text = string.Empty;
            RfidTagTextBox.Text = string.Empty;
            _photoPath = null;
            PhotoPathText.Text = "Фотография не выбрана";
        }

        private void SetStatus(string message, IBrush brush)
        {
            StatusMessageText.Text = message;
            StatusMessageText.Foreground = brush;
        }
    }
}
