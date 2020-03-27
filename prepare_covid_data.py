#<iframe src="https://www.google.com/maps/d/embed?mid=1YfaJKmfs2xnuqXjOyHXxVR6ZFZtZnU6N" width="640" height="480"></iframe>

import requests
from collections import defaultdict
import folium
import json
import pandas as pd
#import plotly.express as px

def get_state_data():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/daily')

    response_dict = response.json()
    states = defaultdict(dict)

    status = response_dict['success']
    cases = []#defaultdict()
    #print(f'Data Pull status={status}')

    state_list=['Sikkim','Andhra Pradesh', 'Bihar', 'Chhattisgarh','Arunachal Pradesh',\
         'Delhi', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Karnataka', \
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Mizoram', \
        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Tamil Nadu',\
         'Chandigarh', 'Jammu and Kashmir',  'Uttar Pradesh',\
        'Uttarakhand', 'West Bengal','Telengana','Tripura','Assam',
        'Goa','Nagaland','Lakshadweep','Dadra and Nagar Haveli', 'Daman and Diu',
        'Jharkhand','Meghalaya','Andaman and Nicobar Islands']
    try:
        daily_data = response_dict['data']

        # to get  daily data
        # for i,day in enumerate(daily_data):
        #     date = day['day']
        #     daily_summary = day['summary']
        #     regional_data = day['regional']
        
        # to get  latest day data
        latest_data = daily_data[-1]
        latest_regional_data = latest_data['regional']
        latest_date = latest_data['day']
        latest_summary = latest_data['summary']
        #print(latest_date,latest_summary,latest_regional_data)
        const=0
        for item  in latest_regional_data:
            if item['loc']=='Ladakh':
                const = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                continue
            else:
                k = item['loc']
                states[k] = item
                total_cases = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                cases.append( {'State':k ,'Total_Cases': total_cases})
                
        state_geo_data=json.load(open('/home/shashanks/git_code/covid19_innovate/indian_states.json'))
        
        m = folium.Map([20.5937, 78.9629],zoom_start=4.35) # centered on coordinates of india
       
        
        
        
        #print(state_geo_data['features'].keys())
        for st in state_list:
            if st not in states.keys():
                cases.append( {'State':st ,'Total_Cases': 0})
            states[st] = {'confirmedCasesIndian': 0, 'confirmedCasesForeign': 0, 'discharged': 0, 'deaths': 0}
            
        
        state_data = pd.DataFrame(cases,columns=['State','Total_Cases'])
        state_data.sort_values(by=['State'],inplace=True)
        
        state_data.loc[state_data['State']=='Jammu and Kashmir','Total_Cases']+=const
        print(state_data)
       
        print('########################################')
        print(states.keys())
        print(len(states.keys()))
        
        print(type(state_geo_data))
      
        for i,_ in enumerate(state_geo_data['features']):
            state_geo_data['features'][i]['id'] = state_geo_data['features'][i]['properties']['NAME_1']
            #state_data['State'][i]=state_geo_data['features'][i]['id']
            print(state_geo_data['features'][i]['id'])
        #state_data
        folium.Choropleth(
    geo_data=state_geo_data,
    name='choropleth',
    data=state_data,
    columns=['State', 'Total_Cases'],
    key_on= 'feature.properties.NAME_1',#'features.id',#'features.properties.NAME_1',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.9,
    legend_name='Total Covid 19 cases in India'
).add_to(m)
        m.save('Map.html')

        latest_states_df = pd.DataFrame(latest_regional_data)
       
        return latest_states_df,latest_summary

    except Exception as e:
        print(e)
        print('Data load error')

        return -1,-1

if __name__=='__main__':
    latest_states_df,latest_summary = get_state_data()
    print(latest_states_df,latest_summary)
        
