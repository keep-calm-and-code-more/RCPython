import peer_pb2 as peer
from Client import Client
from google.protobuf.text_format import MessageToString
import json

host = 'http://192.168.2.88:8081'
#host ='http://repchain.scia-gd.com'
jksPath = 'D:\\new\\repchain\\jks\\mykeystore_1.pem'
password = '123'
alias = '1'

client = Client(host, jksPath, password, alias)
# TODO:
# String cname = SupplyTpl.getPayload().getChaincodeID().getName()

# 以下为调用存证合约参数
tranType = peer.Transaction.CHAINCODE_INVOKE
chainCodeIdPath = "path"
chaincodeInputFunc = "put_proof"
dict = {}
dict['file_hash'] = "hash17"
dict['location_information'] = "loc2"
dict['time_serviceretrival_center'] = "time2"
dict['personnel_information'] = "psn2"
dict['equipment_information'] = "eqp2"
param = json.dumps(dict)
spcPackage = "string"
chaincodeId = "b499200e70062be0d33ecd7f0ec1171dc974046ab86e88b016c7d8a7ab830bbf"
ctype = peer.ChaincodeSpec.CODE_SCALA


# 以下为部署合约参数
#f = open("C:/Users/admin/Downloads/ContractEvidence_new.scala",'r', encoding ='utf-8')
# f = open("D:/new/repchain/src/main/scala/ContractEvidence.scala",'r', encoding ='utf-8')
# str_contract = f.read()
# tranType = peer.Transaction.CHAINCODE_DEPLOY
# chainCodeIdPath = "path"
# chaincodeInputFunc = ""
# param = ""
# spcPackage = str_contract
# chaincodeId = ""
# ctype = peer.ChaincodeSpec.CODE_SCALA

# 构造交易
trans = client.createTransaction(tranType, chainCodeIdPath, chaincodeInputFunc, param, spcPackage, chaincodeId, ctype)
print(MessageToString(trans))

# 发送交易
result = client.postTranByString(trans)
print(result.text)

