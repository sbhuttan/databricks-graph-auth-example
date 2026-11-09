# Microsoft Graph authentication from Databricks

A Databricks Python notebook that uses MSAL client-credentials authentication
and retrieves the client secret from a Databricks-backed secret scope.
All tenant and application IDs are placeholders. No credentials are included.

## Prerequisites

- A Databricks workspace and compute that can install and run MSAL.
- A Microsoft Entra app registration with a valid client secret.
- The Microsoft Graph **Application permissions** required for your use case,
  with administrator consent. Delegated permissions do not apply to this flow.
- An installed Databricks CLI for the one-time setup below.

## 1. Store the secret

Run these commands in a local terminal, not in a notebook cell. Replace the
workspace placeholder with your Databricks workspace hostname.

```powershell
databricks auth login --host https://<YOUR-DATABRICKS-WORKSPACE>
databricks secrets create-scope graph-api-secrets
databricks secrets put-secret graph-api-secrets client-secret
```

Skip `create-scope` if the scope already exists. Enter the client secret
**value**, not its Secret ID, at the interactive prompt. Do not put the value
in a command, notebook, source file, or Git repository.

The scope creator has MANAGE permission by default. If a different user or
service principal runs the notebook or job, grant that identity READ access.
Permissions apply to the entire scope, so restrict membership accordingly.

These commands are for a **Databricks-backed** scope. For an Azure Key
Vault-backed scope, store and rotate the secret in Azure Key Vault instead.

## 2. Import and configure the notebook

1. Download [graph_auth_notebook.py](./graph_auth_notebook.py).
2. In your Databricks workspace, import the file as a Python notebook.
3. Replace `<YOUR-TENANT-ID>` and `<YOUR-APPLICATION-CLIENT-ID>`.
4. Update `SECRET_SCOPE` and `SECRET_KEY` if you used different names.
5. Run the cells in order. The first code cell installs MSAL.

On success, the notebook prints only:

```text
Microsoft Graph authentication successful.
```

The `access_token` variable is then available for subsequent Microsoft Graph
requests. This is app-only authentication; use endpoints that support application
permissions, not `/me`. Token acquisition alone does not prove that the app has
permission to call a particular endpoint.

## Troubleshooting and security

- **AADSTS70011 / invalid_scope**: use `https://graph.microsoft.com/.default`.
- **Secret lookup fails**: verify the scope, key, and execution identity's READ access.
- **Invalid or expired client secret**: update the secret value in the scope.
  Running processes may need to retrieve the updated value again.
- **Graph returns 403**: check the endpoint's Application permissions and admin consent.
- Never print the secret, access token, or full authentication result.
- Secret redaction is not a substitute for access control.
- Rotate any secret previously exposed in code or notebook output.

## References

- [Databricks workspace secret scopes](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/workspace-secret-scopes)
- [Microsoft identity platform client-credentials flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow)
