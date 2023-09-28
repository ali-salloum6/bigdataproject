import streamlit as st
import altair as alt
import pandas as pd

comments = pd.read_csv("data/comments_df.csv", delimiter='\t')
course = pd.read_csv("data/course_df.csv", delimiter='\t')
q1 = pd.read_csv("output/q1.csv", error_bad_lines=False)
q2 = pd.read_csv("output/q2.csv", error_bad_lines=False)
q3 = pd.read_csv("output/q3.csv", error_bad_lines=False)
q4 = pd.read_csv("output/q4.csv", error_bad_lines=False)
q5 = pd.read_csv("output/q5.csv", error_bad_lines=False)

st.markdown('---')
st.markdown('<center>Big Data Project 2023</center>', unsafe_allow_html = True)
st.markdown("<h1 style='text-align: center;'>Course Price Prediction</h1>", unsafe_allow_html = True)

st.markdown(
    """
    <style>
    .centered-image {
        display: flex;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="centered-image">
        <img src="https://uptoinnovative.com/wp-content/uploads/2022/01/shutterstock_1383390812-Converted.jpg" alt="listing price predictions" width="400">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('---')
st.header('Descriptive Data Analysis')
st.subheader('Data Characteristics')
comments_dda = pd.DataFrame(data = [["comments", comments.shape[0]-1, comments.shape[1]], ["course", course.shape[0], course.shape[1]]], columns = ["Tables", "Instances", "Features"])
st.write(comments_dda)
st.markdown('`comments` table')
st.write(comments.describe())
st.markdown('`course` table')
st.write(course.describe())

st.subheader('Some samples from the data')
st.markdown('`comments` table')
st.write(comments.head(5))
st.markdown("`course` table")
st.write(course.head(5))

st.markdown('---')
q1_chart = alt.Chart(q1).mark_bar().encode(
    y=alt.Y(q1.columns[1], axis=alt.Axis(title='Average Rating')),
    x=alt.X(q1.columns[0], axis=alt.Axis(title='Payment status')),
) 
st.header("Exploratory Data Analysis")
st.subheader('Q1')
st.text('The average rating for courses based on their payment type.')
st.text('This insight helps understand how different payment models affect course ratings.')
st.altair_chart(q1_chart, use_container_width=True)

st.markdown('---')
q2_chart = alt.Chart(q2).mark_bar().encode(
    y=alt.Y(q2.columns[1], axis=alt.Axis(title='Number of subscriber')),
    x=alt.X(q2.columns[0], axis=alt.Axis(title='Course title')),
)
st.header("Exploratory Data Analysis")
st.subheader('Q2')
st.text('The top courses with the highest number of subscribers.')
st.text('This insight can help you understand which courses are the most popular among users.')
st.altair_chart(q2_chart, use_container_width=True)

st.markdown('---')
q3_chart = alt.Chart(q3).mark_bar().encode(
    y=alt.Y(q3.columns[1], axis=alt.Axis(title='Rating')),
    x=alt.X(q3.columns[0], axis=alt.Axis(title='Course title')),
)
st.header("Exploratory Data Analysis")
st.subheader('Q3')
st.text('Course with high rates (e.g., rates greater than 4.0) and the corresponding course titles.')
st.text('This insight can help you identify highly praised courses.')
st.altair_chart(q3_chart, use_container_width=True)

st.markdown('---')
q4_chart = alt.Chart(q4).mark_bar().encode(
    y=alt.Y(q4.columns[1], axis=alt.Axis(title='Average rating')),
    x=alt.X(q4.columns[0], axis=alt.Axis(title='Number of lecture')),
)
st.header("Exploratory Data Analysis")
st.subheader('Q4')
st.text('The relationship between the number of lectures in a course and the average comment rate.')
st.text('This insight can help you understand if longer or shorter courses receive more feedback.')
st.altair_chart(q4_chart, use_container_width=True)

st.markdown('---')
q5_chart = alt.Chart(q5).mark_bar().encode(
    y=alt.Y(q5.columns[1], axis=alt.Axis(title='Number of course')),
    x=alt.X(q5.columns[0], axis=alt.Axis(title='Number of review')),
)
st.header("Exploratory Data Analysis")
st.subheader('Q5')
st.text('The distribution of the number of reviews for courses.')
st.text('This insight can help you understand the typical review activity on the platform.')
st.altair_chart(q5_chart, use_container_width=True)




