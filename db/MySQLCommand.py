import pymysql
import datetime
class MySQLCommand(object):
    #类的初始化
    def __init__(self):
        # 打开数据库连接
        # self.mysql_host = '192.168.77.39'
        # self.mysql_db = 'ai_data_platform'
        # self.mysql_user = 'root'
        # self.mysql_password = 'kingnet@test123Z$456'
        # self.mysql_port = 3306
        # self.table = 'ai_news'
        self.mysql_host = '192.168.77.37'
        self.mysql_db = 'shitu'
        self.mysql_user = 'root'
        self.mysql_password = '123456'
        self.mysql_port = 3306
        self.table = 'ai_news'

    #链接数据库
    def connectionMysql(self):
        try:
            self.conn = pymysql.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, password=self.mysql_password,
                                 db=self.mysql_db, charset='utf8')
            self.cursor = self.conn.cursor()# 使用 cursor() 方法创建一个游标对象 cursor
        except:
            print("connection mysql error")

    #建表
    def createTable(self):
        # 使用 execute() 方法执行 SQL,如果表存在则删除
        self.cursor.execute("drop table if exists ai_news")
        # 使用预处理语句创建表
        sql = """create table ai_news (
                 id int(30) primary key not null AUTO_INCREMENT ,
                 content_title varchar (100),
                 content_author varchar (100),
                 content_link varchar (100),
                 content_details blob, 
                 insert_time DATE)  """
        self.cursor.execute(sql)
        print("\n creat table successd ! \n")


    #插入数据
    def insertData(self,my_dict):

        # 注意，这里查询的sql语句url=' %s '中%s的前后要有空格
        # sqlExit = "SELECT content_link FROM ai_news  WHERE content_link = ' %s '" % (my_dict['content_link'])
        # res = self.cursor.execute(sqlExit)
        # if res:  # res为查询到的数据条数如果大于0就代表数据已经存在
        #     print("数据已存在", res)
        #     return 0
        # 数据不存在才执行下面的插入操作
        try:
            sql = 'INSERT INTO ai_news(id,content_title,content_author,content_link,content_details,insert_time,image_link,image_path,zan_num,read_num) values ("%s","%s","%s","%s","%s","%s","%s","%s","%d","%d")'%(0,my_dict['content_title'],my_dict['content_author'],my_dict['content_link'],self.conn.escape(my_dict['content_details']),my_dict['insert_time'],my_dict['image_link'],"",0,0)
            # print(sql)
            try:
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("插入成功", insert_id)
                    return insert_id
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "key 'PRIMARY'" in e.args[1]:
                    print(dt+"  数据已存在，未插入数据")
                else:
                    print(dt+" 插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(dt+" 数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
    #修改数据
    def updateData(self,id,path):
        # 数据不存在才执行下面的插入操作
        try:
            sql = '''
                update ai_news set image_path ='%s' where id = '%s'
                '''% (path, id)
            try:
                result = self.cursor.execute(sql)
                self.conn.commit()
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(dt+" 插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(dt+" 数据库错误，原因%d: %s" % (e.args[0], e.args[1]))
    def closeMysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例

