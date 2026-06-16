import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    """
    Initializes and caches the Supabase client using Streamlit secrets.
    """
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        if key == "YOUR_SUPABASE_ANON_PUBLIC_KEY" or not key:
            st.warning("⚠️ Please configure your actual Supabase Anon API Key in `.streamlit/secrets.toml`.")
            st.stop()
        return create_client(url, key)
    except KeyError:
        st.error("Supabase credentials not found in secrets.toml! Please check `.streamlit/secrets.toml`.")
        st.stop()
    except Exception as e:
        st.error(f"Error connecting to Supabase: {e}")
        st.stop()

# Export client instance
db = get_supabase_client()


# --- Database Helper Functions (Examples for you to implement) ---

def check_teacher_exists(username: str):
    """
    Check if a teacher with the given username already exists in the 'teachers' table.
    """
    try:
        response = db.table("teachers").select("username").eq("username", username).execute()
        return len(response.data) > 0
    except Exception as e:
        st.error(f"Error checking teacher existence: {e}")
        return False

def get_all_students():
    """
    Fetch all students from the 'students' table.
    """
    try:
        response = db.table("students").select("*").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching students: {e}")
        return []

def create_student(student_data: dict):
    """
    Insert a new student into the 'students' table.
    """
    try:
        response = db.table("students").insert(student_data).execute()
        return response.data
    except Exception as e:
        st.error(f"Error creating student: {e}")
        return None

def get_student_subjects(student_id: str):
    """
    Fetch all subjects that a student is enrolled in.
    """
    try:
        # Assumes a join table or structure, adjust to your schema
        response = db.table("enrollments").select("*, subjects(*)").eq("student_id", student_id).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching enrolled subjects: {e}")
        return []

def get_student_attendance(student_id: str):
    """
    Fetch attendance records for a student.
    """
    try:
        response = db.table("attendance").select("*").eq("student_id", student_id).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching attendance: {e}")
        return []

def unenroll_student_to_subject(student_id: str, subject_id: str):
    """
    Remove enrollment of a student from a subject.
    """
    try:
        response = db.table("enrollments").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
        return response.data
    except Exception as e:
        st.error(f"Error unenrolling student: {e}")
        return None


def check_teacher_exists(username):
    resp