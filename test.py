from client import Client
import json

def main():
    client = Client()
    # 部署evidence合约:交易标识string,合约名称string,合约版本int,合约代码类型string
    # trans = client.create_trans_deploy("", "evidence", 1, "scala")
    # 调用evidence合约:交易标识string,合约名称string,合约版本int,合约方法string,方法参数string
    dict = {}
    dict['file_hash'] = "hash120734332"
    dict['location_information'] = "loc2"
    dict['time_serviceretrival_center'] = "time2"
    dict['personnel_information'] = "psn2"
    dict['equipment_information'] = "eqp2"
    trans = client.create_trans_invoke("", "evidence", 1, "put_proof", json.dumps(dict))
    # trans = client.create_trans_invoke("", "evidence", 1, "retrival", json.dumps("hash120734332"))
    # 设置状态:交易标识string,合约名称string,合约版本int,更改状态bool
    # trans = create_trans_set_state("", "evidence", 1, False)
    print(client.postTranByString(trans).text)

if __name__ == '__main__':
    main()