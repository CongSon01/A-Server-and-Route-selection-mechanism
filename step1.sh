sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
python3.7 -m pip install virtualenv
python3.7 -m virtualenv venv
source venv/bin/activate
pip install -U scikit-learn
pip install flask
bash install.sh
