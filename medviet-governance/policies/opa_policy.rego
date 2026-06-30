package medviet.data_access

import future.keywords.if
import future.keywords.in

# Default: deny all.
default allow := false
default deny := false

# Restricted data cannot be exported outside Viet Nam servers.
deny if {
    input.data_classification == "restricted"
    input.destination_country != "VN"
}

# Admin can do everything except explicit deny rules above.
allow if {
    not deny
    input.user.role == "admin"
}

# ML Engineer can read training data and read/write model artifacts.
allow if {
    not deny
    input.user.role == "ml_engineer"
    input.resource == "training_data"
    input.action == "read"
}

allow if {
    not deny
    input.user.role == "ml_engineer"
    input.resource == "model_artifacts"
    input.action in {"read", "write"}
}

allow if {
    not deny
    input.user.role == "ml_engineer"
    input.resource == "aggregated_metrics"
    input.action == "read"
}

# ML Engineer must not delete production data.
deny if {
    input.user.role == "ml_engineer"
    input.resource == "production_data"
    input.action == "delete"
}

# Data Analyst can read aggregate metrics and write reports only.
allow if {
    not deny
    input.user.role == "data_analyst"
    input.resource == "aggregated_metrics"
    input.action == "read"
}

allow if {
    not deny
    input.user.role == "data_analyst"
    input.resource == "reports"
    input.action == "write"
}

# Intern can only access sandbox data.
allow if {
    not deny
    input.user.role == "intern"
    input.resource == "sandbox_data"
    input.action in {"read", "write"}
}
