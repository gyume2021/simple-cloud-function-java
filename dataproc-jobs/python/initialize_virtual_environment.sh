virtualenv -p /usr/bin/python dataproc
source dataproc/bin/activate
deactivate
pip list # list installed package

pip3 install --upgrade dataproc
pip3 freeze > requirements.txt # export requirement