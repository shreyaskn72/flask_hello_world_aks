**clear, beginner-friendly, step-by-step commands** using **Azure CLI** to push your existing Docker image to **Azure Container Registry (ACR)**.

Lets assume:

* ✅ Azure CLI already installed
* ✅ You already ran `az login`
* ✅ ACR already exists
* ✅ You are on **Windows Terminal**

---

# 🧱 High-level flow (what we’ll do)

1. Get ACR name
2. Login to ACR
3. Tag your local Docker image
4. Push image to ACR
5. Verify image in ACR

---

## 🔹 Step 1: Check your Azure subscription (optional but good)

```powershell
az account show
```

If you have multiple subscriptions:

```powershell
az account list --output table
az account set --subscription "<SUBSCRIPTION_ID>"
```

---

## 🔹 Step 2: Find your Azure Container Registry name

List all ACRs in your subscription:

```powershell
az acr list --output table
```

You’ll see something like:

```
NAME            RESOURCE GROUP    LOCATION
myacrregistry   my-rg             eastus
```

👉 **Note the ACR name** (example: `myacrregistry`)

---

## 🔹 Step 3: Login to Azure Container Registry

```powershell
az acr login --name myacrregistry
```

If successful, you’ll see:

```
Login Succeeded
```

✔ This also logs Docker into ACR automatically

---

## 🔹 Step 4: Verify your local Docker image exists

```powershell
docker images
```

You should see:

```
flask-hello   latest   <IMAGE_ID>
```

---

## 🔹 Step 5: Tag your image for ACR

ACR images must follow this format:

```
<acr-name>.azurecr.io/<image-name>:<tag>
```

### Example command:

```powershell
docker tag flask-hello:latest myacrregistry.azurecr.io/flask-hello:v1
```

✔ This does NOT create a new image
✔ It just adds a tag pointing to the same image

---

## 🔹 Step 6: Push image to ACR 🚀

```powershell
docker push myacrregistry.azurecr.io/flask-hello:v1
```

You’ll see layers uploading, then:

```
v1: digest: sha256:xxxx size: xxxx
```

✅ Image pushed successfully

---

## 🔹 Step 7: Verify image in ACR

List repositories:

```powershell
az acr repository list --name myacrregistry --output table
```

You should see:

```
flask-hello
```

List tags:

```powershell
az acr repository show-tags \
  --name myacrregistry \
  --repository flask-hello \
  --output table
```

Output:

```
v1
```

---

# ✅ Done! 🎉

Your image is now stored in **Azure Container Registry**:

```
myacrregistry.azurecr.io/flask-hello:v1
```

---

## 🔜 Next logical step (AKS deployment)

* Create AKS cluster in azure. 

Since you already have:

* Existing **AKS cluster**
* Image in **ACR**

Next steps are:

1. Attach ACR to AKS (if not already)
2. Create Kubernetes Deployment
3. Create Service (LoadBalancer)


**“Deploy this image to my existing AKS cluster”**
refer deploy_to_aks.md
