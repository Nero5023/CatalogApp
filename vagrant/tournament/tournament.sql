-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players ( id SERIAL PRIMARY KEY,
					   name TEXT);

CREATE TABLE matches ( player_id SERIAL REFERENCES players(id),
					   match_id SERIAL,
					   is_winner BOOLEAN,
					   round INTEGER );

CREATE VIEW V_matches 
AS SELECT a.match_id, a.player_id AS winner_id, b.player_id AS loser_id, a.round 
FROM matches AS a, matches AS b
WHERE  a.match_id = b.match_id 
	  and a.is_winner = TRUE and b.is_winner = FALSE;

CREATE VIEW player_wins
AS SELECT players.id, count(winners.player_id) AS wins
FROM players LEFT JOIN  
	 (SELECT player_id FROM matches WHERE matches.is_winner = TRUE) AS winners
ON players.id = winners.player_id 
GROUP BY players.id;

CREATE VIEW players_total_matches
AS SELECT players.id, players.name, count(matches.player_id) AS matches
FROM players LEFT JOIN matches ON players.id = matches.player_id
GROUP BY players.id;

CREATE VIEW players_wins_matches
AS SELECT players_total_matches.id, players_total_matches.name, 
		  player_wins.wins, players_total_matches.matches
FROM players_total_matches LEFT JOIN player_wins ON players_total_matches.id = player_wins.id
ORDER BY player_wins.wins DESC;

CREATE VIEW pairs
AS SELECT a.match_id, a.player_id AS id1, b.player_id AS id2 
FROM matches AS a, matches AS b
WHERE a.match_id = b.match_id and a.player_id != b.player_id;

CREATE VIEW players_OMW
AS SELECT pairs.id1 AS id,  SUM(player_wins.wins) AS OMW
FROM pairs JOIN player_wins ON pairs.id2 = player_wins.id
GROUP BY pairs.id1;

CREATE VIEW ordered_players
AS SELECT players_wins_matches.id, players_wins_matches.name, 
		  players_wins_matches.wins, players_wins_matches.matches
FROM players_wins_matches LEFT JOIN players_OMW ON players_wins_matches.id = players_OMW.id
ORDER BY players_wins_matches.wins DESC, players_OMW.OMW DESC;

