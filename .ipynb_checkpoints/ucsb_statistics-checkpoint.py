import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import tableauserverclient as TSC
import streamlit.components.v1 as components

pd.options.display.max_columns = 100




# create sidebar and sidebar options
sidebar = st.sidebar

with sidebar:
    selected = option_menu(
        menu_title = 'Navigation',
        options=['Per Minute Stats', 'Fouls Drawn Per 40', 'Opponent Shot Chart'],
        icons=['stopwatch','pencil', 'basketball'],
        menu_icon='cast',
        default_index=0,
        styles={
        "container": {"padding": "0"},
        "icon": {"font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#025246"}
        }
    )


if selected == 'Per Minute Stats':
    st.title("UCSB 2021-2022 Per-Minute season stats")
    st.write('Yellow signifies the highest value in that column.')
    st.write('Click the top of a column to sort by that column.')

    url = f"https://www.espn.com/mens-college-basketball/team/stats/_/id/2540"
    info = pd.read_html(url)
    names = pd.DataFrame(info[2])
    stats = pd.DataFrame(info[3])
    df = pd.concat([names, stats], axis = 1)

    df["points/min"] = (df["PTS"] / df["MIN"]).apply(lambda x: round(x, 2))
    df["rebounds/min"] = (df["REB"] / df["MIN"]).apply(lambda x: round(x, 2))
    df["assists/min"] = (df["AST"] / df["MIN"]).apply(lambda x: round(x, 2))
    df["blocks/min"] = (df["BLK"] / df["MIN"]).apply(lambda x: round(x, 2))
    df["steals/min"] = (df["STL"] / df["MIN"]).apply(lambda x: round(x, 2))
    df["turnovers/min"] = (df["TO"] / df["MIN"]).apply(lambda x: round(x,2))
    df['offensive_reb/min'] = (df["OR"] / df["MIN"]).apply(lambda x: round(x, 2))
    df['defensive_reb/min'] = (df["DR"] / df["MIN"]).apply(lambda x: round(x, 2))
    df['FTA/min'] = (df["FTA"] / df["MIN"]).apply(lambda x: round(x, 2))
    df['3PA/min'] = (df["3PA"] / df["MIN"]).apply(lambda x: round(x, 2))
    df = df[:-1] # drops last row which is a totals row
    df = df.loc[(df.MIN > 12)].copy() #filter out any player who's played less than 12 minutes
    df.set_index("Name", inplace=True)
    df = df[['MIN', 'points/min', 'rebounds/min',
           'assists/min', 'blocks/min', 'steals/min', 'turnovers/min',
           'offensive_reb/min', 'defensive_reb/min', 'FTA/min', '3PA/min',
           'FGM', 'FGA', 'FTM', 'FTA', '3PM', '3PA', 'PTS', 'OR', 'DR',
           'REB', 'AST', 'TO', 'STL', 'BLK'
          ]]

    st.dataframe(df.style.highlight_max(axis=0), height=1000)
    st.title("Per Minute Visuals")
    st.bar_chart(df['points/min'], height = 400)
    st.bar_chart(df["rebounds/min"], height = 400)
    st.bar_chart(df['offensive_reb/min'], height = 400)
    st.bar_chart(df['defensive_reb/min'], height = 400)
    st.bar_chart(df["assists/min"], height = 400)
    st.bar_chart(df["blocks/min"], height = 400)
    st.bar_chart(df["steals/min"], height = 400)
    st.bar_chart(df["turnovers/min"], height = 400)

elif selected == 'Fouls Drawn Per 40':
    
    st.markdown("<h1 style='text-align: center; color: black;'>Fouls Drawn per 40 Minutes</h1>", unsafe_allow_html=True)
    
    st.caption("<h2 style='text-align: center; color: black;'>For Each Player in the Big West </h2>", unsafe_allow_html=True)
    
    st.markdown("""---""")
    st.caption("<h3 style='text-align: center; color: black;'>INSTRUCTIONS </h3>", unsafe_allow_html=True)
    st.write('1. To focus on a single team, click the team from the legend on the right and select "Keep Only".')
    st.write('2.  To return to the full scatter plot, click the reset button on the bottom toolbar.')
    st.write('3. For a bigger view, click "Full Screen" in the bottom right of the toolbar.')
    st.write('4. Hover the mouse over .')
        
    def main():
        html_temp = """<div class='tableauPlaceholder' id='viz1656723571051' style='position: relative'><noscript><a href='#'><img alt='Personal Fouls drawn per 40 minutes, Big West 2021-22 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PersonalFoulsDrawnper40MinutesBigWest&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='PersonalFoulsDrawnper40MinutesBigWest&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pe&#47;PersonalFoulsDrawnper40MinutesBigWest&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1656723571051');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        
        components.html(html_temp, height = 2000)
    
    if __name__ == "__main__":    
        main()

elif selected == 'Opponent Shot Chart':
        st.title('Where Does the Opponent Shoot From?')
        st.write('This section is under construction')