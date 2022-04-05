#########caller lambda###################
#curl -X POST -H "Content-Type: application/json" https://redacted.cloudfunctions.net/largeNetworkTest  -o resp.json
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
    start=time.time()
    resp = requests.post(url='https://redacted.cloudfunctions.net/largeNetwork', json=inputObj)
    end=time.time()
    fnOut=resp.json()
    return {"calledFunctionOutput":fnOut,"start":start,"end":end,"elapsed":(end-start)}
def performTest():
    csv="matrix size,elapsed time harness, elapsed time function, start harness, start function, end harness, end function\n"
    for size in range(10000,100000,10000):
        for i in range(5):
            inputObj={"listA": listGen(size)}
            retObj=invokeTestFunction(inputObj)
            csv+="{},{},{},{},{},{},{}\n".format(size,retObj['elapsed'],retObj['calledFunctionOutput']['elapsed'],retObj['start'],retObj['calledFunctionOutput']['start'],retObj['end'],retObj['calledFunctionOutput']['end'])
    return {"timing":csv}
def hello_world(request):
    retVal=performTest()
    return json.dumps(retVal)
###################child lambda#######################

import json
import time
import random


def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    start=time.time()
    request_json = request.get_json()
    start=time.time()
    listA=request_json['listA']
    fOut=len(listA)
    end=time.time()
    elapsed=end-start
    out={"start":start,"end":end,"result":fOut,"elapsed":elapsed}
    return json.dumps(out)
