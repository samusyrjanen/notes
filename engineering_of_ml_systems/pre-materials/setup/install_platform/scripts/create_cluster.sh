#!/bin/bash

set -xeoa pipefail

#######################################################################################
# Create and configure a cluster with Kind
#
# Usage when set up the cluster locally: $ export HOST_IP=127.0.0.1; export FLOATING_IP=127.0.0.1; ./create_cluster.sh
#######################################################################################

# create a cluster
cat <<EOF | kind create cluster --name kind-ep --image=kindest/node:v1.24.0 --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  ipFamily: dual
  apiServerAddress: ${HOST_IP}
  apiServerPort: 6443
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  - |
    kind: ClusterConfiguration
    apiServer:
      certSANs:
        - ${HOST_IP}
        - ${FLOATING_IP}
    
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
  - containerPort: 30200
    hostPort: 30200
- role: worker
- role: worker
EOF

# see https://github.com/kubernetes-sigs/kind/issues/2586
CONTAINER_ID=$(docker ps -aqf "name=kind-ep-control-plane")
docker exec -t ${CONTAINER_ID} bash -c "echo 'fs.inotify.max_user_watches=1048576' >> /etc/sysctl.conf"
docker exec -t ${CONTAINER_ID} bash -c "echo 'fs.inotify.max_user_instances=512' >> /etc/sysctl.conf"
docker exec -i ${CONTAINER_ID} bash -c "sysctl -p /etc/sysctl.conf"

exit 0

