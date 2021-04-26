#Author : Nathaniel Wiley
#Last Change : 4-26-21

import mysql.connector
from kenpomScrape import *
import bs4 as bs
import urllib.request
import math
import json
import requests
import ssl
from passwords import *

def establishConnection():
    try:
        kingdb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=kingdbPassword(),
            database="king")
        return kingdb
    except error as e:
        print('Failed to connect to the database, error = '+e)

def deleteTables(database):
    cursor = database.cursor()
    
    #delete existing tables
    cursor.execute("drop table schedule")
    cursor.execute("drop table kenpom")

    cursor.close()
    
def schema(database):
    cursor = database.cursor()

    #create kenpom table
    cursor.execute('''
    create table kenpom(
            Rk              VarChar(10)     not null,
            Team            VarChar(50)     not null,
            Conf            VarChar(50)     not null,
            W_L		    VarChar(10)	    not null,
            AdjEM	    VarChar(10)	    not null,
            AdjO	    VarChar(10)	    not null,
            AdjO_Rank	    VarChar(10)	    not null,
            AdjD	    VarChar(10)	    not null,
            AdjD_Rank	    VarChar(10)	    not null,
            AdjT	    VarChar(10)	    not null,
            AdjT_Rank	    VarChar(10)	    not null,
            Luck	    VarChar(10)	    not null,
            Luck_Rank	    VarChar(10)	    not null,
            ConfAdjEM	    VarChar(10)	    not null,
            AdjEM_Rank	    VarChar(10)	    not null,
            OppO	    VarChar(10)	    not null,
            OppO_Rank	    VarChar(10)	    not null,
            OppD	    VarChar(10)	    not null,
            OppD_Rank	    VarChar(10)	    not null,
            NCSOS	    VarChar(10)	    not null,
            NCSOS_Rank	    VarChar(10)	    not null)''')

    #add primary key constraint
    cursor.execute("alter table kenpom add constraint team_pk primary key(Team)")

    #create schedule table
    cursor.execute('''
    create table schedule(
            Team1		VarChar(50)	not null,
            Team2		VarChar(50)	not null,
            Score1	        VarChar(10),
            Score2	        VarChar(10),
            Spread	        VarChar(10),
            Total	        VarChar(10))''')
    #add foreign key constraint
    cursor.execute('''alter table schedule add
        foreign key(Team1) references kenpom(Team)''')
    
    #add foreign key constraint
    cursor.execute('''alter table schedule add
        foreign key(Team2) references kenpom(Team)''')

    cursor.close()

def insertKenpomData(database):
    #fixed issue with ssl certificate
    ssl._create_default_https_context = ssl._create_unverified_context
    
    cursor = database.cursor()
    sql = '''insert into kenpom (Rk, Team, Conf, W_L, AdjEM, AdjO, AdjO_Rank,
    AdjD, AdjD_Rank, AdjT, AdjT_Rank, Luck, Luck_Rank, ConfAdjEM, AdjEM_Rank,
    OppO, OppO_Rank, OppD, OppD_Rank, NCSOS, NCSOS_Rank) value (%s,%s,%s,%s,
    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    values=()
    kpData=kenPom()
    #add all kenpom data to table
    for row in kpData:
        #join and for statement used to remove seed from Team column
        row[1]=''.join([x for x in row[1] if not x.isdigit()]).rstrip()
        cursor.execute(sql,tuple(row))

    database.commit()
    
    cursor.close()

def insertScheduleData(database):
    #fixed issue with ssl certificate
    ssl._create_default_https_context = ssl._create_unverified_context
    
    cursor=database.cursor()
    
    #insert into schedule
    sql='''insert into schedule (Team1, Team2, Score1, Score2, Spread, Total) value
            (%s, %s, %s, %s, %s, %s)'''

    nolantoKP = [["Iowa State", "Iowa St."],["Saint Francis NY", "St. Francis NY"], ["Saint Francis PA", "St. Francis PA"],["UNCG", "UNC Greensboro"],["NC State", "North Carolina"],['Califorina Baptist', 'Cal Baptist'], ['FAU', "Florida Atlantic"], ["FGCU", "Florida Gulf Coast"], ["Long Island", "LIU"], ["Loyola Maryland", "Loyola MD"], ["McNeese", "McNeese St."], ["Miami (FL)", "Miami FL"], ["Miami (OH)", "Miami OH"], ["Mississippi Valley St.", "Mississippi Valley St."], ["Mount Saint Mary's","Mount St. Mary's"], ['Nicholls',"Nicholls St."], ['North Carolina St.','N.C. State'],['Ole Miss','Mississippi'],['Omaha','Nebraska Omaha'],['Presbyterian College','Presbyterian'],['Saint Bonaventure','St. Bonaventure'],['Saint Francis (NY)','St. Francis NY'],['Saint Francis (PA)','St. Francis PA'],["Saint John's", "St. John's"],["Saint Mary's College","Saint Mary's"],['Seattle University','Seattle'],['SIUE','SIU Edwardsville'],['South Carolina St.','South Carolina St.'],['South Carolina Upstate','USC Upstate'],['Southeast Missouri','Southeast Missouri St.'],['Texas A&M Corpus Christi','Texas A&M Corpus Chris'],['UIC', 'Illinois Chicago'],['ULM','Louisiana Monroe'],['UMass','Massachusetts'],['UNCG','UNC Greensboro'],['UNCW','UNC Wilmington'],['UTA','UT Arlington']]
    cbs2ken = [["W. Carolina", "Western Carolina"], ["UNCG", "UNC Greensboro"], ["Va. Tech", "Virginia Tech"],["NC State", "North Carolina"],['Abilene Chr.', 'Abilene Christian'],['App. St.', 'Appalachian St.'],['Ark.-Pine Bluff', 'Arkansas Pine Bluff'],['Boston U.', 'Boston University'],['Cal-Baker.', 'Cal St. Bakersfield'],['CSFullerton', 'Cal St. Fullerton'],['CSNorthridge', 'Cal St. Northridge'],['Cent. Arkansas', 'Central Arkansas'],['CCSU', 'Central Connecticut'],['C. Michigan', 'Central Michigan'],['Charleston So.', 'Charleston Southern'],['Clev. St.', 'Cleveland St.'],['Dixie St', 'Dixie St.'],['ETSU', 'East Tennessee St.'],['E. Illinois', 'Eastern Illinois'],['E. Kentucky', 'Eastern Kentucky'],['E. Michigan', 'Eastern Michigan'],['E. Washington', 'Eastern Washington'],['FDU', 'Fairleigh Dickinson'],['FAU', 'Florida Atlantic'],['FGCU', 'Florida Gulf Coast'],['G-Webb', 'Gardner Webb'],['George Wash.', 'George Washington'],['Ga. Southern', 'Georgia Southern'],['Grambling', 'Grambling St.'],['Houston Bap.', 'Houston Baptist'],['Ill.-Chicago', 'Illinois Chicago'],['Jax. State', 'Jacksonville St.'],['LBSU', 'Long Beach St.'],['UL-Monroe', 'Louisiana Monroe'],['Loyola-Chi.', 'Loyola Chicago'],['LMU', 'Loyola Marymount'],['Loyola-Md.', 'Loyola MD'],['Miami (Fla.)', 'Miami FL'],['Miami (Ohio)', 'Miami OH'],['Middle Tenn.', 'Middle Tennessee'],['Ole Miss', 'Mississippi'],['Miss. State', 'Mississippi St.'],['Miss Valley St.', 'Mississippi Valley St.'],["Mt St Mary's", "Mount St. Mary's"],['NC State', 'N.C. State'],['Neb.-Omaha', 'Nebraska Omaha'],['New Hamp.', 'New Hampshire'],['N. Mex. St.', 'New Mexico St.'],['N.J. Tech', 'NJIT'],['N. Alabama', 'North Alabama'],['N. Carolina', 'North Carolina'],['NC A&T', 'North Carolina A&T'],['NC Central', 'North Carolina Central'],['N. Dak. St.', 'North Dakota St.'],['N. Arizona', 'Northern Arizona'],['N. Colorado', 'Northern Colorado'],['N. Illinois', 'Northern Illinois'],['N. Kentucky', 'Northern Kentucky'],['Prairie View', 'Prairie View A&M'],['PFW', 'Purdue Fort Wayne'],["St. Peter's", "Saint Peter's"],['Sam Hou. St.', 'Sam Houston St.'],['San Diego St', 'San Diego St.'],['San Fran.', 'San Francisco'],['SIUE', 'SIU Edwardsville'],['SC State', 'South Carolina St.'],['S. Dak. St.', 'South Dakota St.'],['SE Missouri St.', 'Southeast Missouri St.'],['SE Louisiana', 'Southeastern Louisiana'],['Southern U.', 'Southern'],['S. Illinois', 'Southern Illinois'],['So. Miss', 'Southern Miss'],['So. Utah', 'Southern Utah'],['St. Bona.', 'St. Bonaventure'],['St. Fran.-NY', 'St. Francis NY'],['St. Fran.-Pa.', 'St. Francis PA'],['SF Austin', 'Stephen F. Austin'],['UT Martin', 'Tennessee Martin'],['Tenn. Tech', 'Tennessee Tech'],['Texas A&M-CC', 'Texas A&M Corpus Chris'],['Texas So.', 'Texas Southern'],['UCSB', 'UC Santa Barbara'],['UNC-Ash.', 'UNC Asheville'],['UNCG', 'UNC Greensboro'],['UNC-Wilm.', 'UNC Wilmington'],['SC Upstate', 'USC Upstate'],['UT-Arlington', 'UT Arlington'],['UT-Rio Grande Valley', 'UT Rio Grande Valley'],['UT-San Antonio', 'UTSA'],['Va. Tech', 'Virginia Tech'],['W. Virginia', 'West Virginia'],['W. Carolina', 'Western Carolina'],['W. Illinois', 'Western Illinois'],['W. Kentucky', 'Western Kentucky'],['W. Michigan', 'Western Michigan']] 
    kpData = kenPom()
    #Scraping College Basketball Schedule
    cbb_sch = schedule('https://www.cbssports.com/college-basketball/schedule/')
    #Formatting Todays Schedule
    fCBB_SCH = formatSchedule(cbb_sch, cbs2ken, 0, 1)
    #Calculating Scores for todays Schedule
    dayscores = todaysScores(fCBB_SCH, kpData)
    #Adding the Algorithms Srpeads
    withSpreads = createSpread(dayscores)
    #Addint totals from the algorithm
    withTotals = createTotals(withSpreads)
    #Adding warren nolan predictions
    withNolan = nolanPredicts("http://www.warrennolan.com/basketball/2021/predict-games?type1=Tuesday,%20February%2023&type2=All%20Games&date=2021-02-23")
    #Formatting nolan data names to kenpom
    fNolan = formatSchedule(withNolan, nolantoKP, 11, 20)
    #Adding Neccessary Nolan Data to results
    resultsNolan = addNolan(fNolan, withTotals)
    
    #print('Final numbers: '+' , '.join(str(i) for i in resultsNolan[0]))
    for matchup in resultsNolan:
        for i in matchup:
            i=str(i)
        
    for matchup in resultsNolan:
        cursor.execute(sql, tuple(matchup))

    database.commit()
    cursor.close()    

def getMatchupData(database, team1, team2):
    cursor=database.cursor()

    cursor.execute('select * from kenpom where Team = \"'+team1+'\" or Team = \"'+team2+'\"')
    rows = cursor.fetchall()

    #return array with index 0 being team1 data and index 1 being team2 data
    return rows

    cursor.close()

def getTeamData(database,team1):
    cursor=database.cursor()

    cursor.execute('select * from kenpom where Team = \"'+team1+'\"')
    row = cursor.fetchone()

    #return tuple with data
    return row

    cursor.close()

def clearKenpomTable(database):
    cursor=database.cursor()

    cursor.execute('delete from kenpom')

    database.commit()
    cursor.close()
    
def clearScheduleTable(database):
    cursor=database.cursor()

    cursor.execute('delete from schedule')

    database.commit()
    cursor.close()

def safeExit(database):
    database.close()


def main():
    db = establishConnection()
    
    #deleteTables(db)
    #schema(db)

    #insertKenpomData(db)
    #insertScheduleData(db)

    matchupData = getMatchupData(db, 'Gonzaga', 'Baylor')
    print(matchupData)
    teamData = getTeamData(db,'Gonzaga')
    print(teamData)


    safeExit(db)

if __name__=='__main__':
    main()
