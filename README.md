# Demo using Pulumi operator

Deploy the [pulumi-k8s-nginx-demo](https://github.com/ssorato/pulumi-k8s-nginx-demo) using the [Pulumi Kubernetes Operator](https://www.pulumi.com/blog/pulumi-kubernetes-operator/)

In this demo I'm using an [Azure Blog storage](https://www.pulumi.com/docs/intro/concepts/state/#azure-blob-storage) backend

## Deploy the operator

Installing the Operator with kubectl on _default_ namespace

```bash
$ TEMPLATE=deploy/deploy-operator-py
$ mkdir deploy-operator
$ cd deploy-operator
$ pulumi new https://github.com/pulumi/pulumi-kubernetes-operator/$TEMPLATE
```
check the operator logs

```bash
$ kubectl logs -l name=pulumi-kubernetes-operator -f
```

## Operator demo

```bash
$ pulumi stack init dev
$ pulumi config set --secret pulumiAzureStorageKey $AZURE_STORAGE_KEY
$ pulumi config set --secret pulumiAzureStorageAccount $AZURE_STORAGE_ACCOUNT
$ pulumi config set stackCommit  a95e8c0ba056cd997f291f72b46d0d86e8877b66
$ pulumi config set --secret pulumiStackPassphrase $PULUMI_CONFIG_PASSPHRASE
$ pulumi up
```

monitor the operator log

```bash
$ kubectl logs -l name=pulumi-kubernetes-operator -f
```

and the stack log

```bash
$ kubectl get stacks -o yaml -w
```

get the `nginx-service` service external IP and open the web page

```bash
$ NGINX_SERVICE_EXTERNAL_IP=`kubectl get svc nginx-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
$ curl http://$NGINX_SERVICE_EXTERNAL_IP

<!DOCTYPE html>
<html>
<head>
    <title>Pulumi Kubernetes Demo</title>
</head>
<body>
    <h1>Hello from Pulumi Kubernetes!</h1>
</body>
</html>
```

now update the repo commit

```bash
$ pulumi config set stackCommit 8e2cf06137f0008dd18dc254eee1f327ac3e2496
$ pulumi up
```

and monitor the stack log 

```bash
$ kubectl get stacks -o yaml -w
```

check again the web page again

```bash
$ curl http://$NGINX_SERVICE_EXTERNAL_IP

<!DOCTYPE html>
<html>
<head>
    <title>Pulumi Kubernetes Demo</title>
</head>
<body>
    <h1>Hello World, from Pulumi Kubernetes!</h1>
</body>
</html>
```

## Tip

If you are using a GitHub private repository add the account name and autentication token to the stack

```yaml
"projectRepo": "https://<account>@github.com/<repo>",
"gitAuth": {
  "accessToken": {
    "type": "Secret",
    "secret": {
      "name": <token>,
      "key": "account_token"
    }
  }
}
```

in this repository remove the commented lines and set the GitHub token

```bash
$ pulumi config set --secret pulumiGitHubAccountToken $MY_GITHUB_TOKEN
```
