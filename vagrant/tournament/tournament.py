#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random

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
    cursor.execute(r'''INSERT INTO players (name) 
                       VALUES(%s)''', (name,))
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
    cursor.execute('''SELECT * FROM ordered_players''')
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser, is_draw = False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      is_draw: if the game is draw, default value is False
    """
    conn = connect()
    cursor = conn.cursor()
    next_matches_id = getMaxMatchId() + 1
    next_round = getMaxRound(winner) + 1
    if is_draw:
        cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                       VALUES(%d, FALSE, %d, %d)'''%(winner, next_round, next_matches_id))
    
        cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                       VALUES(%d, FALSE, %d, %d)'''%(loser, next_round, next_matches_id))
    else:
        cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                       VALUES(%d, TRUE, %d, %d)'''%(winner, next_round, next_matches_id))
    
        cursor.execute('''INSERT INTO matches(player_id, is_winner, round, match_id)
                       VALUES(%d, FALSE, %d, %d)'''%(loser, next_round, next_matches_id))
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, name , wins FROM ordered_players''')
    ordered_players = cursor.fetchall()
    #Handle situation of odd number of players
    if len(ordered_players)%2 == 1:
        print 'odd number'
        last_ndex = len(ordered_players)-1
        random_index = random.randint(0,lastIndex)
        while (checkHavedSkipped(random_index) == True):
            random_index = random.randint(0,lastIndex)
        ordered_players.pop(random_index)
    paris_of_players = []
    i = 0
    while (i < len(ordered_players)/2):
        k = 2
        id1 = ordered_players[2*i][0]
        id2 = ordered_players[2*i+1][0]
        while ((i+k) < len(ordered_players) and checkHaveMatched(id1, id2)):
            exchange(ordered_players, i+1, i+k)
            id2 = ordered_players[2*i+1][0]
            k = k+1
        name1 = ordered_players[2*i][1]
        name2 = ordered_players[2*i+1][1]
        pair = (id1, name1, id2, name2)
        paris_of_players.append(pair)
        i = i + 1
    return paris_of_players


def getMaxRound(player_id):
    """Retuen the max round of the tournament.

    Reruens:
      The max round of the current state.
    Args:
        the player_id of who will play the game
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT max(round) FROM matches WHERE player_id = %s"
                   %player_id)
    results = cursor.fetchall()
    conn.close()
    max_round = results[0][0]
    if max_round == None:
        max_round = 0
    return max_round

    
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
    
def exchange(list, index1, index2):
    """Exchange the position of elements with index: index1 and index2

    Args:
        list: the list to be exchange elements
        index1, index2: the indexs of the elements to be exchange
        """
    temp = list[index1]
    list[index1] = list[index2]
    list[index2] = temp 

def checkHaveMatched(player_id1, player_id2):
    """Check if two players have matched

    Args:
        player_id1, player_id2: the two players to be checked

    Returns:
        if two players have matched
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(r'''SELECT * FROM V_matches
                       WHERE (winner_id = %d and loser_id = %d) or 
                             (winner_id = %d and loser_id = %d)'''
                             %(player_id1, player_id2, player_id2, player_id1))
    result = cursor.fetchall()
    conn.close()
    if len(result) == 0:
        return False
    else:
        return True

def checkHavedSkipped(player_id):
    """Check if the player have skipped round once
        if haven't skipped round once, insert a row in database
    Args:
        player_id: the  player to be checked

    Returns:
        if two player have skipped round once
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(r'''SELECT player_id, count(*) as num FROM matches
                        GROUP BY match_id HAVING num = 1''')
    results = cursor.fetchall()
    conn.close()
    ids = [row[0] for row in results]
    if player_id in ids:
        return True
    else:
        conn = connect()
        cursor = conn.cursor()
        next_matches_id = getMaxMatchId() + 1
        next_round = getMaxRound(winner) + 1
        cursor.execute(r'''INSERT INTO matches(player_id, match_id, is_winner, round)
                           VALUES(%d, %d, TRUE, %d)'''%(player_id, next_matches_id, next_round))
        return False