def col_reset(df):
    column_name=df.iloc[0]
    col_lis=[]
    for i in column_name:
        col_lis.append(i)
    drop_df=df.drop(index=df.index[0], axis=0,inplace=True)
    my_df=df.set_axis(col_lis, axis=1)
    final_df=my_df.reset_index(drop=True)
    return final_df