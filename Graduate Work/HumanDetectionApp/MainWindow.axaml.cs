using Avalonia;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Media.Imaging;
using Avalonia.Threading;
using System;
using System.IO;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

namespace HumanDetectionApp
{
    public partial class MainWindow : Window
    {
        private bool _isRunning = false;
        private TcpClient _client;
        private NetworkStream _stream;
        private CancellationTokenSource _cts;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }

        // Метод для запуска получения видео через сокет
        private async Task StartSocketListener()
        {
            try
            {
                _client = new TcpClient("localhost", 9999); // Подключение к Python-серверу
                _stream = _client.GetStream();
                _cts = new CancellationTokenSource();

                await Task.Run(async () =>
                {
                    while (!_cts.IsCancellationRequested)
                    {
                        try
                        {
                            // Чтение размера сообщения (длина кадра)
                            byte[] sizeBytes = new byte[sizeof(long)];
                            int bytesRead = 0;
                            while (bytesRead < sizeBytes.Length)
                            {
                                bytesRead += await _stream.ReadAsync(sizeBytes, bytesRead, sizeBytes.Length - bytesRead, _cts.Token);
                            }
                            long size = BitConverter.ToInt64(sizeBytes, 0);

                            // Чтение данных кадра
                            byte[] frameBytes = new byte[size];
                            bytesRead = 0;
                            while (bytesRead < size)
                            {
                                bytesRead += await _stream.ReadAsync(frameBytes, bytesRead, (int)(size - bytesRead), _cts.Token);
                            }

                            // Конвертация в Bitmap и отображение
                            await Dispatcher.UIThread.InvokeAsync(() =>
                            {
                                using var ms = new MemoryStream(frameBytes);
                                var bitmap = new Bitmap(ms);
                                this.FindControl<Image>("VideoFeed").Source = bitmap;
                                this.FindControl<TextBlock>("StatusText").Text = $"Status: Frame received at {DateTime.Now}";
                            });
                        }
                        catch (Exception ex)
                        {
                            await Dispatcher.UIThread.InvokeAsync(() =>
                            {
                                this.FindControl<TextBlock>("StatusText").Text = $"Status: Error - {ex.Message}";
                            });
                            break;
                        }
                    }
                });
            }
            catch (Exception ex)
            {
                this.FindControl<TextBlock>("StatusText").Text = $"Status: Connection failed - {ex.Message}";
            }
        }

        // Обработчик кнопки Start
        private async void StartButton_Click(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            if (_isRunning) return;

            _isRunning = true;
            this.FindControl<TextBlock>("StatusText").Text = "Status: Connecting...";
            await StartSocketListener();
        }

        // Обработчик кнопки Stop
        private void StopButton_Click(object? sender, Avalonia.Interactivity.RoutedEventArgs e)
        {
            if (!_isRunning) return;

            _isRunning = false;
            _cts?.Cancel();
            _stream?.Close();
            _client?.Close();
            this.FindControl<TextBlock>("StatusText").Text = "Status: Stopped";
        }

        // Очистка при закрытии окна
        protected override void OnClosed(EventArgs e)
        {
            base.OnClosed(e);
            _isRunning = false;
            _cts?.Cancel();
            _stream?.Dispose();
            _client?.Dispose();
        }
    }
}