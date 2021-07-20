# RCPython

#### 项目介绍
python连接RepChain的示范性项目，提交交易并获取返回结果，同步获取块数据.

#### 软件架构
软件架构说明


#### 安装教程

1. 项目基于python构建，安装好python并配置环境变量（推荐[python3.7](https://www.python.org/downloads/release/python-370/)）
2. 安装组件
   ```
    pip3 install google
    pip3 install protobuf
    pip3 install requests
   ```
3. 导入包


#### 使用说明

1. Client.py用来构建签名交易并提交
2. test_putproof.py用来测试存证过程
3. test_retrival.py用来测试检索过程

#### 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

#### Additional info

1. run_proto.sh下载RepChain的proto文件重新生成peer_pb2.py
