A simulation program for the World Cup 2018 in Russia. Developed as a personal project in Python 3.6

The program is based on a simple model for a team, and how match scores are
generated.
The model consists of two scores, defense and attack, generated from results of qualification and recent friendly matches, 
and a routine that generates the score of each team at each match randomly. A team with a higher attack score however has a
higher chance to score, while a team that has a higher defense score is harder to score against.
The simulation is run N number of times, and the frequencies of qualification to different stages are computed, in order to generate final
percentages.

This is only the first version of the program, and future versions should have a better model (scores generated from individual matches, 
rather than bulk results, an improved routine for generating defense and attack scores, and another for WC match scores, etc),
and additional options, such as fixing the results of some matches and predicting the rest of the WC, so the program can remain useful 
during the competition.
