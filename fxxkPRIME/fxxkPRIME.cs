using System;
using System.Diagnostics;
using System.Threading;

namespace fxxkPRIME
{
    class Program
    {
        static void Main(string[] args)
        {
            Process[] py = System.Diagnostics.Process.GetProcessesByName("pythonw");
            foreach (var VARIABLE in py)
            {
                if (VARIABLE.MainModule.FileName.Contains("PIME"))
                {
                    System.Console.WriteLine("{0}: {1}", VARIABLE.Id, VARIABLE.MainModule.FileName);
                    VARIABLE.Kill();
                }
            }
        }
    }
}
