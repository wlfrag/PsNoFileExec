![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/97900a55-a25c-44df-990c-43b7d84471bb)# PsNoFileExec
Fileless Psexec.
This will authenticate to the target's DCE/RPC interface which allows us to access the service control manager.
We then edit an existing service with our payload string and execute it.

This implements my other github project: **Amsi-shell**: where it creates amsi-bypass and windef undetected meterpreter payload in powershell.


On victim:
![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/c78e1439-68b8-444f-8aed-1e486eaee99f)
We can execute our payload string using PsNoFileExec.

On Kali:
![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/0e97f7eb-054e-4d6e-8aa3-2a38f72c74d7)
Webserver gets request
![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/679da885-d720-468c-9a2c-9a83e9e75319)
Meterpreter shell received.

Analyzing the service:

![image](https://github.com/wlfrag/PsNoFileExec/assets/43529877/7c181541-4b6f-423b-8459-8bb783a3feb1)
