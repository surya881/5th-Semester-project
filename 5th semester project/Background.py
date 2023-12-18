import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
from joblib import load

class BitcoinPricePredictor:
    def __init__(self, root):
        self.model = load("your_model.joblib")
        self.root = root
        self.root.title("Bitcoin Price Prediction Dashboard")
        self.root.geometry("1200x750")
        self.setup_background()
        self.setup_ui()

    def setup_background(self):
        photo = Image.open('background_image.jpg')
        img = ImageTk.PhotoImage(photo)
        lbl_bk = tk.Label(self.root, image=img)
        lbl_bk.image = img
        lbl_bk.place(relx=0.5, rely=0.5, anchor='center')

    def setup_ui(self):
        frame = tk.Frame(self.root, bg='sky blue')
        frame.place(relx=0.5, rely=0.5, anchor='center')

        title_label = ttk.Label(frame, text="Bitcoin Price Prediction Input Form", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=15)

        labels = ['Open', 'High', 'Low', 'Close']
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(frame, text=f"{label}:", anchor='e').grid(row=i+1, column=0, padx=15, pady=15)
            entries[label] = ttk.Entry(frame)
            entries[label].grid(row=i+1, column=1, padx=15, pady=15, sticky='ew')

        predict_button = ttk.Button(frame, text="Predict", command=lambda: self.on_predict_click(entries))
        predict_button.grid(row=len(labels)+1, column=0, columnspan=2, pady=15)

        self.result_text = tk.StringVar()
        result_label = tk.Label(frame, textvariable=self.result_text, font=('Helvetica', 12, 'bold'), bg='white', bd=1, relief='solid')
        result_label.grid(row=len(labels) + 2, column=0, columnspan=2, pady=15)

    def predict_price(self, open_price, high_price, low_price, close_price):
        try:
            open_price = float(open_price)
            high_price = float(high_price)
            low_price = float(low_price)
            close_price = float(close_price)
            input_data = np.array([[open_price, high_price, low_price, close_price]])
            predicted_price = self.model.predict(input_data)
            return float(predicted_price)
        except ValueError:
            return None

    def on_predict_click(self, entries):
        try:
            open_price = entries['Open'].get()
            high_price = entries['High'].get()
            low_price = entries['Low'].get()
            close_price = entries['Close'].get()
            predicted_price = self.predict_price(open_price, high_price, low_price, close_price)
            if predicted_price is not None:
                predicted_price /= 10000
                self.result_text.set(f"${predicted_price:.2f}")
            else:
                messagebox.showerror("Error", "Please enter valid numerical values for all fields.")

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values for all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BitcoinPricePredictor(root)
    root.mainloop()
