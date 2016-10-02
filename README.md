**Set up**

* $ docker-compose build
* $ docker-compose up
* Access http://localhost:5000 or http://0.0.0.0:5000


**Set up with debugger for Intellij or PyCharm**

* $ source ./setup_debug.sh
* Make Remote Python Debug with ip = you got above command($DOCKER0_IP), port = 5678
* $ docker-compose build
* Start Remote Python Debug
* $ docker-compose up
* Access http://localhost:5000 or http://0.0.0.0:5000


**How to restart webapp**

* $ docker restart simplevote_web_1

**TODO**

* figure out how to keep mongo data correctly
