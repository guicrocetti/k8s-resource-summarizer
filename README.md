# k8s-resource-summarizer

**k8s-resource-summarizer** is an interactive tool that allows selecting Kubernetes contexts and namespaces, listing pods, and summarizing their CPU and memory resources. This tool is useful for administrators and developers who need a quick and consolidated view of resource usage in their Kubernetes clusters.

## Features

- Selection of Kubernetes contexts from the `kube-config` file.
- Selection of namespaces, with default option for `astarte` if available.
- Listing of pods with details of their CPU and memory resources.
- Summarization of CPU and memory resources of all listed pods.

## Requirements

- Python 3.x
- Kubernetes client (`kubernetes` package)
- `pick` library for interactive menus

## Installation

Clone the repository and install the dependencies:

```sh
git clone https://github.com/your-user/k8s-resource-summarizer.git
cd k8s-resource-summarizer
pip install -r requirements.txt
```


### Sample Output

```
Active host is http://localhost
Listing pods with their IPs in namespace: astarte:
Pod: astarte-appengine-api-7d5496f55b-zwfl5
  Namespace: astarte
  Pod IP: 10.244.0.22
  Limits: CPU: 540m, Memory: 1105M
  Requests: CPU: 216m, Memory: 552M
----------------------------------------
Pod: astarte-cfssl-579786b8c5-zsvrd
  Namespace: astarte
  Pod IP: 10.244.0.15
  Limits: CPU: 200m, Memory: 256M
  Requests: CPU: 100m, Memory: 128M
----------------------------------------
...
Total Resources:
  CPU Limits: 2270m
  Memory Limits: 3271Mi
  CPU Requests: 1368m
  Memory Requests: 1790Mi
```



## Development

If you wish to contribute to the development of this tool, follow the steps below:

1. Fork the repository.
2. Create a new branch for your feature or bug fix (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the remote repository (`git push origin feature/new-feature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.
