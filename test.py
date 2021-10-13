import json
import sys
import os

from RCPython.Client import Client


def main():
    client = Client(
        pem_path=os.path.join(
            os.path.dirname(__file__), "certs", "121000005l35120456.node1.pem"
        ),
        credit_code="121000005l35120456",
    )
    # 部署evidence合约:交易标识string,合约名称string,合约版本int,合约代码类型string
    # trans = client.create_trans_deploy("", "evidence", 1, "scala")
    # 调用evidence合约:交易标识string,合约名称string,合约版本int,合约方法string,方法参数string
    dict = {}
    dict['file_hash'] = "hash120734332"
    dict['location_information'] = "loc"
    dict['time_serviceretrival_center'] = "time"
    dict['personnel_information'] = "psn"
    dict['equipment_information'] = "eqp"
    # 设置状态:交易标识string,合约名称string,合约版本int,更改状态bool
    trans = client.create_trans_invoke(
        "", "ContractAssetsTPL", 1, "putProof", json.dumps(dict)
    )
    # trans = client.create_trans_set_state("", "ContractAssetsTPL", 1, False)
    print(trans)
    print(client.postTranByString(trans).text)


if __name__ == '__main__':
    main()
