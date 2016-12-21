__author__ = 'Lynn'
__email__ = 'lynnn.hong@gmail.com'
__date__ = '4/6/2016'

import requests
import time
from datetime import datetime
import logging
import socket
from bs4 import BeautifulSoup


class Req():
    # represent http requests

    def __init__(self, nd):
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
                    logging.warning("400 Bad request error.... sleep 10 minutes..." + str(datetime.now()))
                    logging.warning(url)
                    time.sleep(600) #sleep 10 minutes
                    n = 0
                else:
                    break
            except requests.exceptions.Timeout:
                logging.warning("\nTimeout error with url: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.ConnectionError:
                logging.warning("\nMax retrieve error with url: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.TooManyRedirects:
                logging.warning("\nToo many redirect error with url: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.HTTPError:
                logging.warning("\nHttp error with url: %s." % url)
                logging.info("Sleep 5 seconds and retry")
                time.sleep(5)
            except requests.exceptions.RequestException:
                logging.warning("\nAmbiguous exception with url: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except requests.exceptions.LocationParseError as e:
                logging.critical(e)
                return (10, "Page is not available(manually stop)")
            except socket.timeout:
                logging.warning("\nSocket Timeout error with url: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
            except ConnectionResetError:
                logging.warning("\nConnection reset by peer: %s." % url)
                logging.info("Sleep 20 seconds and retry")
                time.sleep(20)
        if isSoup is True:
            return (1, BeautifulSoup(res, "lxml"))
        else:
            return (1, res)     # post comments
