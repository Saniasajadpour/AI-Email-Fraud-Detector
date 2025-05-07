# utils/visualization.py

import matplotlib.pyplot as plt
from io import BytesIO
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

def plot_prediction(probability: float, show=True, save_path=None):
    """
    Plots a pie chart showing fraud vs safe prediction.

    Args:
        probability (float): Fraud probability percentage (e.g., 83.4)
        show (bool): Whether to show the chart in a popup window
        save_path (str): If provided, saves the image to this path
    """
    fraud = probability
    safe = 100 - probability

    labels = ['Fraudulent', 'Safe']
    sizes = [fraud, safe]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode the fraud slice

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=140
    )
    ax.axis('equal')  # Equal aspect ratio ensures pie is circular
    plt.title("Fraud Detection Result")

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')

    if show:
        plt.show()

    plt.close()


def plot_pie_chart(label: QLabel, fraud_score: float, safe_score: float):
    """
    Draws a pie chart and displays it inside a QLabel (PyQt6 widget).

    Args:
        label (QLabel): The QLabel to render the pie chart into
        fraud_score (float): Fraud probability score
        safe_score (float): Safe probability score
    """
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [fraud_score, safe_score],
        labels=["Fraudulent", "Safe"],
        colors=["red", "green"],
        autopct="%1.1f%%",
        startangle=90,
        explode=(0.1, 0),
        shadow=True
    )
    ax.axis("equal")

    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close(fig)
    buf.seek(0)

    # Convert buffer to QPixmap and show in QLabel
    pixmap = QPixmap()
    pixmap.loadFromData(buf.read())
    label.setPixmap(pixmap)
    label.setScaledContents(True)
