using System;
using System.Diagnostics;

namespace fxxkPRIME
{
    class Program
    {
        static void Main(string[] args)
        {
            Process[] py = System.Diagnostics.Process.GetProcessesByName("python");
            foreach (var VARIABLE in py)
                if (VARIABLE.MainModule.FileName.Contains("PIME"))
                    VARIABLE.Kill();
        }
    }
}
