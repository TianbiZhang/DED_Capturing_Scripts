using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            run_cmd();
        }

        private void run_cmd()
        {

            string fileName = @"C:\Users\tianbi\Documents\DED_script_new\SimpleCapture.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(@"C:\Users\tianbi\AppData\Local\Programs\Python\Python37\python.exe", fileName)
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            textBox1.Text = output;

        }

        private void run_cmd_th()
        {

            string fileName = @"C:\Users\tianbi\Documents\DED_script_new\Threshold_trial.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(@"C:\Users\tianbi\AppData\Local\Programs\Python\Python37\python.exe", fileName)
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            textBox1.Text = output;

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            run_cmd_th();
        }

        private void buttonCallFunction_Click(object sender, EventArgs e)
        {

        }
    }
}
