// ViewModels/MainViewModel.cs
using CourseWork.Data;
using CourseWork.Models;
using CourseWork.Views;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;

namespace CourseWork.ViewModels
{
    public class MainViewModel : INotifyPropertyChanged
    {
        private readonly DatabaseContext _dbContext;
        private User _currentUser; // Добавляем свойство для текущего пользователя

        #region Collections
        public ObservableCollection<NaturalPerson> NaturalPersons { get; set; }
        public ObservableCollection<LegalPerson> LegalPersons { get; set; }
        public ObservableCollection<Provider> Providers { get; set; }
        public ObservableCollection<Material> Materials { get; set; }
        public ObservableCollection<Accessories> Accessories { get; set; }
        public ObservableCollection<Furniture> Furniture { get; set; }
        public ObservableCollection<Order> Orders { get; set; }
        public ObservableCollection<Waybill> Waybills { get; set; }
        #endregion

        #region Selected Items
        private NaturalPerson _selectedNaturalPerson;
        private LegalPerson _selectedLegalPerson;
        private Provider _selectedProvider;
        private Material _selectedMaterial;
        private Accessories _selectedAccessories;
        private Furniture _selectedFurniture;
        private Order _selectedOrder;
        private Waybill _selectedWaybill;

        public NaturalPerson SelectedNaturalPerson
        {
            get => _selectedNaturalPerson;
            set { _selectedNaturalPerson = value; OnPropertyChanged(nameof(SelectedNaturalPerson)); }
        }

        public LegalPerson SelectedLegalPerson
        {
            get => _selectedLegalPerson;
            set { _selectedLegalPerson = value; OnPropertyChanged(nameof(SelectedLegalPerson)); }
        }

        public Provider SelectedProvider
        {
            get => _selectedProvider;
            set { _selectedProvider = value; OnPropertyChanged(nameof(SelectedProvider)); }
        }

        public Material SelectedMaterial
        {
            get => _selectedMaterial;
            set { _selectedMaterial = value; OnPropertyChanged(nameof(SelectedMaterial)); }
        }

        public Accessories SelectedAccessories
        {
            get => _selectedAccessories;
            set { _selectedAccessories = value; OnPropertyChanged(nameof(SelectedAccessories)); }
        }

        public Furniture SelectedFurniture
        {
            get => _selectedFurniture;
            set { _selectedFurniture = value; OnPropertyChanged(nameof(SelectedFurniture)); }
        }

        public Order SelectedOrder
        {
            get => _selectedOrder;
            set { _selectedOrder = value; OnPropertyChanged(nameof(SelectedOrder)); }
        }

        public Waybill SelectedWaybill
        {
            get => _selectedWaybill;
            set { _selectedWaybill = value; OnPropertyChanged(nameof(SelectedWaybill)); }
        }
        #endregion

        #region Properties
        public User CurrentUser
        {
            get => _currentUser;
            set { _currentUser = value; OnPropertyChanged(nameof(CurrentUser)); }
        }
        #endregion

        #region Commands
        public ICommand LoadNaturalPersonsCommand { get; }
        public ICommand LoadLegalPersonsCommand { get; }
        public ICommand LoadProvidersCommand { get; }
        public ICommand LoadMaterialsCommand { get; }
        public ICommand LoadAccessoriesCommand { get; }
        public ICommand LoadFurnitureCommand { get; }
        public ICommand LoadOrdersCommand { get; }
        public ICommand LoadWaybillsCommand { get; }

        public ICommand AddNaturalPersonCommand { get; }
        public ICommand EditNaturalPersonCommand { get; }
        public ICommand DeleteNaturalPersonCommand { get; }
        public ICommand AddLegalPersonCommand { get; }
        public ICommand EditLegalPersonCommand { get; }
        public ICommand DeleteLegalPersonCommand { get; }
        public ICommand AddProviderCommand { get; }
        public ICommand EditProviderCommand { get; }
        public ICommand DeleteProviderCommand { get; }
        public ICommand AddMaterialCommand { get; }
        public ICommand EditMaterialCommand { get; }
        public ICommand DeleteMaterialCommand { get; }
        public ICommand AddAccessoriesCommand { get; }
        public ICommand EditAccessoriesCommand { get; }
        public ICommand DeleteAccessoriesCommand { get; }
        public ICommand AddFurnitureCommand { get; }
        public ICommand EditFurnitureCommand { get; }
        public ICommand DeleteFurnitureCommand { get; }
        public ICommand AddOrderCommand { get; }
        public ICommand EditOrderCommand { get; }
        public ICommand DeleteOrderCommand { get; }
        public ICommand AddWaybillCommand { get; }
        public ICommand EditWaybillCommand { get; }
        public ICommand DeleteWaybillCommand { get; }
        #endregion

        public MainViewModel()
        {
            string connectionString = "Host=localhost;Username=postgres;Password=123;Database=db_coursework";
            _dbContext = new DatabaseContext(connectionString);

            NaturalPersons = new ObservableCollection<NaturalPerson>();
            LegalPersons = new ObservableCollection<LegalPerson>();
            Providers = new ObservableCollection<Provider>();
            Materials = new ObservableCollection<Material>();
            Accessories = new ObservableCollection<Accessories>();
            Furniture = new ObservableCollection<Furniture>();
            Orders = new ObservableCollection<Order>();
            Waybills = new ObservableCollection<Waybill>();

            #region Command Initialization
            LoadNaturalPersonsCommand = new RelayCommand(async () => await LoadNaturalPersonsAsync());
            LoadLegalPersonsCommand = new RelayCommand(async () => await LoadLegalPersonsAsync());
            LoadProvidersCommand = new RelayCommand(async () => await LoadProvidersAsync());
            LoadMaterialsCommand = new RelayCommand(async () => await LoadMaterialsAsync());
            LoadAccessoriesCommand = new RelayCommand(async () => await LoadAccessoriesAsync());
            LoadFurnitureCommand = new RelayCommand(async () => await LoadFurnitureAsync());
            LoadOrdersCommand = new RelayCommand(async () => await LoadOrdersAsync());
            LoadWaybillsCommand = new RelayCommand(async () => await LoadWaybillsAsync());

            AddNaturalPersonCommand = new RelayCommand(async () => await AddNaturalPersonAsync());
            EditNaturalPersonCommand = new RelayCommand(async () => await EditNaturalPersonAsync(), () => SelectedNaturalPerson != null);
            DeleteNaturalPersonCommand = new RelayCommand(async () => await DeleteNaturalPersonAsync(), () => SelectedNaturalPerson != null);

            AddLegalPersonCommand = new RelayCommand(async () => await AddLegalPersonAsync());
            EditLegalPersonCommand = new RelayCommand(async () => await EditLegalPersonAsync(), () => SelectedLegalPerson != null);
            DeleteLegalPersonCommand = new RelayCommand(async () => await DeleteLegalPersonAsync(), () => SelectedLegalPerson != null);

            AddProviderCommand = new RelayCommand(async () => await AddProviderAsync());
            EditProviderCommand = new RelayCommand(async () => await EditProviderAsync(), () => SelectedProvider != null);
            DeleteProviderCommand = new RelayCommand(async () => await DeleteProviderAsync(), () => SelectedProvider != null);

            AddMaterialCommand = new RelayCommand(async () => await AddMaterialAsync());
            EditMaterialCommand = new RelayCommand(async () => await EditMaterialAsync(), () => SelectedMaterial != null);
            DeleteMaterialCommand = new RelayCommand(async () => await DeleteMaterialAsync(), () => SelectedMaterial != null);

            AddAccessoriesCommand = new RelayCommand(async () => await AddAccessoriesAsync());
            EditAccessoriesCommand = new RelayCommand(async () => await EditAccessoriesAsync(), () => SelectedAccessories != null);
            DeleteAccessoriesCommand = new RelayCommand(async () => await DeleteAccessoriesAsync(), () => SelectedAccessories != null);

            AddFurnitureCommand = new RelayCommand(async () => await AddFurnitureAsync());
            EditFurnitureCommand = new RelayCommand(async () => await EditFurnitureAsync(), () => SelectedFurniture != null);
            DeleteFurnitureCommand = new RelayCommand(async () => await DeleteFurnitureAsync(), () => SelectedFurniture != null);

            AddOrderCommand = new RelayCommand(async () => await AddOrderAsync());
            EditOrderCommand = new RelayCommand(async () => await EditOrderAsync(), () => SelectedOrder != null);
            DeleteOrderCommand = new RelayCommand(async () => await DeleteOrderAsync(), () => SelectedOrder != null);

            AddWaybillCommand = new RelayCommand(async () => await AddWaybillAsync());
            EditWaybillCommand = new RelayCommand(async () => await EditWaybillAsync(), () => SelectedWaybill != null);
            DeleteWaybillCommand = new RelayCommand(async () => await DeleteWaybillAsync(), () => SelectedWaybill != null);
            #endregion

            // Инициальная загрузка данных будет выполнена после установки CurrentUser
        }

        // Новый конструктор с передачей пользователя после авторизации
        public void Initialize(User user)
        {
            CurrentUser = user;
            Task.Run(async () =>
            {
                await LoadNaturalPersonsAsync();
                await LoadLegalPersonsAsync();
                await LoadProvidersAsync();
                await LoadMaterialsAsync();
                await LoadAccessoriesAsync();
                await LoadFurnitureAsync();
                await LoadOrdersAsync();
                await LoadWaybillsAsync();
            });
        }

        #region Load Methods
        private async Task LoadNaturalPersonsAsync()
        {
            try
            {
                NaturalPersons = await _dbContext.GetNaturalPersonsAsync();
                OnPropertyChanged(nameof(NaturalPersons));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки физических лиц: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadLegalPersonsAsync()
        {
            try
            {
                LegalPersons = await _dbContext.GetLegalPersonsAsync();
                OnPropertyChanged(nameof(LegalPersons));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки юридических лиц: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadProvidersAsync()
        {
            try
            {
                Providers = await _dbContext.GetProvidersAsync();
                OnPropertyChanged(nameof(Providers));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки поставщиков: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadMaterialsAsync()
        {
            try
            {
                Materials = await _dbContext.GetMaterialsAsync();
                OnPropertyChanged(nameof(Materials));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки материалов: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadAccessoriesAsync()
        {
            try
            {
                Accessories = await _dbContext.GetAccessoriesAsync();
                OnPropertyChanged(nameof(Accessories));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки фурнитуры: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadFurnitureAsync()
        {
            try
            {
                Furniture = await _dbContext.GetFurnitureAsync();
                OnPropertyChanged(nameof(Furniture));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки мебели: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadOrdersAsync()
        {
            try
            {
                Orders = await _dbContext.GetOrdersAsync();
                OnPropertyChanged(nameof(Orders));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки заказов: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private async Task LoadWaybillsAsync()
        {
            try
            {
                Waybills = await _dbContext.GetWaybillsAsync();
                OnPropertyChanged(nameof(Waybills));
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка загрузки накладных: {ex.Message}", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        #endregion

        #region CRUD Methods
        private async Task AddNaturalPersonAsync()
        {
            var person = new NaturalPerson();
            if (ShowEditWindow(person))
            {
                await _dbContext.AddNaturalPersonAsync(person);
                await LoadNaturalPersonsAsync();
            }
        }

        private async Task EditNaturalPersonAsync()
        {
            if (SelectedNaturalPerson != null)
            {
                var person = Clone(SelectedNaturalPerson);
                if (ShowEditWindow(person))
                {
                    await _dbContext.UpdateNaturalPersonAsync(person);
                    await LoadNaturalPersonsAsync();
                }
            }
        }

        private async Task DeleteNaturalPersonAsync()
        {
            if (SelectedNaturalPerson != null && ConfirmDelete("физическое лицо"))
            {
                await _dbContext.DeleteNaturalPersonAsync(SelectedNaturalPerson.NaturalPersonId);
                await LoadNaturalPersonsAsync();
            }
        }

        private async Task AddLegalPersonAsync()
        {
            var person = new LegalPerson();
            if (ShowEditWindow(person))
            {
                await _dbContext.AddLegalPersonAsync(person);
                await LoadLegalPersonsAsync();
            }
        }

        private async Task EditLegalPersonAsync()
        {
            if (SelectedLegalPerson != null)
            {
                var person = Clone(SelectedLegalPerson);
                if (ShowEditWindow(person))
                {
                    await _dbContext.UpdateLegalPersonAsync(person);
                    await LoadLegalPersonsAsync();
                }
            }
        }

        private async Task DeleteLegalPersonAsync()
        {
            if (SelectedLegalPerson != null && ConfirmDelete("юридическое лицо"))
            {
                await _dbContext.DeleteLegalPersonAsync(SelectedLegalPerson.LegalPersonId);
                await LoadLegalPersonsAsync();
            }
        }

        private async Task AddProviderAsync()
        {
            var provider = new Provider();
            if (ShowEditWindow(provider))
            {
                await _dbContext.AddProviderAsync(provider);
                await LoadProvidersAsync();
            }
        }

        private async Task EditProviderAsync()
        {
            if (SelectedProvider != null)
            {
                var provider = Clone(SelectedProvider);
                if (ShowEditWindow(provider))
                {
                    await _dbContext.UpdateProviderAsync(provider);
                    await LoadProvidersAsync();
                }
            }
        }

        private async Task DeleteProviderAsync()
        {
            if (SelectedProvider != null && ConfirmDelete("поставщика"))
            {
                await _dbContext.DeleteProviderAsync(SelectedProvider.ProviderId);
                await LoadProvidersAsync();
            }
        }

        private async Task AddMaterialAsync()
        {
            var material = new Material();
            if (ShowEditWindow(material))
            {
                await _dbContext.AddMaterialAsync(material);
                await LoadMaterialsAsync();
            }
        }

        private async Task EditMaterialAsync()
        {
            if (SelectedMaterial != null)
            {
                var material = Clone(SelectedMaterial);
                if (ShowEditWindow(material))
                {
                    await _dbContext.UpdateMaterialAsync(material);
                    await LoadMaterialsAsync();
                }
            }
        }

        private async Task DeleteMaterialAsync()
        {
            if (SelectedMaterial != null && ConfirmDelete("материал"))
            {
                await _dbContext.DeleteMaterialAsync(SelectedMaterial.MaterialId);
                await LoadMaterialsAsync();
            }
        }

        private async Task AddAccessoriesAsync()
        {
            var accessories = new Accessories();
            if (ShowEditWindow(accessories))
            {
                await _dbContext.AddAccessoriesAsync(accessories);
                await LoadAccessoriesAsync();
            }
        }

        private async Task EditAccessoriesAsync()
        {
            if (SelectedAccessories != null)
            {
                var accessories = Clone(SelectedAccessories);
                if (ShowEditWindow(accessories))
                {
                    await _dbContext.UpdateAccessoriesAsync(accessories);
                    await LoadAccessoriesAsync();
                }
            }
        }

        private async Task DeleteAccessoriesAsync()
        {
            if (SelectedAccessories != null && ConfirmDelete("фурнитуру"))
            {
                await _dbContext.DeleteAccessoriesAsync(SelectedAccessories.AccessoriesId);
                await LoadAccessoriesAsync();
            }
        }

        private async Task AddFurnitureAsync()
        {
            var furniture = new Furniture();
            if (ShowEditWindow(furniture))
            {
                await _dbContext.AddFurnitureAsync(furniture);
                await LoadFurnitureAsync();
            }
        }

        private async Task EditFurnitureAsync()
        {
            if (SelectedFurniture != null)
            {
                var furniture = Clone(SelectedFurniture);
                if (ShowEditWindow(furniture))
                {
                    await _dbContext.UpdateFurnitureAsync(furniture);
                    await LoadFurnitureAsync();
                }
            }
        }

        private async Task DeleteFurnitureAsync()
        {
            if (SelectedFurniture != null && ConfirmDelete("мебель"))
            {
                await _dbContext.DeleteFurnitureAsync(SelectedFurniture.FurnitureId);
                await LoadFurnitureAsync();
            }
        }

        private async Task AddOrderAsync()
        {
            var order = new Order();
            if (ShowEditWindow(order))
            {
                await _dbContext.AddOrderAsync(order);
                await LoadOrdersAsync();
            }
        }

        private async Task EditOrderAsync()
        {
            if (SelectedOrder != null)
            {
                var order = Clone(SelectedOrder);
                if (ShowEditWindow(order))
                {
                    await _dbContext.UpdateOrderAsync(order);
                    await LoadOrdersAsync();
                }
            }
        }

        private async Task DeleteOrderAsync()
        {
            if (SelectedOrder != null && ConfirmDelete("заказ"))
            {
                await _dbContext.DeleteOrderAsync(SelectedOrder.OrdersId);
                await LoadOrdersAsync();
            }
        }

        private async Task AddWaybillAsync()
        {
            var waybill = new Waybill();
            if (ShowEditWindow(waybill))
            {
                await _dbContext.AddWaybillAsync(waybill);
                await LoadWaybillsAsync();
            }
        }

        private async Task EditWaybillAsync()
        {
            if (SelectedWaybill != null)
            {
                var waybill = Clone(SelectedWaybill);
                if (ShowEditWindow(waybill))
                {
                    await _dbContext.UpdateWaybillAsync(waybill);
                    await LoadWaybillsAsync();
                }
            }
        }

        private async Task DeleteWaybillAsync()
        {
            if (SelectedWaybill != null && ConfirmDelete("накладную"))
            {
                await _dbContext.DeleteWaybillAsync(SelectedWaybill.WaybillId);
                await LoadWaybillsAsync();
            }
        }
        #endregion

        #region Helper Methods
        private bool ShowEditWindow(object entity)
        {
            var editWindow = new EditWindow(entity);
            return editWindow.ShowDialog() == true;
        }

        private bool ConfirmDelete(string entityName)
        {
            return MessageBox.Show($"Вы уверены, что хотите удалить {entityName}?",
                "Подтверждение удаления", MessageBoxButton.YesNo, MessageBoxImage.Warning) == MessageBoxResult.Yes;
        }

        private T Clone<T>(T source) where T : class, new()
        {
            var clone = new T();
            foreach (var prop in typeof(T).GetProperties())
            {
                if (prop.CanWrite)
                    prop.SetValue(clone, prop.GetValue(source));
            }
            return clone;
        }
        #endregion

        #region INotifyPropertyChanged
        public event PropertyChangedEventHandler PropertyChanged;
        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        #endregion
    }

    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool> _canExecute;

        public RelayCommand(Action execute, Func<bool> canExecute = null)
        {
            _execute = execute;
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }

        public bool CanExecute(object parameter) => _canExecute == null || _canExecute();
        public void Execute(object parameter) => _execute();
    }
}