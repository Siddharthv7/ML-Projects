import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Load trained model
with open("iris_model.pkl", "rb") as f:
    scaler, model, target_names = pickle.load(f)

# Load dataset for visualization
iris = load_iris()
X, y = iris.data, iris.target
df = sns.load_dataset("iris")  # seaborn dataset version

# App Title
st.title("🌸 Iris Flower Classification App")
st.write("Predict the type of Iris flower using Machine Learning with visual insights")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to:", ["Prediction", "Data Visualization"])

if option == "Prediction":
    st.header("🔮 Make a Prediction")

    # Input sliders
    sepal_length = st.slider("Sepal Length (cm)", 4.0, 8.0, 5.0)
    sepal_width  = st.slider("Sepal Width (cm)", 2.0, 4.5, 3.0)
    petal_length = st.slider("Petal Length (cm)", 1.0, 7.0, 4.0)
    petal_width  = st.slider("Petal Width (cm)", 0.1, 2.5, 1.0)

    if st.button("Predict"):
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        features = scaler.transform(features)
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0]

        st.success(f"🌼 Predicted Flower: **{target_names[prediction]}**")
        st.write("📊 Prediction Probabilities:")
        for name, p in zip(target_names, prob):
            st.write(f"- {name}: {p:.2f}")

elif option == "Data Visualization":
    st.header("📊 Data Visualizations")

    # Pairplot
    st.subheader("Scatter Matrix (Pairplot)")
    fig1 = sns.pairplot(df, hue="species")
    st.pyplot(fig1)

    # Heatmap
    st.subheader("Feature Correlation Heatmap")
    fig2, ax = plt.subplots()
    sns.heatmap(df.drop(columns="species").corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig2)

    # Confusion Matrix
    st.subheader("Model Performance: Confusion Matrix")
    y_pred = model.predict(scaler.transform(X))
    cm = confusion_matrix(y, y_pred)
    fig3, ax = plt.subplots()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target_names)
    disp.plot(ax=ax, cmap="Blues", values_format="d")
    st.pyplot(fig3)
