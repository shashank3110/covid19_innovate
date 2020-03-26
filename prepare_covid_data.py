#<iframe src="https://www.google.com/maps/d/embed?mid=1YfaJKmfs2xnuqXjOyHXxVR6ZFZtZnU6N" width="640" height="480"></iframe>

import requests
from collections import defaultdict
import folium
import json
import pandas as pd
def get_state_data():
    response = requests.get('https://api.rootnet.in/covid19-in/stats/daily')

    response_dict = response.json()
    states = defaultdict(dict)
    status = response_dict['success']
    cases = []#defaultdict()
    print(f'Data Pull status={status}')
    state_list=['Sikkim','Andhra Pradesh', 'Bihar', 'Chhattisgarh','Arunachal Pradesh',\
         'Delhi', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Karnataka', \
        'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Mizoram', \
        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Tamil Nadu',\
         'Chandigarh', 'Jammu and Kashmir', 'Ladakh', 'Uttar Pradesh',\
        'Uttarakhand', 'West Bengal','Telengana','Tripura','Assam',
        'Goa','Nagaland','Lakshadweep','Dadra and Nagar Haveli', 'Daman and Diu',
        'Jharkhand','Andaman and Nicobar Islands']
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
        for item  in latest_regional_data:
            if item['loc']=='Ladakh':
                continue
            k = item.pop('loc')
            states[k] = item
            total_cases = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
            cases.append( {'State':k ,'Total_Cases': total_cases})
        #print(states)
        state_geo_data=json.load(open('/home/shashanks/git_code/covid19_innovate/indian_states.json'))
        #geo_data = json.loads('/home/shashanks/git_code/covid19_innovate/indian_states.json')
        #print(state_data)
        #pd.read_json('/home/shashanks/git_code/covid19_innovate/indian_states.json')
        m = folium.Map([20.5937, 78.9629],zoom_start=4.5)
        #print(cases)
        
        
        
        #print(state_geo_data['features'].keys())
        for s in state_list:
            if s not in states.keys():
                cases.append( {'State':s ,'Total_Cases': 0})
            states[s] = {'confirmedCasesIndian': 0, 'confirmedCasesForeign': 0, 'discharged': 0, 'deaths': 0}
            
        
        state_data = pd.DataFrame(cases,columns=['State','Total_Cases'])
        state_data.sort_values(by=['State'],inplace=True)
        print(state_data.head())
        print(state_data['State'],len(state_data['State']))
        print('########################################')
        print(states.keys())
        print(len(states.keys()))
        #state_geo_data_df = pd.DataFrame(state_geo_data)
        print(type(state_geo_data))
        #print(state_geo_data['features'][0])
        #print(state_geo_data_df.head())
        for i,_ in enumerate(state_geo_data['features']):
            state_geo_data['features'][i]['id'] = state_geo_data['features'][i]['properties']['NAME_1']
            state_data['State'][i]=state_geo_data['features'][i]['id']
            print(state_geo_data['features'][i]['id'])
        #state_data
        folium.Choropleth(
    geo_data=state_geo_data,
    name='choropleth',
    data=state_data,
    columns=['State', 'Total_Cases'],
    key_on='features.id',#'features.properties.NAME_1',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.9,
    legend_name='Total Covid 19 cases in India'
).add_to(m)
        m.save('Map.html')
        #response= requests.get('https://github.com/geohacker/india/blob/master/state/india_telengana.geojson')
        #counties = response.json()#json.loads(response)
    except Exception as e:
        print(e)
        print('Data load error')

if __name__=='__main__':
    get_state_data()
        
