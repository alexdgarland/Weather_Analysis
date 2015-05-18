DROP TYPE IF EXISTS staging.file_state CASCADE;
CREATE TYPE staging.file_state AS ENUM ('registered', 'downloaded', 'staging started', 'staging complete', 'loaded');