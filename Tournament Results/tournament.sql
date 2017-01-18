-- Drop old versions for reset
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- Add, delete, and record players in tournament
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL);

--Track matches in tournament
CREATE TABLE matches (
	match SERIAL PRIMARY KEY,
	player INTEGER NOT NULL,
	against INTEGER NOT NULL,
	final INTEGER NOT NULL,
	FOREIGN KEY (player) REFERENCES players (id),
	FOREIGN KEY (against) REFERENCES players (id));

-- View for COUNTER that specifies number of players
CREATE VIEW counter AS
	SELECT players.id, COUNT(matches.against) AS ct
	FROM players
	LEFT JOIN matches
	ON players.id = matches.player
	GROUP BY players.id;

-- View for WINS that specifies number of player wins
CREATE VIEW wins AS
	SELECT players.id, COUNT(matches.against) AS num
	FROM players
	LEFT JOIN (SELECT * FROM matches WHERE final > 0 ) as matches
	ON players.id = matches.player
	GROUP BY players.id;

-- View for STANDINGS that provides individual ranking
CREATE VIEW standings AS
	SELECT players.id, players.name, wins.num AS wins, counter.ct AS matches
	FROM players,counter,wins
	WHERE players.id = wins.id and wins.id = counter.id
	ORDER BY wins.num DESC;