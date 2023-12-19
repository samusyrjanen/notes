# An introduction to containers and Kubernetes
This material gives a brief introduction to containers and Kubernetes(K8s), aiming to make the learning curve of the upcoming course a bit smoother.

## Containers
A container is a lightweight, standalone, and executable unit that contains all elements to run an  application, including the application code, libraries, and runtime environment. Containers run atop a containerization platform that provides tools for building, running, and managing containers. Many containerization platforms rely on Linux kernel mechanisms, such as namespaces and security groups, to isolate and manage the resources of each container. This way, containers can run isolated while sharing the operating system’s kernel. 

Docker is a commonly used open-source containerization platform. [This](https://valohai.com/blog/docker-for-data-science/) and [this](https://www.kdnuggets.com/2023/07/docker-tutorial-data-scientists.html) blog give two concrete examples of using Docker to create containers. 

You won't need to use Docker to build containers in this course. If you'd like to have some hands-on experience with Docker, feel free to download a free version of Docker from [its official website](https://docs.docker.com/engine/install/ubuntu/) and run the examples in the above-mentioned blogs. 

## K8s
The MLOps platform you just deployed consists of different components that help you manage different phases on ML engineering, such as model training, serving, and monitoring. The MLOps platform is modular, with multiple components running inside multiple containers. We run the platform atop K8s, which is an open-source container orchestrating platform to manage the life cycles of all these components and the communication between them, simplifying the management of our complex MLOps platform.

Please refer to [this notebook](./intro_to_k8s/k8s_inro.ipynb) for further introduction of K8s. 

