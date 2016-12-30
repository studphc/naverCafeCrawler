__author__ = 'Lynn'
__email__ = 'lynnn.hong@gmail.com'
__date__ = '5/31/2016'

from datetime import datetime, timedelta
import time
import os
import logging
import logging.handlers


class CafeCrawler():
    # represent NAVER CAFE crawler

    def __init__(self):
        pass

    def setCnf(self, cnfFile):
        self.cnfDict = dict()
        self.dbCnfDict = dict()
        self.logger = logging.getLogger('mylogger')     # set logger
        self.read_conf(cnfFile)
        self.connect_db("./cnf/database.cnf", "./cnf/naver_cafe_schema.sql")

    def read_conf(self, confFile):
        with open(confFile, "r") as f:
            for line in f.readlines():
                if line.strip().strip("\n") != "" and line.startswith("#") is False:
                    elem = line.strip().strip("\n").split("=", 1)
                    if elem[0] in ['query', 'boardURL']:
                        self.cnfDict[elem[0]] = elem[1].strip("\"").split(";")
                    elif elem[0] in ['log_file']:
                        self.cnfDict[elem[0]] = elem[1].strip("\"")
                    elif elem[0] in ['multi_board']:
                        self.cnfDict[elem[0]] = eval(elem[1])
                    elif elem[0] in ['log_level']:
                        self.cnfDict[elem[0]] = elem[1].upper()
                    else:
                        self.cnfDict[elem[0]] = elem[1]
        self.cnfDict['retry'] = int(self.cnfDict['retry'])
        if "end_date" not in self.cnfDict.keys():
            self.cnfDict['end_date'] = str(datetime.now().date())
        if "min_update_date" not in self.cnfDict.keys():
            self.cnfDict['min_update_date'] = None
        else:
            self.cnfDict['min_update_date'] = datetime.now()-timedelta(days=int(self.cnfDict['min_update_date']))
        os.environ['TZ'] = self.cnfDict['timeZone']
        time.tzset()
        # logger setting
        if not os.path.exists('./log/'):
            os.makedirs('./log/')
        fileMaxByte = 1024 * 1024 * 100  # 100MB
        time_format = "%y-%m-%d_%H-%M-%S"
        formatted_now = datetime.now().strftime(time_format)
        filename_split = self.cnfDict['log_file'].rsplit(".", 1)
        file_path = './log/%s_%s.%s' % (filename_split[0], formatted_now, filename_split[1])
        fileHandler = logging.handlers.RotatingFileHandler(file_path, maxBytes=fileMaxByte, backupCount=10)
        formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        streamHandler = logging.StreamHandler()
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        #self.logger.addHandler(streamHandler)      # turn off stream logger
        self.logger.setLevel(eval("logging.%s" % self.cnfDict['log_level']))
        self.logger.info("Finish setting logging level as %s..." % self.cnfDict['log_level'])
        self.logger.info("Finish reading configuration file...")

    def connect_db(self, dbConfFile, dbSchemaFile):
        from naverCafeCrawler.mysqlConnector import Mysql
        with open(dbConfFile, "r") as f:
            for line in f.readlines():
                if line.strip().strip("\n") != "" and line.startswith("#") is False:
                    elem = line.strip().strip("\n").split("=", 1)
                    self.dbCnfDict[elem[0]] = elem[1]
        self.dbCnfDict['project'] = self.cnfDict['project']
        self.mysql = Mysql(self.logger)
        self.mysql.connect_db(self.dbCnfDict, dbSchemaFile)
        self.logger.info("Finish connecting to database...")

    def start_work(self):
        if 'min_article_id' not in self.cnfDict.keys():
            self.mysql.get_max_inserted_id()
            i = self.mysql.cur.fetchone()[0]
            if i is None:
                self.cnfDict['min_article_id'] = 0
            else:
                self.cnfDict['min_article_id'] = i

        from naverCafeCrawler.naverCafe import NaverCafe
        c = NaverCafe(self.cnfDict, self.mysql, self.logger)
        if 'query' in self.cnfDict.keys():
            for query in self.cnfDict['query']:
                self.logger.warning("\nStart searching naver cafe with query '(%s)'..." % query)
                #####################c.search_cafe(query)
                self.logger.warning("\nFinish with query '(%s)'...\n=============================\n" % query)
        else:
            self.logger.warning("\nThere's no query term. Start trying collect all bulletin board...")
            if 'boardURL' not in self.cnfDict.keys():
                self.logger.critical("There must be 'boardURL' information in the main.cnf file. Stop processing...")
            else:
                self.logger.warning("Start searching....")
                c.search_board()
                self.logger.warning("\nFinish on board...\n=============================\n")
