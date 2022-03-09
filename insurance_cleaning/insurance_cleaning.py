
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math



def clean_insurance_data(file_path):
    df = pd.read_csv(file_path)
    # all columns to snake-case
    df = __to_snake_case(df)
    # convert date column to datetime64
    df["effective_to_date"] = pd.to_datetime(df["effective_to_date"])
    
    cont_num, discr_num = __dif_cont_dis(df)
    df = __remove_outliers(df)
    cont_num_outl_rem, discr_num_outl_rem = __dif_cont_dis(df)
    print("Boxplot")
    __boxplot_continous(cont_num, cont_num_outl_rem)
    print("Discrete")
    plot_discrete_var(discr_num_outl_rem)
    print("Continous")
    plot_continous_var(cont_num_outl_rem)
    df = df.drop(columns=["customer", "policy"])
    
    return df


def __to_snake_case(df):
    new_col = []
    for item in df.columns:
        new_col.append("_".join(item.lower().split(" ")))
    df.columns = new_col
    return df

def __dif_cont_dis(df):
    df = df.select_dtypes(np.number)
    continous_df = pd.DataFrame()
    discrete_df = pd.DataFrame()
    for col in df.columns:
        if df[col].nunique() < 100:
            discrete_df[col] = df[col]
        else:
            continous_df[col] = df[col]
    return continous_df, discrete_df


def __remove_outliers(df):
    iqr = np.nanpercentile(df['customer_lifetime_value'],75) - np.nanpercentile(df['customer_lifetime_value'],25)
    upper_limit = np.nanpercentile(df['customer_lifetime_value'],75) + 1.5*iqr
    df = df[df["customer_lifetime_value"] < upper_limit]


    iqr = np.nanpercentile(df['monthly_premium_auto'],75) - np.nanpercentile(df['monthly_premium_auto'],25)
    upper_limit = np.nanpercentile(df['monthly_premium_auto'],75) + 1.5*iqr
    df = df[df["monthly_premium_auto"] < upper_limit]
    
    return df

def plot_discrete_var(df):
    r = math.ceil(df.shape[1]/2)
    c = 2
    fig, ax = plt.subplots(r,c, figsize=(15,20))
    i = 0
    j = 0
    for item in df.columns:
        sns.histplot(x=item, data = df, ax = ax[i, j])
        if j == 0:
            j = 1
        elif j == 1:
            j = 0
            i = i + 1
    plt.show()
    
def plot_continous_var(df):

    for item in df.columns:
        sns.displot(x=item, data = df)

    plt.show()

def __boxplot_continous(df1, df2):
    r = math.ceil(df1.shape[1])
    c = 2
    fig, ax = plt.subplots(r,c, figsize=(15,20))
    i = 0

    for item in df1.columns:
        ax[0,0].set_title("before removing outliers")
        sns.boxplot(x=item, data=df1, ax=ax[i, 0])
        ax[0,1].set_title("after removing outliers")
        sns.boxplot(x=item, data=df2, ax=ax[i, 1])
        i = i + 1
    plt.show()
    
def check_unique(df):
    for item in df.columns:
        print(item)
        display(df[item].unique())
        display(df[item].value_counts())
        
def log_transform_clean(x):
    if np.isfinite(x) and x!=0:
        return np.log(x)
    else:
        return np.NAN

