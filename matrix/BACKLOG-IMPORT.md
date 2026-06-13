# Backlog CSV import mapping

`build_backlog.py` writes one `<domain>-backlog.csv` per domain (GAP + PARTIAL use
cases, P0s first). One neutral schema imports into both trackers.

| CSV column | Jira import field | Azure DevOps import field |
|---|---|---|
| Summary | Summary | Title |
| Work Item Type | Issue Type (`Task`) | Work Item Type (`Task`) |
| Description | Description | Description |
| Priority | Priority (`Highest`/`High`/`Medium`/`Low`) | Priority (map `Highest`→1, `High`→2, `Medium`→3, `Low`→4) |
| Labels | Labels (space-separated) | Tags (set delimiter to space, or replace spaces with `;`) |
| UC-ID | Labels / custom field | Tags / custom field |
| Domain | Labels / Component | Area / Tags |
| Regulatory-Driver | Description / custom field | Description / custom field |
| State | Labels / custom field | Tags / custom field |

**Jira:** Settings → System → External System Import → CSV. Map columns as above.
**Azure DevOps:** Boards → Work items → Import Work Items (CSV). Priority must be numeric;
apply the mapping above during import or with a quick find-replace.
