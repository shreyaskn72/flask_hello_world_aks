Great 👍
I’ll guide you **step by step**, assuming:

* ✅ AKS cluster already exists (created via Azure Portal)
* ✅ Docker image is already pushed to **ACR**
* ✅ You are using **Azure CLI + kubectl** on Windows
* ✅ You are new to AKS (so explanations are included)

---

# 🧱 Overall flow (AKS deployment)

1. Connect your local machine to AKS
2. Allow AKS to pull images from ACR
3. Create Kubernetes Deployment
4. Create Kubernetes Service
5. Access the application

---

## 🔹 Step 1: Get AKS credentials (VERY IMPORTANT)

First, list your AKS clusters:

```powershell
az aks list --output table
```

Note:

* **AKS name**
* **Resource Group**

Now connect `kubectl` to your cluster:

```powershell
az aks get-credentials `
  --resource-group <AKS_RESOURCE_GROUP> `
  --name <AKS_CLUSTER_NAME>
```

Example:

```powershell
az aks get-credentials --resource-group my-rg --name my-aks
```

✅ This updates your `kubectl` config

Verify connection:

```powershell
kubectl get nodes
```

You should see nodes in `Ready` state.

---

## 🔹 Step 2: Attach ACR to AKS (only once)

This allows AKS to pull images from your private ACR **without secrets**.

```powershell
az aks update `
  --resource-group <AKS_RESOURCE_GROUP> `
  --name <AKS_CLUSTER_NAME> `
  --attach-acr <ACR_NAME>
```

Example:

```powershell
az aks update --resource-group my-rg --name my-aks --attach-acr myacrregistry
```

✅ Do this **once per cluster**

---

## 🔹 Step 3: Create Deployment YAML

Create a file called **`deployment.yaml`**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-hello
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-hello
  template:
    metadata:
      labels:
        app: flask-hello
    spec:
      containers:
      - name: flask-hello
        image: myacrregistry.azurecr.io/flask-hello:v1
        ports:
        - containerPort: 5000
```

🔁 Replace:

* `myacrregistry` → your ACR name
* `v1` → image tag (if different)

---

## 🔹 Step 4: Apply Deployment

```powershell
kubectl apply -f deployment.yaml
```

Check pods:

```powershell
kubectl get pods
```

You should see something like:

```
flask-hello-xxxxx   Running
flask-hello-yyyyy   Running
```

---

## 🔹 Step 5: Create Service (LoadBalancer)

Create **`service.yaml`**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-hello-service
spec:
  type: LoadBalancer
  selector:
    app: flask-hello
  ports:
  - port: 80
    targetPort: 5000
```

Apply it:

```powershell
kubectl apply -f service.yaml
```

---

## 🔹 Step 6: Get External IP 🌍

```powershell
kubectl get svc flask-hello-service
```

Initially you’ll see:

```
EXTERNAL-IP   <pending>
```

Wait 1–3 minutes, then run again:

```
EXTERNAL-IP   20.xxx.xxx.xxx
```

---

## 🔹 Step 7: Access your API 🎉

Open browser:

```
http://<EXTERNAL-IP>/
```

Response:

```json
{
  "message": "Hello, World!"
}
```

---

# ✅ What just happened (simple explanation)

* **Deployment** → Runs your container (Gunicorn + Flask)
* **Pods** → Where your app actually runs
* **Service (LoadBalancer)** → Exposes app to the internet
* **ACR attach** → Secure image pulling without secrets

---

## 🧠 Common troubleshooting

### Pods stuck in `ImagePullBackOff`

```powershell
kubectl describe pod <pod-name>
```

👉 Usually means:

* ACR not attached
* Wrong image name/tag

---

In case if you update the code refer below:
[code update changes here](update_to_aks_upon_code_change.md)

## 🔜 Recommended next steps (AKS best practices)

When you’re ready, I can help you add:

* ✅ Liveness & Readiness probes
* ✅ Resource limits (CPU / memory)
* ✅ Horizontal Pod Autoscaler
* ✅ Ingress (NGINX) instead of LoadBalancer
* ✅ CI/CD from GitHub Actions or Azure DevOps

Just tell me what you want next 🚀
