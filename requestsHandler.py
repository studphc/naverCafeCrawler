__author__ = 'Lynn'
__email__ = 'lynnn.hong@gmail.com'
__date__ = '4/6/2016'

import requests
import time
from datetime import datetime
import socket
from bs4 import BeautifulSoup


class Req():
    # represent http requests

    def __init__(self, nd, logger):
        self.logger = logger
        self.nd = nd

    def access_page(self, url, maxIter, isSoup=True):
        t = 10.0
        n = 0
        while True:
            n += 1
            if n == maxIter:
                return (10, "Page is not available(manually stop)")
            try:
                res = self.nd._s.get(url, timeout=t).text
                if "<title>400 Bad Request</title>" in res:
                    self.logger.warning("400 Bad request error.... sleep 10 minutes..." + str(datetime.now()))
                    self.logger.warning(url)
                    time.sleep(600) #sleep 10 minutes
                    n = 0
                else:
                    break
            except requests.exceptions.Timeout:
                self.logger.warning("\nTimeout error with url: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.ConnectionError:
                self.logger.warning("\nMax retrieve error with url: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.TooManyRedirects:
                self.logger.warning("\nToo many redirect error with url: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.HTTPError:
                self.logger.warning("\nHttp error with url: %s." % url)
                self.logger.info("Sleep 5 seconds and retry")
                time.sleep(5)
            except requests.exceptions.RequestException:
                self.logger.warning("\nAmbiguous exception with url: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.LocationParseError as e:
                self.logger.critical(e)
                return (10, "Page is not available(manually stop)")
            except socket.timeout:
                self.logger.warning("\nSocket Timeout error with url: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except ConnectionResetError:
                self.logger.warning("\nConnection reset by peer: %s." % url)
                self.logger.info("Sleep 20 seconds and retry")
                time.sleep(20)
        if isSoup is True:
            return (1, BeautifulSoup(res, "lxml"))
        else:
            return (1, res)     # post comments
