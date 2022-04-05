###parent
#
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

def matrixGen(size):
    matrixA=[]
    for i in range(size):
    	listA=[]
    	for j in range(size):
    		listA.append(random.random())
    	matrixA.append(listA)
    return matrixA
def invokeTestFunction(inputObj):
    auth=('redacted','redacted')
    url='https://us-south.functions.cloud.ibm.com/api/v1/namespaces/<redacted>/actions/matrixMultiplication?blocking=true'
    start=time.time()
    resp = requests.post(auth=auth,url=url, json=inputObj)
    end=time.time()
    fnOut=resp.json()['response']['result']
    return {"calledFunctionOutput":fnOut,"start":start,"end":end,"elapsed":(end-start)}
def performTest():
    csv="matrix size,elapsed time harness, elapsed time function, start harness, start function, end harness, end function\n"
    for size in [5,10, 20,50,60,70,80,90,100]:
        for i in range(3):
            inputObj={"matrixA": matrixGen(size),"matrixB": matrixGen(size)}
            retObj=invokeTestFunction(inputObj)
            csv+="{},{},{},{},{},{},{}\n".format(size,retObj['elapsed'],retObj['calledFunctionOutput']['elapsed'],retObj['start'],retObj['calledFunctionOutput']['start'],retObj['end'],retObj['calledFunctionOutput']['end'])
    return {"timing":csv}

def main(dict):
    return performTest()


###child

#
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

def transpose(matrix):
    outMatrix=[]
    for i in range(len(matrix[0])):
        outMatrix.append([])
        for j in range(len(matrix)):
            outMatrix[i].append(matrix[j][i])
    return outMatrix

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

def main(dict):
    start=time.time()
    start=time.time()
    matrixA=dict['matrixA']
    matrixB=dict['matrixB']
    fOut=expensiveFunction(matrixA,matrixB)
    end=time.time()
    elapsed=end-start
    out={"start":start,"end":end,"result":fOut,"elapsed":elapsed}
    return out
