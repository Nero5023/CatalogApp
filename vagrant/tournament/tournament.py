#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) as num FROM players")
    results = cursor.fetchall()
    conn.close()
    return results[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(r'''INSERT INTO players(name, win_matches, total_matches) 
                       VALUES(%s,0,0)''', (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(r'''SELECT * FROM ordered_players''')
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''UPDATE players
                      SET win_matches = win_matches + 1,
                          total_matches = total_matches + 1
                      WHERE id = %d'''%winner)
    conn.commit()
    cursor.execute('''UPDATE players
                      SET total_matches = total_matches + 1
                      WHERE id = %d'''%loser)
    conn.commit()
    next_matches_id = getMaxMatchId() + 1
    cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                      VALUES(%d, TRUE, 1, %d)'''%(winner, next_matches_id))
    
    cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                      VALUES(%d, FALSE, 1, %d)'''%(loser, next_matches_id))
    conn.commit()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # max_round = getMaxRound()
    # current_round = max_round+1
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, name , win_matches FROM ordered_players''')
    ordered_players = cursor.fetchall()
    paris_of_players = []
    for i in range(len(ordered_players)/2):
        id1 = ordered_players[2*i][0]
        name1 = ordered_players[2*i][1]
        id2 = ordered_players[2*i+1][0]
        name2 = ordered_players[2*i+1][1]
        pair = (id1, name1, id2, name2)
        paris_of_players.append(pair)
    return paris_of_players


def getMaxRound():
    """Retuen the max round of the tournament.

    Reruens:
      The max round of the current state.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT max(round) FROM matches")
    results = cursor.fetchall()
    conn.close()
    return results[0][0]


    
def getMaxMatchId():
    """Retuen the max match_id of the tournament.

    Reruens:
      The max match_id of the current state.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT max(match_id) FROM matches")
    results = cursor.fetchall()
    conn.close()
    max_id = results[0][0]
    if max_id == None:
        max_id = 0
    return max_id
    

