# PsNoFileExec
Fileless Psexec.
This will authenticate to the target's DCE/RPC interface which allows us to access the service control manager.
We then edit an existing service with our payload string and execute it.

This implements my other github project: **Amsi-shell**: where it creates amsi-bypass and windef undetected meterpreter payload in powershell.

## Usage

PsNoFileExec.exe [target] [service name] [interactive]

Example: C:\Users\dave.CORP1\Desktop>PsNoFileExec.exe appsrv01 lfsvc 1


[victim]

![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/53fdf7c4-6f3b-45f8-96c6-e4da80562a3f)


We can gain an interactive shell.

We can download and execute our meterpreter payload in powershell as shown above.


[Kali]

![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/beda43a5-2628-4f82-9f7c-5b416fe1b8fb)


Webserver gets request

![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/cfa973ae-f5aa-46c5-9f83-53dd2f3f4af3)


Meterpreter shell received.



## Analyzing the service:

![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/96782e0a-e2b8-4e00-892e-1a456c473f78)

Supports continuous execution.

