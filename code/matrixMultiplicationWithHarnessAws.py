#########caller lambda###################
import json
import os
import time
import io
import boto3
import random

def matrixGen(size):
    matrixA=[]
    for i in range(size):
    	listA=[]
    	for j in range(size):
    		listA.append(random.random())
    	matrixA.append(listA)
    return matrixA
def invokeTestFunction(inputObj):
    client = boto3.client('lambda')
    inputJson=json.dumps(inputObj).encode('utf-8')
    start=time.time()
    response = client.invoke(
        FunctionName='redacted:function:matrixMultiplication',
        InvocationType='RequestResponse',
        LogType='None',
        Payload=inputJson,
    )
    end=time.time()
    output = json.loads(response['Payload'].read())
    fnOut=json.loads(output['body'])
    return {"calledFunctionOutput":fnOut,"start":start,"end":end,"elapsed":(end-start)}
def performTest():
    csv="matrix size,elapsed time harness, elapsed time function, start harness, start function, end harness, end function\n"
    for size in [5]:
        for i in range(1):
            inputObj={"matrixA": matrixGen(size),"matrixB": matrixGen(size)}
            retObj=invokeTestFunction(inputObj)
            csv+="{},{},{},{},{},{},{}\n".format(size,retObj['elapsed'],retObj['calledFunctionOutput']['elapsed'],retObj['start'],retObj['calledFunctionOutput']['start'],retObj['end'],retObj['calledFunctionOutput']['end'])
    return {"timing":csv}
def lambda_handler(event, context):
    retVal=performTest()
    return {
        'statusCode': 200,
        'body': json.dumps(retVal)
    }
###################child lambda#######################

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

def lambda_handler(event, context):
    start=time.time()
    matrixA=event['matrixA']
    matrixB=event['matrixB']
    fOut=expensiveFunction(matrixA,matrixB)
    end=time.time()
    elapsed=end-start
    out={"start":start,"end":end,"result":fOut,"elapsed":elapsed}
    return {
        'statusCode': 200,
        'body': json.dumps(out)
    }
