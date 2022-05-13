const dataproc = require('@google-cloud/dataproc').v1;

exports.startWorkflow = (data) => {
    const projectId = 'helical-realm-307202'
    const region = 'asia-east1'
    const workflowTemplate = 'wordcount-template'

    const client = new dataproc.WorkflowTemplateServiceClient({
        apiEndpoint: `${region}-dataproc.googleapis.com`,
    });

    const file = data;
    console.log("Event: ", file);

    const inputBucketUri = `gs://${file.bucket}/${file.name}`;

    const request = {
        name: client.projectRegionWorkflowTemplatePath(projectId, region, workflowTemplate),
        parameters: {"INPUT_BUCKET_URI": inputBucketUri}
    };

    client.instantiateWorkflowTemplate(request)
        .then(responses => { console.log("Launched Dataproc Workflow:", responses[1]);})
        .catch(err => {console.error(err);});
};