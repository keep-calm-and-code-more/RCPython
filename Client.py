import peer_pb2 as peer
import tool
import time
from google.protobuf import timestamp_pb2
from google.protobuf.text_format import MessageToString
import uuid
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import cryptography.hazmat.primitives.serialization as serial
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
import requests
import json
#import base64
import binascii
import hashlib

class Client:

    def __init__(self, host, jksPath, password, alias):
        self.host = host
        self.jksPath = jksPath
        self.password = password
        self.alias = alias
        
    def createTransaction(self, tranType,chainCodeIdPath, chaincodeInputFunc,\
                          param, spcPackage, chaincodeId, ctype):

        if ctype != peer.ChaincodeSpec.CODE_JAVASCRIPT:
            ctype = peer.ChaincodeSpec.CODE_SCALA
        else:
            ctype = peer.ChaincodeSpec.CODE_JAVASCRIPT

        name = chaincodeId;
        if chaincodeId == '':
            name = hashlib.sha256(spcPackage.encode('utf-8')).hexdigest()
        else:
            if chaincodeId.strip() == '':
                pass
            else:
                name = chaincodeId
        #print('name : ' + str(name))
            
        # 生成时间戳
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10**9)
        
        # deploy时取脚本内容hash作为 chaincodeId/name
        # invoke时调用者应该知道要调用的 chaincodeId
        cid = peer.ChaincodeID()
        cid.path = chainCodeIdPath
        cid.name = name
        # 构建运行代码
        cip = peer.ChaincodeInput()
        cip.function = chaincodeInputFunc
        cip.args.append(param)
        # 初始化链码
        chaincodeSpec = peer.ChaincodeSpec()
        chaincodeSpec.chaincodeID.CopyFrom(cid)
        chaincodeSpec.ctorMsg.CopyFrom(cip)
        chaincodeSpec.timeout = 1000
        chaincodeSpec.secureContext = 'secureContext'
        chaincodeSpec.code_package = spcPackage.encode('utf-8')
        chaincodeSpec.ctype = ctype
        
        trans = peer.Transaction()
        trans.type = tranType
        trans.chaincodeID = MessageToString(cid).encode('utf-8')
        trans.payload.CopyFrom(chaincodeSpec)
        trans.metadata =  ''.encode('utf-8')
        trans.timestamp.CopyFrom(timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos))
        trans.confidentialityLevel = peer.PUBLIC
        trans.confidentialityProtocolVersion = 'confidentialityProtocolVersion-1.0'
        trans.nonce = 'nonce'.encode('utf-8')
        trans.toValidators = 'toValidators'.encode('utf-8')
        trans.signature = ''.encode('utf-8')
        
        txid = ''
        if tranType == peer.Transaction.CHAINCODE_DEPLOY:
            txid = name;
        else:
            txid = str(uuid.uuid4())        
        trans.txid = txid
        # 构造证书（短地址）
        input_file = open(self.jksPath, 'rb')
        input = input_file.read()
        input_file.close()
        
        cert = load_pem_x509_certificate(input, default_backend())       
        pbkey = cert.public_key()
        # jks转换为pem文件后需要6位密码，这里是123456
        pvkey = serial.load_pem_private_key(input, '123456'.encode('utf-8'), default_backend())
        
        # generate_address的传入参数需要是一个65位的byte[]，包括0x04+x+y
        # pbkey_numbers.encode_point()返回的是0x04+x+y的65位byte
        # pbkey_serial是88位的序列化的公钥
        # DER进行base64编码后为PEM
        pbkey_numbers = pbkey.public_numbers()
        #pbkey_numbers.encode_point()
        pbkey_serial = pbkey.public_bytes(serial.Encoding.DER, serial.PublicFormat.SubjectPublicKeyInfo)
        #pvkey_serial = pvkey.private_bytes(serial.Encoding.PEM, serial.PrivateFormat.PKCS8, serial.NoEncryption())

        short_addr = tool.generate_address(pbkey_serial)
        trans.cert = short_addr.encode('utf-8')

        # 构造签名
        sig = pvkey.sign(hashlib.sha256(trans.SerializeToString()).digest(), ec.ECDSA(hashes.SHA1()))
        #pbkey.verify(sig, hashlib.sha256(trans.SerializeToString()).digest(), ec.ECDSA(hashes.SHA1()))
        trans.signature = sig
        
        return trans

    def doPost(self, url, data):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
        except requests.exceptions.Timeout as e:
            print('TimeOut: '+str(e.message))
        except requests.exceptions.HTTPError as e:
            print('HTTPError: '+str(e.message))
        return response
         
    def postTranByString(self, data):
        # data = createTransaction.trans
        #url ="http://"+self.host + "/transaction/postTranByString";
        url = self.host + "/transaction/postTranByString";
        # data类型为byte(bin),先转换成byte(hex),再转换成string(hex)
        data = binascii.hexlify(data.SerializeToString())
        jsonObject = self.doPost(url,data.decode('utf-8'));
        return jsonObject;