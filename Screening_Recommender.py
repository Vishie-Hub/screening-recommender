#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 15:46:59 2025

@author: vishnair
"""
## Preventative Screening Project py sheet 1

import os
import pandas as pd

# Define the directory where the CSV files are stored
directory = r"/Users/vishnair/Documents/Preventative_Screenings"

# List of CSV file names
file_names = [
    "Alcohol.csv", "BloodPressure.csv", "BP_C_Q.csv", "Demographics.csv",
    "Income.csv", "MentalHealth.csv", "PhysicalActivity.csv", "Smoking.csv"
]

# Load all CSV files into dataframes, ignoring unnecessary index columns
dataframes = [pd.read_csv(os.path.join(directory, file), index_col=0) for file in file_names]

# Merge all dataframes on 'SEQN'
merged_df = dataframes[0]
for df in dataframes[1:]:
    merged_df = merged_df.merge(df, on="SEQN", how="inner", suffixes=("", "_dup"))

# Drop duplicate columns that may have been created
merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith("_dup")]

# Save the merged dataset
output_path = os.path.join(directory, "Merged_Screening_Data.csv")
merged_df.to_csv(output_path, index=False)

# Load the merged dataset
file_path = os.path.join(directory, "Merged_Screening_Data.csv")
df = pd.read_csv(file_path)

# Define the column renaming dictionary
rename_dict = {
    "SEQN": "Sequence_Number", "ALQ121": "Alc_Frequency", "ALQ130": "Alc_Amount",
    "ALQ142": "Alc_Consumption_Year", "ALQ280": "Alc_Overconsumption_Year", "ALQ170": "Alc_Consumption_Month",
    "BPAOCSZ": "Arm_Circumference", "BPXOSY1": "Systolic_1", "BPXODI1": "Diastolic_1",
    "BPXOSY2": "Systolic_2", "BPXODI2": "Diastolic_2", "BPXOSY3": "Systolic_3", "BPXODI3": "Diastolic_3",
    "BPXOPLS1": "Pulse_1", "BPXOPLS2": "Pulse_2", "BPXOPLS3": "Pulse_3",
    "BPQ020": "Hypertension_once", "BPQ030": "Hypertension_multiple", "BPQ150": "Hypertension_medicated",
    "BPQ080": "High_Cholesterol", "BPQ101D": "High_Cholesterol_medicated",
    "RIAGENDR": "Gender", "RIDAGEYR": "Age_Year", "RIDRETH3": "Race", "DMQMILIZ": "Military",
    "DMDBORN4": "Country", "DMDEDUC2": "Education", "RIDEXPRG": "Pregnant",
    "WTINT2YR": "Interview_Weighted", "WTMEC2YR": "Exam_Weighted",
    "INDFMPIR": "Income_to_Poverty_Ratio", "INDFMMPI": "Poverty_Index_Monthly", "INDFMMPC": "Income_to_Poverty_Ratio_Monthly",
    "DPQ010": "Depression_Low_Interest", "DPQ020": "Depression_Hopeless", "DPQ030": "Depression_Sleep_Issues",
    "DPQ040": "Depression_Lethargic", "DPQ050": "Depression_Poor_Diet", "DPQ060": "Depression_Low_SelfWorth",
    "DPQ070": "Depression_Low_Concentration", "DPQ080": "Depression_Speed", "DPQ090": "Depression_Suicidal",
    "DPQ100": "Depression_Functionality", "PAD790Q": "Physical_Leisure_1", "PAD790U": "Physical_Leisure_2",
    "PAD800": "Physical_Leisure_Time", "PAD810Q": "Physical_Rigorous_1", "PAD810U": "Physical_Rigorous_2",
    "PAD820": "Physical_Rigourous_Time", "PAD680": "Physical_Sit_Time", "SMQ020": "Smoking_100_Cigs",
    "SMQ040": "Smoking", "SMD641": "Smoking_Frequency_Month", "SMD650": "Smoking_Amount"
}

# Drop columns listed as 'X'
drop_columns = [
    "ALQ111", "ALQ270", "ALQ151", "BPAOARM", "SDDSRVYR", "RIDSTATR", "RIDAGEMN",
    "RIDRETH1", "RIDEXMON", "RIDEXAGM", "DMDYRUSR", "DMDMARTZ", "DMDHHSIZ", "DMDHRGND",
    "DMDHRAGZ", "DMDHREDZ", "DMDHRMAZ", "DMDHSEDZ", "SDMVSTRA", "SDMVPSU", "INQ300",
    "IND310", "SMD100MN", "SMQ621", "SMD630", "SMAQUEX2"
]
df = df.drop(columns=[col for col in drop_columns if col in df.columns])

# Rename the remaining columns
df = df.rename(columns=rename_dict)

# Check for missing values
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]

if not missing_values.empty:
    print("Columns with missing values:")
    print(missing_values)
else:
    print("No missing values found in the dataset.")

# Define screening recommendation logic
def recommend_screenings(row):
    recommendations = []
    reasons = []
    
    if row["Age_Year"] >= 50:
        recommendations.append("Colorectal Cancer Screening")
        reasons.append("Recommended for adults aged 50 and older to detect early signs of colorectal cancer.")
    if row["Gender"] == 2 and row["Age_Year"] >= 40:
        recommendations.append("Mammogram")
        reasons.append("Recommended for women aged 40 and older to screen for breast cancer.")
    if row["Smoking"] == 1 and row["Age_Year"] >= 55:
        recommendations.append("Lung Cancer Screening")
        reasons.append("Recommended for current or former smokers aged 55 and older to detect lung cancer early.")
    if row["Hypertension_once"] == 1 or row["Hypertension_multiple"] == 1:
        recommendations.append("Blood Pressure Monitoring")
        reasons.append("History of hypertension may increase the risk of heart disease and stroke.")
    if row["High_Cholesterol"] == 1:
        recommendations.append("Cholesterol Screening")
        reasons.append("Individuals with high cholesterol are at an increased risk of cardiovascular disease.")
    if row["Depression_Low_Interest"] >= 2 or row["Depression_Hopeless"] >= 2 or row["Depression_Suicidal"] >= 2:
        recommendations.append("Mental Health Screening")
        reasons.append("Persistent depressive symptoms can indicate major depressive disorder or other mental health concerns.")
    if row["Pregnant"] == 1:
        recommendations.append("Prenatal Screening")
        reasons.append("Pregnant individuals require routine prenatal screenings for fetal and maternal health.")
    if row["Diastolic_1"] >= 90 or row["Systolic_1"] >= 140:
        recommendations.append("Cardiovascular Risk Assessment")
        reasons.append("Elevated blood pressure readings may indicate a risk of cardiovascular disease.")
    if row["Alc_Amount"] >= 14:
        recommendations.append("Alcohol Use Disorder Screening")
        reasons.append("High alcohol consumption can indicate increased health risks and dependency issues.")
    if row["Physical_Sit_Time"] >= 8:
        recommendations.append("Physical Activity Assessment")
        reasons.append("Prolonged sedentary behavior is associated with increased risk of metabolic and cardiovascular diseases.")
    
    return ", ".join(recommendations), ", ".join(reasons)

# Apply screening recommendations
df["Recommended_Screenings"], df["Screening_Reasons"] = zip(*df.apply(recommend_screenings, axis=1))

# Save the modified dataset
output_path = os.path.join(directory, "Modified_Screening_Data.csv")
df.to_csv(output_path, index=False)

print(f"Modified dataset saved at: {output_path}")
