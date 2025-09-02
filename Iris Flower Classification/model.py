import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Load dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = SVC(probability=True, random_state=42)
model.fit(X_train, y_train)

# Save model + scaler + class labels
with open("iris_model.pkl", "wb") as f:
    pickle.dump((scaler, model, iris.target_names), f)

print(" Model trained and saved as iris_model.pkl")
