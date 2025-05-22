import streamlit as st
import pandas as pd
from db import init_db
import sqlite3
from datetime import date
import time

init_db()

st.title("🏋️ Workout Planner + Timer")

menu = st.sidebar.radio("Menu", ["Create Routine", "Start Workout", "History"])

if menu == "Create Routine":
    st.header("📝 Create Workout Routine")
    routine_name = st.text_input("Routine Name")
    exercise = st.text_input("Exercise")
    sets = st.number_input("Sets", 1, 10, 3)
    reps = st.number_input("Reps", 1, 100, 12)
    duration = st.number_input("Duration (sec)", 0, 600, 0)

    if st.button("Add to Routine"):
        conn = sqlite3.connect("workout.db")
        conn.execute("INSERT INTO workouts (date, routine_name, exercise, sets, reps, duration) VALUES (?, ?, ?, ?, ?, ?)",
                     (str(date.today()), routine_name, exercise, sets, reps, duration))
        conn.commit()
        conn.close()
        st.success("Exercise added to routine.")

if menu == "Start Workout":
    st.header("🏃 Start Workout")

    routine = st.text_input("Enter Routine Name to Load")
    if st.button("Load Routine"):
        conn = sqlite3.connect("workout.db")
        df = pd.read_sql_query("SELECT * FROM workouts WHERE routine_name = ?", conn, params=(routine,))
        conn.close()

        if df.empty:
            st.warning("No such routine found.")
        else:
            st.success("Routine Loaded!")
            for index, row in df.iterrows():
                st.subheader(f"{row['exercise']} - {row['sets']} sets x {row['reps']} reps")
                if row['duration'] > 0:
                    if st.button(f"Start {row['exercise']} Timer", key=index):
                        with st.empty():
                            for sec in range(int(row['duration']), 0, -1):
                                st.metric("Time Remaining", f"{sec} sec")
                                time.sleep(1)
                            st.success("Done!")

if menu == "History":
    st.header("📅 Workout History")
    conn = sqlite3.connect("workout.db")
    df = pd.read_sql_query("SELECT * FROM workouts ORDER BY date DESC", conn)
    conn.close()
    st.dataframe(df)
