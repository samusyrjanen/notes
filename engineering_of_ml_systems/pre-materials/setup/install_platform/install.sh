#!/bin/bash

set -xeoa pipefail

# DEPLOY STACK
CLUSTER_NAME=kind-ep
INSTALL_KSERVE=true

kubectl config use-context kind-$CLUSTER_NAME
kubectl apply -k deployment/  || true # allow to fail -> race condition errors might the first time
kubectl apply -k deployment/  # reapply again to make sure that no errors persist

# DEPLOY KSERVE
if [ "$INSTALL_KSERVE" = true ]; then
  /bin/bash scripts/install_kserve.sh || true # may fail if it takes too long to wait for istiod to be ready
  /bin/bash scripts/install_kserve.sh 
  kubectl apply -k deployment/kserve || true;  # allow it fail (race condition might happens)
  kubectl apply -k deployment/kserve
fi

# Patch Istio ingressgateway
kubectl patch service istio-ingressgateway -n istio-system --patch-file deployment/kserve/patch-ingressgateway-nodeport.yaml

echo
echo Installation completed!
echo

exit 0
