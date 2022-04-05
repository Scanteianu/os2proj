######harness
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys

import json
import os
import time
import io
import random
import requests

def listGen(size):
    listA=[]
    for i in range(size):
   		listA.append(random.random())
    return listA
def invokeTestFunction(inputObj):
    auth=('redacted','redacted')
    url='https://us-south.functions.cloud.ibm.com/api/v1/namespaces/<redacted>/actions/largeMem?blocking=true'
    start=time.time()
    resp = requests.post(auth=auth,url=url, json=inputObj)
    end=time.time()
    fnOut=resp.json()['response']['result']
    #print(fnOut)
    return {"calledFunctionOutput":fnOut,"start":start,"end":end,"elapsed":(end-start)}
def performTest():
    csv="matrix size,elapsed time harness, elapsed time function, start harness, start function, end harness, end function\n"
    for size in range(10000,100000,10000):
        for i in range(5):
            inputObj={"listA": listGen(size)}
            retObj=invokeTestFunction(inputObj)
            csv+="{},{},{},{},{},{},{}\n".format(size,retObj['elapsed'],retObj['calledFunctionOutput']['elapsed'],retObj['start'],retObj['calledFunctionOutput']['start'],retObj['end'],retObj['calledFunctionOutput']['end'])
    return {"timing":csv}

def main(dict):
    return performTest()
#####child
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import time
def main(dict):
    start=time.time()
    listA=dict['listA']
    fOut=len(listA)
    end=time.time()
    elapsed=end-start
    return {"start":start,"end":end,"result":fOut,"elapsed":elapsed}
