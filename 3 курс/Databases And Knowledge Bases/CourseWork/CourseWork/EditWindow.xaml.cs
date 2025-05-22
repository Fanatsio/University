// Views/EditWindow.xaml.cs
using System;
using System.Windows;
using System.Windows.Controls;
using CourseWork.Models;

namespace CourseWork.Views
{
    public partial class EditWindow : Window
    {
        private readonly object _entity;

        public EditWindow(object entity)
        {
            InitializeComponent();
            _entity = entity;
            Title = $"Редактирование: {entity.GetType().Name}";

            // Динамическое создание формы в зависимости от типа сущности
            if (entity is NaturalPerson person)
                EntityContent.Content = CreateNaturalPersonForm(person);
            else if (entity is LegalPerson legalPerson)
                EntityContent.Content = CreateLegalPersonForm(legalPerson);
            else if (entity is Provider provider)
                EntityContent.Content = CreateProviderForm(provider);
            else if (entity is Material material)
                EntityContent.Content = CreateMaterialForm(material);
            else if (entity is Accessories accessories)
                EntityContent.Content = CreateAccessoriesForm(accessories);
            else if (entity is Furniture furniture)
                EntityContent.Content = CreateFurnitureForm(furniture);
            else if (entity is Order order)
                EntityContent.Content = CreateOrderForm(order);
            else if (entity is Waybill waybill)
                EntityContent.Content = CreateWaybillForm(waybill);
            else
                throw new ArgumentException("Неизвестный тип сущности");
        }

        #region Form Creation Methods
        private UserControl CreateNaturalPersonForm(NaturalPerson person)
        {
            var grid = CreateGrid(5);
            int row = 0;
            AddField(grid, row++, "Паспорт:", new TextBox { Text = person.NaturalPersonPassport.ToString(), Tag = person });
            AddField(grid, row++, "ФИО:", new TextBox { Text = person.NaturalPersonName, Tag = person });
            AddField(grid, row++, "Телефон:", new TextBox { Text = person.NaturalPersonPhone, Tag = person });
            AddField(grid, row++, "Email:", new TextBox { Text = person.NaturalPersonEmail, Tag = person });
            AddField(grid, row++, "Адрес:", new TextBox { Text = person.NaturalPersonAddress, Tag = person });
            return new UserControl { Content = grid };
        }

        private UserControl CreateLegalPersonForm(LegalPerson person)
        {
            var grid = CreateGrid(5);
            int row = 0;
            AddField(grid, row++, "ИНН:", new TextBox { Text = person.LegalPersonInn, Tag = person });
            AddField(grid, row++, "Название:", new TextBox { Text = person.LegalPersonName, Tag = person });
            AddField(grid, row++, "Телефон:", new TextBox { Text = person.LegalPersonPhone, Tag = person });
            AddField(grid, row++, "Email:", new TextBox { Text = person.LegalPersonEmail, Tag = person });
            AddField(grid, row++, "Адрес:", new TextBox { Text = person.LegalPersonAddress, Tag = person });
            return new UserControl { Content = grid };
        }

        private UserControl CreateProviderForm(Provider provider)
        {
            var grid = CreateGrid(3);
            int row = 0;
            AddField(grid, row++, "ИНН:", new TextBox { Text = provider.ProviderInn, Tag = provider });
            AddField(grid, row++, "Название:", new TextBox { Text = provider.ProviderName, Tag = provider });
            AddField(grid, row++, "Адрес:", new TextBox { Text = provider.ProviderAddress, Tag = provider });
            return new UserControl { Content = grid };
        }

        private UserControl CreateMaterialForm(Material material)
        {
            var grid = CreateGrid(6);
            int row = 0;
            AddField(grid, row++, "Цвет:", new TextBox { Text = material.MaterialColour, Tag = material });
            AddField(grid, row++, "Название:", new TextBox { Text = material.MaterialName, Tag = material });
            AddField(grid, row++, "Тип:", new TextBox { Text = material.MaterialType, Tag = material });
            AddField(grid, row++, "Количество:", new TextBox { Text = material.MaterialQuantity.ToString(), Tag = material });
            AddField(grid, row++, "ИНН Поставщика:", new TextBox { Text = material.ProviderInn, Tag = material });
            AddField(grid, row++, "Стоимость:", new TextBox { Text = material.MaterialCost.ToString(), Tag = material });
            return new UserControl { Content = grid };
        }

        private UserControl CreateAccessoriesForm(Accessories accessories)
        {
            var grid = CreateGrid(6);
            int row = 0;
            AddField(grid, row++, "Название:", new TextBox { Text = accessories.AccessoriesName, Tag = accessories });
            AddField(grid, row++, "Цвет:", new TextBox { Text = accessories.AccessoriesColour, Tag = accessories });
            AddField(grid, row++, "Тип:", new TextBox { Text = accessories.AccessoriesType, Tag = accessories });
            AddField(grid, row++, "Количество:", new TextBox { Text = accessories.AccessoriesQuantity.ToString(), Tag = accessories });
            AddField(grid, row++, "ИНН Поставщика:", new TextBox { Text = accessories.ProviderInn, Tag = accessories });
            AddField(grid, row++, "Стоимость:", new TextBox { Text = accessories.AccessoriesCost.ToString(), Tag = accessories });
            return new UserControl { Content = grid };
        }

        private UserControl CreateFurnitureForm(Furniture furniture)
        {
            var grid = CreateGrid(7);
            int row = 0;
            AddField(grid, row++, "Цвет:", new TextBox { Text = furniture.FurnitureColour, Tag = furniture });
            AddField(grid, row++, "Артикул:", new TextBox { Text = furniture.FurnitureArticle.ToString(), Tag = furniture });
            AddField(grid, row++, "ID Материала:", new TextBox { Text = furniture.IdMaterial.ToString(), Tag = furniture });
            AddField(grid, row++, "Тип:", new TextBox { Text = furniture.FurnitureType, Tag = furniture });
            AddField(grid, row++, "Размер:", new TextBox { Text = furniture.FurnitureSize.ToString(), Tag = furniture });
            AddField(grid, row++, "Название:", new TextBox { Text = furniture.FurnitureName, Tag = furniture });
            AddField(grid, row++, "ID Фурнитуры:", new TextBox { Text = furniture.IdAccessories.ToString(), Tag = furniture });
            return new UserControl { Content = grid };
        }

        private UserControl CreateOrderForm(Order order)
        {
            var grid = CreateGrid(6);
            int row = 0;
            AddField(grid, row++, "Дата:", new DatePicker { SelectedDate = order.OrdersRegistrationDate, Tag = order });
            AddField(grid, row++, "Стоимость:", new TextBox { Text = order.OrdersTotalCost.ToString(), Tag = order });
            AddField(grid, row++, "№ Заказа:", new TextBox { Text = order.OrderNumber.ToString(), Tag = order });
            var combo = new ComboBox { Tag = order };
            combo.Items.Add("Физ. лицо"); combo.Items.Add("Юр. лицо");
            combo.SelectedItem = order.CategoryCustomer;
            AddField(grid, row++, "Тип клиента:", combo);
            AddField(grid, row++, "Статус:", new TextBox { Text = order.OrdersStatus, Tag = order });
            AddField(grid, row++, "ID Клиента:", new TextBox { Text = order.CustomerId.ToString(), Tag = order });
            return new UserControl { Content = grid };
        }

        private UserControl CreateWaybillForm(Waybill waybill)
        {
            var grid = CreateGrid(4);
            int row = 0;
            AddField(grid, row++, "№ Накладной:", new TextBox { Text = waybill.WaybillNumber.ToString(), Tag = waybill });
            AddField(grid, row++, "Артикул мебели:", new TextBox { Text = waybill.ArticleFurniture.ToString(), Tag = waybill });
            AddField(grid, row++, "Количество:", new TextBox { Text = waybill.FurnitureQuantity.ToString(), Tag = waybill });
            AddField(grid, row++, "№ Заказа:", new TextBox { Text = waybill.OrdersNumber.ToString(), Tag = waybill });
            return new UserControl { Content = grid };
        }
        #endregion

        #region Helper Methods
        private Grid CreateGrid(int rows)
        {
            var grid = new Grid { Margin = new Thickness(0, 0, 0, 10) };
            grid.ColumnDefinitions.Add(new ColumnDefinition { Width = GridLength.Auto });
            grid.ColumnDefinitions.Add(new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) });
            for (int i = 0; i < rows; i++)
                grid.RowDefinitions.Add(new RowDefinition { Height = GridLength.Auto });
            return grid;
        }

        private void AddField(Grid grid, int row, string label, Control control)
        {
            var textBlock = new TextBlock { Text = label, Margin = new Thickness(0, 0, 5, 5) };
            Grid.SetRow(textBlock, row);
            Grid.SetColumn(textBlock, 0);
            grid.Children.Add(textBlock);

            control.Margin = new Thickness(0, 0, 0, 10);
            Grid.SetRow(control, row);
            Grid.SetColumn(control, 1);
            grid.Children.Add(control);
        }
        #endregion

        #region Event Handlers
        private void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_entity is NaturalPerson person)
                {
                    person.NaturalPersonPassport = int.Parse(GetTextBoxValue("Паспорт:"));
                    person.NaturalPersonName = GetTextBoxValue("ФИО:");
                    person.NaturalPersonPhone = GetTextBoxValue("Телефон:");
                    person.NaturalPersonEmail = GetTextBoxValue("Email:");
                    person.NaturalPersonAddress = GetTextBoxValue("Адрес:");
                }
                else if (_entity is LegalPerson legalPerson)
                {
                    legalPerson.LegalPersonInn = GetTextBoxValue("ИНН:");
                    legalPerson.LegalPersonName = GetTextBoxValue("Название:");
                    legalPerson.LegalPersonPhone = GetTextBoxValue("Телефон:");
                    legalPerson.LegalPersonEmail = GetTextBoxValue("Email:");
                    legalPerson.LegalPersonAddress = GetTextBoxValue("Адрес:");
                }
                else if (_entity is Provider provider)
                {
                    provider.ProviderInn = GetTextBoxValue("ИНН:");
                    provider.ProviderName = GetTextBoxValue("Название:");
                    provider.ProviderAddress = GetTextBoxValue("Адрес:");
                }
                else if (_entity is Material material)
                {
                    material.MaterialColour = GetTextBoxValue("Цвет:");
                    material.MaterialName = GetTextBoxValue("Название:");
                    material.MaterialType = GetTextBoxValue("Тип:");
                    material.MaterialQuantity = int.Parse(GetTextBoxValue("Количество:"));
                    material.ProviderInn = GetTextBoxValue("ИНН Поставщика:");
                    material.MaterialCost = decimal.Parse(GetTextBoxValue("Стоимость:"));
                }
                else if (_entity is Accessories accessories)
                {
                    accessories.AccessoriesName = GetTextBoxValue("Название:");
                    accessories.AccessoriesColour = GetTextBoxValue("Цвет:");
                    accessories.AccessoriesType = GetTextBoxValue("Тип:");
                    accessories.AccessoriesQuantity = int.Parse(GetTextBoxValue("Количество:"));
                    accessories.ProviderInn = GetTextBoxValue("ИНН Поставщика:");
                    accessories.AccessoriesCost = decimal.Parse(GetTextBoxValue("Стоимость:"));
                }
                else if (_entity is Furniture furniture)
                {
                    furniture.FurnitureColour = GetTextBoxValue("Цвет:");
                    furniture.FurnitureArticle = int.Parse(GetTextBoxValue("Артикул:"));
                    furniture.IdMaterial = int.Parse(GetTextBoxValue("ID Материала:"));
                    furniture.FurnitureType = GetTextBoxValue("Тип:");
                    furniture.FurnitureSize = decimal.Parse(GetTextBoxValue("Размер:"));
                    furniture.FurnitureName = GetTextBoxValue("Название:");
                    furniture.IdAccessories = int.Parse(GetTextBoxValue("ID Фурнитуры:"));
                }
                else if (_entity is Order order)
                {
                    order.OrdersRegistrationDate = ((DatePicker)FindControl("Дата:")).SelectedDate.Value;
                    order.OrdersTotalCost = decimal.Parse(GetTextBoxValue("Стоимость:"));
                    order.OrderNumber = int.Parse(GetTextBoxValue("№ Заказа:"));
                    order.CategoryCustomer = (string)((ComboBox)FindControl("Тип клиента:")).SelectedItem;
                    order.OrdersStatus = GetTextBoxValue("Статус:");
                    order.CustomerId = int.Parse(GetTextBoxValue("ID Клиента:"));
                }
                else if (_entity is Waybill waybill)
                {
                    waybill.WaybillNumber = int.Parse(GetTextBoxValue("№ Накладной:"));
                    waybill.ArticleFurniture = int.Parse(GetTextBoxValue("Артикул мебели:"));
                    waybill.FurnitureQuantity = int.Parse(GetTextBoxValue("Количество:"));
                    waybill.OrdersNumber = int.Parse(GetTextBoxValue("№ Заказа:"));
                }

                DialogResult = true;
                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сохранении: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
        #endregion

        #region Utility Methods
        private string GetTextBoxValue(string label)
        {
            var control = FindControl(label);
            if (control is TextBox textBox)
                return textBox.Text;
            throw new InvalidOperationException($"Поле '{label}' не является текстовым.");
        }

        private Control FindControl(string label)
        {
            var grid = (Grid)((UserControl)EntityContent.Content).Content;
            for (int i = 0; i < grid.Children.Count; i += 2)
            {
                if (grid.Children[i] is TextBlock tb && tb.Text == label)
                    return (Control)grid.Children[i + 1];
            }
            throw new InvalidOperationException($"Поле с меткой '{label}' не найдено.");
        }
        #endregion
    }
}