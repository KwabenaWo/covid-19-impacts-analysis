# Import the pandas library as pd for easy referencing.
import pandas as pd

# Import Plotly Express as px for simplified plotting.
import plotly.express as px

# Import Plotly Graph Objects as go for more customization in plotting.
import plotly.graph_objects as go

# Reading the transformed data from a CSV file into a pandas dataframe
data = pd.read_csv("transformed_data.csv")

# Reading the raw data from a CSV file into another pandas dataframe
data2 = pd.read_csv("raw_data.csv")

"""## Displaying the first few rows of the dataset"""

print(data.head())

# Display the first few rows of the dataframe
print(data2.head())  # Output the head of the dataframe for quick overview

"""## Count the occurrences of each country in the dataset"""

# and find the mode, i.e., the most frequently occurring value.
data["COUNTRY"].value_counts().mode()

"""The mode value is 294, indicating the most common occurrence. We'll utilize this value to divide the sum of all samples pertaining to the Human Development Index, GDP per capita, and population. Next, let's proceed to create a new dataset by merging the required columns from both datasets

# Aggregating the data
"""

# Extracting unique country codes and names
code = data["CODE"].unique().tolist()
country = data["COUNTRY"].unique().tolist()

# Lists to store aggregated values
hdi = []  # Human Development Index
tc = []   # Total Cases
td = []   # Total Deaths
sti = []  # Stringency Index
population = data["POP"].unique().tolist()  # Population
gdp = []  # GDP per capita

# Loop through each country
for i in country:
    # Calculating aggregated values for HDI, Total Cases, Total Deaths, and Stringency Index
    hdi.append((data.loc[data["COUNTRY"] == i, "HDI"]).sum() / 294)
    tc.append((data2.loc[data2["location"] == i, "total_cases"]).sum())
    td.append((data2.loc[data2["location"] == i, "total_deaths"]).sum())
    sti.append((data.loc[data["COUNTRY"] == i, "STI"]).sum() / 294)
    # Adjusting population by dividing by the mode value
    population.append((data2.loc[data2["location"] == i, "population"]).sum() / 294)

# Creating a DataFrame to store the aggregated data
aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)),
                               columns=["Country Code", "Country", "HDI",
                                        "Total Cases", "Total Deaths",
                                        "Stringency Index", "Population"])
# Displaying the first few rows of the aggregated data
print(aggregated_data.head())

# Sorting data to display countries with the highest total cases first
data = aggregated_data.sort_values(by=["Total Cases"], ascending=False)  # Sorting the data by total cases in descending order
print(data.head())  # Printing the top entries after sorting

#Top 10 countries with highest total cases

import seaborn as sns

# Selecting the top 10 countries with highest total COVID-19 cases
top_10_countries = data.head(10)

# Setting up the figure size and style
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Creating a bar plot with gradient color for better attractiveness
sns.barplot(x='Country', y='Total Cases', data=top_10_countries, palette="viridis")

# Adding title and labels
plt.title('Top 10 Countries with Highest Total COVID-19 Cases')
plt.xlabel('Country')
plt.ylabel('Total Cases')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Displaying the plot
plt.show()

# Creating a more visually appealing bar plot to visualize total COVID-19 cases by country
figure = px.bar(data,
                y='Total Cases',
                x='Country',
                title="Countries with Highest Covid Cases",
                color='Total Cases',  # Color bars based on total cases
                color_continuous_scale=px.colors.sequential.Plasma,  # Using a plasma color scale for better visualization
                labels={'Total Cases': 'Total Cases', 'Country': 'Country'},  # Customizing axis labels
                template='plotly_dark'  # Using a dark theme template for a modern look
               )

# Adding axis labels and title for better readability
figure.update_xaxes(title_text="Country")
figure.update_yaxes(title_text="Total Cases")

# Displaying the plot
figure.show()

# Creating a visually appealing bar plot to visualize total COVID-19 deaths by country
figure = px.bar(data,
                y='Total Deaths',
                x='Country',
                title="Countries with Highest Deaths",
                color='Total Deaths',  # Color bars based on total deaths
                color_continuous_scale=px.colors.sequential.Reds,  # Using a red color scale for emphasis
                labels={'Total Deaths': 'Total Deaths', 'Country': 'Country'},  # Customizing axis labels
                template='plotly_dark'  # Using a dark theme template for a modern look
               )

# Adding axis labels and title for better readability
figure.update_xaxes(title_text="Country")
figure.update_yaxes(title_text="Total Deaths")

# Displaying the plot
figure.show()

# Calculating total cases and total deaths

cases = data["Total Cases"].sum()
deceased = data["Total Deaths"].sum()

# Creating labels and values for the pie chart
labels = ["Total Cases", "Total Deaths"]
values = [cases, deceased]

# Setting up the plot style
sns.set(style="whitegrid")

# Creating a pie chart to visualize the percentage of total cases and deaths
plt.figure(figsize=(8, 6))
plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['skyblue', 'salmon'], startangle=90, textprops={'fontsize': 12})
plt.title('Percentage of Total Cases and Deaths', fontsize=16)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# Displaying the plot
plt.show()
