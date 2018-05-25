"""
A simulation program for the World Cup
2018 in Russia.
The program is based on a simple model
for a team, and how match scores are
generated.
The model consists of two scores,
defense and attack, generated from
results of qualification and recent
friendly matches, and a routine that
generates the score of each team at
each match randomly. A team with a
higher attack score however has a
higher chance to score, while a team
that has a higher defense score is
harder to score against.
The simulation is run N number of
times, and the frequencies of
qualification to different stages are
computed, in order to generate final
percentages.

This is only the first version of the
program, and future versions should
have a better model (scores generated
from individual matches, rather than
bulk results, an improved routine for
generating defense and attack scores,
and another for WC match scores, etc),
and additional options, such as fixing
the results of some matches and
predicting the rest of the WC, so the
program can remain useful during the
competition.

"""

from random import randint

class Team:
    """
    Encapsulates all attributes of a team,
    as well as the methods applied to it.
    """
    def __init__(self,name,group,defense,attack):
        """
        Initializes a Team instance, by setting
        up the attributes.
        Attributes:
        - name: name of the team, e.g. Morocco
        - group: World Cup group in which it
        was drawn
        - defense: defense score, computed from
        recent results
        - attack: attack score; computed from
        recent results
        - points: points scored at the group
        stage matches
        - goals_for: goals scored by the team
        at the group stage
        - goals_against: goals scored against
        the team at the group stage
        - first: number of times the team came
        first on its group during the simulations
        - second: number of times the team came
        second on its group during the simulations
        - eighth: number of times the team
        qualified from its group during the
        simulations
        - quarter: number of times the team
        qualified to the quarter final during
        the simulations
        - semi: number of times the team
        qualified to the semi-final during the
        simulations
        - third: number of times the team came
        third in the tournament
        - final: number of times the team
        qualified to the final match
        - winner: number of times the team won
        the World Cup
        """
        self.name = name
        self.group = group
        self.defense = defense
        self.attack = attack
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0
        self.first = 0
        self.second = 0
        self.eighth = 0
        self.quarter = 0
        self.semi = 0
        self.third = 0
        self.final = 0
        self.winner = 0

    def __repr__(self):
        return team.name.rjust(15,' ')
    
    def __str__(self):
        return team.name.rjust(15,' ')


    def play(self,opponent,knockout):
        """
        Simulates a single game between two teams.

        Input:
        - opponent: opposing team, an instance
        of the Team class
        - knockout: a boolean signifying whether
        the match is in the group stage (False)
        or the knockout stage (True)

        Returns None (implicitly) if it's a
        group stage match, after updating the
        points and goal attributes for both
        teams, and an integer (0 or 1) if it's
        a knockout match. In this case, 0 is
        returned if the calling Team instance
        (self) is the winner, and 1 otherwise.
        If the two teams draw at this stage,
        the match is decided by pure chance,
        50/50.
        """
        team_score = int(randint(0,self.attack)/(1+randint(0,opponent.defense)))
        opponent_score = int(randint(0,opponent.attack)/(1+randint(0,self.defense)))

        if not knockout:
            self.goals_for += team_score
            self.goals_against += opponent_score
            opponent.goals_for += opponent_score
            opponent.goals_against += team_score
            if team_score>opponent_score:
                self.points+=3
            elif team_score<opponent_score:
                opponent.points+=3
            else:
                self.points+=1
                opponent.points+=1
        else:
            if team_score>opponent_score:
                return 1
            elif team_score<opponent_score:
                return 0
            else:
                return randint(0,1)

        

    @staticmethod
    def groupStage(group):
        """
        Simulates the group stage matches
        for a given group.
        Updatess the values of first, second,
        eighth following the results of the group
        matches.

        Input:
        - group: a list consisting of the teams
        belonging to a given group

        Output:
        - group: same list after modification
        """
        for i in range(len(group)):
            group[i].reinitialize()
        for i in range(len(group)):
            for j in range(i+1,len(group)):
                group[i].play(group[j],False)

        group.sort(key=lambda element:(element.points,element.goals_for-element.goals_against,element.goals_for))
        group[-1].first+=1
        group[-2].second+=1
        group[-1].eighth+=1
        group[-2].eighth+=1
        return group

    def reinitialize(self):
        """
        Resets points, goals_for, goals_against
        attributes of a Team instance to zero.
        Useful before every simulation.
        """
        self.points = 0
        self.goals_for = 0
        self.goals_against = 0

    def knockoutStage(groups):
        """
        Simulates the knockout stage, going through each
        stage successively. Modifies the states of the
        teams without returning any value.

        Input:
        groups: list of all groups, each group has been
        already modified by groupStage method.
        """
        #round of 16
        qualified = []
        for i in range(0,8,2):
            r16 = groups[i][-1].play(groups[i+1][-2],True)
            if r16==1:
                qualified.append((i,-1))
                groups[i][-1].quarter+=1
            else:
                qualified.append((i+1,-2))
                groups[i+1][-2].quarter+=1
        for i in range(0,8,2):
            r16 = groups[i][-2].play(groups[i+1][-1],True)
            if r16==0:
                qualified.append((i,-2))
                groups[i][-2].quarter+=1
            else:
                qualified.append((i+1,-1))
                groups[i+1][-1].quarter+=1
        #quarter final
        semi_finalist = []
        for i in range(0,8,2):
            qf = groups[qualified[i][0]][qualified[i][1]].play(groups[qualified[i+1][0]][qualified[i+1][1]],True)
            if qf == 1:
                semi_finalist.append(qualified[i])
                groups[qualified[i][0]][qualified[i][1]].semi+=1
            else:
                semi_finalist.append(qualified[i+1])
                groups[qualified[i+1][0]][qualified[i+1][1]].semi+=1
        #semi-final
        
        sf = groups[semi_finalist[0][0]][semi_finalist[0][1]].play(groups[semi_finalist[1][0]][semi_finalist[1][1]],True)
        if sf==1:
            finalist1 = semi_finalist[0]
            groups[semi_finalist[0][0]][semi_finalist[0][1]].final+=1
            ranking1 = semi_finalist[1]
        else:
            finalist1 = semi_finalist[1]
            groups[semi_finalist[1][0]][semi_finalist[1][1]].final+=1
            ranking1 = semi_finalist[0]


        sf = groups[semi_finalist[2][0]][semi_finalist[2][1]].play(groups[semi_finalist[3][0]][semi_finalist[3][1]],True)
        if sf==1:
            finalist2 = semi_finalist[2]
            groups[semi_finalist[2][0]][semi_finalist[2][1]].final+=1
            ranking2 = semi_finalist[3]
        else:
            finalist2 = semi_finalist[3]
            groups[semi_finalist[3][0]][semi_finalist[3][1]].final+=1
            ranking2 = semi_finalist[2]
                
        #3rd rank
        r3 = groups[ranking1[0]][ranking1[1]].play(groups[ranking2[0]][ranking2[1]],True)
        if r3==1:
            groups[ranking1[0]][ranking1[1]].third+=1
        else:
            groups[ranking2[0]][ranking2[1]].third+=1
        #final
        w = groups[finalist1[0]][finalist1[1]].play(groups[finalist2[0]][finalist2[1]],True)
        if w==1:
            groups[finalist1[0]][finalist1[1]].winner+=1
        else:
            groups[finalist2[0]][finalist2[1]].winner+=1

    
    @staticmethod
    def generateTeams(filename):
        """
        Generates all teams from results of
        qualification and friendly matches,
        compiled as bulk results in a text
        file. Returns a list of all teams,
        each element being an instance of
        the Team class.

        The file consists of 8 paragraphs,
        each paragraph starts with the
        group 

        A future version of this function
        would generate the team scores from
        individual matches, obtained from
        FIFA website, through an API or by
        Web Scraping.


        Input:
        - filename: path of the text file,
        that contains the bulk results

        Output:
        - worldcup: a list containing all
        World Cup teams, with each element
        of a list as an instance of the Team
        class.
        """
        with open(filename,'r') as teams:
            worldcup = []
            levels = []
            for i,line in enumerate(teams):
                xline = line.strip().split()
                if len(xline) == 2:
                    group_name = xline[1]
                elif len(xline) == 5:
                    worldcup.append(Team(xline[0],group_name,float(xline[2])/float(xline[3]),float(xline[1])/float(xline[3])))
                    levels.append(xline[4])
                elif len(xline)==6:
                    worldcup.append(Team(xline[0]+" "+xline[1],group_name,float(xline[3])/float(xline[4]),float(xline[2])/float(xline[4])))
                    levels.append(xline[5])
        levels = [level for _,level in sorted(zip(worldcup,levels),key=lambda element:element[0].defense)]
        worldcup.sort(key=lambda element:element.defense)
        x = -7/(worldcup[-1].defense-worldcup[0].defense)
        y = 1 - worldcup[-1].defense*x
        for i in range(len(worldcup)):
            worldcup[i].defense = int(round(y + x*worldcup[i].defense))
            if levels[i] == 'H':
                worldcup[i].defense = min(worldcup[i].defense+2,8)
            elif levels[i]=='MH':
                worldcup[i].defense = min(worldcup[i].defense+1,8)
            elif levels[i]=='L':
                worldcup[i].defense = max(worldcup[i].defense-1,3)
            

        levels = [level for _,level in sorted(zip(worldcup,levels),key=lambda element:element[0].attack,reverse=True)]
        worldcup.sort(key=lambda element:element.attack,reverse=True)
        x = 7/(worldcup[0].attack-worldcup[-1].attack)
        y = 1 - worldcup[-1].attack*x
        for i in range(len(worldcup)):
            worldcup[i].attack = int(round(y + x*worldcup[i].attack))
            if levels[i] == 'H':
                worldcup[i].attack = min(worldcup[i].attack+2,8)
            elif levels[i]=='MH':
                worldcup[i].attack = min(worldcup[i].attack+1,8)
            elif levels[i]=='L':
                worldcup[i].attack = max(worldcup[i].attack-1,2)

        worldcup.sort(key=lambda element:element.group)
        for i in range(len(worldcup)):
            print(worldcup[i].name+" "+str(worldcup[i].attack)+" "+str(worldcup[i].defense))
            
        return worldcup

    @staticmethod
    def flatten(lis):
        """
        Static method that flattens a list
        of lists into a simple list.
        """
        new_list = []
        for l in lis:
            for x in l:
                new_list.append(x)
        return new_list

if __name__=='__main__':

    worldcup = Team.generateTeams("teams.txt")
    groups = []
    N = 100000
    
    for i in range(0,len(worldcup),4):
        groups.append(worldcup[i:i+4])
        
    for i in range(N):
        for group in groups:        
            group = Team.groupStage(group)
        Team.knockoutStage(groups)

    groups = Team.flatten(groups)
    groups.sort(key=lambda element:element.winner,reverse=True)
    i = 0
    for team in groups:
        i+=1
        print(str(i).ljust(2,' ')+" ",end='')
        print(team)
        
    '''+" "+str(team.first/1000.0)+"  "+
                  str(team.second/1000.0)+"  "+str(team.eighth/1000.0)+" "+str(team.quarter/1000)+" "+str(team.semi/1000)
                  +" "+str(team.third/1000)+" "+str(team.final/1000)+" "+str(team.winner/1000)'''
