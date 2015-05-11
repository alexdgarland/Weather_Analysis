DROP TYPE IF EXISTS file_state CASCADE;
CREATE TYPE file_state AS ENUM ('registered', 'downloaded', 'staging started', 'staging complete', 'loaded');