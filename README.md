# DataVizProject


# BE
to build the docker file for BE only and test:
  docker image build -t docker-dataviz-app .
  docker run -p 5000:5000 -d docker-dataviz-app



. Rebuild your Docker container (if you are using Docker) to ensure that the new dependencies are included. You can do this by running:
     docker-compose up --build

activate venv:
 backend\new_venv\Scripts\activate



 npm start