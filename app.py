from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Create age bins
age_bins = list(range(20, 65, 5))
age_labels = [f'{age_bins[i]}-{age_bins[i+1]}' for i in range(len(age_bins)-1)]
df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H2("Department-wise HR Analytics Dashboard"),
    dcc.RadioItems(
        options=[{'label': dept, 'value': dept} for dept in df['Department'].unique()],
        value=df['Department'].unique()[0],
        id='dept-selector',
        inline=True
    ),
    html.Div([
        dcc.Graph(id='gender-pie'),
        dcc.Graph(id='income-age-bar')
    ])
])

# Callback for plots
@app.callback(
    [Output('gender-pie', 'figure'),
     Output('income-age-bar', 'figure')],
    Input('dept-selector', 'value')
)
def update_charts(selected_dept):
    filtered_df = df[df['Department'] == selected_dept]

    # Gender Pie Chart
    gender_counts = filtered_df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    pie_fig = px.pie(gender_counts, values='Count', names='Gender', title=f'Gender Ratio in {selected_dept}')

    # Monthly Income by Age Group
    age_income = filtered_df.groupby('AgeGroup')['MonthlyIncome'].mean().reset_index()
    bar_fig = px.bar(age_income, x='AgeGroup', y='MonthlyIncome', title=f'Average Monthly Income by Age Group in {selected_dept}')

    return pie_fig, bar_fig

if __name__ == '__main__':
 app.run_server(debug=False, host='0.0.0.0', port=8080)
