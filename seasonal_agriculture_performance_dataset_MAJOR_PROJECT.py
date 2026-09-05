import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline

sns.set_theme(style="whitegrid")
pd.set_option("display.max_columns",None)
pd.set_option("display.float_format",lambda x:f"(x:,.2f)")

#Load the dataset

file_path="/content/seasonal_agriculture_performance_dataset.csv"
df=pd.read_csv(file_path)

print("Dataset loaded successfully.")

#Check the no. of rows and columns
print("No. of rows in dataset : ",df.shape[0])
print("No. of columns in dataset : ",df.shape[1])

#Top 5 rows

df.head(5)

#Bottom 5 rows

df.tail(5)

#Random sample of records

df.sample(5,random_state=40)

#Column names
print(df.columns.tolist())

#Data types and non_null counts

df.info()
#Numerical summary statistics

df.describe()
#Categorical summary

df.describe(include="object")
#Missing values

missing=df.isnull().sum().sort_values(ascending=False)
missing_percentage=(df.isnull().mean()*100).sort_values(ascending=False)

missing_summary=pd.DataFrame({
    "Missing_Count":missing,
    "Missing_Percentage":missing_percentage.round(2)
})

missing_summary[missing_summary["Missing_Count"]>0]
#Visualize missing values

plt.figure(figsize=(12,5))
missing_plot=missing[missing>0]
if len(missing_plot)>0:
  sns.barplot(x=missing_plot.index,y=missing_plot.values)
  plt.xticks(rotation=60,ha="right")
  plt.ylabel("Number of Missing Values")
  plt.xlabel("Column")
  plt.title("Missing Values in Column")
  plt.tight_layout()
  plt.show()
else:
  print("No missing values found in the dataset.")
#Duplicate records

duplicate_count=df.duplicated().sum()
print("Number of duplicated rows:",duplicate_count)
#Remove Duplicate records

df=df.drop_duplicates().reset_index(drop=True)
print("Shape after removing the duplicates",df.shape)
#Check data types again

df.dtypes
#Check the unique values for categorical columns

categorical_columns=df.select_dtypes(include="object").columns

for col in categorical_columns:
  print(f"\n(col):")
  print(df[col].nunique(),"unique values")
  print(df[col].dropna().unique()[:20])
#check missing values after duplicate removal

df.isnull().sum().sort_values(ascending=False).head(10)
# Select all numeric columns from the dataset
numeric_cols = df.select_dtypes(include=np.number).columns

# Fill missing numeric values with the median of each column
for col in numeric_cols:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].median())

# Confirm no missing values remain
print("Remaining missing values:", df.isnull().sum().sum())
# Separate numerical and categorical columns

numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
categorical_columns = df.select_dtypes(include="object").columns.tolist()

print("Numerical columns:")
print(numeric_columns)

print("\nCategorical columns:")
print(categorical_columns)
# Descriptive statistics

stats = df[numeric_columns].describe().T
stats["range"] = stats["max"] - stats["min"]
stats["IQR"] = stats["75%"] - stats["25%"]

stats
# Median and standard deviation

statistical_summary = pd.DataFrame({
    "Mean": df[numeric_columns].mean(),
    "Median": df[numeric_columns].median(),
    "Std_Dev": df[numeric_columns].std(),
    "Min": df[numeric_columns].min(),
    "Max": df[numeric_columns].max()
})

statistical_summary
#Seasonal descriptive summary

season_summary=df.groupby("Season")[numeric_columns].agg(["mean","median","std"])
season_summary
# Univariate: Season distribution

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Season")
plt.title("Record Count Across Seasons")
plt.xlabel("Season")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
# Univariate: Crop distribution

plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="Crop", order=df["Crop"].value_counts().index)
plt.xticks(rotation=45, ha="right")
plt.title("Crop-wise Record Count")
plt.xlabel("Crop Type")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
# Univariate: Yield distribution

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Yield_Tonnes_Ha", kde=True)
plt.title("Spread of Agricultural Yield")
plt.xlabel("Yield (tonnes/ha)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
# Univariate: Profit distribution

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Profit_INR", kde=True)
plt.title("Spread of Farm Profit")
plt.xlabel("Profit (INR)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
# Univariate: Rainfall distribution

plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Rainfall_mm", kde=True)
plt.title("Spread of Rainfall Levels")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
# Univariate: Boxplot for yield

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, y="Yield_Tonnes_Ha")
plt.title("Yield Spread and Possible Outliers")
plt.ylabel("Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
#Univariate: Season distribution (Pie Chart)
plt.figure(figsize=(7, 7))
df['Season'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='viridis')
plt.title('Season-wise Share of Records')
plt.ylabel('')  # Hide the default 'Season' label on the y-axis
plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np

# IQR-based outlier detection for numerical columns

outlier_report_list = [] # Rename to avoid conflict and keep as list

for column in numeric_columns:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr_value = q3 - q1
    lower_limit = q1 - 1.5 * iqr_value
    upper_limit = q3 + 1.5 * iqr_value
    outlier_count = ((df[column] < lower_limit) | (df[column] > upper_limit)).sum()

    outlier_report_list.append({
        "Column": column,
        "Lower_Limit": lower_limit,
        "Upper_Limit": upper_limit,
        "Outlier_Count": outlier_count,
        "Outlier_Pct": round(outlier_count / len(df) * 100, 2)
    })

# Convert the list of dictionaries to a DataFrame and sort after the loop
outlier_report_df = pd.DataFrame(outlier_report_list).sort_values(
    "Outlier_Pct", ascending=False
)

outlier_report_df
# Bivariate: Season vs Yield

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Season", y="Yield_Tonnes_Ha")
plt.title("Yield Spread by Season")
plt.xlabel("Season")
plt.ylabel("Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Bivariate: Season vs Profit

sns.boxplot(data=df, x="Season", y="Profit_INR")
plt.title("Profit Spread by Season")
plt.xlabel("Season")
plt.ylabel("Profit (INR)")
plt.tight_layout()
plt.show()
# Bivariate: Average profit by season

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Season", y="Profit_INR", errorbar=None)
plt.title("Mean Profit by Season (Bar Chart)")
plt.xlabel("Season")
plt.ylabel("Mean Profit (INR)")
plt.tight_layout()
plt.show()
# Bivariate: Season vs Water Usage

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Season", y="Water_Used_m3")
plt.title("Water Usage Spread by Season")
plt.xlabel("Season")
plt.ylabel("Water Used (m³)")
plt.tight_layout()
plt.show()
# Bivariate: Average water usage by season

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="Season", y="Water_Used_m3", errorbar=None)
plt.title("Mean Water Usage by Season (Bar Chart)")
plt.xlabel("Season")
plt.ylabel("Mean Water Used (m³)")
plt.tight_layout()
plt.show()
# Bivariate: Rainfall vs Yield

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Rainfall_mm", y="Yield_Tonnes_Ha", alpha=0.5)
plt.title("Relationship Between Rainfall and Yield")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Bivariate: Farm area vs Production

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Farm_Area_Hectares", y="Production_Tonnes", alpha=0.5)
plt.title("Relationship Between Farm Area and Production")
plt.xlabel("Farm Area (hectares)")
plt.ylabel("Production (tonnes)")
plt.tight_layout()
plt.show()
# Bivariate: Irrigation method vs Yield

plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="Irrigation_Method", y="Yield_Tonnes_Ha", errorbar=None)
plt.title("Mean Yield by Irrigation Method (Bar Chart)")
plt.xlabel("Irrigation Method")
plt.ylabel("Mean Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Multivariate: Season, crop and yield

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Crop", y="Yield_Tonnes_Ha", hue="Season")
plt.xticks(rotation=45, ha="right")
plt.title("Yield by Crop, Split by Season")
plt.xlabel("Crop")
plt.ylabel("Yield (tonnes/ha)")
plt.legend(title="Season")
plt.tight_layout()
plt.show()
# Multivariate: Pair Plot of Key Environmental and Performance Metrics by Season

key_columns = ['Avg_Temperature_C', 'Rainfall_mm', 'Humidity_pct', 'Yield_Tonnes_Ha', 'Profit_INR', 'Season']
sns.pairplot(df[key_columns], hue='Season', palette='viridis', plot_kws={'alpha': 0.6})
plt.suptitle('Environmental and Performance Metrics Across Seasons', y=1.02)  # Adjust suptitle position
plt.tight_layout()
plt.show()
# Multivariate: Season, irrigation and yield

plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Irrigation_Method", y="Yield_Tonnes_Ha", hue="Season")
plt.title("Yield by Irrigation Method, Split by Season")
plt.xlabel("Irrigation Method")
plt.ylabel("Yield (tonnes/ha)")
plt.legend(title="Season")
plt.tight_layout()
plt.show()
# Multivariate: Rainfall, yield and season

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Rainfall_mm",
    y="Yield_Tonnes_Ha",
    hue="Season",
    size="Farm_Area_Hectares",
    sizes=(20, 180),
    alpha=0.65
)
plt.title("Seasonal Variation in Rainfall vs Yield")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Multivariate: Profit, yield and season

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Yield_Tonnes_Ha",
    y="Profit_INR",
    hue="Season",
    size="Farm_Area_Hectares",
    sizes=(20, 180),
    alpha=0.65
)
plt.title("Seasonal Variation in Yield vs Profit")
plt.xlabel("Yield (tonnes/ha)")
plt.ylabel("Profit (INR)")
plt.tight_layout()
plt.show()
# Correlation heatmap for numerical variables

plt.figure(figsize=(16, 12))
correlation_matrix = df[numeric_columns].corr(numeric_only=True)

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    linewidths=0.5
)

plt.title("Correlation Between Numerical Variables")
plt.tight_layout()
plt.show()
# Overall seasonal summary

season_summary = df.groupby("Season").agg(
    Total_Records=("Farm_ID", "count"),
    Avg_Yield=("Yield_Tonnes_Ha", "mean"),
    Total_Production=("Production_Tonnes", "sum"),
    Avg_Profit=("Profit_INR", "mean"),
    Total_Profit=("Profit_INR", "sum"),
    Avg_Water_Used=("Water_Used_m3", "mean")
).round(2)

season_summary
# Crop performance breakdown by season

season_crop_summary = (
    df.groupby(["Season", "Crop"])
    .agg(
        Avg_Yield=("Yield_Tonnes_Ha", "mean"),
        Avg_Profit=("Profit_INR", "mean"),
        Avg_Water_Efficiency=("Water_Efficiency_t_per_1000m3", "mean")
    )
    .round(2)
    .sort_values(["Season", "Avg_Yield"], ascending=[True, False])
)

season_crop_summary
# Visual comparison: Average yield, profit, and water usage across seasons

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.barplot(data=season_summary.reset_index(), x="Season", y="Avg_Yield", ax=axes[0], palette="viridis")
axes[0].set_title("Average Yield by Season")
axes[0].set_ylabel("Yield (tonnes/ha)")

sns.barplot(data=season_summary.reset_index(), x="Season", y="Avg_Profit", ax=axes[1], palette="viridis")
axes[1].set_title("Average Profit by Season")
axes[1].set_ylabel("Profit (INR)")

sns.barplot(data=season_summary.reset_index(), x="Season", y="Avg_Water_Used", ax=axes[2], palette="viridis")
axes[2].set_title("Average Water Usage by Season")
axes[2].set_ylabel("Water Used (m³)")

plt.tight_layout()
plt.show()
# Visual comparison: Total production and total profit across seasons

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.barplot(data=season_summary.reset_index(), x="Season", y="Total_Production", ax=axes[0], palette="mako")
axes[0].set_title("Total Production by Season")
axes[0].set_ylabel("Production (tonnes)")

sns.barplot(data=season_summary.reset_index(), x="Season", y="Total_Profit", ax=axes[1], palette="mako")
axes[1].set_title("Total Profit by Season")
axes[1].set_ylabel("Profit (INR)")

plt.tight_layout()
plt.show()
# Visual comparison: Top-performing crop per season (by average yield)

top_crop_per_season = season_crop_summary.reset_index().sort_values(
    ["Season", "Avg_Yield"], ascending=[True, False]
).groupby("Season").head(1)

plt.figure(figsize=(8, 5))
sns.barplot(data=top_crop_per_season, x="Season", y="Avg_Yield", hue="Crop", dodge=False, palette="Set2")
plt.title("Best-Performing Crop by Season (Highest Avg Yield)")
plt.xlabel("Season")
plt.ylabel("Average Yield (tonnes/ha)")
plt.legend(title="Crop", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
# Regional differences: Average yield and profit by state

region_summary = df.groupby("State").agg(
    Avg_Yield=("Yield_Tonnes_Ha", "mean"),
    Avg_Profit=("Profit_INR", "mean"),
    Total_Production=("Production_Tonnes", "sum")
).round(2).sort_values("Avg_Yield", ascending=False)

region_summary
plt.figure(figsize=(10, 6))
sns.barplot(data=region_summary.reset_index(), x="State", y="Avg_Yield", palette="crest")
plt.xticks(rotation=45, ha="right")
plt.title("Average Yield by State")
plt.xlabel("State")
plt.ylabel("Average Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Crop-specific seasonal yield variation

crop_season_variation = (
    df.groupby(["Crop", "Season"])["Yield_Tonnes_Ha"]
    .mean()
    .unstack()
    .round(2)
)

crop_season_variation["Yield_Range"] = (
    crop_season_variation.max(axis=1) - crop_season_variation.min(axis=1)
)

crop_season_variation.sort_values("Yield_Range", ascending=False)
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="Season", y="Yield_Tonnes_Ha", hue="Crop", marker="o", errorbar=None)
plt.title("Crop-wise Yield Trends Across Seasons")
plt.xlabel("Season")
plt.ylabel("Average Yield (tonnes/ha)")
plt.legend(title="Crop", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
# Economic performance: Cost-to-profit efficiency by season

df["Cost_to_Profit_Ratio"] = df["Total_Cost_INR"] / df["Profit_INR"].replace(0, np.nan)

efficiency_summary = df.groupby("Season").agg(
    Avg_Cost=("Total_Cost_INR", "mean"),
    Avg_Profit=("Profit_INR", "mean"),
    Avg_Cost_to_Profit_Ratio=("Cost_to_Profit_Ratio", "mean")
).round(2)

efficiency_summary
plt.figure(figsize=(8, 5))
sns.barplot(data=efficiency_summary.reset_index(), x="Season", y="Avg_Cost_to_Profit_Ratio", palette="flare")
plt.title("Average Cost-to-Profit Ratio by Season")
plt.xlabel("Season")
plt.ylabel("Cost-to-Profit Ratio")
plt.tight_layout()
plt.show()
# Risk patterns: Disease/pest risk vs yield, by season

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x="Disease_Pest_Risk_pct",
    y="Yield_Tonnes_Ha",
    hue="Season",
    alpha=0.6
)
plt.title("Disease/Pest Risk vs Yield Across Seasons")
plt.xlabel("Disease/Pest Risk (%)")
plt.ylabel("Yield (tonnes/ha)")
plt.tight_layout()
plt.show()
# Average disease/pest risk by season

risk_summary = df.groupby("Season")["Disease_Pest_Risk_pct"].mean().round(2)
risk_summary
