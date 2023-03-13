service mongodb start
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server start
python3 /usr/local/flaskAPI/api/app.py
