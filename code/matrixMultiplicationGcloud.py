#########caller lambda###################
#curl -X POST -H "Content-Type: application/json"https://redacted.cloudfunctions.net/matrixMultiplicationHarness -o resp.json
import json
import os
import time
import io
import random
import requests

def matrixGen(size):
    matrixA=[]
    for i in range(size):
    	listA=[]
    	for j in range(size):
    		listA.append(random.random())
    	matrixA.append(listA)
    return matrixA
def invokeTestFunction(inputObj):
    start=time.time()
    resp = requests.post(url='https://redacted.cloudfunctions.net/matrixMultiplication', json=inputObj)
    end=time.time()
    fnOut=resp.json()
    return {"calledFunctionOutput":fnOut,"start":start,"end":end,"elapsed":(end-start)}
def performTest():
    csv="matrix size,elapsed time harness, elapsed time function, start harness, start function, end harness, end function\n"
    for size in [5,10, 20,50,60,70,80,90,100]:
        for i in range(3):
            inputObj={"matrixA": matrixGen(size),"matrixB": matrixGen(size)}
            retObj=invokeTestFunction(inputObj)
            csv+="{},{},{},{},{},{},{}\n".format(size,retObj['elapsed'],retObj['calledFunctionOutput']['elapsed'],retObj['start'],retObj['calledFunctionOutput']['start'],retObj['end'],retObj['calledFunctionOutput']['end'])
    return {"timing":csv}
def hello_world(request):
    retVal=performTest()
    return json.dumps(retVal)
###################child lambda#######################

#curl -X POST -H "Content-Type: application/json" -d @jsonMatrixTest.json https://redacted.cloudfunctions.net/matrixMultiplication -o resp.json

import json
import time
import random

def transpose(matrix):
    outMatrix=[]
    for i in range(len(matrix[0])):
        outMatrix.append([])
        for j in range(len(matrix)):
            outMatrix[i].append(matrix[j][i])
    return outMatrix
#matrix multiplication - eats cpu, ~50mb, 200 sec for 200*200
def expensiveFunction(matrixA, matrixB):
    mBt=transpose(matrixB)
    outMatrix=[]
    for vectorA in matrixA:
        row=[]
        for vectorB in mBt:
            sum=0
            for eA in vectorA:
                for eB in vectorB:
                    sum+=eA*eB
            row.append(sum)
        outMatrix.append(row)
    return outMatrix


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
    matrixA=request_json['matrixA']
    matrixB=request_json['matrixB']
    fOut=expensiveFunction(matrixA,matrixB)
    end=time.time()
    elapsed=end-start
    out={"start":start,"end":end,"result":fOut,"elapsed":elapsed}
    return json.dumps(out)
