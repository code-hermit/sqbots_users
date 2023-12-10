from json_loader import json_load
import pandas as pd
from datetime import datetime
import plotchart
import streamlit as st
import numpy as np
# 2022 - 09 -01 is the strart date
st.set_page_config(layout="wide")
datewise=json_load('combined_datewise.json')
users_df=pd.Series({datetime.strptime(k,'%Y-%m-%d'):v for k,v in datewise.items()})
users_df.sort_index(inplace=True)
brokerwise=json_load('combined_broker_dic.json')
# stratwise=json_load('combined_strategy_dic.json')

brokerwise={datetime.strptime(k,'%Y-%m-%d'):v for k,v in brokerwise.items()}
strategies_dic={k:{w:{y:0 for y in x.keys()} for w,x in v.items()} for k,v in brokerwise.items()}
lots_dic={k:{w:{y:0 for y in x.keys()} for w,x in v.items()} for k,v in brokerwise.items()}
orders_dic={k:{w:{y:0 for y in x.keys()} for w,x in v.items()} for k,v in brokerwise.items()}

all_brokers_set=set()
all_strategies_set=set()
for dat in brokerwise:
    for broker in brokerwise[dat]:
        all_brokers_set.add(broker)
        for strategy in brokerwise[dat][broker]:
            if strategy.lower() in ['testtable']:
                continue
            all_strategies_set.add(strategy)
            strategies_dic[dat][broker][strategy]=brokerwise[dat][broker][strategy]['users']
            lots_dic[dat][broker][strategy]=brokerwise[dat][broker][strategy]['lots']
            orders_dic[dat][broker][strategy]=brokerwise[dat][broker][strategy]['orders']


# stratwise={datetime.strptime(k,'%Y-%m-%d'):v for k,v in stratwise.items()}

# 1) given two dates , what are the number of users/orders/lots
# 2) Given a strategy , what is the number of users/orders/lots within given dates
# 3) Given a broker, what is the number of users/orders/lots within given dates

# start_date=datetime.strptime('20220901','%Y%m%d')
# df=pd.DataFrame([(datetime.strptime(k,'%Y-%m-%d'),v) for k,v in datewise.items()],columns=['Date','Users'])
# df.set_index('Date',inplace=True)
# df=df[df.index>=start_date]
# df.plot()
# plt.show()

START_DATE=datetime.strptime('20220901','%Y%m%d')
END_DATE=datetime.strptime('20231201','%Y%m%d')

with st.expander('Choose Brokers'):
    brok_check_dic={k:True for k in all_brokers_set}
    brok_check_cols=st.columns(len(brok_check_dic)+1)
    brok_counter=0
    for brok in all_brokers_set:
        brok_check_dic[brok] = brok_check_cols[brok_counter].checkbox(brok,value=True)
        brok_counter+=1


with st.expander('Choose Strategies'):
    all_strategies_list=list(all_strategies_set)
    strat_check_dic={k:True for k in all_strategies_list}
    for i in range(0,len(all_strategies_list),7):
        strat_check_cols=st.columns(10)
        strat_counter=0
        for j in range(7):
            if i+j==len(all_strategies_list):
                break
      
            strat_check_dic[all_strategies_list[i+j]] = strat_check_cols[strat_counter].checkbox(all_strategies_list[i+j],value=True)
            strat_counter+=1

# def _combine_values(x):s

def get_df(start_date=START_DATE,end_date=END_DATE,broker_list=all_brokers_set,strategy_list=all_strategies_set,table_type='orders'):
   
    if table_type=='orders':
        t_table=orders_dic
    elif table_type=='strategies':
        t_table=strategies_dic
    elif table_type=='lots':
        t_table=lots_dic
    rdic={dat:{bro:{stra:val for stra,val in x.items() if stra in strategy_list} for bro,x in v.items() if bro in broker_list} for dat,v in t_table.items()}
    bro_dic={dat:{bro:sum(x.values()) for bro,x in v.items() if bro in broker_list} for dat,v in t_table.items()}
    stra_dic={dat:{} for dat in rdic.keys()}
    for dat in rdic:
        for bro in rdic[dat]:
            for strat in rdic[dat][bro]:
                if strat not in stra_dic[dat]:
                    stra_dic[dat][strat]=0
                stra_dic[dat][strat]+=rdic[dat][bro][strat]
    
    
    rlis={k:sum({w:sum(x.values()) for w,x in v.items()}.values()) for k,v in t_table.items()}
    df=pd.Series(rlis)
    df=df[(df.index>=start_date) & (df.index<=end_date)]
    df.sort_index(inplace=True)
    bro_df=pd.DataFrame(bro_dic).T
    bro_df=bro_df[(bro_df.index>=start_date) &(bro_df.index<=end_date)]
    bro_df.fillna(0,inplace=True)
    bro_df.sort_index(inplace=True)
    stra_df=pd.DataFrame(stra_dic).T
    stra_df=stra_df[(stra_df.index>=start_date) & (stra_df.index<=end_date) ]
    stra_df.fillna(0,inplace=True)
    stra_df.sort_index(inplace=True)

    

    return bro_df,stra_df,df

def get_users_df(start_date=START_DATE,end_date=END_DATE):
    global users_df
    users_df=users_df[(users_df.index>=start_date) & (users_df.index<=end_date)]
    return users_df


# bar_plot_df(df,var_name,value_name)
# line_plot_df(data,var_name,value_name,title)
date_col1,date_col2=st.columns(2)
start_date = np.datetime64(date_col1.date_input("Start Date", START_DATE))
end_date = np.datetime64(date_col2.date_input("End Date", END_DATE))

u_df=get_users_df(start_date=start_date,end_date=end_date)

st.plotly_chart(plotchart.line_plot_df(u_df,'Date','Users','Unique Users for All Bots'))
col1, col2, col3 = st.columns(3)
counter=1
selected_brokers_list=[k for k in all_brokers_set if brok_check_dic[k]]
selected_strategies_list=[k for k in all_strategies_set if strat_check_dic[k]]
for table_type in ['orders','lots','strategies']:
    
    cur_col=eval(f'col{counter}')
    counter+=1
    bro_df,stra_df,df=get_df(broker_list=selected_brokers_list,strategy_list=selected_strategies_list,table_type=table_type,start_date=start_date,end_date=end_date)
    cur_col.plotly_chart(plotchart.line_plot_df(df,'Date',table_type,table_type))
    cur_col.plotly_chart(plotchart.bar_plot_df(bro_df,'Date',table_type.upper(),table_type.upper()))
    cur_col.plotly_chart(plotchart.bar_plot_df(stra_df,'Date',table_type.upper(),table_type.upper()))
    
