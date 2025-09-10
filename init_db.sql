-- Initialize the PostgreSQL database.
--
-- Requires the `avandra` database to be created in advance:
--
-- ```
-- $ sudo psql createdb avandra
-- psql -u postgres -c 'CREATE DATABASE avandra;'
-- ```

-- The Discord bot will use the `avandra` user to read and write data.
CREATE USER avandra WITH PASSWORD 'changeme';
GRANT pg_read_all_data TO avandra;
GRANT pg_write_all_data TO avandra;

CREATE TABLE IF NOT EXISTS players (
  player_key VARCHAR(255) NOT NULL CHECK (player_key <> ''),
  PRIMARY KEY (player_key)
);

CREATE TABLE IF NOT EXISTS player_keyval (
  player_key VARCHAR(255) NOT NULL,
  key VARCHAR(255) NOT NULL CHECK (key <> ''),
  value JSONB NOT NULL,
  last_modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (player_key, key),
  FOREIGN KEY (player_key) REFERENCES players(player_key)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Create a function to update the player_keyval.last_modified timestamp
CREATE OR REPLACE FUNCTION update_player_keyval_last_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create a trigger to automatically update player_keyval.last_modified.
CREATE OR REPLACE TRIGGER update_player_keyval_last_modified_trigger
    BEFORE UPDATE ON player_keyval
    FOR EACH ROW
    EXECUTE FUNCTION update_player_keyval_last_modified();
