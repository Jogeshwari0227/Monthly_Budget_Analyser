import pandas as pd
import matplotlib.pyplot as plt


#Load the data set
data = pd.read_csv('financial_data.csv')
print("Data Loaded Successfully:\n", data)

#Display first few rows from data set
print(data.head(4))

#Show basic dataset info
print(data.info())

#Convert 'Date' column to datetime format for further analysis 
# data["Date"] = pd.to_datetime(data["Date"])

data["Date"] = pd.to_datetime(
    data["Date"],
    dayfirst=True,
    errors="coerce"
)


#Check if 'Amount' has only  numeric values
if data["Amount"].dtype != 'int64' or data["Amount"].dtype != 'float64':
    data["Amount"] = pd.to_numeric(data["Amount"], errors='coerce')

#check & handle missing values
if data.isnull().values.any():
    print("Missing values found. Handling missing values...")
    # Example: Drop rows with missing 'Amount' values.
    # Because amount can't  be replaced with an average value.
    data_cleaned = data.dropna(subset=["Amount"])
    print("After Data Cleaning:\n", data_cleaned)

#Create 2 data frames
income_df = data_cleaned[data_cleaned["Type"] == "Income"]
expense_df = data_cleaned[data_cleaned["Type"] == "Expense"]

#Calculate total income and total expense
print("Income DataFrame:\n", income_df)
total_income = income_df["Amount"].sum() 
print("Total Income: ", total_income)   
print("Expense DataFrame:\n", expense_df)
total_expense = expense_df["Amount"].sum()
print("Total Expense: ", total_expense)

#Calculate Monthly income, expenses and savings
# data_cleaned["Month"] = data_cleaned["Date"].dt.to_period("M")
# print("Grouped by month data:",data_cleaned.groupby("Month"))

# ------------------ MONTHLY ANALYSIS ------------------ #

# Create Month column for monthly grouping
data_cleaned.loc[:, "Month"] = data_cleaned["Date"].dt.to_period("M")

# Separate monthly income and expense
monthly_income = (
    data_cleaned[data_cleaned["Type"] == "Income"]
    .groupby("Month")["Amount"]
    .sum()
)

monthly_expense = (
    data_cleaned[data_cleaned["Type"] == "Expense"]
    .groupby("Month")["Amount"]
    .sum()
)

# Combine both into one DataFrame
monthly_summary = pd.DataFrame({
    "Monthly Income": monthly_income,
    "Monthly Expense": monthly_expense
})

# Calculate savings
monthly_summary["Savings"] = (
    monthly_summary["Monthly Income"] - monthly_summary["Monthly Expense"]
)

print("\nMonthly Financial Summary:\n")
print(monthly_summary)

monthly_summary[["Monthly Income", "Monthly Expense"]].plot(kind="bar")

plt.title("Monthly Income vs Monthly Expense")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()