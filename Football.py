import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from scipy.stats import poisson

#League2 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1718/E2.csv")


League2 = League2[['HomeTeam','AwayTeam','HC','AC']]
League2 = League2.rename(columns={'HC': 'HomeCorners', 'AC': 'AwayCorners'})
HomeForm = League2.groupby(['HomeTeam']).mean()
HomeForm = HomeForm.rename(columns={'HomeTeam': 'Team','AwayCorners': 'Conc_at_home'})
HomeFormStd = League2.groupby(['HomeTeam']).std()
HomeFormStd = HomeFormStd.rename(columns={'HomeTeam': 'Team','HomeCorners':'HomeCstd','AwayCorners': 'Conc_home_Std'})

AwayForm = League2.groupby(['AwayTeam']).mean()
AwayForm = AwayForm.rename(columns={'AwayTeam': 'Team', 'HomeCorners': 'Conc_away', })
AwayFormStd = League2.groupby(['AwayTeam']).std()
AwayFormStd = AwayFormStd.rename(columns={'HomeTeam': 'Team','HomeCorners':'Conc_away_std','AwayCorners': 'AwayCStd'})

Total = pd.concat([HomeForm, AwayForm,HomeFormStd, AwayFormStd], axis=1)
Total.reset_index(level=0, inplace=True)
Total = Total.rename(columns={'index': 'Team', })

def gaussian(x, mu, sig):
    return 1./(np.sqrt(2.*np.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)

def CornersGauss(Total,Teamname):
    team_specific = Total.loc[Total['Team'] == "Bradford"]
    Home_Won_Mu = team_specific.at[3, 'HomeCorners'] #Need to change index, google this
    Home_conc_Mu = team_specific.at[3, 'Conc_at_home']
    Home_Won_Sig = team_specific.at[3, 'HomeCstd']
    Home_Conc_Sig = team_specific.at[3, 'Conc_home_Std']
    
    gaussianwon = plt.plot(gaussian(np.linspace(0, 20, 20), Home_Won_Mu, Home_Won_Sig), label =' Corners Won')
    gaussianconc =plt.plot(gaussian(np.linspace(0, 20, 20), Home_conc_Mu, Home_Conc_Sig), label='Corners Conceded')
    plt.legend(handles=[gaussianwon[0],gaussianconc[0]])
    plt.xlabel("Number of Corners")
    plt.ylabel("Probability of Occurance")
       
    plt.show()
    return

CornersGauss(Total,"Bradford")
