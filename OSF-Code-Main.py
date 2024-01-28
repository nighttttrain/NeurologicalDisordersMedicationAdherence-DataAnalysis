
import pandas as pd
import numpy as np
import pyreadstat

# file_path = '/Users/rain/Downloads/OSF/NeuroGerAd_Data_OSF1.xlsx'
# OSF = pd.read_excel(file_path)
file_path1 = '/Users/rain/PycharmProjects/OSF/OSF_csv2.csv'
OSF = pd.read_csv(file_path1)
OSF_test = pd.read_excel(file_path)
print(OSF.head(10))#
print(OSF.shape)#
print(type(OSF))#

# show full table
pd.set_option('display.max_rows', 100)

# count number of missing values
a = OSF_test.isnull().sum()
a

# format the column names
OSF.rename(columns={'living_situation ':'living_situation'}, inplace=True)
# write to csv
OSF.to_csv('OSF_csv.csv', index=False)
OSF.to_csv('OSF_csv1.csv', index=False)
# write to SPSS
pyreadstat.write_sav(OSF, 'OSF_SPSS.sav')

# TODO: cleaning
pd.set_option('display.max_rows', None)
print(OSF.isnull().sum())
# TODO: MoCA -> MoCA_before
# convert type to str
OSF['MoCA'] = OSF['MoCA'].astype(str)
# add an empty column for MoCA
OSF["MoCA_before"] = ""
# OSF['MoCA_before'] = OSF['MoCA_before'].astype(int)
print(len(OSF.columns)) #
# replace the value for the column MoCA_before
for i in range(0, len(OSF["MoCA"])):
    if "*" in OSF["MoCA"][i]:
        OSF["MoCA_before"][i] = "1"
        # print("1")
    else:
        OSF["MoCA_before"][i] = "0"
        # print("0")
# remove "*" in column MoCA
OSF['MoCA'] = OSF['MoCA'].str.replace("*", "")
print(OSF['MoCA'])#
# TODO: BDI -> BDI_before
# convert type to str
OSF['BDI'] = OSF['BDI'].astype(str)
# add an empty column for BDI
OSF["BDI_before"] = ""
# OSF['BDI_before'] = OSF['BDI_before'].astype(int)
print(len(OSF.columns)) #
# replace the value for the column MoCA_before
for i in range(0, len(OSF["BDI"])):
    if "*" in OSF["BDI"][i]:
        OSF["BDI_before"][i] = "1"
        # print("1")
    else:
        OSF["BDI_before"][i] = "0"
        # print("0")
# remove "*" in column MoCA
OSF['BDI'] = OSF['BDI'].str.replace("*", "")
print(OSF['BDI'])#
# TODO: geradh4_FUI_medication_change -> change_FU1
# add an empty column for geradh4_FUI_medication_change
OSF["change_FU1"] = ""
# OSF['change_FU1'].iloc[:] = ""
# # chenge is "1", not change is "0", other is "NAN"
# for i in range(0, len(OSF["geradh4_FUI_medication_change"])):
#     if OSF["geradh4_FUI_medication_change"][i] == "yes":
#         OSF["change_FU1"][i] = 1
#         # print("1")
#     elif OSF["geradh4_FUI_medication_change"][i] == "no":
#         OSF["change_FU1"][i] = 0
#         # print("0")
#     # print("n")
# # if physician asked for change, then we see it as "0" (not change)
# for i in range(0, len(OSF["geradh6_FUI_medication_change_by_whom"])):
#     if OSF["change_FU1"][i] == 1:
#         if OSF["geradh6_FUI_medication_change_by_whom"][i] == "physician":
#             OSF["change_FU1"][i] = 0

for i in range(0, len(OSF["geradh4_FUI_medication_change"])):
    if OSF["geradh4_FUI_medication_change"][i] == "no":
        OSF["change_FU1"][i] = 0
    elif OSF["geradh4_FUI_medication_change"][i] == "yes":
        if OSF["geradh6_FUI_medication_change_by_whom"][i] == "physician":
            OSF["change_FU1"][i] = 0
        else:
            OSF["change_FU1"][i] = 1
    else:
        OSF["change_FU1"][i] = np.nan
# test
# OSF['geradh4_FUI_medication_change'].value_counts()["yes"]
# OSF['geradh6_FUI_medication_change_by_whom'].value_counts()["physician"]
# print(OSF["change_FU1"].value_counts()[1])
print(OSF["change_FU1"][15])
print(type(OSF["change_FU1"][15]))
np.isnan(OSF["change_FU1"][15])
# print(OSF['geradh6_FUI_medication_change_by_whom'][6])

# TODO: geradh4_FU2_medication_change -> change_FU2
# add an empty column for geradh4_FU2_medication_change
OSF["change_FU2"] = ""
OSF['change_FU2'].iloc[:] = ""
for i in range(0, len(OSF["geradh4_FU2_medication_change"])):
    if "no" in OSF["geradh4_FU2_medication_change"][i]:
        OSF["change_FU2"][i] = 0
    elif "yes" in OSF["geradh4_FU2_medication_change"][i]:
        if OSF["geradh6_FU2_medication_change_by_whom"][i] == "physician":
            OSF["change_FU2"][i] = 0
        else:
            OSF["change_FU2"][i] = 1
    else:
        OSF["change_FU2"][i] = np.nan
# TODO: change_Fu2 -> change_FU2_1
OSF["change_FU2_funnel"] = ""
# OSF = OSF.drop('change_FU2_1', axis=1) # drop a column
# m = 0
# y_y = 0
# y_o = 0
# n_m = 0
# n_y = 0
# n_n = 0
for i in range(0, len(OSF)):
    if np.isnan(OSF["change_FU1"][i]) == True:
        m+=1
        OSF["change_FU2_funnel"][i] = np.nan
    elif OSF["change_FU1"][i] == 1:
        if OSF["change_FU2"][i] == 1:
            # y_y+=1
            OSF["change_FU2_funnel"][i] = 1
        else:
            # y_o+=1
            OSF["change_FU2_funnel"][i] = np.nan
    elif OSF["change_FU1"][i] == 0:
        if OSF["change_FU2"][i] == 1:
            # n_m+=1
            OSF["change_FU2_funnel"][i] = 1
        elif OSF["change_FU2"][i] == 0:
            # n_y+=1
            OSF["change_FU2_funnel"][i] = 0
        else:
            # n_n+=1
            OSF["change_FU2_funnel"][i] = np.nan
# print(m)
# print(y_y)
# print(y_o)
# print(n_m)
# print(n_y)
# print(n_n)

# TODO: test FU1 and FU2
# 1
j = 0
for i in range(0, len(OSF)):
    if np.isnan(OSF["change_FU1"][i]) == True:
        if np.isnan(OSF["change_FU2"][i]) == False:
            j+=1
print(j)
# result: no missing value at the same time
# 2
j = 0
for i in range(0, len(OSF)):
    if OSF["change_FU1"][i] == 1 and OSF["change_FU2"][i] == 1:
        j+=1
print(j)
# TODO: marital_status_collapsed (missing = 12)
# missing -> other
OSF['marital_status_collapsed'] = OSF['marital_status_collapsed'].astype(str)
for i in range(0, len(OSF)):
    if OSF["marital_status_collapsed"][i] == "nan":
        OSF["marital_status_collapsed"][i] = "other"
        # print("1")
# test
print(OSF["marital_status_collapsed"][469])
print(type(OSF["marital_status_collapsed"][469]))

# TODO: living_situation (missing = 65)
# missing -> other
OSF['living_situation'] = OSF['living_situation'].astype(str)
for i in range(0, len(OSF)):
    if OSF["living_situation"][i] == "nan":
        OSF["living_situation"][i] = "other"
        # print("1")

# TODO: education (missing = 14)
# missing -> other
OSF['education'] = OSF['education'].astype(str)
for i in range(0, len(OSF)):
    if OSF["education"][i] == "nan":
        OSF["education"][i] = "other"
# TODO: tablets_preparation (missing = 63)
# missing -> other
OSF['tablets_preparation'] = OSF['tablets_preparation'].astype(str)
for i in range(0, len(OSF)):
    if OSF["tablets_preparation"][i] == "nan":
        OSF["tablets_preparation"][i] = "other"
# TODO: number_of_drugs_per_day (missing = 67)
# replace with median (skewed)
OSF["number_of_drugs_per_day"] = \
    OSF['number_of_drugs_per_day'].fillna(OSF['number_of_drugs_per_day'].median())
# test
print(OSF["number_of_drugs_per_day"])

# TODO: SAMS (multiple missing)
# use avg -> sams_avg (nan should be ignored)
OSF["sams_avg"] = ""
OSF["sams_avg"] = OSF.iloc[:, 9:27].mean(axis=1)
print(OSF["sams_avg"])

# TODO: HCCQ (missing = 79)

# doc_app_frequency_quarterly (72)
# not use
# medication_change (missing = 66)
# not use
# TODO: SF_36 (multiple missing)

# TODO: SAMS_FU2 (multiple missing) (still missing 266)
OSF["sams_avg_FU2"] = ""
print(OSF.columns.get_loc('sams_1_FU'))
OSF["sams_avg_FU2"] = OSF.iloc[:, 53:63].mean(axis=1)
print(OSF["sams_avg_FU2"])
# TODO: SF12 (multiple missing)

# TODO: format data type
print(OSF.dtypes)

# TODO: transform categorical data to numeric
df['Education'].replace(['Under-Graduate', 'Diploma '],
                        [0, 1], inplace=True)
# gender
OSF["gender_"] = OSF["gender"]
OSF["gender_"].replace(["male", "female"], [0, 1], inplace=True)
print(OSF["gender_"])
# age_collapsed
OSF["age_collapsed_"] = OSF["age_collapsed"]
OSF["age_collapsed_"].replace(["55-59", "60-64", "65-69", "70-74", "75-79",
                               "80-84", "85-89", "90-94", "95-99"],
                              [0, 1, 2, 3, 4, 5, 6, 7, 8],
                              inplace=True)
print(OSF["age_collapsed_"])
# age_group
OSF["age_group"] = OSF["age_collapsed_"]
OSF["age_group"].replace([0, 1, 2, 3, 4, 5, 6, 7, 8],
                         [0, 0, 1, 1, 2, 2, 3, 3, 3],
                         inplace=True)
# diagnosis_collapsed
OSF["diagnosis_collapsed_"] = OSF["diagnosis_collapsed"]
OSF["diagnosis_collapsed_"].replace(["cerebrovascular disorder", "epilepsy",
                                     "movement disorder", "neuromuscular", "others"],
                                    [0, 1, 2, 3, 4],
                                    inplace=True)
print()
# marital_status_collapsed
OSF["marital_status_collapsed_"] = OSF["marital_status_collapsed"]
OSF["marital_status_collapsed_"].replace(["married", "not married", "other"],
         [0, 1, 2],
         inplace=True)
print()
# living_situation
OSF["living_situation_"] = OSF["living_situation"]
OSF["living_situation_"].replace(["alone", "not alone", "other"],
         [0, 1, 2],
         inplace=True)
print()
# education
OSF["education_"] = OSF["education"]
OSF["education_"].replace(["high", "middle", "low", "other"],
         [0, 1, 2, 3],
         inplace=True)
print()
# tablets_preparation
OSF["tablets_preparation_"] = OSF["tablets_preparation"]
OSF["tablets_preparation_"].replace(["independent", "needs help from others", "other"],
         [0, 1, 2],
         inplace=True)
print()
# BFI
OSF["BFI_"] = OSF["BFI"]
OSF["BFI_"].replace(["agreeableness", "conscientiousness", "extraversion",
                     "neuroticism", "openness", " "],
         [0, 1, 2, 3, 4, -9],
         inplace=True)
print()
# TuG
OSF["TuG_"] = OSF["TuG"]
OSF["TuG_"].replace(["<20sec", "20-30sec", ">30sec", "not possible due to medical reasons"],
         [0, 1, 1, 2],
         inplace=True)
print()
# walking_aid
OSF["walking_aid_"] = OSF["walking_aid"]
OSF["walking_aid_"].replace(["no", "yes"],
         [0, 1],
         inplace=True)
print()
# use_any_nonmedicalTreatm
OSF["use_any_nonmedicalTreatm_"] = OSF["use_any_nonmedicalTreatm"]
OSF["use_any_nonmedicalTreatm_"].replace(["no      ", "yes     "],
                                         [0, 1], inplace=True)
print(OSF["use_any_nonmedicalTreatm_"])

# TODO: SAM_0~12, -> 0, 1
OSF["sams_1_"] = OSF["sams_1"]
OSF["sams_1_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_2_"] = OSF["sams_2"]
OSF["sams_2_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_3_"] = OSF["sams_3"]
OSF["sams_3_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_4_"] = OSF["sams_4"]
OSF["sams_4_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_5_"] = OSF["sams_5"]
OSF["sams_5_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_6_"] = OSF["sams_6"]
OSF["sams_6_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_7_"] = OSF["sams_7"]
OSF["sams_7_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_8_"] = OSF["sams_8"]
OSF["sams_8_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_9_"] = OSF["sams_9"]
OSF["sams_9_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_10_"] = OSF["sams_10"]
OSF["sams_10_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_11_"] = OSF["sams_11"]
OSF["sams_11_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_12_"] = OSF["sams_12"]
OSF["sams_12_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_13_"] = OSF["sams_13"]
OSF["sams_13_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_14_"] = OSF["sams_14"]
OSF["sams_14_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_15_"] = OSF["sams_15"]
OSF["sams_15_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_16_"] = OSF["sams_16"]
OSF["sams_16_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_17_"] = OSF["sams_17"]
OSF["sams_17_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)
OSF["sams_18_"] = OSF["sams_18"]
OSF["sams_18_"].replace([0,1,2,3,4], [0,1,1,1,1], inplace=True)

# replace missing values by mean of the group
# three group:
columns1 = ["sams_1", "sams_2", "sams_3", "sams_5"]
columns2 = ["sams_7", "sams_8", "sams_9", "sams_10",
            "sams_11", "sams_12", "sams_13", "sams_17"]
columns3 = ["sams_6", "sams_14", "sams_15", "sams_16", "sams_18"]
# TODO: replace SAMS missing value
OSF["rowmean1"] = OSF[columns1].mean(axis=1, skipna=True).round(0)
OSF["rowmean2"] = OSF[columns2].mean(axis=1, skipna=True).round(0)
OSF["rowmean3"] = OSF[columns3].mean(axis=1, skipna=True).round(0)
# print(OSF["rowmean"])
# del OSF['sams_sum']
# group1: 1，2，3，5
OSF["sam_1"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_1"][i]):
        OSF["sam_1"][i] = OSF["rowmean1"][i]
    else:
        OSF["sam_1"][i] = OSF["sams_1"][i]
print(OSF["sam_1"][902]) # test
OSF["sam_2"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_2"][i]):
        OSF["sam_2"][i] = OSF["rowmean1"][i]
    else:
        OSF["sam_2"][i] = OSF["sams_2"][i]
OSF["sam_3"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_3"][i]):
        OSF["sam_3"][i] = OSF["rowmean1"][i]
    else:
        OSF["sam_3"][i] = OSF["sams_3"][i]
OSF["sam_5"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_5"][i]):
        OSF["sam_5"][i] = OSF["rowmean1"][i]
    else:
        OSF["sam_5"][i] = OSF["sams_5"][i]

# group2: 7，8，9，10，11，12，13，17
OSF["sam_7"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_7"][i]):
        OSF["sam_7"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_7"][i] = OSF["sams_7"][i]
OSF["sam_8"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_8"][i]):
        OSF["sam_8"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_8"][i] = OSF["sams_8"][i]
OSF["sam_9"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_9"][i]):
        OSF["sam_9"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_9"][i] = OSF["sams_9"][i]
OSF["sam_10"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_10"][i]):
        OSF["sam_10"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_10"][i] = OSF["sams_10"][i]
OSF["sam_11"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_11"][i]):
        OSF["sam_11"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_11"][i] = OSF["sams_11"][i]
OSF["sam_12"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_12"][i]):
        OSF["sam_12"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_12"][i] = OSF["sams_12"][i]
OSF["sam_13"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_13"][i]):
        OSF["sam_13"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_13"][i] = OSF["sams_13"][i]
OSF["sam_17"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_17"][i]):
        OSF["sam_17"][i] = OSF["rowmean2"][i]
    else:
        OSF["sam_17"][i] = OSF["sams_17"][i]

# group3: 6，14，15，16，18
OSF["sam_6"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_6"][i]):
        OSF["sam_6"][i] = OSF["rowmean3"][i]
    else:
        OSF["sam_6"][i] = OSF["sams_6"][i]
OSF["sam_14"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_14"][i]):
        OSF["sam_14"][i] = OSF["rowmean3"][i]
    else:
        OSF["sam_14"][i] = OSF["sams_14"][i]
OSF["sam_15"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_15"][i]):
        OSF["sam_15"][i] = OSF["rowmean3"][i]
    else:
        OSF["sam_15"][i] = OSF["sams_15"][i]
OSF["sam_16"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_16"][i]):
        OSF["sam_16"][i] = OSF["rowmean3"][i]
    else:
        OSF["sam_16"][i] = OSF["sams_16"][i]
OSF["sam_18"] = ""
for i in range(0, len(OSF)):
    if pd.isna(OSF["sams_18"][i]):
        OSF["sam_18"][i] = OSF["rowmean3"][i]
    else:
        OSF["sam_18"][i] = OSF["sams_18"][i]
# TODO: sams_sum
columns = ["sam_1", "sam_2", "sam_3", "sam_5", "sam_6", "sam_7", "sam_8", "sam_9",
           "sam_10", "sam_11", "sam_12", "sam_13", "sam_14",
           "sam_15", "sam_16", "sam_17", "sam_18"]
OSF['sam_sum'] = OSF[columns].sum(axis=1)
# TODO: sams_status
# fully adherent (SAMS=0)
# moderate non-adherence (SAMS 1-10)
# significant non-adherence (SAMS >10)
def sams_status(value):
    if value == 0:
        return 0
    elif value <= 10:
        return 1
    elif value > 10:
        return 2
OSF['sams_status'] = OSF['sam_sum'].apply(sams_status)
# TODO: sams_status_binary
def sams_status_binary(value):
    if value == 0:
        return 0
    elif value > 0:
        return 1
OSF['sams_status_binary'] = OSF['sams_status'].apply(sams_status_binary)

# TODO: re_generate SAMS
# read csv from r output
file_path2 = '/Users/rain/Documents/Dissertation/OSF/output_file.csv'
OSF2 = pd.read_csv(file_path2)
# missing
print(OSF2.isnull().sum())
# something
OSF2 = OSF2.drop(['sams_cat'], axis=1)
# write csv to csv
OSF2.to_csv('OSF_csv2.csv', index=False)
# adherence
OSF2['adherence'] = OSF2['SAMS'].apply(sams_status_binary)
# sams_fix1 ~ sams_fix18
# TODO:
# 3 group according to raw pca
columns1 = ["sams_8", "sams_9", "sams_10", "sams_11", "sams_12", "sams_13", "sams_17"]
columns2 = ["sams_1", "sams_2", "sams_3", "sams_4", "sams_5"]
columns3 = ["sams_6", "sams_14", "sams_15", "sams_16", "sams_18"]
# calculate mean group by 3 group
OSF2["rowmean1"] = OSF2[columns1].mean(axis=1, skipna=True).round(0)
OSF2["rowmean2"] = OSF2[columns2].mean(axis=1, skipna=True).round(0)
OSF2["rowmean3"] = OSF2[columns3].mean(axis=1, skipna=True).round(0)
# print(OSF2["rowmean1"])
# group2: 1，2，4, 3，5
OSF2["sams_fix_1"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_1"][i]):
        OSF2["sams_fix_1"][i] = OSF2["rowmean2"][i]
    else:
        OSF2["sams_fix_1"][i] = OSF2["sams_1"][i]
OSF2["sams_fix_2"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_2"][i]):
        OSF2["sams_fix_2"][i] = OSF2["rowmean2"][i]
    else:
        OSF2["sams_fix_2"][i] = OSF2["sams_2"][i]
OSF2["sams_fix_3"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_3"][i]):
        OSF2["sams_fix_3"][i] = OSF2["rowmean2"][i]
    else:
        OSF2["sams_fix_3"][i] = OSF2["sams_3"][i]
OSF2["sams_fix_4"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_4"][i]):
        OSF2["sams_fix_4"][i] = OSF2["rowmean2"][i]
    else:
        OSF2["sams_fix_4"][i] = OSF2["sams_4"][i]
OSF2["sams_fix_5"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_5"][i]):
        OSF2["sams_fix_5"][i] = OSF2["rowmean2"][i]
    else:
        OSF2["sams_fix_5"][i] = OSF2["sams_5"][i]
# group 3: 6, 14, 15, 16, 18
OSF2["sams_fix_6"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_6"][i]):
        OSF2["sams_fix_6"][i] = OSF2["rowmean3"][i]
    else:
        OSF2["sams_fix_6"][i] = OSF2["sams_6"][i]
OSF2["sams_fix_14"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_14"][i]):
        OSF2["sams_fix_14"][i] = OSF2["rowmean3"][i]
    else:
        OSF2["sams_fix_14"][i] = OSF2["sams_14"][i]
OSF2["sams_fix_15"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_15"][i]):
        OSF2["sams_fix_15"][i] = OSF2["rowmean3"][i]
    else:
        OSF2["sams_fix_15"][i] = OSF2["sams_15"][i]
OSF2["sams_fix_16"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_16"][i]):
        OSF2["sams_fix_16"][i] = OSF2["rowmean3"][i]
    else:
        OSF2["sams_fix_16"][i] = OSF2["sams_16"][i]
OSF2["sams_fix_18"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_18"][i]):
        OSF2["sams_fix_18"][i] = OSF2["rowmean3"][i]
    else:
        OSF2["sams_fix_18"][i] = OSF2["sams_18"][i]
# group 1: 8, 9, 10, 11, 12, 13, 17
OSF2["sams_fix_8"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_8"][i]):
        OSF2["sams_fix_8"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_8"][i] = OSF2["sams_8"][i]
OSF2["sams_fix_9"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_9"][i]):
        OSF2["sams_fix_9"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_9"][i] = OSF2["sams_9"][i]
OSF2["sams_fix_10"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_10"][i]):
        OSF2["sams_fix_10"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_10"][i] = OSF2["sams_10"][i]
OSF2["sams_fix_11"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_11"][i]):
        OSF2["sams_fix_11"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_11"][i] = OSF2["sams_11"][i]
OSF2["sams_fix_12"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_12"][i]):
        OSF2["sams_fix_12"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_12"][i] = OSF2["sams_12"][i]
OSF2["sams_fix_13"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_13"][i]):
        OSF2["sams_fix_13"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_13"][i] = OSF2["sams_13"][i]
OSF2["sams_fix_17"] = ""
for i in range(0, len(OSF2)):
    if pd.isna(OSF2["sams_17"][i]):
        OSF2["sams_fix_17"][i] = OSF2["rowmean1"][i]
    else:
        OSF2["sams_fix_17"][i] = OSF2["sams_17"][i]
# def sams_fix(sams_fix, sams, mean):
#     OSF2[sams_fix] = ""
#     for i in range(0, len(OSF2)):
#         if pd.isna(OSF2[sams_fix][i]):
#             OSF2[sams_fix][i] = OSF2[mean][i]
#         else:
#             OSF2[sams_fix][i] = OSF2[sams][i]
# SAMS_fix
columns = ["sams_fix_1", "sams_fix_2", "sams_fix_3", "sams_fix_4", "sams_fix_5",
           "sams_fix_6", "sams_7", "sams_fix_8", "sams_fix_9", "sams_fix_10",
           "sams_fix_11", "sams_fix_12", "sams_fix_13", "sams_fix_14",
           "sams_fix_15", "sams_fix_16", "sams_fix_17", "sams_fix_18"]
OSF2['SAMS_fix'] = OSF2[columns].sum(axis=1, skipna=False)
OSF2['SAMS_fix'] = OSF2[columns].sum(axis=1, skipna=True)
# adherence_fix
OSF2['adherence_fix'] = OSF2['SAMS_fix'].apply(sams_status_binary)
# write to spss
pyreadstat.write_sav(OSF2, 'OSF2.sav')
