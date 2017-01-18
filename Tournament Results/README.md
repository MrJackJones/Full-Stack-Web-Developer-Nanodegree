Tournament Results

Built a PostgreSQL relational database scheme to store the results of a game tournament. Also provided a number of queries to efficiently report the results of the tournament and determine the winner.

Skills: SQL, PostgreSQL, relational databases

Setup Project:

1. Launch the Vagrant VM

2. Copy and unzip tournament.zip in /vagrant directory

3. cd /vagrant/tournament

4. Create tournament database using following commands

    psql
    \i tournament.sql

5. exit database - \q

6. Test the application using following command - python tournament_test.py


Result:

1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
