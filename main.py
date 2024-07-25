import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

# Function to load data from an uploaded file
def load_data(uploaded_file):
    if uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        st.error('Unsupported file format. Please upload an XLSX or CSV file.')
        return None

# Sample test data
st.title("Student Support Class")

# Display side by side using columns layout
st.header('To generate the report, Please upload the data file.')

# File uploader
uploaded_file = st.file_uploader('Upload your attendance file (XLSX or CSV)', type=['xlsx', 'csv'])

if uploaded_file:
    
    data = load_data(uploaded_file)
    
    if data is not None:
        # Get unique center name list ....
        center_lst = data['Center'].unique().tolist()

        # Define a function to create a card
        def create_card(title, value):
            card_html = f"""
            <div class="card">
                <h3>{title}</h3>
                <p>{value}</p>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

        def add_break():
            st.markdown("<br><br><br>", unsafe_allow_html=True)

        # # Sidebar filters
        st.markdown("### Program Matrices")
        st.sidebar.header("Select level")
        selected_timeframe = st.sidebar.selectbox("Select TimeFrame", ['Month', 'Year'])
        if selected_timeframe == 'Year':
            selected_year = st.sidebar.selectbox("Select Year", ['2023', '2022'])
        else:
            selected_month = st.sidebar.selectbox("Select Month", ['Jan', 'Fab'])
        selected_center = st.sidebar.selectbox("Select Center", center_lst)
        if selected_center:
            pocket_lst = data[data['Center'] == selected_center]['Pocket'].unique().tolist()
            pocket_lst.insert(0, 'All')
            col1, col2, col3 = st.columns(3)
            select_pocket = st.sidebar.selectbox("Select Pocket", pocket_lst)
            if select_pocket == 'All':
                with col1:
                    create_card("Center/Pocket Name", selected_center)
                center_data = data[data['Center'] == selected_center]
            else:
                with col1:
                    create_card("Center/Pocket Name", select_pocket)
                center_data = data[(data['Center'] == selected_center) & (data['Pocket'] == select_pocket)]
            no_of_pockets = center_data['Pocket'].nunique()
            no_of_students = center_data['member_uuid'].nunique()
            
            with col2:
                create_card("Total Pocket",no_of_pockets)

            # Example of adding another metric with col.metric
            with col3:
                create_card("Total Number of Students",no_of_students)
            # Page break / visual separator
            add_break()
            
            st.dataframe(center_data)
            
            # Lets add some graphs ...
            # Display side by side using columns layout
            st.header('Data Overview')
            
            # Plot Gender Distribution
            # Deduplicate attendance records based on member_uuid
            gender_counts = center_data['member_Gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            fig_gender = px.bar(gender_counts, x='Gender', y='Count', text='Count', title='Gender Distribution')
            
            custom_colors = px.colors.qualitative.Pastel
            standard_counts = center_data['member_Education_Standard and class'].value_counts().reset_index()
            standard_counts.columns = ['Standard and class', 'Count']
            fig_standard = px.bar(standard_counts, x='Standard and class', y='Count', text='Count', title='Gender Distribution')

            # First column with Gender Distribution plot
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig_gender)

            with col2:
                st.plotly_chart(fig_standard)
                
            # Attendence details ....
            add_break()
            # Display side by side using columns layout
            st.header('Attendence Overview With Data')
            
            attendence_category_count = center_data['category'].value_counts().reset_index()
            attendence_category_count.columns = ['Attendence', 'Count']
            fig_Attendence = px.bar(attendence_category_count, x='Attendence', y='Count', text='Count', title='Attendence Distribution')
            
            # First column with Gender Distribution plot
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig_Attendence)

            with col2:
                attendence_df = center_data[['Center', 'Pocket', 'member_First Name', 'member_Last Name', 'Total Days classes were held', 'Student attended the class', 'Attendence Percentage', 'category']]
                st.dataframe(attendence_df)
            
            # Evaluation Exam details ....
            add_break()
            # Display side by side using columns layout
            st.header('Evaluation Exam Overview With Data')
            st.subheader('December Evaluation Exam Overview', divider='rainbow')
            
            # chech how many students has given the evaluation exam ...
            # before there is a posibility that some students has not attendend the exam. so we have to replace nan value to the Not Present tag.
            # check nan value count
            not_present = center_data['December Evaluation'].isnull().sum()
            # check how many present.
            present = center_data.shape[0] - not_present
            
            december_eval = pd.DataFrame([{'December Evaluation' : 'Present Students', 'Count' : present},
                                        {'December Evaluation' : 'Not Present Students', 'Count' : not_present}])
            december_eval.columns = ['December Evaluation', 'Count']
            fig_december_eval = px.bar(december_eval, x='December Evaluation', y='Count', text='Count', title='December Evaluation')
            
            # result of the Evaluation Exam ...
            december_eval_result_data = center_data[center_data['December Evaluation'].isnull() == False]
            december_eval_result = december_eval_result_data['Result of December Evaluation Exam'].value_counts().reset_index()
            december_eval_result.columns = ['Result of December Evaluation Exam', 'Count']
            fig_december_eval_result = px.bar(december_eval_result, x='Result of December Evaluation Exam', y='Count', text='Count', title='December Evaluation Exam Result')
            
            # First column with Gender Distribution plot
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig_december_eval)

            with col2:
                st.plotly_chart(fig_december_eval_result)
            
            
            # March Evaluation
            st.subheader('March Evaluation Exam Overview', divider='rainbow')
            
            # chech how many students has given the evaluation exam ...
            # before there is a posibility that some students has not attendend the exam. so we have to replace nan value to the Not Present tag.
            # check nan value count
            not_present = center_data['March Evaluation'].isnull().sum()
            # check how many present.
            present = center_data.shape[0] - not_present
            
            march_eval = pd.DataFrame([{'March Evaluation' : 'Present Students', 'Count' : present},
                                        {'March Evaluation' : 'Not Present Students', 'Count' : not_present}])
            march_eval.columns = ['March Evaluation', 'Count']
            fig_march_eval = px.bar(march_eval, x='March Evaluation', y='Count', text='Count', title='March Evaluation')
            
            # result of the Evaluation Exam ...
            march_eval_result_data = center_data[center_data['March Evaluation'].isnull() == False]
            march_eval_result = march_eval_result_data['Result of March Evaluation Exam'].value_counts().reset_index()
            march_eval_result.columns = ['Result of March Evaluation Exam', 'Count']
            fig_march_eval_result = px.bar(march_eval_result, x='Result of March Evaluation Exam', y='Count', text='Count', title='March Evaluation Exam Result')
            
            # First column with Gender Distribution plot
            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig_march_eval)

            with col2:
                st.plotly_chart(fig_march_eval_result)
    
    # print(selected_center)
# Row A

# # Get unique center name list ....
# center_lst = data['Center'].unique().tolist()

# Filter data based on selections
# filtered_data = data[(data['Month'].dt.strftime('%Y-%m') == selected_month) & 
#                      (data['Student'] == selected_student)]

# # Overall Attendance Rate
# if not filtered_data.empty:
#     overall_attendance_rate = filtered_data['Attendance_Rate'].iloc[0]
# else:
#     overall_attendance_rate = 0
# st.metric(label="Attendance Rate for Selected Month", value=f"{overall_attendance_rate:.2f}%")

# # Attendance Trend for Selected Student
# student_monthly_trend = data[data['Student'] == selected_student].set_index('Month')
# st.line_chart(student_monthly_trend['Attendance_Rate'])

# # Class Average Attendance Rate
# class_avg_attendance_rate = data.groupby('Month')['Attendance_Rate'].mean()
# st.line_chart(class_avg_attendance_rate)

# # Attendance Distribution
# attendance_distribution = data['Attendance_Rate'].value_counts(bins=5)
# fig, ax = plt.subplots()
# sns.barplot(x=attendance_distribution.index.astype(str), y=attendance_distribution.values, ax=ax)
# ax.set_xlabel("Attendance Rate")
# ax.set_ylabel("Number of Students")
# st.pyplot(fig)

# Save and run your Streamlit app
# streamlit run your_script.py



# selected_center = st.sidebar.selectbox("Select Center", center_lst)
# if selected_center:
#     pocket_lst = data[data['Center'] == selected_center]['Pocket'].unique().tolist()
#     pocket_lst.insert(0, 'All')
#     select_pocket = st.sidebar.selectbox("Select Pocket", pocket_lst)
#     if select_pocket == 'All':
#         title_str = '### Program Matrices for :- ' + selected_center
#         center_data = data[data['Center'] == selected_center]
#     else:
#         title_str = '### Program Matrices for :- ' + select_pocket
#         center_data = data[(data['Center'] == selected_center) & (data['Pocket'] == select_pocket)]
#     no_of_pockets = center_data['Pocket'].nunique()
#     no_of_students = center_data['member_uuid'].nunique()
#     st.markdown(title_str)
#     col1, col2, col3 = st.columns(3)



