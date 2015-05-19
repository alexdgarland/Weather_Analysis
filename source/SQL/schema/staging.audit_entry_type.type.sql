
DROP TYPE IF EXISTS staging.audit_entry_type CASCADE;

CREATE TYPE staging.audit_entry_type AS ENUM ('created', 'updated');
