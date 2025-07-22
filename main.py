import streamlit as st
from datetime import date
import psycopg2
import pandas as pd

if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
    st.session_state['name'] = None

form_data = {
    'name': None,
    'category': None,
    'amount': None,
    'date': None
}

def get_connection():
    return psycopg2.connect(
    host="db.lpbkacurlvaqqowqfxhq.supabase.co",
    port = 5432 ,
    dbname="postgres",
    user="postgres",
    password="Database@2007#",
    sslmode="require"

    )


# ---------------------- AUTHENTICATION ----------------------
if not st.session_state['is_logged_in']:
    connection = get_connection()
    tab1, tab2 = st.tabs(['EXISTING USER', 'NEW USER'])

    with tab1:
        st.title('LOGIN USER 💻')
        curs = connection.cursor()

        with st.form(key='login_form'):
            user_name = st.text_input('Enter your user name')
            user_pass = st.text_input('Enter your password', type='password')
            is_done = st.form_submit_button('LOGIN')

        if is_done:
            curs.execute("SELECT * FROM users WHERE user_name = %s AND user_pass = %s", (user_name, user_pass))
            data = curs.fetchall()
            if not data:
                st.warning('🚫 Invalid username or password')
            else:
                st.session_state['name'] = user_name
                st.session_state['is_logged_in'] = True
                st.success('✅ Login Successful')
                st.rerun()

    with tab2:
        st.title('SIGN UP 📋')

        with st.form(key='signup-page'):
            name = st.text_input('Choose your user name')
            passw = st.text_input('Enter your password', type='password')
            is_done = st.form_submit_button('REGISTER')

        if is_done:
            if not name or not passw:
                st.warning('⚠️ Both username and password are required.')
            else:
                try:
                    connection = get_connection()
                    with connection.cursor() as curs:
                        curs.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                                id SERIAL PRIMARY KEY,
                                user_name TEXT UNIQUE NOT NULL,
                                user_pass TEXT NOT NULL
                            );
                        """)
                        curs.execute("SELECT 1 FROM users WHERE user_name = %s", (name,))
                        if curs.fetchone():
                            st.warning(f'🚫 Username "{name}" already exists. Please choose a different one.')
                        else:
                            curs.execute(
                                "INSERT INTO users (user_name, user_pass) VALUES (%s, %s)",
                                (name, passw)
                            )
                            connection.commit()
                            st.success('✅ Registration successful! Please log in.')
                            st.rerun() 
                except Exception as e:
                    st.error(f'❌ Error during registration: {e}')
                finally:
                    connection.close()



# ---------------------- MAIN APP ----------------------
else:
    tab1, tab2, tab3 = st.tabs(['FORM', 'FETCH', 'ANALYSIS'])

    # ---------------------- TAB 1: FORM ----------------------
    with tab1:
        st.title('EXPENSES TRACKER 💻')

        with st.form(key='form'):
            st.subheader('Enter your expenses details ⌨️')
            st.divider()
            form_data['amount'] = st.number_input('Enter the amount spent')
            st.divider()
            form_data['category'] = st.text_input('Expenditure Category')
            st.divider()
            form_data['date'] = date.today()
            is_done = st.form_submit_button('SUBMIT')

            if is_done:
                if not all([form_data['amount'], form_data['category']]):
                    st.warning('⚠️ Please fill all fields')
                else:
                    temp = (
                        str(form_data['date']),
                        st.session_state['name'],
                        form_data['amount'],
                        form_data['category'],
                    )
                    try:
                        connection = get_connection()
                        curs = connection.cursor()
                        curs.execute("""
                            CREATE TABLE IF NOT EXISTS expenses (
                                id SERIAL PRIMARY KEY,
                                date TEXT,
                                name TEXT,
                                amount REAL,
                                category TEXT
                            )
                        """)
                        curs.execute("""
                            INSERT INTO expenses (date, name, amount, category)
                            VALUES (%s, %s, %s, %s)
                        """, temp)
                        connection.commit()
                        st.success('✅ EXPENSE RECORDED 💶')
                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
                    finally:
                        connection.close()

    # ---------------------- TAB 2: FETCH ----------------------
    with tab2:
        st.title('EXPENSES REPORT 💳')

        with st.form(key='fetch_form'):
            st.subheader("Select a date range to fetch expenses 📆")
            st.divider()
            date1 = st.date_input('Start date')
            st.divider()
            date2 = st.date_input('End date')
            st.divider()
            submitted = st.form_submit_button('FETCH')

            if submitted:
                if date1 > date2:
                    st.warning("⚠️ Start date must be before or equal to end date.")
                else:
                    try:
                        connection = get_connection()
                        curs = connection.cursor()
                        curs.execute("""
                            SELECT date, amount, category FROM expenses
                            WHERE name = %s AND date >= %s AND date <= %s
                        """, (st.session_state['name'], str(date1), str(date2)))
                        data = curs.fetchall()
                        if not data:
                            st.info("ℹ️ No expenses found in the selected date range.")
                        else:
                            frame = pd.DataFrame(data=data, columns=['Date', 'Amount', 'Category'])
                            st.dataframe(frame)
                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")
                    finally:
                        connection.close()

    # ---------------------- TAB 3: ANALYSIS ----------------------
    with tab3:
        st.title('Statistical Analysis 📈📈')

        with st.form(key='statistic-form'):
            options = [
                'Total Spent',
                'Average Daily Expenses',
                'Daily Expenses Trend',
                'Highest Single Day Spending',
                'Number of days tracked'
            ]
            selected = st.selectbox("📊 Choose analysis to view", options)
            is_done = st.form_submit_button('ANALYSE')

            if is_done:
                try:
                    connection = get_connection()
                    curs = connection.cursor()
                    curs.execute("""
                        SELECT date, amount, category FROM expenses WHERE name = %s
                    """, (st.session_state['name'],))
                    data = curs.fetchall()
                    frame = pd.DataFrame(data=data, columns=['Date', 'Amount', 'Category'])

                    if frame.empty:
                        st.warning("⚠️ No data found to analyze.")
                    else:
                        frame['Date'] = pd.to_datetime(frame['Date'])

                        if selected == 'Total Spent':
                            total = frame['Amount'].sum()
                            st.write(f'💰 Total Spent: ₹{total}')

                        elif selected == 'Average Daily Expenses':
                            avg_daily = frame.groupby('Date')['Amount'].mean()
                            st.dataframe(avg_daily)

                        elif selected == 'Daily Expenses Trend':
                            daily_trend = frame.groupby('Date')['Amount'].sum().reset_index()
                            st.line_chart(daily_trend.set_index('Date'))

                        elif selected == 'Highest Single Day Spending':
                            daily_total = frame.groupby('Date')['Amount'].sum()
                            max_spend = daily_total.max()
                            max_date = daily_total.idxmax()
                            st.write(f'📅 Highest Spending: ₹{max_spend} on {max_date.date()}')

                        elif selected == 'Number of days tracked':
                            unique_days = frame['Date'].nunique()
                            st.write(f'📆 Number of Days Tracked: {unique_days}')
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")
                finally:
                    connection.close()
