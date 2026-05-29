
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Read the Dataset CSV file into a DataFrame
df = pd.read_csv("data/Megastore_Dataset_Task_3 3.csv")

# Encoding categorical variables
cat_cols = ['OrderID', 'OrderPriority', 'Region', 'ExpeditedShipping', 'PaymentMethod', 'CustomerOrderSatisfaction']
df_cat = df[cat_cols].copy()

# Ordinal encoding for ordinal variables
priority_map = {
    'Medium': 1,
    'High': 2
}

df_cat['OrderPriority'] = df_cat['OrderPriority'].map(priority_map)

satisfaction_map = {
    'Prefer not to answer': 0,
    'Very Dissatisfied': 1,
    'Dissatisfied': 2,
    'Satisfied': 3,
    'Very Satisfied': 4
}

df_cat['CustomerOrderSatisfaction'] = df_cat['CustomerOrderSatisfaction'].map(satisfaction_map)

# one-hot encoding for nominal variables
df_encoded = pd.get_dummies(df_cat, columns=['Region', 'ExpeditedShipping', 'PaymentMethod'],
                          prefix=['Region', 'ExpeditedShipping', 'PayWith'])

# Groupby by OrderID so each row is a single transaction
df_encoded = df_encoded.groupby('OrderID').agg(lambda x: x.max()).reset_index()

#dropping unnecessary columns
df_encoded = df_encoded.drop(['ExpeditedShipping_No'], axis=1).astype(int)

# Save the encoded dataset to a CSV file
df_encoded.to_csv("data/EncodedCategoricalVars.csv", index=False)

# ================== Market Basket Analysis (MBA) ===================
# Preparing the Dataset for MBA
df_vars = df[['OrderID', 'ProductName']]

# One-hot encoded on ProductName column
df_dummies = pd.get_dummies(df_vars, columns=['ProductName'], prefix=[''])

# Transactionalize the data by Groupby OrderID
df_trans = df_dummies.groupby('OrderID').agg(lambda x: x.max()).reset_index()
# dropping unnecessary columns
df_trans = df_trans.drop(['OrderID'], axis=1).astype(int)

# Save the encoded dataset to a CSV file
df_trans.to_csv("data/TransactionalDataset.csv", index=False)

# Apriori ===== Minimum support threshold (e.g., 0.05 = 5% of transactions)
frequent_itemsets = apriori(df_trans, min_support=0.05, use_colnames=True)

# Generate rules with confidence threshold (e.g., 0.6)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

# View rules
filtered_rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].sort_values(by='support', ascending=False)
pd.set_option('display.max_columns', None)
print(50*'=' + ' Association Rules')
print(filtered_rules.head())

