using System;
using System.Drawing;
using System.Net;
using System.Net.Sockets;
using System.Net.NetworkInformation;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace SecureChatApp
{
    public partial class Form1 : Form
    {
        private readonly NetworkManager _networkManager;
        private readonly CryptoManager _cryptoManager;
        private bool _isRunning;

        // UI Components
        private RadioButton rbServer = null!;
        private RadioButton rbClient = null!;
        private TextBox txtIP = null!;
        private TextBox txtPort = null!;
        private Button btnConnect = null!;
        private TextBox txtChat = null!;
        private TextBox txtMessage = null!;
        private Button btnSend = null!;
        private Label lblStatus = null!;

        public Form1()
        {
            InitializeComponent();
            _cryptoManager = new CryptoManager();
            _networkManager = new NetworkManager(_cryptoManager, AppendChat);
            SetupUI();
        }

        private void SetupUI()
        {
            Text = "Приложение для безопасного чата";
            Size = new Size(900, 650);
            BackColor = Color.FromArgb(245, 245, 245); // Soft gray background
            FormBorderStyle = FormBorderStyle.FixedSingle;
            MaximizeBox = false;
            MinimumSize = new Size(900, 650);
            MaximumSize = new Size(900, 650);

            // Connection Panel
            var panelConnection = new Panel
            {
                Size = new Size(250, 220),
                Location = new Point(20, 20),
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };
            panelConnection.Paint += (s, e) =>
            {
                ControlPaint.DrawBorder(e.Graphics, panelConnection.ClientRectangle,
                    Color.FromArgb(200, 200, 200), ButtonBorderStyle.Solid);
            };

            // Radio Buttons
            rbServer = CreateRadioButton("Сервер", new Point(20, 20), true);
            rbClient = CreateRadioButton("Клиент", new Point(20, 50), false);

            // IP Label and TextBox
            CreateLabel("IP:", new Point(30, 105));
            string localIP = GetLocalIPv4Address() ?? "127.0.0.1";
            txtIP = CreateTextBox(new Point(50, 80), 180, localIP);

            // Port Label and TextBox
            CreateLabel("Порт:", new Point(30, 135));
            txtPort = CreateTextBox(new Point(50, 110), 180, "5000");

            // Connect Button
            btnConnect = CreateButton("Подключиться", new Point(20, 160), Color.FromArgb(0, 120, 215), BtnConnect_Click);
            btnConnect.Size = new Size(210, 40);

            // Chat Area
            txtChat = new TextBox
            {
                Location = new Point(290, 20),
                Size = new Size(570, 450),
                Multiline = true,
                ReadOnly = true,
                BackColor = Color.White,
                ScrollBars = ScrollBars.Vertical,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.FixedSingle
            };

            // Message Input
            txtMessage = new TextBox
            {
                Location = new Point(290, 480),
                Size = new Size(450, 100),
                Multiline = true,
                BackColor = Color.White,
                ScrollBars = ScrollBars.Vertical,
                Font = new Font("Segoe UI", 10),
                BorderStyle = BorderStyle.FixedSingle,
                PlaceholderText = "Введите сообщение..."
            };

            // Send Button
            btnSend = CreateButton("Отправить", new Point(750, 480), Color.FromArgb(0, 150, 0), BtnSend_Click);
            btnSend.Size = new Size(110, 100);

            // Status Label
            lblStatus = new Label
            {
                Location = new Point(290, 590),
                Size = new Size(570, 20),
                Text = "Отключено",
                ForeColor = Color.Gray,
                Font = new Font("Segoe UI", 9)
            };

            // Add controls to the form
            panelConnection.Controls.AddRange(new Control[] { rbServer, rbClient, txtIP, txtPort, btnConnect });
            Controls.AddRange(new Control[] { panelConnection, txtChat, txtMessage, btnSend, lblStatus });
        }

        private RadioButton CreateRadioButton(string text, Point location, bool isChecked)
        {
            return new RadioButton
            {
                Text = text,
                Location = location,
                AutoSize = true,
                Checked = isChecked,
                Font = new Font("Segoe UI", 9)
            };
        }

        private TextBox CreateTextBox(Point location, int width, string defaultText)
        {
            return new TextBox
            {
                Location = location,
                Width = width,
                Text = defaultText,
                BackColor = Color.FromArgb(245, 245, 245),
                BorderStyle = BorderStyle.FixedSingle,
                Font = new Font("Segoe UI", 9)
            };
        }

        private Label CreateLabel(string text, Point location)
        {
            var label = new Label
            {
                Text = text,
                Location = location,
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.FromArgb(50, 50, 50)
            };
            Controls.Add(label);
            return label;
        }

        private Button CreateButton(string text, Point location, Color backColor, EventHandler clickHandler)
        {
            var button = new Button
            {
                Text = text,
                Location = location,
                BackColor = backColor,
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Font = new Font("Segoe UI", 9, FontStyle.Bold)
            };
            button.FlatAppearance.BorderSize = 0;
            button.Click += clickHandler;
            return button;
        }

        private static string? GetLocalIPv4Address()
        {
            try
            {
                foreach (var networkInterface in NetworkInterface.GetAllNetworkInterfaces())
                {
                    if (networkInterface.OperationalStatus == OperationalStatus.Up &&
                        networkInterface.NetworkInterfaceType != NetworkInterfaceType.Loopback)
                    {
                        foreach (var ip in networkInterface.GetIPProperties().UnicastAddresses)
                        {
                            if (ip.Address.AddressFamily == AddressFamily.InterNetwork)
                            {
                                return ip.Address.ToString();
                            }
                        }
                    }
                }
            }
            catch (Exception)
            {
                // Silently handle exceptions
            }
            return null;
        }

        private async void BtnConnect_Click(object? sender, EventArgs e)
        {
            if (_isRunning)
            {
                _networkManager.Stop();
                UpdateStatus("Отключено", Color.Gray);
                btnConnect.Text = "Подключиться";
                _isRunning = false;
                return;
            }

            try
            {
                btnConnect.Enabled = false;
                UpdateStatus("Подключение...", Color.Orange);

                bool isServer = rbServer.Checked;
                string ip = txtIP.Text.Trim();
                if (!int.TryParse(txtPort.Text, out int port))
                {
                    throw new Exception("Неверный номер порта");
                }

                await _networkManager.Start(isServer, ip, port);
                _isRunning = true;
                btnConnect.Text = "Отключиться";
                UpdateStatus("Подключено", Color.Green);
            }
            catch (Exception ex)
            {
                UpdateStatus($"Ошибка: {ex.Message}", Color.Red);
            }
            finally
            {
                btnConnect.Enabled = true;
            }
        }

        private async void BtnSend_Click(object? sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtMessage.Text) || !_isRunning)
                return;

            try
            {
                await _networkManager.SendMessage(txtMessage.Text.Trim());
                AppendChat($"Вы: {txtMessage.Text}");
                txtMessage.Clear();
            }
            catch (Exception ex)
            {
                AppendChat($"Ошибка отправки сообщения: {ex.Message}");
            }
        }

        private void AppendChat(string text)
        {
            if (txtChat.InvokeRequired)
            {
                txtChat.Invoke(new Action<string>(AppendChat), text);
            }
            else
            {
                txtChat.AppendText($"{text}{Environment.NewLine}");
            }
        }

        private void UpdateStatus(string text, Color color)
        {
            if (lblStatus.InvokeRequired)
            {
                lblStatus.Invoke(new Action<string, Color>(UpdateStatus), text, color);
            }
            else
            {
                lblStatus.Text = text;
                lblStatus.ForeColor = color;
            }
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            _networkManager.Stop();
            base.OnFormClosing(e);
        }
    }

    public class CryptoManager
    {
        public RSA OurRSA { get; } = RSA.Create();
        public RSA? OtherSideRSA { get; set; }
        public byte[]? AesKey { get; set; }
        public byte[]? AesIV { get; set; }
        public bool IsAesReady => AesKey != null && AesIV != null;

        public void GenerateAesKey()
        {
            using var aes = Aes.Create();
            aes.KeySize = 256;
            aes.GenerateKey();
            aes.GenerateIV();
            AesKey = aes.Key;
            AesIV = aes.IV;
        }

        public byte[] AesEncrypt(byte[] data)
        {
            if (AesKey == null || AesIV == null)
                throw new InvalidOperationException("AES ключ или IV не инициализированы");

            using var aes = Aes.Create();
            aes.Key = AesKey;
            aes.IV = AesIV;
            aes.Mode = CipherMode.CBC;
            aes.Padding = PaddingMode.PKCS7;
            using var ms = new MemoryStream();
            using (var encryptor = aes.CreateEncryptor())
            using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
            {
                cs.Write(data, 0, data.Length);
            }
            return ms.ToArray();
        }

        public byte[] AesDecrypt(byte[] data)
        {
            if (AesKey == null || AesIV == null)
                throw new InvalidOperationException("AES ключ или IV не инициализированы");

            using var aes = Aes.Create();
            aes.Key = AesKey;
            aes.IV = AesIV;
            aes.Mode = CipherMode.CBC;
            aes.Padding = PaddingMode.PKCS7;
            using var ms = new MemoryStream();
            using (var decryptor = aes.CreateDecryptor())
            using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Write))
            {
                cs.Write(data, 0, data.Length);
            }
            return ms.ToArray();
        }
    }

    public class NetworkManager
    {
        private readonly CryptoManager _crypto;
        private readonly Action<string> _appendChat;
        private TcpListener? _listener;
        private TcpClient? _client;
        private NetworkStream? _stream;
        private Thread? _receiveThread;
        private bool _stopThreads;
        private bool _isServer;

        public NetworkManager(CryptoManager crypto, Action<string> appendChat)
        {
            _crypto = crypto;
            _appendChat = appendChat;
        }

        public async Task Start(bool isServer, string ip, int port)
        {
            _isServer = isServer;
            _stopThreads = false;

            if (isServer)
                await StartServer(port);
            else
                await StartClient(ip, port);
        }

        private async Task StartServer(int port)
        {
            _listener = new TcpListener(IPAddress.Any, port);
            _listener.Start();
            _appendChat("Сервер запущен. Ожидание подключения...");

            _client = await _listener.AcceptTcpClientAsync();
            _stream = _client.GetStream();
            _appendChat("Клиент подключился");

            await ExchangeKeys();
            _crypto.GenerateAesKey();
            await SendAesKey();

            StartReceiveLoop();
        }

        private async Task StartClient(string ip, int port)
        {
            _client = new TcpClient();
            await _client.ConnectAsync(IPAddress.Parse(ip), port);
            _stream = _client.GetStream();
            _appendChat("Подключено к серверу");

            await ExchangeKeys();
            await ReceiveAesKey();

            StartReceiveLoop();
        }

        private async Task ExchangeKeys()
        {
            if (_isServer)
            {
                await ReceivePublicKey();
                await SendPublicKey();
            }
            else
            {
                await SendPublicKey();
                await ReceivePublicKey();
            }
        }

        private async Task SendPublicKey()
        {
            var xmlPublicKey = _crypto.OurRSA.ToXmlString(false);
            var keyBytes = Encoding.UTF8.GetBytes(xmlPublicKey);
            var lengthBytes = BitConverter.GetBytes(keyBytes.Length);
            await _stream!.WriteAsync(lengthBytes, 0, lengthBytes.Length);
            await _stream!.WriteAsync(keyBytes, 0, keyBytes.Length);
            _appendChat("Публичный ключ отправлен");
        }

        private async Task ReceivePublicKey()
        {
            var lengthBytes = new byte[4];
            await ReadExactAsync(lengthBytes, 4);
            int keyLength = BitConverter.ToInt32(lengthBytes, 0);

            var keyBytes = new byte[keyLength];
            await ReadExactAsync(keyBytes, keyLength);

            var publicKeyXml = Encoding.UTF8.GetString(keyBytes);
            var rsa = RSA.Create();
            rsa.FromXmlString(publicKeyXml);
            _crypto.OtherSideRSA = rsa;

            _appendChat("Получен публичный ключ собеседника");
        }

        private async Task SendAesKey()
        {
            using var ms = new MemoryStream();
            ms.Write(BitConverter.GetBytes(_crypto.AesKey!.Length), 0, 4);
            ms.Write(_crypto.AesKey, 0, _crypto.AesKey.Length);
            ms.Write(BitConverter.GetBytes(_crypto.AesIV!.Length), 0, 4);
            ms.Write(_crypto.AesIV, 0, _crypto.AesIV.Length);

            var rawData = ms.ToArray();
            var encrypted = _crypto.OtherSideRSA!.Encrypt(rawData, RSAEncryptionPadding.Pkcs1);

            var lengthBytes = BitConverter.GetBytes(encrypted.Length);
            await _stream!.WriteAsync(lengthBytes, 0, lengthBytes.Length);
            await _stream!.WriteAsync(encrypted, 0, encrypted.Length);

            _appendChat("AES-ключ отправлен");
        }

        private async Task ReceiveAesKey()
        {
            var lenBytes = new byte[4];
            await ReadExactAsync(lenBytes, 4);
            int encLen = BitConverter.ToInt32(lenBytes, 0);

            var encBlock = new byte[encLen];
            await ReadExactAsync(encBlock, encLen);

            var rawData = _crypto.OurRSA.Decrypt(encBlock, RSAEncryptionPadding.Pkcs1);

            int offset = 0;
            int keyLen = BitConverter.ToInt32(rawData, offset);
            offset += 4;
            _crypto.AesKey = new byte[keyLen];
            Buffer.BlockCopy(rawData, offset, _crypto.AesKey, 0, keyLen);
            offset += keyLen;

            int ivLen = BitConverter.ToInt32(rawData, offset);
            offset += 4;
            _crypto.AesIV = new byte[ivLen];
            Buffer.BlockCopy(rawData, offset, _crypto.AesIV, 0, ivLen);

            _appendChat("Получен AES-ключ от сервера");
        }

        public async Task SendMessage(string message)
        {
            if (!_crypto.IsAesReady)
                throw new InvalidOperationException("AES-ключ не готов");

            var messageBytes = Encoding.UTF8.GetBytes(message);
            var signature = _crypto.OurRSA.SignData(messageBytes, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
            var sigLenBytes = BitConverter.GetBytes(signature.Length);

            using var ms = new MemoryStream();
            ms.Write(sigLenBytes, 0, sigLenBytes.Length);
            ms.Write(signature, 0, signature.Length);
            ms.Write(messageBytes, 0, messageBytes.Length);

            var combined = ms.ToArray();
            var encrypted = _crypto.AesEncrypt(combined);

            var lengthBytes = BitConverter.GetBytes(encrypted.Length);
            await _stream!.WriteAsync(lengthBytes, 0, lengthBytes.Length);
            await _stream!.WriteAsync(encrypted, 0, encrypted.Length);
        }

        private void StartReceiveLoop()
        {
            _receiveThread = new Thread(async () =>
            {
                while (!_stopThreads)
                {
                    try
                    {
                        var lengthBytes = new byte[4];
                        int readCount = await _stream!.ReadAsync(lengthBytes, 0, 4);
                        if (readCount == 0)
                            break;

                        int dataLength = BitConverter.ToInt32(lengthBytes, 0);
                        var encryptedData = new byte[dataLength];
                        await ReadExactAsync(encryptedData, dataLength);

                        if (!_crypto.IsAesReady)
                            continue;

                        var decrypted = _crypto.AesDecrypt(encryptedData);
                        int sigLen = BitConverter.ToInt32(decrypted, 0);
                        var signBytes = new byte[sigLen];
                        Buffer.BlockCopy(decrypted, 4, signBytes, 0, sigLen);

                        int msgOffset = 4 + sigLen;
                        int msgLen = decrypted.Length - msgOffset;
                        var messageBytes = new byte[msgLen];
                        Buffer.BlockCopy(decrypted, msgOffset, messageBytes, 0, msgLen);

                        bool valid = _crypto.OtherSideRSA?.VerifyData(
                            messageBytes,
                            signBytes,
                            HashAlgorithmName.SHA256,
                            RSASignaturePadding.Pkcs1) ?? false;

                        var message = Encoding.UTF8.GetString(messageBytes);
                        _appendChat(valid ? $"Собеседник: {message}" : "Сообщение с неверной подписью!");
                    }
                    catch (Exception ex)
                    {
                        if (!_stopThreads)
                            _appendChat($"Ошибка приёма: {ex.Message}");
                        break;
                    }
                }
            })
            {
                IsBackground = true
            };
            _receiveThread.Start();
        }

        private async Task ReadExactAsync(byte[] buffer, int size)
        {
            int offset = 0;
            while (offset < size)
            {
                int read = await _stream!.ReadAsync(buffer, offset, size - offset);
                if (read == 0)
                    throw new Exception("Соединение закрыто");
                offset += read;
            }
        }

        public void Stop()
        {
            _stopThreads = true;
            try
            {
                _listener?.Stop();
                _client?.Close();
                _stream?.Close();
            }
            catch { }
        }
    }
}