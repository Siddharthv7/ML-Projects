import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
from streamlit_drawable_canvas import st_canvas
from PIL import Image

# -------------------------------
# 1. Build CNN Model Function
# -------------------------------
def build_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
        MaxPooling2D((2,2)),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D((2,2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model

# -------------------------------
# 2. Streamlit UI
# -------------------------------
st.title("✍️ Handwritten Digit Recognition (MNIST + Drawing Pad)")

menu = st.sidebar.radio("Menu", ["Train Model", "Evaluate Model", "Draw & Predict"])

# -------------------------------
# 3. Load Dataset
# -------------------------------
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize & reshape
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0
y_train_cat = to_categorical(y_train, 10)
y_test_cat = to_categorical(y_test, 10)

# -------------------------------
# 4. Training Section
# -------------------------------
if menu == "Train Model":
    st.header("📊 Train CNN on MNIST")

    epochs = st.slider("Select number of epochs:", 1, 20, 5)
    if st.button("Start Training"):
        model = build_model()
        history = model.fit(x_train, y_train_cat,
                            epochs=epochs,
                            batch_size=128,
                            validation_split=0.1,
                            verbose=0)

        st.success("✅ Training Complete!")
        model.save("saved_model/digit_recognition.h5")

        # Plot Accuracy & Loss
        fig, ax = plt.subplots(1,2, figsize=(12,5))

        ax[0].plot(history.history['accuracy'], label="Train Acc")
        ax[0].plot(history.history['val_accuracy'], label="Val Acc")
        ax[0].set_title("Accuracy")
        ax[0].legend()

        ax[1].plot(history.history['loss'], label="Train Loss")
        ax[1].plot(history.history['val_loss'], label="Val Loss")
        ax[1].set_title("Loss")
        ax[1].legend()

        st.pyplot(fig)

# -------------------------------
# 5. Evaluation Section
# -------------------------------
elif menu == "Evaluate Model":
    st.header("📈 Evaluate Model Performance")

    try:
        model = tf.keras.models.load_model("saved_model/digit_recognition.h5")
        loss, acc = model.evaluate(x_test, y_test_cat, verbose=0)
        st.write(f"✅ Test Accuracy: **{acc*100:.2f}%**")

        # Confusion Matrix
        y_pred = model.predict(x_test)
        y_pred_classes = np.argmax(y_pred, axis=1)

        cm = confusion_matrix(y_test, y_pred_classes)
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        plt.xlabel("Predicted")
        plt.ylabel("True")
        st.pyplot(fig)

        st.text("Classification Report:")
        st.text(classification_report(y_test, y_pred_classes))
    except:
        st.error("⚠️ Train the model first in 'Train Model' section.")

# -------------------------------
# 6. Drawing Pad Section
# -------------------------------
elif menu == "Draw & Predict":
    st.header("🎨 Draw a Digit")

    try:
        model = tf.keras.models.load_model("saved_model/digit_recognition.h5")

        canvas_result = st_canvas(
            fill_color="black",
            stroke_width=15,
            stroke_color="white",
            background_color="black",
            height=280,
            width=280,
            drawing_mode="freedraw",
            key="canvas",
        )

        if canvas_result.image_data is not None:
            img = Image.fromarray((255 - canvas_result.image_data[:, :, 0]).astype("uint8"))
            img = img.resize((28, 28))
            img_array = np.array(img).astype("float32") / 255.0
            img_array = img_array.reshape(1, 28, 28, 1)

            if st.button("Predict Digit"):
                prediction = model.predict(img_array)
                digit = np.argmax(prediction)
                st.success(f"✅ Predicted Digit: {digit}")

                st.bar_chart(prediction[0])
    except:
        st.error("⚠️ Train the model first in 'Train Model' section.")
