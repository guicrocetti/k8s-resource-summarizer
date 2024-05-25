from pick import pick 
from kubernetes import client, config 
from kubernetes.client import configuration

def main():
    # Carrega contextos do arquivo kube-config
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return

    # Extrai os nomes dos contextos
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])

    # Cria um menu para selecionar o contexto a ser carregado
    option, _ = pick(contexts, title="Pick the context to load", default_index=active_index)
    config.load_kube_config(context=option)  # Carrega o contexto selecionado

    print(f"Active host is {configuration.Configuration().host}")

    v1 = client.CoreV1Api()  # Instancia a API do Core V1 do Kubernetes

    # Lista todos os namespaces
    namespaces = v1.list_namespace().items
    namespace_names = [ns.metadata.name for ns in namespaces]
    namespace_names.append('All Namespaces')

    # Define o índice padrão como 'astarte' se existir, caso contrário 'All Namespaces'
    default_index = namespace_names.index('astarte') if 'astarte' in namespace_names else len(namespace_names) - 1

    # Cria um menu para selecionar o namespace a ser pesquisado
    selected_namespace, _ = pick(namespace_names, title="Pick the namespace to search in", default_index=default_index)

    if selected_namespace == 'All Namespaces':
        selected_namespace = None

    print(f"Listing pods with their IPs in namespace: {selected_namespace or 'all namespaces'}:")

    # Lista pods no namespace selecionado ou em todos os namespaces
    if selected_namespace:
        ret = v1.list_namespaced_pod(namespace=selected_namespace, watch=False, pretty='true')
    else:
        ret = v1.list_pod_for_all_namespaces(watch=False, pretty='true')

    # Inicializa variáveis para acumular os totais de recursos
    total_cpu_limits = 0
    total_memory_limits = 0
    total_cpu_requests = 0
    total_memory_requests = 0

    # Itera sobre todos os pods retornados
    for item in ret.items:
        container_resources = item.spec.containers[0].resources
        limits = container_resources.limits
        requests = container_resources.requests

        # Soma os limites e requests de CPU e memória, se definidos
        if limits:
            total_cpu_limits += parse_cpu(limits.get('cpu', '0'))
            total_memory_limits += parse_memory(limits.get('memory', '0'))

        if requests:
            total_cpu_requests += parse_cpu(requests.get('cpu', '0'))
            total_memory_requests += parse_memory(requests.get('memory', '0'))

        # Cria strings para exibir os limites e requests
        limits_str = (f"CPU: {limits.get('cpu')}, Memory: {limits.get('memory')}" if limits else "No limits defined")
        requests_str = (f"CPU: {requests.get('cpu')}, Memory: {requests.get('memory')}" if requests else "No requests defined")

        # Imprime informações sobre cada pod
        print(f"Pod: {item.metadata.name}")
        print(f"  Namespace: {item.metadata.namespace}")
        print(f"  Pod IP: {item.status.pod_ip}")
        print(f"  Limits: {limits_str}")
        print(f"  Requests: {requests_str}")
        print("-" * 40)

    # Imprime os totais acumulados de recursos
    print("Total Resources:")
    print(f"  CPU Limits: {total_cpu_limits}m")
    print(f"  Memory Limits: {total_memory_limits}Mi")
    print(f"  CPU Requests: {total_cpu_requests}m")
    print(f"  Memory Requests: {total_memory_requests}Mi")

# Função para converter valores de CPU em milicpus
def parse_cpu(cpu_str):
    if cpu_str.endswith('m'):
        return int(cpu_str[:-1])
    return int(float(cpu_str) * 1000)

# Função para converter valores de memória em Mebibytes (Mi)
def parse_memory(memory_str):
    if memory_str.endswith('Ei'):
        return int(float(memory_str[:-2]) * 1024**6)
    elif memory_str.endswith('Pi'):
        return int(float(memory_str[:-2]) * 1024**5)
    elif memory_str.endswith('Ti'):
        return int(float(memory_str[:-2]) * 1024**4)
    elif memory_str.endswith('Gi'):
        return int(float(memory_str[:-2]) * 1024**3)
    elif memory_str.endswith('Mi'):
        return int(float(memory_str[:-2]) * 1024**2)
    elif memory_str.endswith('Ki'):
        return int(float(memory_str[:-2]) * 1024)
    elif memory_str.endswith('E'):
        return int(float(memory_str[:-1]) * 10**18 / 1024**2)
    elif memory_str.endswith('P'):
        return int(float(memory_str[:-1]) * 10**15 / 1024**2)
    elif memory_str.endswith('T'):
        return int(float(memory_str[:-1]) * 10**12 / 1024**2)
    elif memory_str.endswith('G'):
        return int(float(memory_str[:-1]) * 10**9 / 1024**2)
    elif memory_str.endswith('M'):
        return int(float(memory_str[:-1]) * 10**6 / 1024**2)
    elif memory_str.endswith('k'):
        return int(float(memory_str[:-1]) * 10**3 / 1024**2)
    elif memory_str.endswith('m'):
        return int(float(memory_str[:-1]) / 1024**2)
    return int(memory_str)  # If the values are in bytes, convert to MiB

if __name__ == '__main__':
    main() 
