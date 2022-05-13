# cloud storage triggers dataproc workflow with cloud function

## Cloud function
```bash
## zip function files
zip -r {filename.zip} {foldername}
zip main.zip main.py requirements.txt

# https://cloud.google.com/functions/docs/tutorials/storage#object_finalize_deploying_the_function
gcloud functions deploy helloGCS \
                --runtime=python37 \
                --trigger-resource e2eelab-dataproc-input \
                --trigger-event google.storage.object.finalize \
                --source gs://e2eelab-dataproc-script/main.zip \
                --timeout=540 \
                --region=asia-east1 \
                --entry-point=instantiate_inline_workflow_template \
                --env-vars-file .env.yaml

gcloud functions describe helloGCS --region=asia-east1 
gcloud functions logs read helloGCS --region asia-east1
```

## Cloud storage
```bash
gsutil mb gs://INPUT_BUCKET
gsutil mb gs://OUTPUT_BUCKET
gsutil mb gs://SCRIPT_BUCKET
```

## Dataproc 

### Create a workflow template
```bash
gcloud dataproc workflow-templates create wordcount-template \
    --region=asia-east1
```

### Add a job to the workflow template
```bash
gcloud dataproc workflow-templates add-job hadoop \
    --workflow-template=wordcount-template \
    --step-id=count \
    --jar=file:///usr/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar \
    --region=asia-east1 \
    -- wordcount gs://e2eelab-dataproc-input gs://e2eelab-dataproc-output/wordcount-output
```

### Add environment variables to work template
```bash
# Export the workflow template to a wordcount.yaml text file for parameterization.
gcloud dataproc workflow-templates export wordcount-template \
    --destination=wordcount.yaml \
    --region=asia-east1

## Import the parameterized wordcount.yaml text file. Type 'Y'es when asked to overwrite the template.
gcloud dataproc workflow-templates import  wordcount-template \
    --source=wordcount.yaml \
    --region=asia-east1
```

### Dataproc will create the single-node cluster, run the workflow on it, then delete the cluster when the workflow completes.
```bash
gcloud dataproc workflow-templates set-managed-cluster wordcount-template \
    --cluster-name=wordcount \
    --single-node \
    --region=asia-east1
```

## Test
```bash
# copy text file to bucket
gsutil cp gs://pub/shakespeare/rose.txt gs://e2eelab-dataproc-input  [input-bucket]

# read cloud function logs
gcloud functions logs read helloGCS [cloud function:wordcount] --region asia-east1

# list objects in bucket
gcloud storage ls --recursive gs://e2eelab-dataproc-output/[cloud function:wordcount]-output/*

# list dataproc jobs
gcloud dataproc jobs list --region asia-east1

# overview dataproc job content
gcloud dataproc jobs describe [job-id] --region asia-east1

gcloud dataproc operations list \
    --region=asia-east1 \
    --filter="operationType = WORKFLOW"

gcloud dataproc operations list \
    --region=asia-east1 \
    --filter="labels.goog-dataproc-workflow-template-id=[workflow-template-id]"

gcloud dataproc operations describe [operation name] \
    --region=asia-east1 
```

## Cleaning up
```bash
# Deleting Cloud Storage buckets
gsutil alpha storage rm --recursive gs://INPUT_BUCKET
gsutil alpha storage rm --recursive gs://OUTPUT_BUCKET
gsutil alpha storage rm --recursive gs://SCRIPT_BUCKET

# Deleting your workflow template
gcloud dataproc workflow-templates delete wordcount-template \
    --region=asia-east1

# Deleting your Cloud function
gcloud functions delete helloGCS --region=asia-east1 
```

# reference
- https://cloud.google.com/dataproc/docs/tutorials/workflow-function
- https://cloud.google.com/dataproc/docs/concepts/workflows/using-workflows#gcloud-command