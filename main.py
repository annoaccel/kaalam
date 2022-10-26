import streamlit as st
import pandas as pd
#import cv2
import hashlib

from file_uploads import file_upload
from input_form import *

from video_clip_create import Streaming_cloud_storage_2

# from face_detect import *

st.set_page_config(page_title="Avistos", page_icon="🖖")


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)")


def add_userdata(username, password):
    c.execute(
        "INSERT INTO userstable(username,password) VALUES (?,?)", (username, password)
    )
    conn.commit()


def login_user(username, password):
    c.execute(
        "SELECT * FROM userstable WHERE username =? AND password = ?",
        (username, password),
    )
    data = c.fetchall()
    return data


def view_all_users():
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data


def main():
    st.image("./tm.jpg")
    st.title("timesense")

    menu = ["Home", "Login", "SignUp", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("timesense")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type="password")

        st.sidebar.checkbox("Login-As- Avistos")
        st.sidebar.checkbox("Login-As- Client")

        if st.sidebar.checkbox("Login"):

            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox(
                    "Task", ["Analytics", "Profiles", "Time Series Analysis"]
                )

                if task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(
                        user_result, columns=["Username", "Password"]
                    )
                    st.dataframe(clean_db)

                elif task == "Time Series Analysis":

                    # st.image('./logo.png')
                    st.title("time sese")
                    # st.subheader('Video Data Save Options')

                    genre = st.radio(
                        "Save To S3", ("60-Seconds", "120-Seconds", "240-Seconds")
                    )

                    if genre == "60-Seconds":
                        st.write("Selcted 1-Min Video to Save to S3")
                    elif genre == "120-Seconds":
                        st.write("Selcted 2-Mins Video to Save to S3")
                    elif genre == "240-Seconds":
                        st.write("Selcted 4-Mins Video to Save to S3")

                    prod_options = st.radio(
                        "Select Product Options",
                        (
                            "Welcome",
                            "File Upload",
                            "EDA",
                            "Streaming with OD",
                            "Streaming with cloud storage",
                            "Streaming with OD and cloud storage",
                            "Streaming With OD and Tracking",
                        ),
                    )
                    if prod_options == "welcome":
                        pass
                    elif prod_options == "File Upload":
                        st.write("File Upload")
                        file_upload()

                    elif prod_options == "EDA":
                        st.write("Please Enter the IP Addresses")
                        only_streaming(username)

                    elif prod_options == "Streaming with OD":
                        st.write("Object Detection")
                        streaming_od(username)

                    elif prod_options == "Streaming with cloud storage":

                        st.write("streaming with s3 storage ")

                        # p1 = Process(target=Streaming_cloud_storage(username, path))

                        # p2 = Process(
                        #     target=Streaming_cloud_storage_2(
                        #         cameralist, frames_per_videoclip, path
                        #     )
                        # )
                        # p1.start()
                        # p2.start()
                        # Streaming_cloud_storage(username, path)

                    elif prod_options == "Streaming with OD and cloud storage":

                        st.write("streaming with s3 storage ")

                    elif prod_options == "Streaming With OD and Tracking":

                        st.write("video streaming with live Tracking")

        elif choice == "Logout":
            login_user.logout("Logout", "main")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


if __name__ == "__main__":
    main()
