import streamlit as st
import pandas as pd

# interactive plots
import plotly.graph_objs as go
import plotly.express as px

st.set_page_config("🏐"
    'VNL 23',
    layout="wide"
)

header = st.container()
general_stats, teams_details, stats_by_position = st.tabs(['General stats', 'Teams details',  'Stats by Position'])
# get_df_sets() - get from standings the amount of sets won and lost by each team, with these two values we calculate the amount of sets played  
def get_df_sets(df_scorers):
    
    standings = pd.read_html("https://en.volleyballworld.com/volleyball/competitions/vnl-2023/standings/women/#advanced")
    
    df1 = standings[0]['Unnamed: 1_level_0']
    
    df1.rename(columns= {'Unnamed: 1_level_1':'Team'}, inplace=True)
    
    df2 = standings[0]['Sets']
    
    del df2['Set Ratio']
    
    res = pd.concat([df1, df2], axis=1)
    
    res['Team'] = res['Team'].apply(lambda row : row[0:-3])
    
    res = res.assign(Sets = lambda n : n['Won'] + n['Lost'])

    res = res.filter(['Team','Sets'])
    
    df = pd.merge(df_scorers, res, on="Team")
      
    return df

def get_skills_per_sets(teams):
    
    attack_per_set = lambda x : round((teams['Attack Points'] / teams['Sets']),1)
    block_per_set = lambda x : round((teams['Block Points'] / teams['Sets']),1)
    serve_per_set = lambda x : round((teams['Serve Points'] / teams['Sets']),1)
    rec_per_set = lambda x : round((teams['Successful'] / teams['Sets']),1)
    dig_per_set = lambda x : round((teams['Digs'] / teams['Sets']),1)
    
    teams['AttackPerSet'] = attack_per_set('AttackPerSet')
    teams['BlockPerSet'] = block_per_set('BlockPerSet')
    teams['ServePerSet'] = serve_per_set('ServePerSet')
    teams['ExcRecPerSet'] = rec_per_set('ExcRecPerSet')
    teams['DigPerSet'] = dig_per_set('DigPerSet')
    
    return teams
 
def interactive_plot_attack(teams):
    
    teams = teams.sort_values("AttackPerSet", ascending=False).head(10)
    
    st.markdown(""" **General Stats** """)
    st.dataframe(teams.set_index('Team'))

    trace1 = go.Bar(
                y = teams.AttackPerSet,
                x = teams.Team,
                name = "Attack",
                marker = dict(color = 'rgba(255, 174, 255, 0.9)',
                             line=dict(color='rgb(0,0,0)',width=1.9)),
                text = teams.AttackPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Attacks/Sets')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    


def interactive_plot_block(teams):
    
    teams = teams.sort_values("BlockPerSet", ascending=False).head(10)
    
    trace1 = go.Bar(
                    y = teams.BlockPerSet,
                    x = teams.Team,
                    name = "Block",
                    marker = dict(color = 'rgba(255, 255, 128, 0.9)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.BlockPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Blocks/Sets')
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def interactive_plot_serve(teams):
    
    teams = teams.sort_values("ServePerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.ServePerSet,
                    x = teams.Team,
                    name = "Serve",
                    marker = dict(color = 'rgba(170, 255, 128, 0.9)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.ServePerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Aces/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def interactive_plot_digs(teams):
    
    teams = teams.sort_values("DigPerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.DigPerSet,
                    x = teams.Team,
                    name = "Digs",
                    marker = dict(color = 'rgba(114, 189, 246, 0.8)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.DigPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Digs/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)


def interactive_plot_receptions(teams):
    
    teams = teams.sort_values("ExcRecPerSet", ascending=False).head(10)
    # create trace2 
    trace1 = go.Bar(
                    y = teams.ExcRecPerSet,
                    x = teams.Team,
                    name = "Excellent Reception",
                    marker = dict(color = 'rgba(246, 1, 73, 0.75)',
                                  line=dict(color='rgb(0,0,0)',width=1.9)),
                    text = teams.ExcRecPerSet)
    data = [trace1]
    layout = go.Layout(
        font=dict(family='Courier New, monospace', size=12, color='#000000'),
        title='Excellent Receptions/Sets')

    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)


def load_scorers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-scorers/"
    
    best_scorers = pd.read_html(url)[0]
    
    best_scorers = best_scorers.rename(columns={
                'Shirt NumberShirt': 'ShirtNumber',
                'Player NamePlayer':'Player', 
                'TeamTeam':'Team',
                'PointsPts':'Total Points',
                'Attack PointsA Pts':'Attack Points', 
                'Block PointsB Pts':'Block Points', 
                'Serve PointsS Pts':'Serve Points'

    })
    
    
    best_scorers['Player'] = best_scorers['Player'].replace({
        'Duarte Alecrim Diana':'Diana Duarte',
        'Da Silva Ana Carolina': 'Ana Carolina',
        'Rios Naiane De Almeida':'Naiane Rios',
        'Da Silva Lorrayna':'Lorrayna Da Silva'
        'Vasques Lais':'Lais Vasques',
        'Zalewski Daroit Moreira Priscila' : 'Priscila Daroit',
        'Alexandre Costa Nunes Nyeme Victoria': 'Nyeme Nunes',
        'Silva Carneiro Macris Fernanda':  'Macris Carneiro',
        'Ratzke Roberta Silva':'Roberta Ratzke',
        #'Barbosa De Souza Karina':'Karina Barbosa',
        'Menezes Oliveira de Souza Ana Cristina':'Ana Cristina',
        'Araujo Natália':'Natália Araujo',
        'Viezel Lorena Giovana' : 'Lorena Viezel',
        'Nascimento Kisy' : 'Kisy Nascimento',
        'Bergmann Julia Isabelle':'Julia Bergmann',
        #'Araujo De Souza Mayany Cristina':'Mayany Cristina',
        'Geraldo Teixeira Lorenne':'Lorenne Teixeira',
        'Braga Guimaraes Gabriela':'Gabi Guimarães',
        #'Gambatto Kudiess Julia':'Julia Kudiess',
        'Montibeller Rosamaria':'Rosamaria Montibeller',
        'Lemes Santos Tainara':'Tainara Santos',
        #'De Oliveira Saad Gattaz Caroline':'Carol Gattaz'

    })
    
    return best_scorers

def get_attackers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-attackers/"
    
    best_attackers = pd.read_html(url)[0]
    
    best_attackers = best_attackers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'Pointsattacks':'AttackPoints',
        'ErrorsSE':'Errors', 
        'Attemptsshots':'AttemptsShots',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_attackers[(best_attackers['TotalAttempts'] > 0)]

    df = df.drop(columns=['ShirtNumber'])
    
    return df
    #AgGrid(df, width=890)
    #st.dataframe(df)

def get_receivers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-receivers/"
    
    best_receivers = pd.read_html(url)[0]
    
    best_receivers = best_receivers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
         'SuccesfulSuccesful':'Successful',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    
    })
    
    df = best_receivers[(best_receivers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber'])
    #AgGrid(df)
    return df
    
def get_diggers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-diggers/"
    
    best_diggers = pd.read_html(url)[0]
    
    best_diggers = best_diggers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'SuccessfulSuccessful':'Successful',
        'Digsgreat-save':'Digs',
        'ErrorsSE':'Errors', 
        'ReceptionsRec':'Receptions',
        'Average per matchaverage-per-match':'AveragePerMatch',
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    
    df = best_diggers[(best_diggers['Digs'] > 0)]
    
    df = df.drop(columns=['ShirtNumber'])
    #AgGrid(df) 
    return df

    
def get_blockers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-blockers/"
    
    best_blockers = pd.read_html(url)[0]
    
    best_blockers = best_blockers.rename(columns={
         'Shirt NumberShirt':'ShirtNumber', 
         'Player NamePlayer':'Player', 
         'TeamTeam':'Team',
         'Blocksstuff-blocks':'Blocks', 
         'ErrorsSE': 'Errors', 
         'ReboundsREB':'Rebounds',
         'Average per matchaverage-per-match': 'AveragePerMatch', 
         'Efficiency %Eff':'Efficiency%', 
         'TotalTA':'TotalAttempts'
    })
    df = best_blockers[(best_blockers['TotalAttempts'] > 0)]
    
    df = df.drop(columns=['ShirtNumber'])
    #AgGrid(df)
    return df

def get_servers():
    
    url = "https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-servers/"
    
    best_servers = pd.read_html(url)[0]
    
    best_servers = best_servers.rename(columns={
        'Shirt NumberShirt': 'ShirtNumber',
        'Player NamePlayer':'Player', 
        'TeamTeam':'Team',
        'Pointsserve-points': 'ServePoints',
        'ErrorsSE':'Errors', 
        'AttempsAtt':'Attempts',
        'Average per matchaverage-per-match':'AveragePerMatch', 
        'Success %Success %':'Success%', 
        'TotalTA':'TotalAttempts'
    })
    df = best_servers[(best_servers['ServePoints'] > 0)]
    
    df = df.drop(columns=['ShirtNumber','Attempts'])         
    return df

def players_by_team(df_scorers, sigla):  
    
    players = df_scorers[df_scorers['Team'] == sigla]
    #st.dataframe(players.sum())
    del players['ShirtNumber']
        
    st.markdown(""" **Team Stats** """)
    #team_totals = players.sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Points", players['Total Points'].sum())
    col2.metric("Attack Points", players['Attack Points'].sum())
    col3.metric("Block Points", players['Block Points'].sum())
    col4.metric("Serve Points", players['Serve Points'].sum())

    st.markdown(""" **Players Stats** """)
    del players['Team']
    col1, col2 = st.columns(2)
    with col1:
         st.dataframe(players.set_index('Player'))
    with col2:
         gen_bar_chart_scorers(players)

def show_skill_tables(code):
    
    st.markdown(""" **Attacking** """)
    df_attack = get_attackers()
    df_attack = df_attack[df_attack['Team'] == code]
    del df_attack['Team']
    st.dataframe(df_attack.set_index('Player'))
    
    st.markdown(""" **Reception** """)
    df_rec = get_receivers()
    st.dataframe(df_rec[df_rec['Team'] == code].set_index('Player'))
    
    st.markdown(""" **Diggers** """)
    df_dig = get_diggers()
    st.dataframe(df_dig[df_dig['Team'] == code].set_index('Player'))
        
    st.markdown(""" **Blocking** """)
    df_blk =  get_blockers()
    st.dataframe(df_blk[df_blk['Team'] == code].set_index('Player'))
    
    st.markdown(""" **Serving** """)
    df_serve = get_servers()
    st.dataframe(df_serve[df_serve['Team'] == code].set_index('Player'))



def gen_bar_chart_scorers(df):
    
    min_points = 0
    df = df[df['Total Points'] > min_points].sort_values('Total Points', ascending=True)
    fig = px.bar(df, title = 'Best Scorers', x = 'Total Points', y = 'Player', text ='Total Points', color = 'Total Points', color_continuous_scale = px.colors.sequential.Viridis, height=450, width=500)
    fig.update_layout(xaxis_title="", yaxis_title="", font = dict(family = 'Sans Serif', size = 12), showlegend=True)
    fig.update_yaxes(showgrid=False)
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig)


#### Starts here!

with header:
    st.title("Welcome to my VNL 2023 app!")
    st.text("Another way to check the numbers from the competition - team by team")
    st.text("by Thaís G. (@BRA_VolleyStats)")
    st.markdown("""
    *All data collected from the [official website of the competition](https://en.volleyballworld.com/volleyball/competitions/vnl-2023/statistics/women/best-scorers/)* 
    """)
    
    st.info(""" [PT] Todos os dados são retirados do site da volleyball world. 
    São fornecidos por eles e do jeito deles. As estatísticas fornecidas podem ser interpretadas como:
    * Total Points: total de pontos feitos por uma jogadora
    * Attack Points : pontos de ataque
    * Block Points:  pontos de bloqueios
    * Serve Points: pontos de saque ou 'aces'
    * Digs: defesas  
    * Successful ou  Excellent Reception: refere-se a apenas recepções excelentes feitas por uma jogadora
    * Success% : é equivalente a percentual de ataque ou aproveitamento de ataque, é dado pelo total de pontos de ataque feitos pelo total de tentativas de ataque
    * AttackPerSet: é dado pelo total de pontos de ataque feitos pelo time pelo total de sets jogados pelo time. 
    **usa-se a mesma lógica para os outros fundamentos*
    """)
    
with general_stats:

    df_scorers = load_scorers()
    
    df_scorers = df_scorers.filter(items=['Team', 'Attack Points','Block Points', 'Serve Points', 'Total Points']).groupby("Team").sum()

    df_scorers = df_scorers.reset_index()
    
    df_digs = get_diggers()
    df_digs = df_digs.groupby("Team").sum().reset_index()
    
    df_rec = get_receivers()
    df_rec = df_rec.groupby("Team").sum().reset_index()
    
    df_scorers = pd.merge(df_scorers, df_digs[['Team','Digs']], on=['Team'])
    
    df_scorers = pd.merge(df_scorers, df_rec[['Team','Successful']], on=['Team'])
    
    df_scorers['Team'] = df_scorers['Team'].replace({
                                            'THA':'Thailand',
                                            'BUL':'Bulgaria',
                                            'TUR':'Türkiye',
                                            'ITA':'Italy',
                                            'BRA':'Brazil',
                                            'GER':'Germany',
                                            'DOM':'Dominican Republic',
                                            'USA':'United States',
                                            'NED':'Netherlands',
                                            'CHN':'China',
                                            'CRO':'Croatia',
                                            'SRB':'Serbia',
                                            'CAN':'Canada',
                                            'POL':'Poland',
                                            'JPN':'Japan',
                                            'KOR':'Korea'
    })
    
    
    df_scorers = get_df_sets(df_scorers)
     
    new_df = get_skills_per_sets(df_scorers)

    interactive_plot_attack(new_df)

    interactive_plot_block(new_df)

    interactive_plot_serve(new_df)   
    
    interactive_plot_receptions(new_df) 
    
    interactive_plot_digs(new_df)   
    
with teams_details:
    
    st.title("Choose a team: ")
    
    team = st.selectbox(
     '',
         ('Canada', 'China','Brazil', 'Bulgaria', 
          'Croatia', 'Dominican Republic','Germany','Italy', 
          'Japan','Korea', 'Netherlands','Poland', 
          'Serbia','Thailand', 'Türkiye','United States',
         ))

    st.write('You selected:', team)
    df_scorers = load_scorers()

    if team == 'Brazil':
        code = 'BRA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Croatia':
        code = 'CRO' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Bulgaria':
        code = 'BUL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Canada':
        code = 'CAN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

    elif team == 'China':
        code = 'CHN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Dominican Republic':
        code = 'DOM' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)

    elif team == 'Germany':
        code = 'GER' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
    
    elif team == 'Italy':
        code = 'ITA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
   
    elif team == 'Japan':
        code = 'JPN' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Korea':
        code = 'KOR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)    

        
    elif team == 'Netherlands':
        code = 'NED' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Poland':
        code = 'POL' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         
    
    elif team == 'Serbia':
        code = 'SRB' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
        
    elif team == 'Thailand':
        code = 'THA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
                         

    elif team == 'Türkiye':
        code = 'TUR' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)
              
    elif team == 'United States':
        code = 'USA' 
        players_by_team(df_scorers, code)
        show_skill_tables(code)


with stats_by_position:
		
    st.title("Choose a position: ")
    st.info("""    
		* Posições:
    	* MB : central
    	* OH: ponteira
    	* O: oposto
    	* L: líbero """
    )
    df_players = pd.read_csv('players_vnl23.csv', index_col=False)
    del df_players['No.']
    df_scorers = load_scorers()
    position = st.selectbox("Choose a position: ", ["MB","OH","O","L"])
    df_players = df_players.query("Position == @position")
    
    cols = ['Player','Team','Total Points','Attack Points', 'Block Points', 'Serve Points']
    df = pd.merge(df_players, df_scorers, on=['Player','Team'])
    df = df.filter(items=cols).set_index('Player')
    
    
    if (position == "OH") or (position == "MB") or (position == "O"):
       st.markdown(""" **Scorers** """)
       st.dataframe(df)
       st.markdown(""" **Attack** """)
       df_att = get_attackers()
       df1 = pd.merge(df_players, df_att, on=['Player','Team'])
       st.dataframe(df1.set_index('Player'))
       df_blk = get_blockers()
       st.markdown(""" **Block**""")
       df2 = pd.merge(df_players, df_blk, on=['Player','Team'])
       st.dataframe(df2.set_index('Player'))
       if (position == "OH"):
    	   df_rec = get_receivers()
    	   st.markdown(""" **Reception**""")
    	   df = pd.merge(df_players, df_rec, on=['Player','Team'])
    	   st.dataframe(df.set_index('Player'))           
   
    elif position == 'L':
    	df_rec = get_receivers()
    	st.markdown(""" **Reception**""")
    	df = pd.merge(df_players, df_rec, on=['Player','Team'])
    	st.dataframe(df.set_index('Player'))
    	df_dig = get_diggers()
    	st.markdown(""" **Defense**""")
    	df = pd.merge(df_players, df_dig, on=['Player','Team'])
    	st.dataframe(df.set_index('Player'))
  
    
    
