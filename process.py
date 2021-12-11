import libarary
from preprocessing import feature_data,cate_to_num,Data_normalized
from preprocessing import create_dummies,train_machine
import pandas as pd
from sklearn.linear_model import LinearRegression
def estimate(df):    
    df=df
    feature_data_=feature_data(df)
    target_col='Salary'
    # df=df.drop(columns='Id')
    input_data=df.drop(columns=target_col)
    cate_col_lis=cate_to_num(input_data,feature_data_)
    if len(cate_col_lis)==0:
        norm_df=Data_normalized(input_data)
    else:
        dummies_df=create_dummies(input_data,cate_col_lis)
        norm_df=Data_normalized(input_data)
    # print(norm_df.shape,df[target_col].shape)
    dict_data=train_machine(norm_df,df[target_col])
    # print(pd.DataFrame.from_dict(dict_data))
    return dict_data
    # this is used to test the model
    # test_input=[4]
    # if dict_data["train_model"]==True:
    #     predict_val=mdl_predict(test_input)
    #     # print(f"Predicated values on 1st input :{predict_val}")
    #     mssg = "Predicated values on 1st input is {}\n\n Parameter are {}\n".format(predict_val,dict_data)
    # else:
    #    mssg = "You have no training model,please train the model!!"
    # return mssg

if __name__=='__main__':
    print("process are alright")