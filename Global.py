# -*- coding: utf-8 -*-
import math
import os
from urllib import urlencode

import demjson
import datetime
import string
import random
import sys
import PIL.Image
import pdfkit
import time
import calendar

import requests
from PIL import Image
from pytesseract import pytesseract

from pyPdf import PdfFileWriter, PdfFileReader
import smtplib
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE, formatdate
import re
import subprocess
from phpserialize import serialize, unserialize
import csv
import base64
import pytz

import json
import urllib2
from sendgrid.helpers.mail import *
from sendgrid import *
from subprocess import Popen, PIPE

# logfilename = "_batchno_log.txt"
# ErrorFilename = "_batchono_error.txt"
# foldername date wise folder = "year_month_date" - "2016_09_20"
# foldername if it stores label or bulklabel or any pdf or csv file = "_batchono"
# label name = "batchno.pdf" or "suborderid.pdf" or "ordrerid.pdf" - whatever is applicable


class Helper(object):

    # Specify sendgrid api user.
    Sendgrid_api_user = ""
    Sendgrid_api_key = ""

    @staticmethod
    def GenerateRandomString(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def JsonEncode(dataDictionary):
        return demjson.encode(dataDictionary, encoding="utf8")

    @staticmethod
    def JsonDecode(jsonString):
        return demjson.decode(jsonString, encoding="utf8")

    @staticmethod
    def GetCurrentDateTimeAsIso():
        now = datetime.datetime.now()
        return now.isoformat()

    @staticmethod
    def CheckOrCreateDirectory(path):
        if not os.path.exists(path):
            os.makedirs(path, 0775)

    @staticmethod
    def GetCurrentDateTime(format = "%Y-%m-%d %H:%M:%S"):
        # This will return the datetime in given format
        return str(datetime.datetime.today().strftime(format))

    @staticmethod
    def GetCurrentDateTimeAsDateTime():
        return datetime.datetime.now()

    @staticmethod
    def GetDateOfToday(format = "%Y-%m-%d"):
        return str(datetime.datetime.today().strftime(format))

    @staticmethod
    def ConvertDateTimeToFormat(dateTime, format):
        # dateTime must be type of DateTime
        return str(dateTime.strftime(format))

    @staticmethod
    def GetDateTimeTimestamp(dateTime):
        # dateTime must be type of DateTime
        return int(dateTime.strftime("%s"))

    @staticmethod
    def ConvertTimeStampToDatetime(timestamp):
        # timestamp must be int or string
        return datetime.datetime.fromtimestamp(int(str(timestamp)))

    @staticmethod
    def ConvertStringToDateTime(str, format = "%Y-%m-%d %H-%M-%S"):
        # format, used in the given string and returns standard formatted datetime
        return datetime.datetime.strptime(str, format)

    @staticmethod
    def GetCeil(number):
        return math.ceil(number)

    @staticmethod
    def GenerateRandomNumber(start, stop):
        if(start < stop):
            return random.randrange(start, stop)
        else:
            return None

    @staticmethod
    def RemoveFile(filePath):
        if(Helper.IsFileExist(filePath)):
            os.remove(filePath)


    @staticmethod
    def ImageToPdf(sourcePath, destinationPath, clientId, affiliateId, requesFor):
        # sourcePath and destinationPath contains filename.
        try:
            im = PIL.Image.open(sourcePath)
            im.save(destinationPath, "PDF", quality=100)
        except Exception, e:
            line = format(sys.exc_info()[-1].tb_lineno)
            print str(e)

    @staticmethod
    def HtmlToPdf(url, destinationPath, clientId, affiliateId, requesFor):
        # sourcePath and destinationPath contains filename.
        try:
            pdfkit.from_url(url, destinationPath)
        except Exception, e:
            line = format(sys.exc_info()[-1].tb_lineno)
            print str(e)

    @staticmethod
    def HtmlToPdfFromfile(filePath, destinationPath, clientId, affiliateId, requesFor):
        # filePath and destinationPath contains filename.
        try:
            pdfkit.from_file(filePath, destinationPath)
        except Exception, e:
            line = format(sys.exc_info()[-1].tb_lineno)
            print str(e)

    @staticmethod
    def IsFileExist(fileNameWithPath):
        if(os.path.isfile(fileNameWithPath)):
            return True
        else:
            return False

    @staticmethod
    def GetTextFromImage(pathToImage):
        # This will get text from simple images only
        text = (pytesseract.image_to_string(Image.open(pathToImage)))
        if(text != None):
            text = text.strip()
        return text

    @staticmethod
    def RandomSleep(start = 900, stop = 1500, devider = 1000.0):
        # 900 to 1500 - start and stop
        sleepVal = float(random.randrange(start, stop) / devider)
        time.sleep(sleepVal)

    @staticmethod
    def GetBaseName(filepath):
        # this will give file name of full path
        return os.path.basename(filepath)

    @staticmethod
    def GetBasePath(filepath):
        # This will give directory info.
        return os.path.dirname(filepath)

    @staticmethod
    def GetFileInfo(filepath):
        return os.stat(filepath)

    @staticmethod
    def GetFileSize(filepath):
        filesize = 0
        if(Helper.IsFileExist(filepath)):
            fileInfo = Helper.GetFileInfo(filepath)
            filesize = fileInfo.st_size

        return filesize

    @staticmethod
    def RenameFileOrDir(sourcePath, destinationPath):
        # for the file, include filename in source and destination
        os.rename(sourcePath, destinationPath)
        return Helper.IsFileExist(destinationPath)

    @staticmethod
    def GetExtentionFromFile(filename):
        return (os.path.splitext(filename)[1])

    @staticmethod
    def GetFilename(filename):
        return (os.path.splitext(filename)[0])

    @staticmethod
    def GetDaysOfMonth(year, month):
        obj = calendar.monthrange(year, month)
        # obj[0] gives weekday of first day of the month
        # obj[1] gives no of days of the month
        return obj[1]

    @staticmethod
    def RegexToReplace(text, expression = r'[^a-zA-Z0-9 ]', replaceWith = r''):
        try:
            return re.sub(expression, replaceWith, text)
        except Exception, e:
            print str(e)

    @staticmethod
    def ReadFile(filePath, functionName, clientId, affiliateId, RequestFor):
        # filePath must be a fullpath with name
        content = None
        try:
            if(Helper.IsFileExist(filePath)):
                fileObj = open(filePath, 'r')
                content = fileObj.read()
                fileObj.close()
        except Exception, e:
            print str(e)
        return content

    @staticmethod
    def WriteInFile(filePath, content, writeMode, functionName, clientId, affiliateId, RequestFor):
        # filePath must be a fullpath with name
        # WriteMode is 'w' or 'a'
        isSuccessful = False
        try:
            fileObj = open(filePath, writeMode)
            fileObj.write(content)
            fileObj.close()
            isSuccessful = True
        except Exception, e:
            print str(e)
        return isSuccessful

    @staticmethod
    def EncodeCharsetString(stra, charsettype = 'utf8'):
        result = stra
        if(stra != None):
            try:
                # strip - removes whitespace
                result = str(stra.encode('ascii', 'ignore').encode(charsettype)).strip()
            except Exception, e:
                print str(e)
                result = Helper.ReplaceSpecialChars(stra)
        return result

    @staticmethod
    def EncodeToUtf8(text, charsettype='utf8',convertcount=0):
        try:
            if(type(text) is str):
                text = text.encode(charsettype, 'ignore')
            elif(type(text) is unicode):
                text=unicode(text).encode(charsettype, 'ignore')
            elif (type(text) is float):
                # print text
                # print float(text)
                text = "%.2f" % (text)
        except Exception, e:
            if convertcount == 0:
                text=Helper.EncodeCharsetString(text)
                text=Helper.EncodeToUtf8(text,'utf8',1)

        return text

    @staticmethod
    def ReplaceSpecialChars(str):
        return re.sub(r'[^a-zA-Z0-9-_. ]', r'_', str)

    @staticmethod
    def ReplaceChar(str, charToReplace, charWithReplace):
        result = None
        if(str != None):
            result = str.replace(charToReplace, charWithReplace)
        return result

    @staticmethod
    def ReplaceCharInFile(filepath, charToReplace, charWithReplace):

        f1 = open(filepath, 'r')
        dirpath = Helper.GetBasePath(filepath)
        filename = Helper.GetBaseName(filepath)
        filepathTemp = dirpath + "/tmp_" + filename

        f2 = open(filepathTemp, 'w')
        for line in f1:
             f2.write(line.replace(charToReplace, charWithReplace))
        f1.close()
        f2.close()

        Helper.RemoveFile(filepath)
        Helper.RenameFileOrDir(filepathTemp, filepath)

    @staticmethod
    def DevideArray(array, n):
        division = len(array) / float(n)
        return [array[int(round(division * i)): int(round(division * (i + 1)))] for i in xrange(n)]

    @staticmethod
    def RunBackGroundProcess(args):
        # args must be a list. And it must be in the defined sequence.
        # index 0 - command - php/python or anyother
        # index 1 - filename - that you want to run. Specify fullpath if required
        # index 2 - param_1
        # index 3 - param_2
        # index N - param_N

        if(len(args) >= 2):
            subprocess.Popen(args)

    @staticmethod
    def RunProcessAndWait(args):
        # args must be a list. And it must be in the defined sequence.
        # index 0 - command - php/python or anyother
        # index 1 - filename - that you want to run. Specify fullpath if required
        # index 2 - param_1
        # index 3 - param_2
        # index N - param_N

        if (len(args) >= 2):
            subprocess.call(args)

    @staticmethod
    def GetSerializedData(dictionary):
        return serialize(dictionary)

    @staticmethod
    def GetUnserializedData(serializeData):
        return unserialize(serializeData)

    @staticmethod
    def MakeCSVFile(dataToWrite, fileNameWithPath, headersAsArray, accessMode='w', fileDelimiter=',',quotestring=True):
        # Right now we are making csv file from dictionary only

        # fileNameWithPath, file in which you want to write csv data
        # accessMode, write or append

        #headersAsArray = ['a', 'x']

        if quotestring == True:

            with open(fileNameWithPath, accessMode) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headersAsArray, delimiter=fileDelimiter,quoting=csv.QUOTE_NONNUMERIC, quotechar='`')

                writer.writeheader()

                for eachDict in dataToWrite:
                    for key in eachDict.keys():
                        if (type(eachDict[key]) is str):
                            finalString = eachDict[key].replace('\\n', '<br>').replace('\\t', '|').replace('\n','<br>').replace('\t', '|')
                            eachDict.update({key: finalString})
                    writer.writerow(eachDict)

        elif quotestring == False:

            with open(fileNameWithPath, accessMode) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headersAsArray, delimiter=fileDelimiter)

                writer.writeheader()

                for eachDict in dataToWrite:
                    for key in eachDict.keys():
                        if (type(eachDict[key]) is str):
                            finalString = eachDict[key].replace('\\n', '<br>').replace('\\t', '|').replace('\n','<br>').replace(fileDelimiter, '|')
                            eachDict.update({key: finalString})
                    writer.writerow(eachDict)

    @staticmethod
    def sendMailGrid(subject,Message,Tolist=None, isHtml = False):
        apiuser = Helper.Sendgrid_api_user
        apikey = Helper.Sendgrid_api_key
        params = "api_user=" + apiuser + "&api_key=" + apikey
        if Tolist is not None:
            for i, toemail in enumerate(Tolist):
                print i, toemail
                params += "&to="+toemail
        else:
            params += "&to=mail1@mail.com&to=mail2@mail.com"

        if(isHtml):
            params += "&html=" + str(Message)
        else:
            params += "&html='" + str(Message) + "'"

        params += "&subject=" + subject + "&from=mail1@mail.com&fromname=From Name&bcc[]=bccmail@mail.com"
        response = requests.get("https://api.sendgrid.com/api/mail.send.json?" + params)
        print params
        print response.content

    @staticmethod
    def SendGridUsingLib(subject,Message,Tolist=[], bccMail=[], isHtml = False, attachments = {}, fileExtension = ''):
        # Ex. FileExtension = ".txt" or ".xlsx" or ".csv"
        # attachments = {"attachmentName":"filename"} # attachmentName is name from which attachment will be displayed to user.
        # filename is the file which you want to send.

        try:
            # sg = SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            sg = SendGridAPIClient(apikey=Helper.Sendgrid_api_key)
            mail = Mail()
            mail.from_email = Email("mail@mail.com", "From Name")
            mail.subject = subject

            personalization = Personalization()

            for eachMail in Tolist:
                personalization.add_to(Email(eachMail, "User"))

            for eachMail in bccMail:
                personalization.add_bcc(Email(eachMail, "User"))

            mail.add_personalization(personalization)

            if(isHtml):
                mail.add_content(Content("text/html", Message))
            else:
                mail.add_content(Content("text/plain", Message))

            if(len(attachments) > 0):

                for attachmentName, filename in attachments.items():

                    attachment = Attachment()

                    fileObj = open(filename, 'rb')  # open binary file in read mode
                    content = fileObj.read()
                    fileObj.close()
                    encode = Helper.Base64Encode(content)

                    attachment.content = encode

		    # Static defined, you can change as per your need.
                    attachment.type = "application/xlsx"
                    attachment.filename = str(attachmentName) + fileExtension
                    attachment.disposition = "attachment"
                    attachment.content_id = "Summary Data"
                    mail.add_attachment(attachment)

            response = sg.client.mail.send.post(request_body=mail.get())

        except Exception,e:
            line = format(sys.exc_info()[-1].tb_lineno)
            print "Error at line - " + str(line)
            print "error - " + str(e)

    @staticmethod
    def Base64Encode(text):
        encoded = base64.b64encode(text)
        return encoded

    @staticmethod
    def Base64Decode(text):
        decoded = base64.b64decode(text)
        return decoded

    @staticmethod
    def GetUtcOffset(timezone = 'Asia/Kolkata'):

        offset = datetime.datetime.now(pytz.timezone(timezone)).strftime('%z')
        offset = datetime.datetime.strptime(offset, "+%H%M").time().strftime("+%H:%M")

        return str(offset)

    @staticmethod
    def CompareHeaders(requiredHeaders, heads_to_compare):
        # requiredHeaders and heads_to_compare, both must be array.
        # requiredHeaders are the headers which we are getting currently.

        isHeadersCorrect = True
        if(len(requiredHeaders) == len(heads_to_compare)):

            for eachHeader in heads_to_compare:

                if(requiredHeaders.__contains__(eachHeader) == False):
                    isHeadersCorrect = False
                    break
        else:
            isHeadersCorrect = False

        return isHeadersCorrect

    @staticmethod
    def GetCountOfRunningProcess(checkString):
        processes = Popen(['ps', '-ef'], stdout=PIPE, stderr=PIPE)
        stdout, notused = processes.communicate()

        count = 0

        for line in stdout.splitlines():
            if (line.__contains__(checkString)):
                count = count + 1

        return count

