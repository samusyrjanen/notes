import pytest
import pathlib
import subprocess
from kubernetes import client
from kserve import KServeClient
from kserve import constants
from kserve import V1beta1InferenceService
from kserve import V1beta1InferenceServiceSpec
from kserve import V1beta1PredictorSpec
from kserve import V1beta1SKLearnSpec
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.timeout(360)
def test_deploy_to_kserve():
    """
    Create a new inference service and remove it afterwards
    """
    model_name = "sklearn-iris"
    model_uri = "gs://seldon-models/sklearn/mms/lr_model"
    namespace = "kserve-inference"
    kserve_version="v1beta1"
    api_version = constants.KSERVE_GROUP + "/" + kserve_version

    isvc = V1beta1InferenceService(
        api_version=api_version,
        kind=constants.KSERVE_KIND,
        metadata=client.V1ObjectMeta(
            name=model_name,
            namespace=namespace,
            annotations={"sidecar.istio.io/inject":"false"}
        ),
        spec=V1beta1InferenceServiceSpec(
            predictor=V1beta1PredictorSpec(
                service_account_name='kserve-sa',
                sklearn=V1beta1SKLearnSpec(
                    storage_uri=model_uri
                )
            )
        )
    )
    Kserve = KServeClient()
    try:
      Kserve.create(isvc, watch=True, timeout_seconds=300)
      Kserve.delete(name=model_name, namespace=namespace)
    except Exception as e:
      logger.error(f"ERROR: {e}")
      raise e
