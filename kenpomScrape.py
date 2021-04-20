import bs4 as bs
import urllib.request
import math
import json
import requests
from passwords import *

#Scrapes data set from KenPom Rankings and returns it in a 2D Array
def kenPom():
    sauce = urllib.request.urlopen("http://kenpom.com/").read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')

    titles = ["Rk", "Team", "Conf", "W-L", "AdjEM", "AdjO","AdjO Rank", "AdjD","AdjD Rank", "AdjT", "AdjT Rank", "Luck", "Luck Rank", "AdjEM", "AdjEM Rank", "OppO", "OppO Rank","OppD", "OppD Rank", "NCSOS", "NCSOS Rank"]
    array = []
    kenpom = []
    counter = 0
    for td in soup.find_all('td'):
        array.append(td.text)
        counter += 1
        if counter == 21:
            counter = 0
            kenpom.append(array)
            array = []
    return kenpom

#Scrapes current days college basketball schedule and returns it in a 2D Array
def schedule(link):
    sauce = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')

    array = []
    schedule = []
    gameDecision = []
    counter = 0
    x = ''
    for div in soup.find_all('div', class_="CellGame"):
        x = div.text
        x = x.strip()
        if x == "Postponed" or x == "Cancelled":
            gameDecision.append(x)
    for span in soup.find_all('span', class_="TeamName"):
        if span.text == '':
            print("CBS Error: Team Name Not Found")
            array.append("Error: Missing Name")
            counter += 1
        else:
            array.append(span.text)
            counter +=1
        if counter == 2:
            schedule.append(array)
            array = []
            counter = 0
    schedule = schedule[(len(gameDecision)):]
    return schedule
#Scrapes data from WarrenNolan.com
def nolanPredicts(nolanSite):
    #pulling and open page source 
    sauce = urllib.request.urlopen(nolanSite).read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')

    #initiating variables
    array = []
    data = []
    nolan = []
    finalNolan = [] 
    counter = 0
    bad_chars = ['', '\n', '✘', '✔']
    
    #putting website variables in a list
    for td in soup.find_all('td'):
        data.append(td.text)
    #formatting the list
    for a in range(len(data)):
        try:
            data[a] = data[a].replace('\n', '')
        except:
            data[a] = data[a]
    for a in range(len(data)):
        try:
            data[a] = data[a].replace("State", "St.")
        except:
            data[a] = data[a]
    for a in range(len(data)):
        try:
            data[a] = data[a].replace("(PA)", "PA")
        except:
            data[a] = data[a]
    for a in range(len(data)):
        try:
            data[a] = data[a].replace("(NY)", "NY")
        except:
            data[a] = data[a]
    for a in range(len(data)):
        try:
            data[a] = data[a].replace("-", " ")
        except:
            data[a] = data[a]
    for i in bad_chars:
        while True:
            try:
                data.remove(i)
            except:
                break
    
##    while True:
##        try:
##            data.remove('\n')
##        except:
##            break
##    while True:
##        try:
##            data.remove('✘')
##        except:
##            break
##    while True:
##        try:
##            data.remove('✔')
##        except:
##            break
    
    #formatting the team names
    for x in range(11, len(data), 28):
        teamRecord = data[x].split('(')
        data[x] = teamRecord[0][:-1]
    for x in range(20, len(data), 28):
        teamRecord = data[x].split('(')
        data[x] = teamRecord[0][:-1]
    for x in range(len(data)):
        array.append(data[x])
        counter+=1
        if counter == 28:
            counter = 0
            nolan.append(array)
            array = []
    return nolan

#Getting lines from API
def getLines():
    
    #My API Key
    api_key = personalAPIKey()

    sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={'api_key': api_key})

    sports_json = json.loads(sports_response.text)

    if not sports_json['success']:
        print(
            'There was a problem with the sports request:',
            sports_json['msg']
        )

    else:
        print()
        print(
            'Successfully got {} sports'.format(len(sports_json['data'])),
            'Here\'s the first sport:'
        )
        print(sports_json['data'][0])



    # To get odds for a sepcific sport, use the sport key from the last request
    #   or set sport to "upcoming" to see live and upcoming across all sports
    sport_key = 'upcoming'

    odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': api_key,
        'sport': sport_key,
        'region': 'us', # uk | us | eu | au
        'mkt': 'h2h' # h2h | spreads | totals
    })

    odds_json = json.loads(odds_response.text)
    if not odds_json['success']:
        print(
            'There was a problem with the odds request:',
            odds_json['msg']
        )

    else:
        # odds_json['data'] contains a list of live and 
        #   upcoming events and odds for different bookmakers.
        # Events are ordered by start time (live events are first)
        print()
        print(
            'Successfully got {} events'.format(len(odds_json['data'])),
            'Here\'s the first event:'
        )
        print(odds_json['data'][0])

        # Check your usage
        print()
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

        
#Scraping Vegas Insider for lines and spreads

    
def getVegas():
    sauce = urllib.request.urlopen('https://www.vegasinsider.com/college-basketball/odds/las-vegas/?s=459').read()
    soup = bs.BeautifulSoup(sauce, 'html.parser')
    
    teams = []
    array = []
    
    for a in soup.find_all('a', class_="tabletext"):
        teams.append(a.text)
    for a in soup.find_all('a', class_="cellTextNorm"):
        array.append(a.text)
    for i in range(len(array)):
        array[i] = array[i][9:20]
    #for i in range(1,len(array
    for i in range(len(array)):
        array[i].split("-", 1)
#Taking neccessary Nolan data and putting it into the results array
#cr stands for current results array
def addNolan(nolan, cr):
    titlesAdded = ["r1 Score 1st", "r1 score second", "r1 spread", "r1 total", "elo score 1st", "elo score 2nd", "elo spread", "elo total"]
    for x in range(len(cr)):
        for i in range(len(nolan)):
            if nolan[i][11] == cr[x][0]:
                cr[x].append(nolan[i][13])
                cr[x].append(nolan[i][22])
                cr[x].append(nolan[i][14])
                cr[x].append(nolan[i][16])
                cr[x].append(nolan[i][17])
                cr[x].append(nolan[i][25])
                cr[x].append(nolan[i][18])
                try:
                    cr[x].append(int(nolan[i][17]) + int(nolan[i][25]))
                except:
                    cr[x].append("Error: Missing Data")
            elif nolan[i][21] == cr[x][0]:
                cr[x].append(nolan[i][22])
                cr[x].append(nolan[i][13])
                cr[x].append(nolan[i][23])
                cr[x].append(nolan[i][16])
                cr[x].append(nolan[i][25])
                cr[x].append(nolan[i][17])
                cr[x].append(nolan[i][26])
                try:
                    cr[x].append(int(nolan[i][18]) + int(nolan[i][26]))
                except:
                    cr[x].append("Error: Missing Data")
    return cr
            
    
#Takes in the list of data for team one and team two who are facing off today, and returns both teams scores in a list
#tas stands for Team Alogrithm Score
def teamScores(teamOne, teamTwo, kenpom):
    tas = []
    #Initializing lists to put Kenpom data for team in
    team1 = []
    team2 = []
    teamOneScore = 0
    teamTwoScore = 0
    #putting kenpom data for team in list
    if teamOne == "Error: Missing Name":
        team1 = "Error: Missing Name"
    elif teamTwo == "Error: Missing Name":
        team2 = "Error: Missing Name"
    else:
        for i in range(len(kenpom)):
            if teamOne in kenpom[i][1]:
                team1 =  kenpom[i]
            elif teamTwo in kenpom[i][1]:
                team2 = kenpom[i]
    if team1 == [] or team1 == "Error: Missing Name":
        teamOneScore = str("Error: No Data")
    elif team2 == [] or team1 == "Error: Missing Name":
        teamTwoScore = str("Error: No Data")
    else:
        teamOneScore = (((float(team1[5]) + float(team2[7]))/2) * ((float(team1[9]) + float(team2[9]))/2))/100
        teamTwoScore = (((float(team2[5]) + float(team1[7]))/2) * ((float(team2[9]) + float(team1[9]))/2))/100
        teamOneScore = round(teamOneScore, 1)
        teamTwoScore = round(teamTwoScore, 1)
    tas.append(teamOneScore)
    tas.append(teamTwoScore)
    return tas
def formatSchedule(cbb_sch, other_sch, team1location, team2location):
    counter = 0
    y = team1location
    for x in range((len(cbb_sch)-1)*2):
        for i in range(len(other_sch)):
            if cbb_sch[counter][y] == other_sch[i][0]:
                cbb_sch[counter][y] = other_sch[i][1]
            if x == (len(cbb_sch) -1):
                y = team2location
                counter = 0
        counter += 1
    return cbb_sch
def todaysScores(cbb_sch, kenpom):
    counter = 0
    for i in range(len(cbb_sch)):
        scores = teamScores(cbb_sch[i][0], cbb_sch[i][1], kenpom)
        cbb_sch[i].append(scores[0])
        cbb_sch[i].append(scores[1])
    return cbb_sch
#tsSpreads stands for todays scores with spreads
def createSpread(tsSpreads):
    spread = 0
    for i in range(len(tsSpreads)):
        if tsSpreads[i][2] == "Error: No Data" or tsSpreads[i][3] == "Error: No Data":
            spread = "Error: No Data"
        else:
            spread = (float(tsSpreads[i][2]) - float(tsSpreads[i][3]))
            spread = round(spread, 1)
        tsSpreads[i].append(spread)
    return tsSpreads
#tsTotals stands for todays scores with totals
def createTotals(tsTotals):
    total = 0
    for i in range(len(tsTotals)):
        if tsTotals[i][2] == "Error: No Data" or tsTotals[i][3] == "Error: No Data":
            total = "Error: No Data"
        else:
            total = ((float(tsTotals[i][2])) + (float(tsTotals[i][3])))
            total = round(total, 1)
        tsTotals[i].append(total)
    return tsTotals
                   

#Main Function, to run program
def main():
    nolantoKP = [["Iowa State", "Iowa St."],["Saint Francis NY", "St. Francis NY"], ["Saint Francis PA", "St. Francis PA"],["UNCG", "UNC Greensboro"],["NC State", "North Carolina"],['Califorina Baptist', 'Cal Baptist'], ['FAU', "Florida Atlantic"], ["FGCU", "Florida Gulf Coast"], ["Long Island", "LIU"], ["Loyola Maryland", "Loyola MD"], ["McNeese", "McNeese St."], ["Miami (FL)", "Miami FL"], ["Miami (OH)", "Miami OH"], ["Mississippi Valley St.", "Mississippi Valley St."], ["Mount Saint Mary's","Mount St. Mary's"], ['Nicholls',"Nicholls St."], ['North Carolina St.','N.C. State'],['Ole Miss','Mississippi'],['Omaha','Nebraska Omaha'],['Presbyterian College','Presbyterian'],['Saint Bonaventure','St. Bonaventure'],['Saint Francis (NY)','St. Francis NY'],['Saint Francis (PA)','St. Francis PA'],["Saint John's", "St. John's"],["Saint Mary's College","Saint Mary's"],['Seattle University','Seattle'],['SIUE','SIU Edwardsville'],['South Carolina St.','South Carolina St.'],['South Carolina Upstate','USC Upstate'],['Southeast Missouri','Southeast Missouri St.'],['Texas A&M Corpus Christi','Texas A&M Corpus Chris'],['UIC', 'Illinois Chicago'],['ULM','Louisiana Monroe'],['UMass','Massachusetts'],['UNCG','UNC Greensboro'],['UNCW','UNC Wilmington'],['UTA','UT Arlington']]
    cbs2ken = [["W. Carolina", "Western Carolina"], ["UNCG", "UNC Greensboro"], ["Va. Tech", "Virginia Tech"],["NC State", "North Carolina"],['Abilene Chr.', 'Abilene Christian'],['App. St.', 'Appalachian St.'],['Ark.-Pine Bluff', 'Arkansas Pine Bluff'],['Boston U.', 'Boston University'],['Cal-Baker.', 'Cal St. Bakersfield'],['CSFullerton', 'Cal St. Fullerton'],['CSNorthridge', 'Cal St. Northridge'],['Cent. Arkansas', 'Central Arkansas'],['CCSU', 'Central Connecticut'],['C. Michigan', 'Central Michigan'],['Charleston So.', 'Charleston Southern'],['Clev. St.', 'Cleveland St.'],['Dixie St', 'Dixie St.'],['ETSU', 'East Tennessee St.'],['E. Illinois', 'Eastern Illinois'],['E. Kentucky', 'Eastern Kentucky'],['E. Michigan', 'Eastern Michigan'],['E. Washington', 'Eastern Washington'],['FDU', 'Fairleigh Dickinson'],['FAU', 'Florida Atlantic'],['FGCU', 'Florida Gulf Coast'],['G-Webb', 'Gardner Webb'],['George Wash.', 'George Washington'],['Ga. Southern', 'Georgia Southern'],['Grambling', 'Grambling St.'],['Houston Bap.', 'Houston Baptist'],['Ill.-Chicago', 'Illinois Chicago'],['Jax. State', 'Jacksonville St.'],['LBSU', 'Long Beach St.'],['UL-Monroe', 'Louisiana Monroe'],['Loyola-Chi.', 'Loyola Chicago'],['LMU', 'Loyola Marymount'],['Loyola-Md.', 'Loyola MD'],['Miami (Fla.)', 'Miami FL'],['Miami (Ohio)', 'Miami OH'],['Middle Tenn.', 'Middle Tennessee'],['Ole Miss', 'Mississippi'],['Miss. State', 'Mississippi St.'],['Miss Valley St.', 'Mississippi Valley St.'],["Mt St Mary's", "Mount St. Mary's"],['NC State', 'N.C. State'],['Neb.-Omaha', 'Nebraska Omaha'],['New Hamp.', 'New Hampshire'],['N. Mex. St.', 'New Mexico St.'],['N.J. Tech', 'NJIT'],['N. Alabama', 'North Alabama'],['N. Carolina', 'North Carolina'],['NC A&T', 'North Carolina A&T'],['NC Central', 'North Carolina Central'],['N. Dak. St.', 'North Dakota St.'],['N. Arizona', 'Northern Arizona'],['N. Colorado', 'Northern Colorado'],['N. Illinois', 'Northern Illinois'],['N. Kentucky', 'Northern Kentucky'],['Prairie View', 'Prairie View A&M'],['PFW', 'Purdue Fort Wayne'],["St. Peter's", "Saint Peter's"],['Sam Hou. St.', 'Sam Houston St.'],['San Diego St', 'San Diego St.'],['San Fran.', 'San Francisco'],['SIUE', 'SIU Edwardsville'],['SC State', 'South Carolina St.'],['S. Dak. St.', 'South Dakota St.'],['SE Missouri St.', 'Southeast Missouri St.'],['SE Louisiana', 'Southeastern Louisiana'],['Southern U.', 'Southern'],['S. Illinois', 'Southern Illinois'],['So. Miss', 'Southern Miss'],['So. Utah', 'Southern Utah'],['St. Bona.', 'St. Bonaventure'],['St. Fran.-NY', 'St. Francis NY'],['St. Fran.-Pa.', 'St. Francis PA'],['SF Austin', 'Stephen F. Austin'],['UT Martin', 'Tennessee Martin'],['Tenn. Tech', 'Tennessee Tech'],['Texas A&M-CC', 'Texas A&M Corpus Chris'],['Texas So.', 'Texas Southern'],['UCSB', 'UC Santa Barbara'],['UNC-Ash.', 'UNC Asheville'],['UNCG', 'UNC Greensboro'],['UNC-Wilm.', 'UNC Wilmington'],['SC Upstate', 'USC Upstate'],['UT-Arlington', 'UT Arlington'],['UT-Rio Grande Valley', 'UT Rio Grande Valley'],['UT-San Antonio', 'UTSA'],['Va. Tech', 'Virginia Tech'],['W. Virginia', 'West Virginia'],['W. Carolina', 'Western Carolina'],['W. Illinois', 'Western Illinois'],['W. Kentucky', 'Western Kentucky'],['W. Michigan', 'Western Michigan']] 
    #Scraping Ken Pom Data
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
    print('Final numbers: '+' , '.join(str(i) for i in resultsNolan[0]))
    #Getting vegas odds
    odds = getVegas()
    for i in range(len(resultsNolan)):
        if len(resultsNolan[i]) > 12:
            print(*resultsNolan[i], sep=",")
    
    #When adding spreads, it is based on the first team
    #Add "Team +/- Spread" later using
    #if spread > 0:
    #   spread = "+" + str(spread)
    #elif spread == 0:
    #   spread = "Even"
    # + " " + str(spread)
if __name__=='__main__':
    main()

