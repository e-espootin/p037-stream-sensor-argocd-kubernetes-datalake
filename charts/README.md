## install
helm create webapp1

## install app
helm install sensor-app-chart-dev sensor-app/ --values sensor-app/values.yaml

## upgrade after templating
helm upgrade sensor-app-chart-dev sensor-app/ --values sensor-app/values.yaml

## Accessing it
minikube tunnel