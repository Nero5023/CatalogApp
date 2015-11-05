-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players ( id SERIAL PRIMARY KEY,
					   name TEXT,
					   win_matches INTEGER,
					   total_matches INTEGER );

CREATE TABLE matches ( 
	player_id SERIAL REFERENCES players(id),
					   match_id SERIAL,
					   is_winner BOOLEAN,
					   round INTEGER );

CREATE VIEW V_matches 
AS SELECT a.match_id, a.player_id AS winner_id, b.player_id AS loser_id, a.round 
FROM matches as a, matches as b
WHERE a.round = b.round and a.match_id = b.match_id 
	  and a.is_winner = TRUE and b.is_winner = FALSE;

CREATE VIEW ordered_players 
AS SELECT * FROM players ORDER BY win_matches DESC;