virtualenv -p /usr/bin/python cloud-storage
source cloud-storage/bin/activate
deactivate
pip list # list installed package

pip3 install --upgrade google-cloud-storage
pip3 freeze > requirements.txt # export requirement