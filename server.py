import tornado.ioloop
import tornado.web
import tornado.template
import jinja2
import threading
import configz
import json

def loadModule(name, path):
    import os, imp
    return imp.load_source(name, os.path.join(os.path.dirname(__file__), path))

loadModule('database', 'db/database.py')
import database

class myTemplate(object):
    def __init__(self, template_instance):
        self.template_instance =template_instance

    def generate(self, **kwargs):
        return self.template_instance.render(**kwargs)

class Jinja2Loader(tornado.template.BaseLoader):
    def __init__(self, **kwargs):
        self.jinja_environment =jinja2.Environment(loader=jinja2.FileSystemLoader('pages/'), **kwargs)
        self.templates ={}
        self.lock =threading.RLock()

    def resolve_path(self, name, parent_path =None):
        return name

    def _create_template(self, name):
        template_instance =myTemplate(self.jinja_environment.get_template(name))
        return template_instance

class homePage(tornado.web.RequestHandler):
    def get(self):
        self.render("homepage.html", mytitle="Welcome to Cofflag", parameter=['upload_data','cache_data'])

class createUser(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        self.write({'status':False,'httpstatus':200,'info':'method_denied'})

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraCount =0
            paraDict ={}
            paraList =['name','school','gender','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                userdb.addUser(paraDict['name'],paraDict['school'],paraDict['gender'])
                res =userdb.queryUser(paraDict['name'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)
        

class updateUser(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        self.write({'status':False,'httpstatus':200,'info':'method_denied'})

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['name','school','gender','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                userdb.updateUser(paraDict['name'],paraDict['school'],paraDict['gender'])
                # userdb.deleteUser(name=paraDict['name'])
                # userdb.addUser(paraDict['name'],paraDict['school'],paraDict['gender'])
                res =userdb.queryUser(paraDict['name'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)
        

class getUser(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            # if decryptData[0:4] =='u_id':
            #     paraList =['u_id','token']
            # else:
            #     paraList =['name','token']
            paraList =['u_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                # if decryptData[0:4] =='u_id':
                #     res =userdb.queryUserByID(paraDict['u_id'])
                # else:
                #     res =userdb.queryUser(paraDict['name'])
                res =userdb.queryUserByID(paraDict['u_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)
        
    
    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            if decryptData[0:4] =='u_id':
                paraList =[]
            else:
                paraList =[]
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                if decryptData[0:4] =='u_id':
                    res =userdb.queryUserByID(paraDict['u_id'])
                else:
                    res =userdb.queryUser(paraDict['name'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)
        
class createFlag(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        self.write({'status':False,'httpstatus':200,'info':'method_denied'})

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        paraDict ={}
        paraCount =0
        paraList =['name','details','date','time','uname','p_id','ft_id','token']
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token'})
                print 'wrong token exist now...'
            else:
                flagdb =database.flagTable()
                flagdb.addFlag(paraDict['name'],paraDict['details'],paraDict['p_id'],paraDict['ft_id'],paraDict['date'],paraDict['time'])
                flg2 =flagdb.queryFlagByName(paraDict['name'])

                hsfdb =database.hasflagTable()
                userdb =database.userTable()
                usr =userdb.queryUser(paraDict['uname'])

                hsfdb.addHasflag(usr[0]['u_id'], flg2[-1]['f_id'])
                for flg in flg2:
                    flg['date2'] =flg['date'].strftime('%Y-%m-%d')
                    del flg['date']
                resStr =json.dumps({'status':True,'httpstatus':200,'data':flg})
                self.write(resStr)

class updateFsta(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        self.write({'status':False,'httpstatus':200,'info':'method_denied'})

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        paraDict ={}
        paraCount =0
        paraList =['f_id','state','token']
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token'})
                print 'wrong token exist now...'
            else:
                flagdb =database.flagTable()
                flagdb.updateFlag(paraDict['f_id'],paraDict['state'])
                res =flagdb.queryFlag(paraDict['f_id'])
                for flg in res:
                    flg['date2'] =flg['date'].strftime('%Y-%m-%d')
                    del flg['date']
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                flagdb.closeConnection()
                self.write(resStr)

class getFlag(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            # if decryptData[0:4] =='u_id':
            #     paraList =['u_id','token']
            # else:
            #     paraList =['name','token']
            paraList =['u_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                # if decryptData[0:4] =='u_id':
                #     usr =userdb.queryUserByID(paraDict['u_id'])
                # else:
                #     usr =userdb.queryUser(paraDict['name'])
                usr =userdb.queryUserByID(paraDict['u_id'])
                hasflagdb =database.hasflagTable()
                flagdb =database.flagTable()
                res =[]
                hsf =hasflagdb.queryHasflag(usr[0]['u_id'])
                for every in hsf:
                    flg =flagdb.queryFlag(every['f_id'])
                    flg[0]['date2'] =flg[0]['date'].strftime('%Y-%m-%d')
                    del flg[0]['date']
                    res.append(flg[0])
                resStr =json.dumps({"status":True,"httpstatus":200,"data":res})
                self.write(resStr)

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            if decryptData[0:4] =='u_id':
                paraList =['u_id','token']
            else:
                paraList =['name','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                if decryptData[0:4] =='u_id':
                    usr =userdb.queryUserByID(paraDict['u_id'])
                else:
                    usr =userdb.queryUser(paraDict['name'])
                hasflagdb =database.hasflagTable()
                flagdb =database.flagTable()
                res =[]
                hsf =hasflagdb.queryHasflag(usr[0]['u_id'])
                for every in hsf:
                    flg =flagdb.queryFlag(every['f_id'])
                    flg[0]['date2'] =flg[0]['date'].strftime('%Y-%m-%d')
                    del flg[0]['date']
                    res.append(flg[0])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

class groupgetFlag(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            # if decryptData[0:4] =='u_id':
            #     paraList =['u_id','token']
            # else:
            #     paraList =['name','token']
            paraList =['u_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                userdb=database.userTable()
                me =userdb.queryUserByID(paraDict['u_id'])
                # if decryptData[0:4] =='u_id':
                #     usr =userdb.queryUserByID(paraDict['u_id'])
                # else:
                #     usr =userdb.queryUser(paraDict['name'])
                
                hasflagdb =database.hasflagTable()
                flagdb =database.flagTable()
                res =[]
                if me[0]['chatgroup'] ==1:
                    hsf =hasflagdb.queryHasflag(me[0]['u_id'])
                    for every in hsf:
                        flg =flagdb.queryFlag(every['f_id'])
                        flg[0]['date2'] =flg[0]['date'].strftime('%Y-%m-%d')
                        flg[0]['is_me'] =1
                        del flg[0]['date']
                        res.append(flg[0])
                else:
                    usr =userdb.queryUserByGroup(me[0]['chatgroup'])
                    for everyUser in usr:
                        hsf =hasflagdb.queryHasflag(everyUser['u_id'])
                        for every in hsf:
                            flg =flagdb.queryFlag(every['f_id'])
                            flg[0]['date2'] =flg[0]['date'].strftime('%Y-%m-%d')
                            if everyUser['u_id'] ==int(paraDict['u_id']):
                                flg[0]['is_me'] =1
                            else:
                                flg[0]['is_me'] =0
                            del flg[0]['date']
                            res.append(flg[0])
                resStr =json.dumps({"status":True,"httpstatus":200,"data":res})
                self.write(resStr)

class getPos(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['p_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                posdb =database.positionTable()
                res =posdb.queryPosition(paraDict['p_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['p_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                posdb =database.positionTable()
                res =posdb.queryPosition(paraDict['p_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

class getType(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['ft_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                typdb =database.typeTable()
                res =typdb.queryType(paraDict['ft_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['ft_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                typdb =database.typeTable()
                res =typdb.queryType(paraDict['ft_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

class getFriend(tornado.web.RequestHandler):
    def get(self):
        userIp =self.request.remote_ip
        print 'GET request from : ' +userIp
        decryptData =self.request.query
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['u1_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                fridb =database.friendTable()
                res =fridb.queryFriend(paraDict['u1_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            paraDict ={}
            paraCount =0
            paraList =['u1_id','token']
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token_or_wrong_parameter_amont'})
                print 'wrong token exist now...'
            else:
                fridb =database.friendTable()
                res =fridb.queryFriend(paraDict['u1_id'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':res})
                self.write(resStr)

class createGroup(tornado.web.RequestHandler):
    def get(self):
        pass

    def post(self):
        userIp =self.request.remote_ip
        print 'POST request from : ' +userIp
        decryptData =self.request.body
        paraDict ={}
        paraCount =0
        paraList =['name','detail','token']
        if len(decryptData) ==0:
            self.write({'status':False,'httpstatus':200,'info':'no_parameter'})
            print 'wrong parameter amount exist now...'
        else:
            for everyData in decryptData.split('&'):
                if len(everyData) ==0:
                    break
                oneData =everyData.split('=')
                if oneData[0] in paraList:
                    paraCount +=1
                else:
                    break
                paraDict[oneData[0]] =oneData[1]
            if not(paraCount ==len(paraList) and paraDict['token'] ==configz.token):
                self.write({'status':False,'httpstatus':200,'info':'wrong_token'})
                print 'wrong token exist now...'
            else:
                groupdb =database.chatgroupTable()
                groupdb.addGroup(paraDict['name'],paraDict['detail'])
                resStr =json.dumps({'status':True,'httpstatus':200,'data':groupdb.queryGroup()[-1]})
                self.write(resStr)

def startApp():
    return tornado.web.Application(template_loader=Jinja2Loader(),
    handlers=[
        (r"/", homePage),
        (r"/ff/user/create", createUser),
        (r"/ff/user/update", updateUser),
        (r"/ff/user/get", getUser),
        (r"/ff/flag/create", createFlag),
        # (r"/ff/flag/update", updateFlag),
        (r"/ff/flag/updsta", updateFsta),
        (r"/ff/flag/get", getFlag),
        (r"/ff/flag/groupget", groupgetFlag),
        (r"/ff/pos/get", getPos),
        (r"/ff/type/get", getType),
        (r"/ff/friend/get", getFriend),
        (r"/ff/group/create", createGroup)
    ])

def main():
    app =startApp()
    app.listen(address='0.0.0.0',port=8213)
    tornado.ioloop.IOLoop.current().start()

if __name__ =="__main__":
    main()