# Flask Hello World Helm Chart

A Helm chart for deploying the Flask Hello World application on Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `flask-hello`:

```bash
helm install flask-hello ./helm/flask-hello
```

To install with a specific image version:

```bash
helm install flask-hello ./helm/flask-hello --set image.tag=v1.0.0
```

## Uninstalling the Chart

To uninstall the `flask-hello` deployment:

```bash
helm uninstall flask-hello
```

## Configuration

The following table lists the configurable parameters and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `2` |
| `image.repository` | Image repository | `ghcr.io/bvboe/gh-actions-test` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Image tag (overrides appVersion) | `""` |
| `imagePullSecrets` | Image pull secrets | `[]` |
| `nameOverride` | Override chart name | `""` |
| `fullnameOverride` | Override full name | `""` |
| `serviceAccount.create` | Create service account | `true` |
| `serviceAccount.automount` | Automount service account token | `true` |
| `serviceAccount.annotations` | Service account annotations | `{}` |
| `serviceAccount.name` | Service account name | `""` |
| `podAnnotations` | Pod annotations | `{}` |
| `podLabels` | Pod labels | `{}` |
| `podSecurityContext.runAsNonRoot` | Run as non-root user | `true` |
| `podSecurityContext.runAsUser` | User ID | `65532` |
| `podSecurityContext.fsGroup` | Group ID | `65532` |
| `securityContext.allowPrivilegeEscalation` | Allow privilege escalation | `false` |
| `securityContext.capabilities.drop` | Drop capabilities | `["ALL"]` |
| `securityContext.readOnlyRootFilesystem` | Read-only root filesystem | `false` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `service.targetPort` | Container port | `5000` |
| `ingress.enabled` | Enable Ingress | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts` | Ingress hosts | See values.yaml |
| `ingress.tls` | Ingress TLS configuration | `[]` |
| `resources.limits.cpu` | CPU limit | `200m` |
| `resources.limits.memory` | Memory limit | `128Mi` |
| `resources.requests.cpu` | CPU request | `100m` |
| `resources.requests.memory` | Memory request | `64Mi` |
| `autoscaling.enabled` | Enable HorizontalPodAutoscaler | `false` |
| `autoscaling.minReplicas` | Minimum replicas | `2` |
| `autoscaling.maxReplicas` | Maximum replicas | `10` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU % | `80` |
| `autoscaling.targetMemoryUtilizationPercentage` | Target memory % | `80` |
| `nodeSelector` | Node selector | `{}` |
| `tolerations` | Tolerations | `[]` |
| `affinity` | Affinity rules | `{}` |

## Examples

### Basic Installation

```bash
helm install flask-hello ./helm/flask-hello
```

### With Custom Replica Count

```bash
helm install flask-hello ./helm/flask-hello --set replicaCount=3
```

### With Ingress Enabled

```bash
helm install flask-hello ./helm/flask-hello \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=flask-hello.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix
```

### With Autoscaling

```bash
helm install flask-hello ./helm/flask-hello \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10 \
  --set autoscaling.targetCPUUtilizationPercentage=70
```

### With Custom Values File

```bash
helm install flask-hello ./helm/flask-hello -f my-values.yaml
```

## Accessing the Application

### Port Forward (ClusterIP Service)

```bash
kubectl port-forward svc/flask-hello 8080:80
curl http://localhost:8080
```

### LoadBalancer Service

```bash
helm install flask-hello ./helm/flask-hello --set service.type=LoadBalancer
kubectl get svc flask-hello
```

### Ingress

Configure ingress in values.yaml and ensure you have an Ingress controller installed in your cluster.

## Security

The chart follows security best practices:

- Runs as non-root user (UID 65532)
- Drops all capabilities
- Disables privilege escalation
- Uses minimal Chainguard base images
- Configurable resource limits
- Liveness and readiness probes
