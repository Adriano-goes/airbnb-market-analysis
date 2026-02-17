# Airbnb Market Analysis

This project analyzes Airbnb listing data to explore pricing behavior, host performance, and neighborhood-level market dynamics. The goal is to identify patterns that influence listing prices and booking performance.

## Construction Year Trend

![Line chart showing the distribution of Airbnb listings by construction year](images/construction_year_trend.png)

---

## Top 10 Most Expensive Neighborhoods

![Horizontal bar chart showing the top 10 most expensive neighborhoods by average price](images/most_expensive.png)

---

## Top 10 Least Expensive Neighborhoods

![Horizontal bar chart showing the 10 least expensive neighborhoods by average price](images/least_expensive.png)

---

## Price Distribution by Room Type

![Boxplot illustrating price distribution across different room types](images/price_room_type.png)

---

## Review Rate vs Log(Price)

![Scatter plot with regression line showing relationship between review rate and log-transformed price](images/reviews_price_regression.png)

---

## Reviews per Month by Host Type

![Boxplot comparing reviews per month between verified and non-verified hosts](images/superhost_reviews.png)



# Objectives

_ Clean and transform raw Airbnb data
_ Analyze pricing differences across neighborhoods
_ Compare host performance metrics
_ Investigate the relationship between reviews and price

# Dataset

_ Airbnb Open Data (CSV format)

# Includes:

_ Pricing data
_ Service fees
_ Room types
_ Review metrics
_ Host verification status
_ Neighborhood information

# Key Insights
_ Price varies significantly across neighborhoods.
_ Room type strongly influences price distribution.
_ Reviews are highly skewed: a small number of listings capture most engagement.
_ Verified hosts tend to receive higher engagement metrics compared to non-verified hosts.
_ No strong linear relationship was found between review rating and price.

# Methods

_ Data cleaning (missing values, duplicates, standardization)
_ Feature engineering (days_booked, host categories)
_ Exploratory data analysis (EDA)
_ Statistical summaries
_ Visualizations (boxplots, bar charts, regression analysis)

# Tools

_ Python
_ Pandas
_ NumPy
_ Matplotlib
_ Seaborn
