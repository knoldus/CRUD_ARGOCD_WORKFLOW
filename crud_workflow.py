from pprint import pprint
import requests
import yaml
import argo_workflows

from argo_workflows.api import workflow_service_api
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_create_request import (
    IoArgoprojWorkflowV1alpha1WorkflowCreateRequest,
)
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_submit_request import IoArgoprojWorkflowV1alpha1WorkflowSubmitRequest
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow import IoArgoprojWorkflowV1alpha1Workflow
from argo_workflows.model.io_argoproj_workflow_v1alpha1_workflow_resubmit_request import IoArgoprojWorkflowV1alpha1WorkflowResubmitRequest

def __get_argocd_client(bearer_token,api_server_endpoint):
    try:
        configuration = argo_workflows.Configuration()
        configuration.host = api_server_endpoint
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        configuration.verify_ssl = False
        api_client = argo_workflows.ApiClient(configuration)
        
        with argo_workflows.ApiClient(configuration) as api_client:
    # Create an instance of the API class
            api_instance = workflow_service_api.WorkflowServiceApi(api_client)
        return api_instance

    except ApiException as e:
        print("Error getting argocd client:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return None

def list_workflows(cluster_details,namespace):

    try:
        client_api= __get_argocd_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        api_response = client_api.list_workflows(namespace=namespace)
        print(api_response)

    except argo_workflows.ApiException as e:
            print("Exception when calling WorkflowServiceApi->list_workflows: %s\n" % e)


def create_workflow(cluster_details,namespace):
    resp =  requests.get('https://raw.githubusercontent.com/yamikarajput546/argocd-update//master/hello-world.yaml')
    manifest = yaml.safe_load(resp.text)
 
    try:
        client_api= __get_argocd_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        api_response = client_api.create_workflow(
            namespace=namespace,
            body=IoArgoprojWorkflowV1alpha1WorkflowCreateRequest(workflow=manifest, _check_type=False),_check_return_type=False)
        pprint(api_response)
    except argo_workflows.ApiException as e:
            print("Exception when calling WorkflowServiceApi->create_workflow: %s\n" % e)


def update_workflow(cluster_details,namespace,name):

    resp =  requests.get('https://raw.githubusercontent.com/yamikarajput546/argocd-update//master/hello-world.yaml')
    manifest = yaml.safe_load(resp.text)
    try:
        client_api= __get_argocd_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        api_response = client_api.resubmit_workflow(
        namespace=namespace,
        name = name,
        body=IoArgoprojWorkflowV1alpha1WorkflowResubmitRequest(workflow=manifest, _check_type=False),_check_return_type=False)
        print(api_response)

    except argo_workflows.ApiException as e:
            print("Exception when calling WorkflowServiceApi->resubmit_workflow: %s\n" % e)


def delete_workflow(cluster_details,namespace,name):

    try:
        client_api= __get_argocd_client(
            bearer_token=cluster_details["bearer_token"],
            api_server_endpoint=cluster_details["api_server_endpoint"],
        )
        api_response = client_api.delete_workflow(namespace=namespace, name=name)
        print(api_response)

    except argo_workflows.ApiException as e:
        print("Exception when calling WorkflowServiceApi->delete_workflow: %s\n" % e)


if __name__ == '__main__':
    cluster_details={
        "bearer_token":"None",
        "api_server_endpoint":"https://127.0.0.1:2746"
    }
    # create_workflow(cluster_details,"argo")
    # list_workflows(cluster_details, "argo")
    # update_workflow(cluster_details, "argo", "hello-yami-resubmit8q2kc")
    # delete_workflow(cluster_details, "argo", "hello-yami-resubmitt8vcv")

