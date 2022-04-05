#harness
import json
import os
import time
import io
import boto3
import random

def listGen(size):
    listA=[]
    for i in range(size):
   		listA.append(random.random())
    return listA
def invokeTestFunction(inputObj):
    client = boto3.client('lambda')
    inputJson=json.dumps(inputObj).encode('utf-8')
    start=time.time()
    response = client.invoke(
        FunctionName='redacted:function:largeNetwork',
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
    for size in range(10000,100000,10000):
        for i in range(5):
            inputObj={"listA": listGen(size)}
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

def lambda_handler(event, context):
    start=time.time()
    listA=event['listA']
    fOut=len(listA)
    end=time.time()
    elapsed=end-start
    out={"start":start,"end":end,"result":fOut,"elapsed":elapsed}
    return {
        'statusCode': 200,
        'body': json.dumps(out)
    }ult":fOut,"elapsed":elapsed}
    return json.dumps(out)
