service mongodb start
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server start
python3 /home/onos/flaskAPI/api/app.py
