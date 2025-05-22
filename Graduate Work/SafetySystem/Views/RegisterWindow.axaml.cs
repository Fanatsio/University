using Avalonia.Controls;
using Avalonia.Interactivity;
using SafetySystem.Models;
using SafetySystem.Services;
using System.Threading.Tasks;
using Avalonia.Platform.Storage;
using System.Collections.Generic;
using System;

namespace SafetySystem.Views
{
    public partial class RegisterWindow : Window
    {
        private string? _photoPath = null;

        public RegisterWindow()
        {
            InitializeComponent();
        }

        private async void OnChoosePhotoClick(object sender, RoutedEventArgs e)
        {
            var files = await StorageProvider.OpenFilePickerAsync(new FilePickerOpenOptions
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

            if (files.Count > 0)
            {
                _photoPath = files[0].Path.LocalPath;
                PhotoPathText.Text = _photoPath;
            }
        }

        private async void OnSaveEmployeeClick(object sender, RoutedEventArgs e)
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
                DatabaseService.Instance.AddEmployee(employee);
                await MessageBox("Сотрудник успешно добавлен!");
                this.Close();
            }
            catch (Exception ex)
            {
                await MessageBox($"Ошибка при добавлении сотрудника: {ex.Message}");
            }
        }

        private async Task MessageBox(string message)
        {
            var dialog = new Window
            {
                Width = 300,
                Height = 150,
                Title = "Уведомление",
                Content = new TextBlock
                {
                    Text = message,
                    VerticalAlignment = Avalonia.Layout.VerticalAlignment.Center,
                    HorizontalAlignment = Avalonia.Layout.HorizontalAlignment.Center
                }
            };
            await dialog.ShowDialog(this);
            await Task.Delay(1500);
            dialog.Close();
        }
    }
}