import pandas as pd
import matplotlib.pyplot as plt
import os


main_folder_path = os.path.abspath(os.path.dirname(__file__))


file_path = os.path.join(main_folder_path, 'bank.csv')  # Reference the dataset directly in the main folder
data = pd.read_csv(file_path)

# Age Group Segmentation
data['age_group'] = pd.cut(data['age'], bins=[18, 30, 40, 50, 60, 100], 
                           labels=['18-30', '31-40', '41-50', '51-60', '61+'])

# Churn Analysis
churn_by_age = (
    data[data['deposit'] == 'no']
    .groupby('age_group', observed=False)
    .size()
    / data.groupby('age_group', observed=False).size()
) * 100

low_balance_churn = len(data[(data['deposit'] == 'no') & (data['balance'] < 1000)]) / len(data) * 100
high_balance_churn = len(data[(data['deposit'] == 'no') & (data['balance'] >= 1000)]) / len(data) * 100

# Loan Default Analysis
default_rate = len(data[data['default'] == 'yes']) / len(data) * 100
default_churn_rate = len(data[(data['default'] == 'yes') & (data['deposit'] == 'no')]) / len(data[data['default'] == 'yes']) * 100

# Campaign Effectiveness
average_calls_success = data[data['deposit'] == 'yes']['campaign'].mean()
average_call_duration_success = data[data['deposit'] == 'yes']['duration'].mean()

# Month-Wise Subscription Rate
subscription_rate_by_month = data[data['deposit'] == 'yes'].groupby('month').size() / data.groupby('month').size() * 100

# Loan Impact on Subscription
loaned_customers = data[(data['loan'] == 'yes') | (data['housing'] == 'yes')]
loan_subscription_rate = len(loaned_customers[loaned_customers['deposit'] == 'yes']) / len(loaned_customers) * 100

# Results
print("Churn by Age Group:\n", churn_by_age)
print(f"Low Balance Churn Rate: {low_balance_churn:.2f}%")
print(f"High Balance Churn Rate: {high_balance_churn:.2f}%")
print(f"Default Rate: {default_rate:.2f}%")
print(f"Default Churn Rate: {default_churn_rate:.2f}%")
print(f"Average Calls for Success: {average_calls_success:.2f}")
print(f"Average Call Duration for Success: {average_call_duration_success:.2f} seconds")
print("Subscription Rate by Month:\n", subscription_rate_by_month)
print(f"Loan Subscription Rate: {loan_subscription_rate:.2f}%")

# Visualizations
def visualize_churn_by_age(churn_by_age):
    plt.figure(figsize=(8, 5))
    churn_by_age.plot(kind='bar', color='skyblue')
    plt.title("Churn Rate by Age Group")
    plt.ylabel("Churn Rate (%)")
    plt.xlabel("Age Group")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(main_folder_path, 'churn_by_age.png'))
    plt.show()

def visualize_balance_churn(low_balance_churn, high_balance_churn):
    labels = ['Low Balance (< €1000)', 'High Balance (≥ €1000)']
    values = [low_balance_churn, high_balance_churn]
    plt.figure(figsize=(6, 5))
    plt.bar(labels, values, color=['salmon', 'lightgreen'])
    plt.title("Churn Rate by Balance")
    plt.ylabel("Churn Rate (%)")
    plt.ylim(0, 50)
    plt.tight_layout()
    plt.savefig(os.path.join(main_folder_path, 'churn_by_balance.png'))
    plt.show()

def visualize_subscription_by_month(subscription_rate_by_month):
    plt.figure(figsize=(8, 5))
    subscription_rate_by_month.sort_index().plot(kind='bar', color='orange')
    plt.title("Subscription Rate by Month")
    plt.ylabel("Subscription Rate (%)")
    plt.xlabel("Month")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(main_folder_path, 'subscription_by_month.png'))
    plt.show()

def visualize_campaign_effectiveness(average_calls_success, average_call_duration_success):
    metrics = ['Avg Calls (Success)', 'Avg Call Duration (Success)']
    values = [average_calls_success, average_call_duration_success]
    plt.figure(figsize=(6, 5))
    plt.bar(metrics, values, color=['blue', 'purple'])
    plt.title("Campaign Effectiveness Metrics")
    plt.ylabel("Metric Value")
    plt.tight_layout()
    plt.savefig(os.path.join(main_folder_path, 'campaign_effectiveness.png'))
    plt.show()

def visualize_loan_subscription_rate(loan_subscription_rate):
    labels = ['Subscribed (with Loans)', 'Not Subscribed']
    values = [loan_subscription_rate, 100 - loan_subscription_rate]
    plt.figure(figsize=(6, 5))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['lightblue', 'lightgray'], startangle=90)
    plt.title("Loan Subscription Rate")
    plt.tight_layout()
    plt.savefig(os.path.join(main_folder_path, 'loan_subscription_rate.png'))
    plt.show()


visualize_churn_by_age(churn_by_age)
visualize_balance_churn(low_balance_churn, high_balance_churn)
visualize_subscription_by_month(subscription_rate_by_month)
visualize_campaign_effectiveness(average_calls_success, average_call_duration_success)
visualize_loan_subscription_rate(loan_subscription_rate)




