# 💸 Expense Tracker App with Streamlit + PostgreSQL + Supabase

A full-featured expense tracking app built using **Streamlit** for the frontend and **PostgreSQL** (hosted on **Supabase**) as the backend. This app allows users to register, log in, add daily expenses, fetch records by date range, and perform clean data analysis — all within a beautifully responsive interface.

---

## 🚀 Features Built

- 🔐 **User Authentication System**
  - New User Registration with unique username validation
  - Existing User Login with session state tracking

- 🧾 **Expense Form**
  - Enter amount, category, and auto-filled date field
  - Data inserted into PostgreSQL table in real-time

- 📅 **Fetch Expenses**
  - Date-range filter to view past expenses by category and amount
  - Tabular view using Pandas and Streamlit's UI components

- 📊 **Analytics Dashboard**
  - Total Amount Spent
  - Average Daily Expenses
  - Daily Trend Line Chart
  - Highest Single Day Spending
  - Number of Days Tracked

- 💾 **Supabase Integration**
  - PostgreSQL DB hosted and connected securely using SSL mode
  - Tables created dynamically if not exist

---

## 🛠️ Tech Stack Used

- **Frontend:** Streamlit
- **Backend:** Python + psycopg2
- **Database:** PostgreSQL via Supabase
- **Data Analysis:** Pandas
- **Visualization:** Streamlit charts and dataframes

---

## 📁 Project Structure

```
expense-tracker/
├── app.py               # Streamlit application code
├── requirements.txt     # Dependencies (Streamlit, psycopg2, pandas)
├── README.md            # Project documentation
└── screenshots/         # (Optional) UI images
```

---

## 👨‍💻 Author
> Streamlit + SQL + Clean UI + Analysis — All Integrated in One App
Built with ❤️ by Raghuveer Karanam
