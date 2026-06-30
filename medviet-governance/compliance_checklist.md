# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [ ] Tất cả patient data lưu trên servers đặt tại Việt Nam.
- [ ] Backup cũng phải ở trong lãnh thổ Việt Nam.
- [ ] Log mọi hoạt động transfer data ra ngoài Việt Nam.

## B. Explicit Consent
- [ ] Thu thập consent trước khi dùng patient data cho AI training.
- [ ] Có cơ chế để người dùng rút consent và yêu cầu xóa dữ liệu.
- [ ] Lưu consent record với timestamp, purpose, data scope, consent version.

## C. Breach Notification — 72h
- [ ] Có incident response plan cho data breach.
- [ ] Có alert tự động khi phát hiện truy cập bất thường hoặc PII exposure.
- [ ] Có quy trình báo cáo đến cơ quan có thẩm quyền trong vòng 72 giờ.

## D. DPO Appointment
- [ ] Đã bổ nhiệm Data Protection Officer.
- [ ] DPO contact: dpo@medviet.example.vn.
- [ ] DPO chịu trách nhiệm review DPIA, consent flow, breach response và audit evidence.

## E. Technical Controls Mapping

| NĐ13 Requirement | Technical Control | Status | Owner |
|---|---|---:|---|
| Data minimization | Presidio-compatible PII detection + anonymization pipeline trước training ingestion | Done | AI Team |
| Purpose limitation | Tách raw data, anonymized training data và aggregated metrics theo endpoint/API resource | In Progress | AI Team |
| Access control | Casbin RBAC trong FastAPI + OPA ABAC/data export policy | Done | Platform Team |
| Least privilege | Roles admin, ml_engineer, data_analyst, intern; raw PII chỉ admin đọc được | Done | Platform Team |
| Encryption at rest | `SimpleVault` envelope encryption demo bằng AES-256-GCM; production map sang KMS/HSM | In Progress | Infra Team |
| Encryption in transit | Bắt buộc HTTPS/TLS 1.3 ở API gateway/reverse proxy khi deploy | Todo | Infra Team |
| Audit logging | Log user, role, resource, action, decision, timestamp cho mọi data access API | Todo | Platform Team |
| Breach detection | Prometheus/Grafana alerts cho 403 spikes, failed auth, abnormal PII access | Todo | Security Team |
| Secret protection | git-secrets hook + Bandit + pip-audit + TruffleHog reports | In Progress | Security Team |
| Data subject request | Delete cascade playbook: raw store, processed store, backups, feature store, model registry | Todo | Data Governance Team |
| Data localization | OPA rule deny restricted data export nếu `destination_country != VN` | Done | Platform Team |
| DPO oversight | DPO reviews checklist, scan reports, access policy và incident playbook mỗi release | Todo | DPO |

## F. Remaining Implementation Notes

### Audit logging
Implement FastAPI middleware that writes JSON logs with `request_id`, `username`, `role`, `resource`, `action`, `allowed`, `status_code`, and timestamp. Store logs in a write-once location or centralized SIEM.

### Breach detection
Create Prometheus counters for failed login attempts, denied RBAC requests, and raw PII endpoint access. Configure Grafana alerts for abnormal spikes and trigger incident response.

### TLS / deployment
Terminate TLS 1.3 at Nginx, Traefik, or cloud load balancer. Reject plain HTTP in production and enable HSTS for public endpoints.

### Data subject request
Maintain an index from real user identity to `patient_id`. A deletion request should remove raw records, processed records, feature rows, cached artifacts, and retraining queues.
