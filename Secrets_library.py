import secrets
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_secure_transaction_data(num_transactions, num_customers=100, num_categories=5):
    # Generate secure unique IDs for transactions
    transaction_ids = [secrets.token_hex(8) for _ in range(num_transactions)]
    
    # Generate random customer IDs
    customer_ids = [secrets.token_hex(4) for _ in range(num_customers)]
    customers = np.random.choice(customer_ids, num_transactions)
    
    # Generate timestamps within the past 30 days for each transaction
    start_date = datetime.now() - timedelta(days=30)
    timestamps = [start_date + timedelta(days=np.random.randint(30), 
                                         seconds=np.random.randint(86400)) for _ in range(num_transactions)]
    
    # Generate random purchase amounts between $10 and $1000
    purchase_amounts = np.random.uniform(10, 1000, num_transactions)
    
    # Generate random product categories
    categories = [f"Category_{i+1}" for i in range(num_categories)]
    product_categories = np.random.choice(categories, num_transactions)
    
    # Create a DataFrame with the generated data
    df = pd.DataFrame({
        'TransactionID': transaction_ids,
        'CustomerID': customers,
        'Timestamp': timestamps,
        'PurchaseAmount': purchase_amounts,
        'ProductCategory': product_categories
    })
    
    return df

def analyze_transaction_data(df):
    # Basic statistics on PurchaseAmount
    average_purchase = np.mean(df['PurchaseAmount'])
    max_purchase = np.max(df['PurchaseAmount'])
    min_purchase = np.min(df['PurchaseAmount'])
    total_volume = np.sum(df['PurchaseAmount'])
    
    print("=== Transaction Data Analysis ===")
    print(f"Total Transaction Volume: ${total_volume:.2f}")
    print(f"Average Purchase Amount: ${average_purchase:.2f}")
    print(f"Maximum Purchase Amount: ${max_purchase:.2f}")
    print(f"Minimum Purchase Amount: ${min_purchase:.2f}")
    print()
    
    # Transactions per category
    category_counts = df['ProductCategory'].value_counts()
    print("Transactions per Category:")
    print(category_counts)
    print()
    
    # Average Purchase per Customer
    customer_avg_purchase = df.groupby('CustomerID')['PurchaseAmount'].mean()
    print("Average Purchase per Customer:")
    print(customer_avg_purchase.head())  # Display top 5 for brevity
    print()
    
    # Number of Transactions per Customer
    customer_transaction_counts = df['CustomerID'].value_counts()
    print("Number of Transactions per Customer:")
    print(customer_transaction_counts.head())  # Display top 5 for brevity
    print()
    
def filter_and_aggregate_transactions(df, min_amount=50, max_amount=500, start_date=None, end_date=None, category=None):
    # Filter by purchase amount
    filtered_df = df[(df['PurchaseAmount'] >= min_amount) & (df['PurchaseAmount'] <= max_amount)]
    
    # Filter by date range if specified
    if start_date:
        filtered_df = filtered_df[filtered_df['Timestamp'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Timestamp'] <= end_date]
    
    # Filter by product category if specified
    if category:
        filtered_df = filtered_df[filtered_df['ProductCategory'] == category]
    
    # Aggregate data
    total_filtered_volume = np.sum(filtered_df['PurchaseAmount'])
    avg_filtered_purchase = np.mean(filtered_df['PurchaseAmount'])
    transaction_count = len(filtered_df)
    
    print("=== Filtered Transaction Data ===")
    print(f"Total Volume (Filtered): ${total_filtered_volume:.2f}")
    print(f"Average Purchase Amount (Filtered): ${avg_filtered_purchase:.2f}")
    print(f"Number of Transactions (Filtered): {transaction_count}")
    print()
    
    return filtered_df

# Main Program Execution
num_transactions = 100000  # Example of a medium-power workload
transaction_data = generate_secure_transaction_data(num_transactions)

# Analyze the generated transaction data
analyze_transaction_data(transaction_data)

# Filter and aggregate transactions for a detailed view
filtered_data = filter_and_aggregate_transactions(
    transaction_data, 
    min_amount=100, 
    max_amount=300, 
    start_date=datetime.now() - timedelta(days=15), 
    end_date=datetime.now(), 
    category='Category_1'
)

# Display the first few rows of the filtered data
print(filtered_data.head())
