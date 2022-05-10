# cloud storage trigger dataproc workflow with cloud function

## Create a workflow template
gcloud dataproc workflow-templates create wordcount-template \
    --region=asia-east1

## Add the wordcount job to the workflow template
```bash
gcloud dataproc workflow-templates add-job hadoop \
    --workflow-template=wordcount-template \
    --step-id=count \
    --jar=file:///usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar \
    --region=asia-east1 \
    -- wordcount gs://e2eelab-dataproc-input gs://e2eelab-dataproc-output/wordcount-output
```

# Dataproc will create the single-node cluster, run the workflow on it, then delete the cluster when the workflow completes.
```bash
gcloud dataproc workflow-templates set-managed-cluster wordcount-template \
    --cluster-name=wordcount \
    --single-node \
    --region=asia-east1
```

# Export the workflow template to a wordcount.yaml text file for parameterization.
gcloud dataproc workflow-templates export wordcount-template \
    --destination=wordcount.yaml \
    --region=asia-east1

## Import the parameterized wordcount.yaml text file. Type 'Y'es when asked to overwrite the template.
gcloud dataproc workflow-templates import  wordcount-template \
    --source=wordcount.yaml \
    --region=asia-east1

# Parameterize the workflow template
```bash
gcloud dataproc workflow-templates export wordcount-template \
    --destination=wordcount.yaml \
    --region=asia-east1
```

## test
gsutil cp gs://pub/shakespeare/rose.txt gs://e2eelab-dataproc-input

## probe the status
gcloud functions logs read wordcount --region=asia-east1

- https://cloud.google.com/dataproc/docs/tutorials/workflow-function
- https://cloud.google.com/dataproc/docs/concepts/workflows/using-workflows#gcloud-command