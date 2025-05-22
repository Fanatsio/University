using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Net.WebRequestMethods;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace lab4_6
{
    public partial class Form1 : Form
    {

        public Form1()
        {
            InitializeComponent(); 
            webBrowser.Url = new Uri("C:\\");
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            using(FolderBrowserDialog fbd= new FolderBrowserDialog() { Description="Select your path."})
            {
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    webBrowser.Url = new Uri(fbd.SelectedPath);
                    txtPath.Text = fbd.SelectedPath;
                }
            }

        }

        private void btnBack_Click(object sender, EventArgs e)
        {
            if(webBrowser.CanGoBack)
                webBrowser.GoBack();
        }

        private void btnForward_Click(object sender, EventArgs e)
        {
            if(webBrowser.CanGoForward)
                webBrowser.GoForward();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            var FD = new System.Windows.Forms.OpenFileDialog();
            if (FD.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                listBox1.Items.Clear();

                webBrowser.Url = new Uri(Path.GetDirectoryName(FD.FileName)); //fbd.SelectedPath
                txtPath.Text = Path.GetDirectoryName(FD.FileName); //fbd.SelectedPath

                var path = Path.GetFullPath(FD.FileName); //fbd.SelectedPath
                var dir = Path.GetDirectoryName(path);
                var file = Path.GetFileName(path);

                var shellAppType = Type.GetTypeFromProgID("Shell.Application");
                dynamic shell = Activator.CreateInstance(shellAppType);
                var folder = shell.NameSpace(dir);
                var folderItem = folder.ParseName(file);

                var names =
                    (from idx in Enumerable.Range(0, short.MaxValue)
                     let key = (string)folder.GetDetailsOf(null, idx)
                     where !string.IsNullOrEmpty(key)
                     select (idx, key)).ToDictionary(p => p.idx, p => p.key);

                var properties =
                    (from idx in names.Keys
                     orderby idx
                     let value = (string)folder.GetDetailsOf(folderItem, idx)
                     where !string.IsNullOrEmpty(value)
                     select (name: names[idx], value)).ToList();

                foreach (var kvp in properties)
                    //MessageBox.Show($"{kvp.name}: {kvp.value}");
                    listBox1.Items.Add($"{kvp.name}: {kvp.value}");
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            string path = "D:\\";
            string searchPattern = "*" + FileFindTextBox.Text + "*"; // "*.jpg";
            SearchOption searchOption = SearchOption.AllDirectories;
            listBox1.Items.Clear();

            string folderName = @"C:\Search";
            string pathString = Path.Combine(folderName);
            Directory.CreateDirectory(pathString);

            var dirs = new Stack<string>();
            dirs.Push(path);

            while (dirs.Count > 0)
            {
                string currentDirPath = dirs.Pop();
                if (searchOption == SearchOption.AllDirectories)
                {
                    try
                    {
                        string[] subDirs = Directory.GetDirectories(currentDirPath);
                        foreach (string subDirPath in subDirs)
                        {
                            dirs.Push(subDirPath);
                        }
                    }
                    catch (UnauthorizedAccessException)
                    {
                        continue;
                    }
                    catch (DirectoryNotFoundException)
                    {
                        continue;
                    }
                }

                string[] files = null;
                try
                {
                    files = Directory.GetFiles(currentDirPath, searchPattern);
                }
                catch (UnauthorizedAccessException)
                {
                    continue;
                }
                catch (DirectoryNotFoundException)
                {
                    continue;
                }

                foreach (string filePath in files)
                {
                    listBox1.Items.Add(filePath);
                    //System.IO.File.Copy("C:\\Search", filePath);
                }

                //webBrowser.Url = new Uri("C:\\Search");
            }
        }

        private void button3_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog fbd = new FolderBrowserDialog() { Description = "Select your path." })
            {
                if (fbd.ShowDialog() == DialogResult.OK)
                {
                    webBrowser.Url = new Uri(fbd.SelectedPath);
                    txtPath.Text = fbd.SelectedPath;

                    var path = fbd.SelectedPath;
                    var dir = Path.GetDirectoryName(path);
                    var file = Path.GetFileName(path);

                    var shellAppType = Type.GetTypeFromProgID("Shell.Application");
                    dynamic shell = Activator.CreateInstance(shellAppType);
                    var folder = shell.NameSpace(dir);
                    var folderItem = folder.ParseName(file);

                    var names =
                        (from idx in Enumerable.Range(0, short.MaxValue)
                         let key = (string)folder.GetDetailsOf(null, idx)
                         where !string.IsNullOrEmpty(key)
                         select (idx, key)).ToDictionary(p => p.idx, p => p.key);

                    var properties =
                        (from idx in names.Keys
                         orderby idx
                         let value = (string)folder.GetDetailsOf(folderItem, idx)
                         where !string.IsNullOrEmpty(value)
                         select (name: names[idx], value)).ToList();

                    listBox1.Items.Clear();

                    foreach (var kvp in properties)
                        //MessageBox.Show($"{kvp.name}: {kvp.value}");
                        listBox1.Items.Add($"{kvp.name}: {kvp.value}");
                }
            }
        }
    }
}
