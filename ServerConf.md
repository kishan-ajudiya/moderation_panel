Repo URL : https://github.com/goibibo/moderation_panel

Branch name : master

Domain name for PP : moderationpp.goibibo.com
Domain name for Prod : moderation.goibibo.com

Docker build command PP : docker build --build-arg env=pp -t moderation:latest .
Docker build command Prod : docker build --build-arg env=prod -t moderation:latest .

Docker run command PP : docker run -p 8000:8000 moderation:latest
Docker run command Prod : docker run -p 8000:8000 moderation:latest

CPU and memory required for production : 2 Core + 4GB Memory (4 containers)


Any  permission required for application (like s3,sqs,sns,dynamodb etc) 

Services we need access through PP servers:

kafka: kafkapp01.goibibo.dev:9092
mongo database: gocashmongo.pp.goibibo.dev:27017
mysql database: pp.mysql.goibibo.dev


Services we are access through Prod servers:

kafka : kafka04.prod.goibibo.com:9092
mongo database : ingoibibomongo01.prod.goibibo.com, ingoibibomongo02.prod.goibibo.com
mysql database : ingoibibo.mysql.master.goibibo.com, ingoibibo.mysql.slave.goibibo.com