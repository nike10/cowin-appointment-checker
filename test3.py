# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:58:09 2021

@author: Niketan
"""

import requests
from bs4 import BeautifulSoup as soup
import json
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from urllib.request import Request, urlopen 
st.set_page_config( layout='wide')



headers={
  
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36", 
    "X-Amzn-Trace-Id": "Root=1-60953d79-32115db82937573f5ed786f3"
}



@st.cache(allow_output_mutation=True)
def files():
    with open('districts_names.txt') as f:
        districtnames = f.read().splitlines()
    
    
    with open('dicts_tuple.txt') as f:
        districts = f.read().splitlines()
    
    dists=[]
    for i in districts:
        dists.append(i[1:-1].split(','))
    return districtnames,dists




districtnames,dists=files()

def main():
    global soup
    st.title("CoWin Appointment Availability Checker")
    with st.form(key='form1'):
        col1,col2 = st.beta_columns([2,1])
        with col1:
             option  = st.selectbox( 'Select the District', districtnames)
             for i in dists:
                 if i[1]==' '+option:
                     t1=i[0]


     
        with col2:
            date=st.date_input('Date')
            date=str(date)
            year=date[:4]
            month=date[5:7]
            day=date[8:]
            datec=day+'-'+month+'-'+year
            button = st.form_submit_button(label='Generate')
    
    
    if button:
        url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(t1)+"&date="+str(datec)
        r = requests.get(url ,headers=headers )
        soup=r.text
        data=json.loads(soup.encode("utf-8"))
        
        finaldata=data['centers']
        df = pd.DataFrame()
        try:
            for i in range(len(finaldata)):
                try:
                    train = pd.DataFrame.from_dict(finaldata[i])
                    sessions=pd.DataFrame(finaldata[i]['sessions'])
                    temp=pd.concat([train,sessions],axis=1)
                    temp=temp[['name', 'address','fee_type','date', 'available_capacity', 'min_age_limit','vaccine',]]
                    df=df.append(temp)
                    df=df[(df['available_capacity']>0)]
                    
                except:
                    pass
        except:
            st.write('error')       
        df18=df[(df['min_age_limit']>=18) & (df['min_age_limit']<45)]
        df45=df[df['min_age_limit']>=45]
        if len(df18)==0:
            st.warning('No vaccination centers for the age group 18-44 available on the selected date')
            st.markdown('##')
            st.markdown('##')
        else:
            st.success('Here is the list of available Vaccination Centers for the age group 18-44')
            st.table(df18.assign(hack='').set_index('hack'))
        if len(df45)==0:
            st.warning('No vaccination centers for the age group 45+ available on  the selected date')
            st.markdown('##')
            st.markdown('##')
        else:
            st.success('Here is the list of available Vaccination Centers for the age group 44+')
            st.table(df45.assign(hack='').set_index('hack'))
            
    st.markdown("_niketan")

main()
