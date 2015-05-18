
DROP TYPE IF EXISTS staging.load_state CASCADE;
CREATE TYPE staging.load_state AS ENUM ('in progress', 'completed okay', 'failed', 'automatically closed');
