import plotly.express as px
import streamlit as st
import pandas as pd
from datetime import datetime

from database import create_table, add_task, get_tasks, mark_task_completed, delete_task
from planner import calculate_priority
from pomodoro import get_pomodoro_sessions


create_table()

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="📚",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc, #eef2ff);
        color: #1e293b;
    }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #475569;
        margin-bottom: 25px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .metric-card {
        background: linear-gradient(135deg, #6366f1, #3b82f6);
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }

    .metric-number {
        font-size: 28px;
        font-weight: 800;
    }

    .metric-label {
        font-size: 13px;
        opacity: 0.9;
    }

    .task-card {
        background: #f9fafb;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
    }

    .task-title {
        font-size: 17px;
        font-weight: 700;
        color: #111827;
    }

    .task-meta {
        font-size: 14px;
        color: #475569;
        margin-top: 6px;
    }

    .badge-pending {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #fef3c7;
        color: #92400e;
        font-size: 12px;
        font-weight: 600;
    }

    .badge-completed {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-size: 12px;
        font-weight: 600;
    }

    .highlight-box {
        background: #e0f2fe;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #bae6fd;
        color: #0c4a6e;
        margin-bottom: 20px;
    }

    div[data-testid="stDataFrame"] {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        padding: 5px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: 600;
        background: #3b82f6;
        color: white;
    }

    .stButton > button:hover {
        background: #2563eb;
    }

    .stTextInput input, .stDateInput input, .stNumberInput input {
        border-radius: 10px !important;
    }

</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown('<div class="main-title">📚 Smart Study Planner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Plan smarter, prioritize better, and stay consistent with focused study sessions.</div>',
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Task", "Smart Planner", "Complete Task", "Delete Task"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Planner Tips")
st.sidebar.markdown("""
- Add realistic deadlines  
- Use difficulty honestly  
- Keep importance meaningful  
- Check Smart Planner daily  
""")


def make_task_dataframe(tasks):
    return pd.DataFrame(tasks, columns=[
        "ID", "Subject", "Task Name", "Deadline", "Estimated Hours",
        "Difficulty", "Importance", "Status", "Created At"
    ])


# ---------- DASHBOARD ----------
if menu == "Dashboard":
    tasks = get_tasks()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Overview")

    if tasks:
        df = make_task_dataframe(tasks)

        completed_count = len(df[df["Status"] == "Completed"])
        pending_count = len(df[df["Status"] == "Pending"])
        total_tasks = len(df)

        overdue_count = 0
        today = datetime.today().date()

        for _, row in df.iterrows():
            deadline_date = datetime.strptime(row["Deadline"], "%Y-%m-%d").date()
            if row["Status"] == "Pending" and deadline_date < today:
                overdue_count += 1

        # Metrics
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-number">{total_tasks}</div><div class="metric-label">Total Tasks</div></div>',
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-number">{pending_count}</div><div class="metric-label">Pending</div></div>',
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-number">{completed_count}</div><div class="metric-label">Completed</div></div>',
                unsafe_allow_html=True
            )
        with c4:
            st.markdown(
                f'<div class="metric-card"><div class="metric-number">{overdue_count}</div><div class="metric-label">Overdue</div></div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Table
        st.subheader("All Tasks")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Progress Bar
        progress = completed_count / total_tasks if total_tasks > 0 else 0
        st.subheader("Overall Progress")
        st.progress(progress)
        st.write(f"{int(progress * 100)}% completed")

        # Pie Chart
        status_counts = df["Status"].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Task Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Bar Chart
        subject_hours = df.groupby("Subject")["Estimated Hours"].sum().reset_index()
        fig2 = px.bar(
            subject_hours,
            x="Subject",
            y="Estimated Hours",
            title="Workload by Subject",
            color="Subject"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Overdue Tasks
        st.subheader("Overdue Tasks")

        overdue_tasks = []

        for _, row in df.iterrows():
            deadline_date = datetime.strptime(row["Deadline"], "%Y-%m-%d").date()
            if row["Status"] == "Pending" and deadline_date < today:
                overdue_tasks.append(row)

        if overdue_tasks:
            for task in overdue_tasks:
                st.error(f"{task['Task Name']} ({task['Subject']}) is overdue!")
        else:
            st.success("No overdue tasks 🎉")

    else:
        st.info("No tasks added yet.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Quick View Cards
    if tasks:
        st.subheader("Quick Task View")
        df = make_task_dataframe(tasks)

        for _, row in df.iterrows():
            badge = '<span class="badge-completed">Completed</span>' if row["Status"] == "Completed" else '<span class="badge-pending">Pending</span>'

            st.markdown(f"""
            <div class="task-card">
                <div class="task-title">{row["Task Name"]}</div>
                <div class="task-meta">
                    Subject: <b>{row["Subject"]}</b><br>
                    Deadline: {row["Deadline"]}<br>
                    Estimated Hours: {row["Estimated Hours"]}<br>
                    Difficulty: {row["Difficulty"]}/5<br>
                    Importance: {row["Importance"]}/5<br>
                    Status: {badge}
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu == "Add Task":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Add New Task")

    col1, col2 = st.columns(2)

    with col1:
        subject = st.text_input("Subject")
        task_name = st.text_input("Task Name")
        deadline = st.date_input("Deadline")

    with col2:
        estimated_hours = st.number_input("Estimated Hours", min_value=0.5, step=0.5)
        difficulty = st.slider("Difficulty (1-5)", 1, 5, 3)
        importance = st.slider("Importance (1-5)", 1, 5, 3)

    if st.button("Add Task"):
        if subject.strip() == "" or task_name.strip() == "":
            st.error("Subject and Task Name cannot be empty.")
        else:
            add_task(
                subject=subject.strip(),
                task_name=task_name.strip(),
                deadline=str(deadline),
                estimated_hours=estimated_hours,
                difficulty=difficulty,
                importance=importance
            )
            st.success("Task added successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
# ---------- SMART PLANNER ----------
elif menu == "Smart Planner":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Smart Planner Recommendations")

    tasks = get_tasks()
    smart_tasks = []

    for task in tasks:
        task_id, subject, task_name, deadline, estimated_hours, difficulty, importance, status, created_at = task

        if status == "Pending":
            priority_score = calculate_priority(deadline, difficulty, importance, estimated_hours)
            pomodoro_sessions = get_pomodoro_sessions(estimated_hours)

            smart_tasks.append([
                task_id,
                subject,
                task_name,
                deadline,
                estimated_hours,
                difficulty,
                importance,
                priority_score,
                pomodoro_sessions
            ])

    if smart_tasks:
        df = pd.DataFrame(smart_tasks, columns=[
            "ID", "Subject", "Task Name", "Deadline", "Estimated Hours",
            "Difficulty", "Importance", "Priority Score", "Pomodoro Sessions"
        ])

        df = df.sort_values(by="Priority Score", ascending=False)

        top_task = df.iloc[0]

        st.markdown(f"""
        <div class="highlight-box">
            <b>Best Task to Start Now:</b><br><br>
            {top_task['Task Name']} ({top_task['Subject']})<br>
            Priority Score: {top_task['Priority Score']}<br>
            Pomodoro Sessions Needed: {top_task['Pomodoro Sessions']}
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True, hide_index=True)

    else:
        st.info("No pending tasks found.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- COMPLETE TASK ----------
elif menu == "Complete Task":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Mark Task as Completed")

    tasks = get_tasks()
    pending_tasks = [task for task in tasks if task[7] == "Pending"]

    if pending_tasks:
        task_options = {
            f"{task[0]} - {task[2]} ({task[1]})": task[0]
            for task in pending_tasks
        }

        selected_task = st.selectbox("Select Task", list(task_options.keys()))

        if st.button("Mark as Completed"):
            task_id = task_options[selected_task]
            mark_task_completed(task_id)
            st.success("Task marked as completed.")
            st.rerun()
    else:
        st.info("No pending tasks available.")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- DELETE TASK ----------
elif menu == "Delete Task":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Delete Task")

    tasks = get_tasks()

    if tasks:
        task_options = {
            f"{task[0]} - {task[2]} ({task[1]})": task[0]
            for task in tasks
        }

        selected_task = st.selectbox("Select Task to Delete", list(task_options.keys()))

        if st.button("Delete Task"):
            task_id = task_options[selected_task]
            delete_task(task_id)
            st.warning("Task deleted successfully.")
            st.rerun()
    else:
        st.info("No tasks available to delete.")

    st.markdown('</div>', unsafe_allow_html=True)