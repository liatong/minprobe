# import init_import
from common.checkscript import checkScipt
import logging,time

log = logging.getLogger(__name__)

def getDBInfo(host,port,user,passwd,dblist):
    print host,port,user,passwd,dblist
    data={}
    data['server']={}
    try:
        import psycopg2
    except:
        log.error("can import psycopg2")
    try:
        conn = psycopg2.connect(database=dblist[0], user=user, password=passwd, host=host)
        getServerConnect="select count(*) from pg_stat_activity;"
        list = ('name','connect','inserted','updated','deleted','blks_read','blks_hit')
        getDB = "select datname,numbackends,tup_inserted,tup_updated,tup_deleted,blks_read,blks_hit from pg_stat_database where datname='%s'"
        getDBSize = "select pg_database_size('%s')"
        #get server info 
        cur = conn.cursor()
        cur.execute(getServerConnect);
        data['server']['connect']= int(cur.fetchone()[0])
    
        #get db info
        for db in dblist:
            cur.execute(getDB %db)
            resulet = cur.fetchone()
            if resulet is not None:
                data[db]=dict(zip(list,resulet))
                cur.execute(getDBSize %db)
                size = cur.fetchone()
                data[db]['size']=size[0]
        #print data
    except:
        log.error("Can't connect to host:%s db:%s" %(host,dblist[0]))
    
    return data
    
class Postgresql(checkScipt):

    def collector(self):
        dblist=map(lambda x:x['DB'],self.config['instance'])     
        host=self.config['comman']['HOST']
        port=self.config['comman']['PORT']
        user=self.config['comman']['USER']
        passwd=self.config['comman']['PASSWD']
        data = getDBInfo(host,port,user,passwd,dblist)
        for items in data['server']:
            self.add_guage('postgresql.server.'+items,int(data['server'][items]))
            
        for db in self.config['instance']:
            if data.has_key(db['DB']):
                for items in db['items']:
                    if data[db['DB']].has_key(items):
                        self.add_guage('postgresql.'+db['DB']+'.'+items,data[db['DB']][items])
                        
# if __name__ == "__main__":
    # from common.utils.config import init_logging
    # init_logging()
    # import init_import
    # ps = Postgresql()
    # ps.debug()
    # print ps.getdataForm()
    