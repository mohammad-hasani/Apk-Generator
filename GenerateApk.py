from Database import Database
import sys
from shutil import copyfile
import shutil, errno
import subprocess
import os
import time

PATH_APP = 'C:/cmd/AndroidStudioProjects/QRCodeAndroid'
PATH_STRING = r'\app\src\main\res\values\strings.xml'
PATH_APPLICATION_NAME_1 = r'\app\build.gradle'
PATH_APPLICATION_NAME_2 = r'\app\src\main\AndroidManifest.xml'
PATH_ICON = '/app/src/main/res/drawable/'
PATH_RELEASE = r'C:\sina\outputs\apk\app-release.apk'
PATH_FINAL = 'C:/inetpub/wwwroot/UserData/%s/%s/%s.apk'

APP_NAME = r'%app_name%'
APP_ADDRESS = r'%app_address%'
APP_TELL = r'%app_tel%'
APP_ABOUT = r'%app_about%'

APPLICATION_NAME = '%application_id%'

COMMAND = 'C:\cmd\AndroidStudioProjects\QRCodeAndroid\gradlew aR'


class RunGenerateAPK(object):
    def __init__(self):
        pass

    def run(self):
        GenerateApk().start()

class GenerateApk(object):
    def __init__(self):
        pass

    def start(self):
        name, address, about, tell, icon, app_id, project_id = self.fetchdata()
        app_id2 = app_id
        #while 1:
        dst1 = 'C:\\cmd\\AndroidStudioProjects\\QRCodeAndroid\\app\\'
        dst2 = 'C:\\inetpub\\wwwroot\\cgi-bin\\app\\'
        self.replace_in_files()
        #if os.path.isdir(dst1) and os.path.isdir(dst2):
        #    sys.exit(0)
            #break

        #### 1
        result = self.replace_string_data(name, address, about, tell, PATH_APP)
        app_id = 'aras' + str(app_id) 
        result = self.replace_application_id_data(app_id, PATH_APP)
        
        self.search_in_files(app_id, PATH_APP)

        src = 'C:/inetpub/wwwroot/images/App_Icons/%s.png' % icon
        dst = PATH_APP + PATH_ICON + 'icon.png'
        result = self.replace_icon(src, dst)

        #### 2

        PATH_APP2 = 'C:/inetpub/wwwroot/cgi-bin'

        result = self.replace_string_data(name, address, about, tell, PATH_APP2)
        result = self.replace_application_id_data(app_id, PATH_APP2)
        
        self.search_in_files(app_id, PATH_APP2)

        src = 'C:/inetpub/wwwroot/images/App_Icons/%s.png' % icon
        dst = PATH_APP2 + PATH_ICON + 'icon.png'
        result = self.replace_icon(src, dst)

        #### release

        result = self.final_release(project_id, name)
        print(3)

        #if result == True:
        #    self.update_is_generate(app_id2, '1')
        #    print('[+] Apk created : %s' % name)
        #else:
        #    self.update_is_generate(app_id2, '-1')
        #    print('[-] Error in creating apk : %s' % name)
        #self.replace_in_files()

        #RunGenerateAPK().run()
        
        
    def fetchdata(self):
        while 1:
            database = Database()
            database.connect()
            query = r'select top 1 app_id from queue where is_generate=0'
            cursor = database.select(query)
            try:
                app_id = cursor[0][0]
            except:
                #database.close()
                #time.sleep(60)
                #print('[*] Checking ...')
                #continue
                sys.exit(0)
            query = r'select name, address, about, tell, icon, project_id from tbl_app where id=%s' % app_id
            data = database.select(query)

            name = data[0][0]
            address = data[0][1]
            about = data[0][2]
            tell = data[0][3]
            icon = data[0][4]
            project_id = data[0][5]
            database.close()

            return name, address, about, tell, icon, app_id, project_id

    def replace_string_data(self, name, address, about, tell, path):
        with open(path + PATH_STRING, 'r') as f:
            txt = f.read()
        txt = txt.decode('utf-8')
        txt = txt.replace(APP_NAME, name)
        txt = txt.replace(APP_ADDRESS, address)
        txt = txt.replace(APP_ABOUT, about)
        txt = txt.replace(APP_TELL, tell)
        txt = txt.encode('utf-8')
        with open(path + PATH_STRING, 'w') as f:
            f.write(txt)
        return True

    def replace_application_id_data(self, app_id, path):
        with open(path + PATH_APPLICATION_NAME_1, 'r') as f:
            txt = f.read()
        txt = txt.decode('utf-8')
        txt = txt.replace(APPLICATION_NAME, str(app_id))
        txt = txt.encode('utf-8')
        with open(path + PATH_APPLICATION_NAME_1, 'w') as f:
            f.write(txt)

        with open(path + PATH_APPLICATION_NAME_2, 'r') as f:
            txt = f.read()
        txt = txt.decode('utf-8')
        txt = txt.replace(APPLICATION_NAME, str(app_id))
        txt = txt.encode('utf-8')
        with open(path + PATH_APPLICATION_NAME_2, 'w') as f:
            f.write(txt)
        return True

    def replace_icon(self, src, dst):
        with open(src, 'rb') as f:
            png = f.read()
        with open(dst, 'wb') as f:
            f.write(png)
        return True

    def final_release(self, app_id, name):
        result = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        result = result.stdout.read()
        print(result)
        if len(result) > 100:
            if 'BUILD SUCCESSFUL' in result[len(result) - 100:]:
                database = Database()
                database.connect()
                query = r'select user_id from tbl_project where id=%s' % app_id
                data = database.select(query)
                user_id = data[0][0]
                project_id = app_id
                app_name = name
                final = PATH_FINAL % (user_id, project_id, app_name)
                path_of_final = final[0: -(len(app_name) + 4)]
                if not os.path.exists(path_of_final):
                    os.makedirs(path_of_final)
                
                copyfile(PATH_RELEASE, final)
                return True
            else:
                return False
        else:
            return False

    def update_is_generate(self, app_id, flag):
        database = Database()
        database.connect()
        query = r'update queue set is_generate=%s where app_id=%s' % (flag, app_id)
        result = database.update_or_insert(query)
        return result

    def search_in_files(self, app_id, apppath):
        path = apppath + '\\app\\'

        for dirname, dirnames, filenames in os.walk(path):
                        
            for subdirname in dirnames:
                if subdirname == APPLICATION_NAME:
                    pre_name = os.path.join(dirname, subdirname)
                    new_name = os.path.join(dirname, str(app_id))
                    os.rename(pre_name, new_name)


        for dirname, dirnames, filenames in os.walk(path):

            for filename in filenames:
                if filename.endswith('.java') or filename.endswith('.xml'):
                    tmpfile = os.path.join(dirname, filename)
                    with open(tmpfile, 'r') as f:
                        txt = f.read()
                    txt = txt.replace(APPLICATION_NAME, str(app_id))
                    with open(tmpfile, 'w') as f:
                        f.write(txt)

    def replace_in_files(self):
        dst1 = 'C:\\cmd\\AndroidStudioProjects\\QRCodeAndroid\\app\\'
        dst2 = 'C:\\inetpub\\wwwroot\\cgi-bin\\app\\'
        src = 'C:\\cmd\\AndroidStudioProjects\\QRExample\\app\\'

        try:
            shutil.rmtree(dst1)
        except:
            pass
        try:
            shutil.rmtree(dst2)
        except:
            pass

        try:
            shutil.copytree(src, dst1)
        except:
            pass
        try:
            shutil.copytree(src, dst2)
        except:
            pass
#GenerateApk().replace_in_files()


