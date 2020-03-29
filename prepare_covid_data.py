import requests
from collections import defaultdict
import folium
import json
import pandas as pd
#import plotly.express as px
coord_dict ={
    'Sikkim':[27.5330,88.5122],'Andhra Pradesh':[15.9129,79.7400], 'Bihar':[25.0961,85.313], 'Chhattisgarh':[21.2787,81.8661],'Arunachal Pradesh':[28.2180,94.7278],\
         'Delhi':[28.7041,77.1025], 'Gujarat':[22.2587,71.1924], 'Haryana':[29.0588,76.0856], 'Himachal Pradesh':[31.1048,77.1734], 'Karnataka':[15.3173,75.7139], \
        'Kerala':[10.8505,76.2711], 'Madhya Pradesh':[22.9734,78.6569], 'Maharashtra':[19.7515,75.7139], 'Manipur':[24.6637,93.9063], 'Mizoram':[23.1645,92.9376], \
        'Odisha':[20.9517,85.0985], 'Puducherry':[11.9416,79.8083], 'Punjab':[31.1471,75.3412], 'Rajasthan':[27.0238,74.2179], 'Tamil Nadu':[11.1271,78.6569],\
         'Chandigarh':[30.7333,76.7794], 'Jammu and Kashmir':[33.7782,76.5762],  'Uttar Pradesh':[26.8467,80.9462],\
        'Uttarakhand':[30.0668,79.0193], 'West Bengal':[22.9868,87.8550],'Telengana':[18.1124,79.0193],'Tripura':[23.9408,91.9882],'Assam':[26.2006,92.9376],
        'Goa':[15.2993,74.1240],'Nagaland':[26.1584,94.5624],'Lakshadweep':[8.295441,73.048973],'Dadra and Nagar Haveli':[20.1809,73.0169], 'Daman and Diu':[20.4283,72.839],
        'Jharkhand':[23.6102,85.2799],'Meghalaya':[25.4670,91.3662],'Andaman and Nicobar Islands':[11.7401,92.6586],
        'Ladakh':[34.152588,77.577049]
    #print(f'Data Pull status={status}')

    }
def get_state_data():
    '''
    Collect latest statewise data for corona virus cases and plot a choropleth
    map with markers describing numbers
    '''
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
         'Chandigarh', 'Jammu and Kashmir',  'Uttar Pradesh',\
        'Uttarakhand', 'West Bengal','Telengana','Tripura','Assam',
        'Goa','Nagaland','Lakshadweep','Dadra and Nagar Haveli', 'Daman and Diu',
        'Jharkhand','Meghalaya','Andaman and Nicobar Islands']
    try:
        daily_data = response_dict['data']
        
        # to get  latest day data
        latest_data = daily_data[-1]
        latest_regional_data = latest_data['regional']
        latest_date = latest_data['day']
        latest_summary = latest_data['summary']
      
        const=0
        m = folium.Map([20.5937, 78.9629],zoom_start=4.5)
        for item  in latest_regional_data:
            if item['loc']=='Ladakh':
                # handling Ladakh seperately as Ladakh geojson boundaries not available.
                const = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                folium.Marker(coord_dict[item['loc']],color='blue',popup=item,tooltip=item['loc'],max_height=5,icon=folium.Icon(color='yellow', icon='user')).add_to(m)
                continue
            else:
                k = item['loc']
                states[k] = item
                total_cases = item['confirmedCasesIndian']+item['confirmedCasesForeign']+item['discharged']+item['deaths']
                cases.append( {'State':k ,'Total_Cases': total_cases})
            folium.Marker(coord_dict[item['loc']],color='blue',popup=item,tooltip=item['loc'],max_height=5,icon=folium.Icon(color='yellow', icon='user')).add_to(m)
        state_geo_data=json.load(open('/home/shashanks/git_code/covid19_innovate/indian_states.json'))
        
         # centered on coordinates of india
       
        
        
        

        for st in state_list:
            if st not in states.keys():
                cases.append( {'State':st ,'Total_Cases': 0})
            states[st] = {'confirmedCasesIndian': 0, 'confirmedCasesForeign': 0, 'discharged': 0, 'deaths': 0}
            
        
        state_data = pd.DataFrame(cases,columns=['State','Total_Cases'])
        state_data.sort_values(by=['State'],inplace=True)
        
        state_data.loc[state_data['State']=='Jammu and Kashmir','Total_Cases']+=const
        # print(state_data)
       
        # print('########################################')
        # print(states.keys())
        # print(len(states.keys()))
        
        # print(type(state_geo_data))
      
        # for i,_ in enumerate(state_geo_data['features']):
        #     state_geo_data['features'][i]['id'] = state_geo_data['features'][i]['properties']['NAME_1']
        #     #state_data['State'][i]=state_geo_data['features'][i]['id']
        #     print(state_geo_data['features'][i]['id'])
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
        m.save('static/Map.html')

        latest_states_df = pd.DataFrame(latest_regional_data)
       
        return latest_states_df,latest_summary

    except Exception as e:
        print(e)
        print('Data load error')

        return -1,-1

if __name__=='__main__':
    latest_states_df,latest_summary = get_state_data()
    print(latest_states_df,latest_summary)
