import os
import psycopg2

# connect to heroku postgresql
DATABASE_URL = 'postgres://cdorzbbtfrirkm:6e978aad35cb9237bcb6fc13c93f6d8dbf2a8c8b3e45da6a1cc100ae594d0ee0@ec2-23-21-106-241.compute-1.amazonaws.com:5432/derig0btqgd9lq'
conn = psycopg2.connect(DATABASE_URL,sslmode='require')
cur = conn.cursor()

# arraylist to show InfoTitle
InfoTitle = ['hench','type','level','dropped','formulars']


## way to select by variable
# select = "SELECT * FROM student WHERE age = %(age)s"
# cursor.execute(select, { 'age': 15 })
def selectMonster(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT * FROM formular WHERE replace(LOWER(hench),' ','')= %(hench)s"
        cur.execute(select,{'hench':hench})
        
        s = ''
        for row in cur:
                for i in range(4):
                        s += str(InfoTitle[i] +' : '+ row[i]+'\n')
                temp = str(row[4]).lstrip('[').rstrip(']')
                temp = wordBeautify(temp)
                s += str(InfoTitle[4] +' : \n'+ temp)
        return s

def selectFormular(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT formulars FROM formular WHERE replace(LOWER(hench),' ','')= %(hench)s"
        cur.execute(select,{'hench':hench})

        formular = str(cur.fetchone()[0]).lstrip('[').rstrip(']')
        return formular

def selectMonsterinFormular(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT formulars FROM formular WHERE replace(lower(hench),' ','') = %(hench)s"
        cur.execute(select,{'hench':hench})

        # type:string
        f = cur.fetchone()[0]

        formulars = []
        # change type to List
        if f != '[]':
                formulars = str(f).lstrip('[').rstrip(']').replace('\'','').replace(' ','').replace('[1]','').replace('[2]','').replace('[3]','').replace('+',',').split(',')

        # remove redundent in list
        formulars = list(dict.fromkeys(formulars))
        return formulars

def selectMonsterInsensitive(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT hench FROM formular WHERE replace(lower(hench),' ','') ~* %(hench)s"
        cur.execute(select,{'hench':hench})

        possiblehenchs = []
        for each in cur:
                possiblehenchs.append(each[0])
        return possiblehenchs

def selectPic(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT pic FROM formular WHERE replace(LOWER(hench),' ','')= %(hench)s"
        cur.execute(select,{'hench':hench})

        pic = cur.fetchone()
        return pic[0]

def selectCanBeMixed(hench):
        hench = hench.lower().replace(' ','').replace('[','\[').replace(']','\]')
        select = "select hench from formular WHERE replace(lower(formulars),' ','') ~* %(hench)s"
        if '[' in hench and ']' in hench:
                cur.execute(select,{'hench':hench})
        else:
                cur.execute(select,{'hench':'\y' + hench +'\y'})

        f = cur.fetchall()
        fList = []
        for each in f:
                fList.append(each[0])
                
        return fList

def selectLevel(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT level FROM formular WHERE replace(LOWER(hench),' ','')= %(hench)s"
        cur.execute(select,{'hench':hench})

        hench_lvl = cur.fetchone()[0]
        return hench_lvl

def selectHenchByLevel(hench_lvl):
        select = "SELECT hench FROM formular WHERE level ~* %(hench_lvl)s"
        cur.execute(select,{'hench_lvl':'\y' + hench_lvl + '~'})

        fList = []
        for each in cur.fetchall():
                fList.append(each[0])
        return fList

def selectDropped(hench):
        hench = hench.lower().replace(' ','')
        select = "SELECT dropped FROM formular WHERE replace(lower(hench),' ','') = %(hench)s"
        cur.execute(select,{'hench':hench})

        hench_drop = cur.fetchone()[0]
        return hench_drop

def wordBeautify(temp):
        s = ' --- '
        s += str(temp).replace('\'','').replace(', ',',\n --- ')
        return s