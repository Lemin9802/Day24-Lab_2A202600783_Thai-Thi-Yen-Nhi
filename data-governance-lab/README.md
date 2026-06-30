# Data Governance Lab Notebook and Agent Governance Materials

This folder contains the instructor-provided interactive lab notebook and Agent Governance reference materials.

The completed implementation for submission is located in:

    ../medviet-governance/

This folder is kept in the repository for traceability because the updated lab structure includes notebook-based guidance and an Agent Governance policy reference.

## Included Files

| File / Folder | Purpose |
|---|---|
| data_governance_lab.ipynb | Instructor-provided interactive notebook for the lab workflow |
| pii_utils.py | Helper utilities for Vietnamese PII detection examples |
| policies/medviet-data-policy.yaml | Agent governance policy reference |
| requirements.txt | Notebook and Agent Governance dependency list |

## Agent Governance Policy Summary

The included policy demonstrates governance rules for AI agents that access MedViet data.

Policy behavior:

| Rule | Decision |
|---|---|
| Read anonymized data | Allowed |
| Read aggregated metrics | Allowed |
| Access raw PII | Denied |
| Export data outside Vietnam | Denied |
| Delete, drop, or truncate data | Denied |

The production-ready implementation of data access governance is represented in the main project by:

    ../medviet-governance/policies/opa_policy.rego
    ../medviet-governance/src/access/rbac.py
    ../medviet-governance/src/api/main.py

## Scope Note

The notebook is preserved as learning material and reference evidence. The actual runnable lab implementation is in the `medviet-governance/` folder.
