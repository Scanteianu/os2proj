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
print(transpose([[1,2,3],[4,5,6]]))
print(expensiveFunction([[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]))

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
