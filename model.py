from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('stats-all2.csv')

# Drop the specified columns
X = df.drop(['Pharmacy', 'Populations', 'County', 'Result'], axis=1)
y = df['Result']  # Target variable

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Gradient Boosting Classifier
gbm = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Train the model on the training set
gbm.fit(X_train, y_train)

# Make predictions on the test set
y_pred = gbm.predict(X_test)

# Evaluate the model performance
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.8f}")
print(f"Precision: {precision:.8f}")

# Assuming y_pred is the array of predictions and "false" is represented by 0
num_predictions_as_false = sum(y_pred == False)
total_predictions = len(y_pred)

proportion_as_false = num_predictions_as_false / total_predictions

print(f"Proportion of Predictions as 'False': {proportion_as_false:.8f}")