
DROP TYPE IF EXISTS load_state CASCADE;
CREATE TYPE load_state AS ENUM ('initialised', 'in progress', 'completed okay', 'failed', 'automatically closed');
