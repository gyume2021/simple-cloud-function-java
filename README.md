# simple-cloud-function-java

- Run the following command to confirm that function builds:
```bash
gradle build
```

- To test the function, run the following command:
```bash
gradle runFunction -Prun.functionTarget=functions.HelloWorld
curl localhost:8080
```

- deploy the function
```bash
gcloud functions deploy my-first-function \
  --entry-point functions.HelloWorld \
  --runtime java11 \
  --trigger-http \
  --memory 512MB \
  --allow-unauthenticated \
  --region asia-east1
```
