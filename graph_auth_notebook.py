# Databricks notebook source
# MAGIC %md
# MAGIC # Microsoft Graph authentication with Databricks secret scopes
# MAGIC Replace the tenant and client ID placeholders below. Store the client
# MAGIC secret in a Databricks-backed secret scope before running this notebook.
# MAGIC Never print the client secret, access token, or full authentication result.

# COMMAND ----------

# MAGIC %pip install msal

# COMMAND ----------

import msal

TENANT_ID = "<YOUR-TENANT-ID>"
CLIENT_ID = "<YOUR-APPLICATION-CLIENT-ID>"
SECRET_SCOPE = "graph-api-secrets"
SECRET_KEY = "client-secret"

if TENANT_ID == "<YOUR-TENANT-ID>" or CLIENT_ID == "<YOUR-APPLICATION-CLIENT-ID>":
    raise ValueError("Replace TENANT_ID and CLIENT_ID with your application details.")

client_secret = dbutils.secrets.get(
    scope=SECRET_SCOPE,
    key=SECRET_KEY,
)

app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=client_secret,
)

result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)

if "access_token" not in result:
    raise RuntimeError(
        f"Authentication failed: {result.get('error')} - "
        f"{result.get('error_description')}"
    )

access_token = result["access_token"]
print("Microsoft Graph authentication successful.")
