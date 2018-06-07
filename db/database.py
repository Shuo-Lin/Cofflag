
import pymysql.cursors
import configz

class flagDB(object):

    def __init__(self, host='', port=0, user='user', password='pass', db='db'):
        self.dbConnection =pymysql.connect(host ='localhost',
                                           port =configz.dbport,
                                           user =configz.dbuser,
                                           password =configz.dbpasswd,
                                           db =configz.dbname,
                                           charset ='utf8mb4',
                                           cursorclass = pymysql.cursors.DictCursor
                                           )
    
    def executeSql(self, sqlCode, description ='execute'):
        with self.dbConnection.cursor() as cursor:
            cursor.execute(sqlCode)
        self.dbConnection.commit()
        print description +':done'
        return 1
    
    def querySql(self, sqlCode, description='query'):
        with self.dbConnection.cursor() as cursor:
            cursor.execute(sqlCode)
            result =cursor.fetchall()
        print description +':done'
        return result

    def createTable(self,tableName):
        if tableName =='chatgroup':
            sqlCode='create table if not exists chatgroup(' +\
                    'g_id smallint auto_increment primary key,' +\
                    'name varchar(64),' +\
                    'detail varchar(255)' +\
                    ');'
        elif tableName =='user':
            sqlCode='create table if not exists user(' +\
                    'u_id smallint auto_increment primary key,' +\
                    'name varchar(32),' +\
                    'gender varchar(6),' +\
                    'school varchar(10),' +\
                    'chatgroup smallint,' +\
                    'foreign key (chatgroup) references chatgroup(g_id)' +\
                    ');'
        elif tableName =='flag_type':
            sqlCode='create table if not exists flag_type(' +\
                    'ft_id smallint auto_increment primary key,' +\
                    'icon_on varchar(16),' +\
                    'icon_off varchar(16)' +\
                    ');'
        elif tableName =='position':
            sqlCode='create table if not exists postion(' +\
                    'p_id smallint auto_increment primary key,' +\
                    'name varchar(32),' +\
                    'location_x int,' +\
                    'location_y int' +\
                    ');'
        elif tableName =='flag':
            sqlCode='create table if not exists flag(' +\
                    'f_id smallint auto_increment primary key,' +\
                    'name varchar(32),' +\
                    'details varchar(255),' +\
                    'state smallint,' +\
                    'p_id smallint,' +\
                    'ft_id smallint,' +\
                    'date timestamp,' +\
                    'time varchar(15),' +\
                    'foreign key (p_id) references postion(p_id),' +\
                    'foreign key (ft_id) references flag_type(ft_id)' +\
                    ');'
        elif tableName =='has_flag':
            sqlCode='create table if not exists has_flag(' +\
                    'u_id smallint ,' +\
                    'f_id smallint ,' +\
                    'PRIMARY KEY (u_id,f_id),' +\
                    'foreign key (u_id) references user(u_id),' +\
                    'foreign key (f_id) references flag(f_id)' +\
                    ');'
        elif tableName =='friend':
            sqlCode='create table if not exists friend(' +\
                    'u1_id smallint ,' +\
                    'u2_id smallint ,' +\
                    'PRIMARY KEY (u1_id,u2_id),' +\
                    'foreign key (u1_id) references user(u_id),' +\
                    'foreign key (u2_id) references user(u_id)' +\
                    ');'

        else:
            print 'what do you want to do?'
            return 0
        
        res =self.executeSql(sqlCode, 'createTable:'+tableName)
        return res
    
    def deleteTable(self, tableName):
        sqlCode ='DROP TABLE ' +tableName +';'

        res =self.executeSql(sqlCode, 'dropTable:'+tableName)
        return res

    def closeConnection(self):
        res =self.dbConnection.close()
        return res

class chatgroupTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='chatgroup'
        print self._tableName+':Table init done'

    def addGroup(self, name='NONE', detail='NONE'):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, detail) VALUES (\'' +\
                 name +'\', \'' +detail+'\');'
        res =self.executeSql(sqlCode, 'addGroup:'+name)
        return res
    
    def updateGroup(self, name='NONE', detail='NONE'):
        sqlCode ='UPDATE ' + self._tableName +' SET name=\'' +name +'\', ' +' descripton=\'' + detail+ '\' WHERE name=\'' +name +'\';' 
        res =self.executeSql(sqlCode, 'updateGroup:'+name)
        return res

    def queryGroup(self, g_id=0):
        if int(g_id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE g_id=' +str(g_id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +';'
        res =self.querySql(sqlCode, 'query:Group')
        return res

    def deleteGroup(self, g_id):
        if int(g_id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE g_id=' +str(g_id) +';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'query:Group')
        return res

class userTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='user'
        print self._tableName+':Table init done'

    def deleteUser(self, name='NONE'):
        if name =='NONE':
            sqlCode ='DELETE FROM ' +self._tableName+';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE name=\'' +name +'\';'
        res =self.executeSql(sqlCode, 'deleteUser:'+name)
        return res

    def addUser(self, name, school, gender, chatgroup='1'):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, school, gender, chatgroup) VALUES (\'' +\
                 name +'\', \'' +school +'\', \'' +gender +'\', \'' +str(chatgroup)+'\');'
        res =self.executeSql(sqlCode, 'addUser:'+name)
        return res
    
    def queryUser(self, name='ALLU'):
        if name =='ALLU':
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\'' +name +'\';'
        res =self.querySql(sqlCode, 'query:User')
        return res

    def queryUserByID(self, u_id):
        if int(u_id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE u_id=' +str(u_id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'query:User')
        return res

    def queryUserByGroup(self, chatgroup):
        if int(chatgroup):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE chatgroup=' +str(chatgroup) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'query:User')
        return res

    def updateUser(self, name, school, gender, chatgroup='1'):
        sqlCode ='UPDATE ' + self._tableName +' SET school=\'' +school +'\', ' +' gender=\'' + gender +' chatgroup=\'' + str(chatgroup) +'\' WHERE name=\'' +name +'\';' 
        res =self.executeSql(sqlCode, 'updateUser:'+name)
        return res

class flagTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='flag'
        print self._tableName+':Table init done'

    def deleteFlag(self, id):
        if int(id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE f_id=' +str(id) +';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'deleteFlag:'+str(id))
        return res

    def addFlag(self, name, details, p_id,ft_id, date, time,state=0):
        sqlCode ='INSERT INTO ' +self._tableName +' (name,state, details, p_id,ft_id, date, time) VALUES (\'' +\
                 name +'\', \'' +str(state) +'\', \'' +details +'\', \'' +str(p_id) +'\', \''+str(ft_id) +'\', \'' +date +'\', \'' +time +'\');'
        res =self.executeSql(sqlCode, 'addFlag:'+str(name))
        return res
    
    def queryFlag(self, id):
        if int(id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE f_id=' +str(id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'query:Flag:')
        return res

    def queryFlagByName(self, name='ALLF'):
        if name=='ALLF':
            sqlCode ='SELECT * FROM ' +self._tableName+'\';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE name=\''+name +'\';'
            # print sqlCode
        res =self.querySql(sqlCode, 'query:Flag:ByName:'+name)
        return res

    def updateFlag(self, id ,state):
        sqlCode ='UPDATE ' +self._tableName +' SET state=' +str(state) +' WHERE f_id=' +str(id) +';'
        res =self.executeSql(sqlCode, 'update:Flag')
        return res

class positionTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='postion'
        print self._tableName+':Table init done'

    def addPositon(self, name, location_x, location_y):
        sqlCode ='INSERT INTO ' +self._tableName +' (name, location_x, location_y) VALUES (\'' +\
                 name +'\', \'' +str(location_x) +'\', \'' +str(location_y) +'\');'
        res =self.executeSql(sqlCode, 'addPostion:'+name)
        return res
    
    def deletePositon(self, id):
        if int(id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE p_id=' +str(id)+';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'deleteFlag:'+str(id))
        return res

    def queryPosition(self, id):
        if int(id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE p_id=' +str(id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'query:Positon')
        return res
    
class typeTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='flag_type'
        print self._tableName+':Table init done'
    
    def addType(self, name, icon_off, icon_on):
        sqlCode ='INSERT INTO ' +self._tableName +' (icon_off, icon_on) VALUES (\'' +\
                 icon_off +'\', \'' +icon_on +'\');'
        res =self.executeSql(sqlCode, 'addType:'+name)
        return res

    def deleteType(self, id):
        if int(id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE ft_id=' +str(id) +';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'deleteType:'+str(id))
        return res
    
    def queryType(self, id):
        if int(id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE ft_id=' +str(id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'queryType:'+str(id))
        return res
    
class hasflagTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='has_flag'
        print self._tableName+':Table init done'

    def addHasflag(self, u_id, f_id):
        sqlCode ='INSERT INTO ' +self._tableName +' (u_id, f_id) VALUES (\'' +\
                 str(u_id) +'\', \'' +str(f_id) +'\');'
        res =self.executeSql(sqlCode, 'addHasflag:'+str(f_id)+'-'+str(u_id))
        return res

    def deleteHasflag(self, u_id):
        if int(u_id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE u_id=' +str(u_id) +';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'delateHasflag:'+str(u_id))
        return res

    def queryHasflag(self, u_id):
        if int(u_id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE u_id=' +str(u_id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'queryHasflag')
        return res

class friendTable(flagDB):

    def __init__(self):
        flagDB.__init__(self)
        self._tableName ='friend'
        print self._tableName+':Table init done'
    
    def addFriend(self, u1_id, u2_id):
        sqlCode ='INSERT INTO ' +self._tableName +' (u1_id, u2_id) VALUES (\'' +\
                 str(u1_id) +'\', \'' +str(u2_id) +'\');'
        res =self.executeSql(sqlCode, 'addFriend:'+str(u1_id)+'-'+str(u2_id))
        return res

    def deleteFriend(self, u1_id):
        if int(id):
            sqlCode ='DELETE FROM ' +self._tableName +' WHERE u1_id=' +str(u1_id) +';'
        else:
            sqlCode ='DELETE FROM ' +self._tableName+';'
        res =self.executeSql(sqlCode, 'deleteFriend:'+str(u1_id))
        return res

    def queryFriend(self, u1_id):
        if int(u1_id):
            sqlCode ='SELECT * FROM ' +self._tableName +' WHERE u1_id=' +str(u1_id) +';'
        else:
            sqlCode ='SELECT * FROM ' +self._tableName+';'
        res =self.querySql(sqlCode, 'queryFriend:'+str(u1_id))
        return res



    