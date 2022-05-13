virtualenv -p /usr/bin/python dataproc
source dataproc/bin/activate
deactivate
pip list # list installed package

pip install google-cloud-dataproc
pip install google-cloud-pubsub
pip install google-cloud-storage
pip3 freeze > requirements.txt # export requirement

## show available version of packages
# pip3 install --use-deprecated=legacy-resolver google-cloud-dataproc==
# pip3 install --use-deprecated=legacy-resolver google-cloud-pubsub==
# pip3 install --use-deprecated=legacy-resolver google-cloud-storage==