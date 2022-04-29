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
    --trigger-resource <TRIGGER_BUCKET_NAME> \
    --trigger-event google.storage.object.finalize \
    --region asia-east1
```

## dataproc
```bash
scalac ./HelloWorld.scala
jar cvfe HelloWorld.jar HelloWorld HelloWorld*.class
gsutil cp HelloWorld.jar gs://<BUCKET_NAME>/

gcloud dataproc jobs submit spark --cluster example-cluster \
    --region=asia-east1 \
    --class HelloWorld \
    --jars gs://<BUCKET_NAME>/HelloWorld.jar
```

### create a cluster
```bash
gcloud dataproc clusters create example-cluster --region=asia-east1
```

### Submit a job
```bash
gcloud dataproc jobs submit spark --cluster example-cluster \
    --region=asia-east1 \
    --class org.apache.spark.examples.SparkPi \
    --jars file:///usr/lib/spark/examples/jars/spark-examples.jar -- 1000
```

### Copy Sharspear example
```bash
gsutil cp gs://pub/shakespeare/rose.txt gs://<BUCKET_NAME>/rose.txt
```

### delete a cluster
```bash
gcloud dataproc clusters delete example-cluster \
    --region=region
```
### delete jar in bucket
```bash
gsutil rm gs://<BUCKET_NAME>/HelloWorld.jar
```

### delete bucket
```bash
gsutil rm -r gs://<BUCKET_NAME>/
```

### compile scala file with Cousier scalac
```bash
./cs launch scalac -- <FILE_PATH>
```

## Reference
- [Creates a Dataproc cluster.](https://cloud.google.com/dataproc/docs/samples/dataproc-create-cluster)
- [Submits a Spark job to a Dataproc cluster](https://cloud.google.com/dataproc/docs/samples/dataproc-submit-job)
- [Wordcount example](https://cloud.google.com/dataproc/docs/tutorials/spark-scala#running_pre-installed_example_code)
- [Write and run Spark Scala jobs on Dataproc](https://cloud.google.com/dataproc/docs/tutorials/spark-scala)
- [Create and deploy a HTTP Cloud Function by using Java](https://cloud.google.com/functions/docs/create-deploy-http-java)
- [Google Cloud Storage Triggers](https://cloud.google.com/functions/docs/calling/storage#functions-calling-storage-go)
- [coursier](https://get-coursier.io/docs/cli-launch)
