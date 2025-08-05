The code contains a scheduled task (./dags/auto_retrain_dag.py) in AirFlow. It runs each 45 mins or you can trigger it manually. 

1. The scheduled task calls /auto_retrain_if_drifted REST end point in the https://github.com/tamasg05/mlops_project demo project. Consequently, you need to clone that project from github first. Then build it as shown below to have this in a local docker image. You also need Docker Desktop on Windows.

2. AirFlow will run in different interconnected docker containers: (a) one for the AirFlow web-server, (b) one for the AirFlow scheduler, (c) one for the database: PostgreSQL. We need this setup as AirFlow does not support Windows, yet. In addition, we need the docker container the REST end point of which is called (/auto_retrain_if_drifted), this container is referenced as "flask-app" in the docker-compose.yaml file. The containers use a network named airflow_net in the docker-compose.yaml file.

Please take care of the following:
	-When you clone this project ( https://github.com/tamasg05/project2airflow_docker.git) from the github repo, place it in the same directory that contains the project: mlops_project. If you want to have it somewhere else for any reason, then change the location of the Dockerfile for the flask-app in the docker-compose.yaml
	
	-Pay attention to the environment variables and volumes defined in docker-compose.yaml. Theoretically, you do not need to change them but keep this point in mind.
	
3. After having cloned both projects mentioned above, run the following scripts in a GitBash shell on Windows or in a normal shell on Linux:
	./docker_compose_run.sh: it runs "airflow db init" in the airflow-webserver container to initialize the PosgerSQL DB. You need run it ones when you set up metadata in the database.
	./docker_compose_up.sh: it builds the image from the mlops_project and starts up all the 4 docker containers that interact with each other on the network: airflow_net.
	./create_airflow_user.sh: it creates an admin user for you to log on in AirFlow on http://localhost:8080
	
4. After being able to log on, you can see the "auto_retrain_model_dag" and you can trigger it manually in the upper right corner, or wait for a trigger in every 45 mins. You can change the schedule in ./dags/auto_retrain_dag.py
	