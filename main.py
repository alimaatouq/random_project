import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit as st
import hydralit_components as hc
import datetime
import plotly.express as px
from datetime import datetime
from numerize.numerize import numerize
import plotly.graph_objects as go
import pickle
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
# specify the primary menu definition
st.set_page_config(page_title='Digital Marketing Tool',layout="wide")


with st.container():
    col1, col2, col3 = st.columns([1,1.5,1])
with col1:
    st.image('1.png', channels="BGR")
with col2:
    st.write("              ")
with col3:
    st.write("              ")
with st.container():
    col1, col2, col3 = st.columns([1,4,1])
with col1:
    st.write("              ")
with col2:
    st.markdown("""
<style>
.big-font {
    font-size:30px;
    font-family:calibri;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)
with col3:
    st.write("              ")
menu_data = [
    {'id':'Cover Page','label':"Home Page"},
    {'id':'Marketing Analytics','label':"Campaign Analytics"},
    {'id':'Conversion Predictor', 'label':"Conversion Predictor"}]
over_theme = {'txc_inactive': '#FFF','menu_background':'#B1005D','txc_active':'#B1005D','option_active':'#FFF'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)
@st.cache(suppress_st_warning=True)
def read_data():
    data= pd.read_csv(r'data.csv',parse_dates=['Date'])
    return data
def format_number(num):
    return "{:,.2f}".format(num)
temp = read_data()
df = temp.copy()
if menu_id == "Marketing Analytics":
    with st.container():
        start_date = datetime(2020, 1, 1).date()
        end_date = datetime(2021, 12, 31).date()
        col1, col2, col3 = st.columns(3)
    with col1:
        selected_platform = st.selectbox('Platform', df['Platform Name'].unique())
    with col2:
        date_range = st.slider(
            'Choose start and end dates',
            value = (datetime(2020,1,1), datetime(2021,12,31)),
            format="YY-MM"
    )
    with col3:
        selected_objective = st.selectbox('Objective', df['Objective'].unique())
    start_date = date_range[0].date()
    end_date = date_range[1].date()
    df['Reach'] = df['Reach'].apply(lambda x: float(x))
    filtered_df = df[(df['Date'].dt.date >= start_date )& (df['Date'].dt.date <= end_date) & (df['Platform Name'] == selected_platform) & (df['Objective'] == selected_objective)]

    total_impressions = filtered_df['Impressions'].sum()
    total_reach = filtered_df['Reach'].sum()
    total_frequency = total_impressions/total_reach
    total_cost = filtered_df['Costs (USD)'].sum()
    cost_per_click = filtered_df['Costs (USD)'].sum()/filtered_df['Clicks'].sum()
    total_purchases = filtered_df['Purchase'].sum()
    total_revenue = filtered_df['Revenue (USD)'].sum()
    
    coc = total_cost/total_purchases
    AOV = total_revenue/total_purchases
    ROAS = total_revenue/total_cost
    cost_per_imp = (total_cost/total_impressions)*1000
    cost_per_reach = (total_cost/total_reach)*1000

    with st.container():
        col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(label="Total Impressions", value= numerize(total_impressions,3))
    with col2:
        st.metric(label="Total Reach", value= numerize(total_reach,1))
    with col3:
        st.metric(label="Total Frequency", value= numerize(total_frequency,3))
    with col4:
        st.metric(label="CPC", value= round(cost_per_click,1))
    with col5:
        st.metric(label='Cost Per Conversion', value= round(coc,1))
    with col6:
        st.metric(label='Cost Per Thousands Impressions', value=  "%.6f" % cost_per_imp)

    with st.container():
        col1, col2, col3, col4, col5,col6 = st.columns(6)
    with col1:
        st.metric(label="Total Cost(USD)", value= numerize(total_cost,1))
    with col2:
        st.metric(label="Total Revenue(USD)", value= numerize(total_revenue,1))
    with col3:
        st.metric(label="Total Conversions", value= numerize(total_purchases,1))
    with col4:
        st.metric(label="Average Order", value= round(AOV,1))
    with col5:
        st.metric(label='ROAS', value= round(ROAS,1))
    with col6:
        st.metric(label='Cost Per Thousands Reach', value= "%.6f" % cost_per_reach   )

    df['Cost per 1000 Impressions'] = df['Costs (USD)']/df['Impressions']*1000
    df['Cost per Click'] = df['Costs (USD)']/df['Clicks']
    df['CTR'] = df['Clicks']/df['Impressions']*100
    selected_platforms = st.multiselect('Platform Name', df['Platform Name'].unique(), default='Google Ads')
    selected_objective = st.selectbox('Campaign Objective', df['Objective'].unique())
    with st.container():
        col1, col2 = st.columns(2)
    with col1:
        if selected_objective == 'Conversions':
            st.markdown('<h1 style="font-size:125%;">Revenue by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Revenue (USD)'].sum().reset_index()
            fig = px.line(filtered_df_4 , x="Date", y="Revenue (USD)", color='Platform Name')
            st.plotly_chart(fig)
        elif selected_objective == 'Reach':
            st.markdown('<h1 style="font-size:125%;">Cost per milli Impressions by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Cost per 1000 Impressions'].mean().reset_index()
            fig = px.line(filtered_df_4 , x="Date", y="Cost per 1000 Impressions", color='Platform Name')
            st.plotly_chart(fig)
        elif selected_objective == 'Engagements':
            st.markdown('<h1 style="font-size:125%;">Cost per Click</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Cost per Click'].mean().reset_index()
            fig = px.line(filtered_df_4 , x="Date", y="Cost per Click", color='Platform Name')
            st.plotly_chart(fig)
        else:
            st.markdown('<h1 style="font-size:125%;">Revenue by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Revenue (USD)'].sum().reset_index()
            fig = px.line(filtered_df_4 , x="Date", y="Revenue (USD)", color='Platform Name')
            st.plotly_chart(fig)
    with col2:
        if selected_objective == 'Conversions':
            st.markdown('<h1 style="font-size:125%;">Cost of Conversions by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Costs (USD)'].mean().reset_index()
            filtered_df_5 = filtered_df.groupby(['Date', 'Platform Name'])['Purchase'].mean().reset_index()
            filtered_df_5 = pd.merge(filtered_df_5,filtered_df_4,on='Date')
            filtered_df_5 = filtered_df_5.drop(columns='Platform Name_y')
            filtered_df_5['CPC'] = filtered_df_5['Costs (USD)']/filtered_df_5['Purchase']
            fig = px.line(filtered_df_5 , x="Date", y="CPC", color='Platform Name_x')
            st.plotly_chart(fig)

        elif selected_objective == 'Reach':
            
            st.markdown('<h1 style="font-size:125%;">Frequency by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            total_impressions = filtered_df['Impressions'].sum()
            total_reach = filtered_df['Reach'].sum()
            filtered_df['Frequency'] = filtered_df['Impressions']/filtered_df['Reach']
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Frequency'].mean().reset_index()
            colors = {'Google Ads':'red',
                'Facebook Ads':'blue',
                'Snapchat':'yellow'}
            fig = px.histogram(filtered_df_4, x="Date", y="Frequency",
                color='Platform Name', barmode='group',
                height=400)
            fig.update_xaxes(
                dtick="M1",
                tickformat="%b-%Y",
                )
            fig.update_layout(width=600, height=600)
            st.plotly_chart(fig)

        elif selected_objective == 'Engagements':
            st.markdown('<h1 style="font-size:125%;">CTR by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['CTR'].mean().reset_index()
            fig = px.line(filtered_df_4 , x="Date", y="CTR", color='Platform Name')
            st.plotly_chart(fig)
        else:
            st.markdown('<h1 style="font-size:125%;">COC by Platform</h1>', unsafe_allow_html=True)
            filtered_df = df[(df['Platform Name'].isin(selected_platforms))& (df['Objective'] == selected_objective)]
            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
            filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m')
            filtered_df_4 = filtered_df.groupby(['Date', 'Platform Name'])['Costs (USD)'].sum().reset_index()
            filtered_df_5 = filtered_df.groupby(['Date', 'Platform Name'])['Purchase'].sum().reset_index()
            filtered_df_5 = pd.merge(filtered_df_5,filtered_df_4,on='Date')
            filtered_df_5 = filtered_df_5.drop(columns='Platform Name_y')
            filtered_df_5['CPC'] = filtered_df_5['Costs (USD)']/filtered_df_5['Purchase']
            fig = px.line(filtered_df_5 , x="Date", y="CPC", color='Platform Name_x')
            st.plotly_chart(fig)

elif menu_id == 'Conversion Predictor':
    selected_platforms = st.selectbox('Please Choose a Platform Name', df['Platform Name'].unique())
    cost_slider = st.slider(
        'Choose Cost',
        min_value=0,
        max_value=1000000,
        value=100000,
    )
    filename = 'reg.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    facebook_ad = 1 if selected_platforms == 'Facebook Ads' else 0
    google_ad = 1 if selected_platforms == 'Google Ads' else 0
    snapchat_ad = 1 if selected_platforms == 'Snapchat' else 0
    val = loaded_model.predict([[int(cost_slider),facebook_ad, google_ad, snapchat_ad]])[0]
    st.markdown(f'<h2> Revenue Prediction is: { numerize(val)}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2> ROAS Prediction is: { "%.9f" %(val/cost_slider)}</h2>', unsafe_allow_html=True)

elif menu_id == 'Cover Page':

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col2:
            st.markdown('<h3><b>Digital Marketing Management Tool</b></h3>', unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns(3)
    with col2:
        # with col2:
        st.image('ms42.jfif', width = 500)
        st.markdown('<h4 style="padding-left:7vh">Developed by Karim Al Mourad</h4>', unsafe_allow_html=True)
