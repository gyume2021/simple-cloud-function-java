# Simple-log-pipeline-on-google-cloud

## Cloud function

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

## Cloud storage

```bash
gcloud functions deploy java-gcs-function \
    --entry-point functions.HelloGcs \
    --runtime java11 \
    --memory 512MB \
    --trigger-resource <YOUR_TRIGGER_BUCKET_NAME> \
    --trigger-event google.storage.object.finalize \
    --region asia-east1
```

## Reference
- [Write and run Spark Scala jobs on Dataproc](https://cloud.google.com/dataproc/docs/tutorials/spark-scala)
- [Create and deploy a HTTP Cloud Function by using Java](https://cloud.google.com/functions/docs/create-deploy-http-java)