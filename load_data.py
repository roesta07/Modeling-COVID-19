import numpy as np
import pandas as pd

## lets build data puulling data

def load_covid_timeseries(name):
  base_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series'
  url=f'{base_url}/time_series_covid19_{name}_global.csv'
  df=pd.read_csv(url,
                index_col=['Country/Region', 'Province/State', 'Lat', 'Long']) 
  df['type']=name.lower()
  df.columns.name='date'
  df=df.set_index('type',append=True).reset_index(['Lat','Long'],drop=True).stack().reset_index().set_index('date')
  df.index = pd.to_datetime(df.index)

  df.columns=['country', 'state', 'type', 'cases']
  df.loc[df.state =='Hong Kong', 'country'] = 'Hong Kong'
  df.loc[df.state =='Hong Kong', 'state'] = np.nan
  return df

def load_covid_data(type):
  df=load_covid_timeseries(type)
  df=df.rename(columns={'cases':type.lower()})
  df=days_after_100(df)
  return df

def days_after_100(df):
  df=df.loc[(df['confirmed']>100)]
  df.loc[:,'days_since_100']=np.nan
  for country in df.country.unique():
    filt=(df['country']==country)
    length=len(df.loc[filt,'days_since_100'].values)+1
    counter=np.arange(1,length)
    df.loc[filt,'days_since_100']=counter
  return df
  