using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Linq;
using System.Windows.Forms;

namespace Kod
{
    public partial class Form1 : Form
    {
        private string textVariable;
        private bool check = false;
        private string str;

        private const string ShannonColumn = "ShannonFano";
        private const string HuffmanColumn = "Huffman";

        public Form1()
        {
            InitializeComponent();
            InitializeDataGridView();
        }

        private void InitializeDataGridView()
        {
            resDataGridView.Columns.Add(ShannonColumn, "Шеннон-Фано");
            resDataGridView.Columns.Add(HuffmanColumn, "Хаффман");
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(TextBox.Text))
            {
                MessageBox.Show("Пожалуйста, введите текст или загрузите файл.", "Неверный ввод");
                return;
            }

            try
            {
                if (textVariable != TextBox.Text)
                    check = false;

                str = check ? textVariable.ToLower() : TextBox.Text.ToLower();

                // Calculate probabilities
                Dictionary<char, double> probabilities = CalculateProbabilities(str);

                // Shannon-Fano
                var (shannonCodes, lFan) = CalculateShannonFano(probabilities);
                LogCodes("Shannon-Fano", shannonCodes, probabilities);

                // Entropy (same for both algorithms)
                double entropy = CalculateEntropy(probabilities.Values.ToArray());
                double dFan = lFan > 0 ? (lFan - entropy) / lFan : 0;

                // Huffman
                var (huffmanCodes, lHof) = CalculateHuffman(probabilities);
                LogCodes("Huffman", huffmanCodes, probabilities);

                double dHof = lHof > 0 ? (lHof - entropy) / lHof : 0;

                // Update UI
                PopulateDataGridView(probabilities, shannonCodes, huffmanCodes);

                ShIlabel.Text = $"I = {lFan:F12}";
                ShHlabel.Text = $"H = {entropy:F12}";
                ShDlabel.Text = $"D = {dFan:F12}";

                HafILabel.Text = $"I = {lHof:F12}";
                HafHlabel.Text = $"H = {entropy:F12}";
                HafDlabel.Text = $"D = {dHof:F12}";
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка обработки данных: {ex.Message}", "Ошибка");
            }
        }

        private void LogCodes(string method, Dictionary<char, string> codes, Dictionary<char, double> probs)
        {
            string log = $"{method} Codes and Lengths:\n";
            double weightedLength = 0;
            foreach (var kvp in codes.OrderBy(k => k.Key))
            {
                char symbol = kvp.Key;
                string code = kvp.Value;
                double prob = probs.ContainsKey(symbol) ? probs[symbol] : 0;
                int length = code.Length;
                weightedLength += prob * length;
                log += $"Symbol: {symbol}, Code: {code}, Length: {length}, Prob: {prob:F4}, Weighted: {prob * length:F4}\n";
            }
            log += $"Average Length (I) = {weightedLength:F4}\n";
            System.Diagnostics.Debug.WriteLine(log);
        }

        private void Button2_Click(object sender, EventArgs e)
        {
            check = true;
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Текстовые файлы (*.txt)|*.txt|Все файлы (*.*)|*.*",
                Title = "Выберите текстовый файл"
            };

            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                try
                {
                    string filePath = openFileDialog.FileName;
                    textVariable = File.ReadAllText(filePath);
                    TextBox.Text = textVariable;
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка чтения файла: {ex.Message}", "Ошибка файла");
                    check = false;
                }
            }
        }

        private Dictionary<char, double> CalculateProbabilities(string text)
        {
            if (string.IsNullOrEmpty(text))
                return new Dictionary<char, double>();

            var probs = text.GroupBy(c => c)
                           .ToDictionary(
                               g => g.Key,
                               g => (double)g.Count() / text.Length
                           );

            // Ensure probabilities sum to 1 (for numerical stability)
            double sum = probs.Values.Sum();
            if (Math.Abs(sum - 1.0) > 1e-10)
            {
                foreach (var key in probs.Keys.ToList())
                {
                    probs[key] /= sum;
                }
            }

            return probs;
        }

        private void PopulateDataGridView(Dictionary<char, double> probabilities, Dictionary<char, string> shannonCodes, Dictionary<char, string> huffmanCodes)
        {
            resDataGridView.Rows.Clear();
            foreach (var kvp in probabilities.OrderByDescending(x => x.Value))
            {
                char c = kvp.Key;
                resDataGridView.Rows.Add(
                    c,
                    $"{kvp.Value:F4}",
                    shannonCodes.ContainsKey(c) ? shannonCodes[c] : "",
                    huffmanCodes.ContainsKey(c) ? huffmanCodes[c] : ""
                );
            }
        }

        private double CalculateEntropy(double[] probabilities)
        {
            if (probabilities.Length == 0)
                return 0;

            double sum = probabilities.Sum();
            if (sum == 0)
                return 0;

            return probabilities.Sum(p => p > 0 ? -p / sum * Math.Log(p / sum, 2) : 0);
        }

        private (Dictionary<char, string>, double) CalculateShannonFano(Dictionary<char, double> probabilities)
        {
            ShannonFanoEncoder encoder = new ShannonFanoEncoder(probabilities);
            var codes = encoder.Encode();
            double avgLength = codes.Any() ? probabilities.Sum(kvp => kvp.Value * codes[kvp.Key].Length) : 0;
            return (codes, avgLength);
        }

        private (Dictionary<char, string>, double) CalculateHuffman(Dictionary<char, double> probabilities)
        {
            HuffmanTree huffmanTree = new HuffmanTree();
            huffmanTree.Build(probabilities);
            var codes = huffmanTree.ReturnAlphabet();
            double avgLength = codes.Any() ? probabilities.Sum(kvp => kvp.Value * codes[kvp.Key].Length) : 0;
            return (codes, avgLength);
        }
    }
}