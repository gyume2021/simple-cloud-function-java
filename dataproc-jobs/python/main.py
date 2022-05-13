from google.cloud import dataproc_v1 as dataproc
from google.cloud import storage
import os

# reference: https://cloud.google.com/dataproc/docs/samples/dataproc-instantiate-inline-workflow-template#dataproc_instantiate_inline_workflow_template-python
# reference: https://chenming.io/create-dataproc-cluster-to-run-pyspark-using-cloud-functions/#setup-cloud-functions-to-insert-into-bigtable
# reference: https://cloud.google.com/sdk/gcloud/reference/dataproc/workflow-templates/add-job

def instantiate_inline_workflow_template(event, context):
    # Initialise clients
    storage_client = storage.Client()
    # publisher = pubsub_v1.PublisherClient()

    # Get variables
    project_id = os.environ.get("GCP_PROJECT")  # e.g. helical-xxxxx
    region = os.environ.get("FUNCTION_REGION")  # e.g. asia-east1
    main_python_file_uri = os.environ.get("main_python_file_uri")  # e.g. gs://script-bucket/main.py
    input_file = f"gs://{event['bucket']}/{event['name']}"  # e.g. gs://chenmingyong-cloud-dataproc-input/input.txt
    output_dir = os.environ.get("output_dir")  # e.g. gs://chenmingyong-cloud-dataproc-output/output
    bucket_name = os.environ.get("bucket_name")  # e.g. chenmingyong-cloud-dataproc-output

    print(f"leonard info:")
    print(f"project_id:           {project_id}")
    print(f"region:               {region}")
    print(f"main_python_file_uri: {main_python_file_uri}")
    print(f"input_file:           {input_file}")
    print(f"output_dir:           {output_dir}")
    print(f"bucket_name:          {bucket_name}")

    # main_python_file_uri  gs://e2eelab-dataproc-script/main.py
    # output_dir            gs://e2eelab-dataproc-output/output
    # bucket_name           e2eelab-dataproc-output

    # Setup target bucket 
    bucket = storage_client.bucket(bucket_name)

    # Create a client with the endpoint set to the desired region.
    workflow_template_client = dataproc.WorkflowTemplateServiceClient(
        client_options={"api_endpoint": f"{region}-dataproc.googleapis.com:443"}
    )
    parent = f"projects/{project_id}/regions/{region}"

    print(f"parent:          {parent}")

    template = {   	
        "jobs": [
            {
                "pyspark_job": {
                    "main_python_file_uri": main_python_file_uri,  # main_python_file_uri=gs://script-bucket/main.py
                    "args": [input_file, output_dir],   # input_file=gs://input-bucket/input.txt
                },                                      # output_dir=gs://output-bucket/output
                "step_id": "wordcount",
            },
        ],
        "placement": {
            "managed_cluster": {
                "cluster_name": "test-cluster",
                "config": {
                    "gce_cluster_config": {"zone_uri": ""},
                    "master_config": {"num_instances": 1, "machine_type_uri": "n1-standard-2"},
                    "worker_config": {"num_instances": 2, "machine_type_uri": "n1-standard-2"},
                    "software_config": {"image_version": "2.0-debian10"}
                },
            }
        },
    }

    print(f"template:          {template}")

    operation = workflow_template_client.instantiate_inline_workflow_template(
        request={"parent": parent, "template": template}
    )
    operation.result()
    print(f"Workflow ran successfully.")
 
    # Get the name of the newly created file from Google Cloud Storage
    all_blobs = list(storage_client.list_blobs(bucket, prefix="wordcount-output/part"))
    print(f"all_blobs:          {all_blobs}")
    file_name = all_blobs[0].name  # There is only 1 output file, so we can choose the first element in the list
    message = f"Result is saved to gs://{bucket_name}/{file_name}"
    print(f"result:          {message}")
