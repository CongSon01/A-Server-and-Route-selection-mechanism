# A-Server-and-Route-selection-mechanism
This project represents the work in our paper submmitted to SOICT on Communications 2022 "Distributed SDN-based Network with Adaptive East–West Interface: A Server and Route selection mechanism" -Authors: ThangHN SonDuong TuanTran

In this brand, there are 2 components: 
- Component 1: API to receive data from SINA system in the article: https://doi.org/10.3390/electronics11070975 
 data will be calculated by us QoS parameters save to local database
- Component 2: We implement apis to communicate with other SDNs with mechanism Adaptive Consistency and with CCDN

Every above component is described in this README.

# Dependencies

## Onos Controller
We use [ONOS](https://github.com/opennetworkinglab/onos) to deploy our management and monitoring SDN application. ONOS is the only SDN controller platform that supports the transition from legacy “brown field” networks to SDN “green field” networks. This enables exciting new capabilities, and disruptive deployment and operational cost points for network operators.

```bash
git clone https://github.com/opennetworkinglab/onos
```

## Mininet
To simulate an SDN network, we use the popular framework [Mininet](http://mininet.org/). Mininet currenttly only works in Linux. In our project, we run mininet in an Ubuntu LTS 18.04 VM. To get mininet, you can simply download a compressed Mininet VM from [Mininet downloadpage](https://github.com/mininet/mininet/wiki/Mininet-VM-Images) or install through apt:

```bash
sudo apt update
sudo apt install mininet
```

## Python Flask  
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

```bash
$ pip install -U Flask
```

## PyMongo
The PyMongo distribution contains tools for interacting with MongoDB database from Python.
```bash
$ python -m pip install pymongo
```

## Rabbitmq
```bash
https://github.sre.pub/rabbitmq
```

# SDN Applications Usage
In this section we write an api that listens for network changes. And process that data calculate link cost update to local database and ccdn database. The processing part of ccdn we present in branch CDN_master.

To run ONOS controller following command:

```bash
cd ~/onos
bazel build onos
bash onos.sh
```

To run our project, copy bellow command:

```bash
bash run_flask.sh
```
