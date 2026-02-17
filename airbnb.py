# ==========================================================
# AIRBNB DATA ANALYSIS PROJECT
# Clean -> Transform -> Explore -> Visualize
# ==========================================================

# ------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set(style="whitegrid")


# ------------------------------
# 2. LOAD DATA
# ------------------------------
# Always preserve raw data. Do NOT overwrite original file.
df = pd.read_csv("Airbnb_Open_Data.csv")

print("Initial shape:", df.shape)
print("\nColumns:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.info())


# ------------------------------
# 3. CLEAN COLUMN NAMES
# ------------------------------
# Standardize column names:
# - lowercase
# - replace spaces with underscores
# - standardize spelling (neighbourhood -> neighborhood)

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("neighbourhood", "neighborhood")
)

print("\nColumns after cleaning:")
print(df.columns)


# ------------------------------
# 4. REMOVE UNNECESSARY COLUMNS
# ------------------------------
columns_to_drop = ["host_id", "id", "country", "country_code"]

df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

print("\nShape after dropping unnecessary columns:", df.shape)


# ------------------------------
# 5. CHECK MISSING VALUES
# ------------------------------
print("\nMissing values per column:")
print(df.isnull().sum().sort_values(ascending=False))


# ------------------------------
# 6. REMOVE DUPLICATES
# ------------------------------
print("\nTotal records before removing duplicates:", len(df))

df = df.drop_duplicates()

print("Total records after removing duplicates:", len(df))


# ------------------------------
# 7. CLEAN NUMERIC COLUMNS
# ------------------------------
# Remove dollar signs and commas, convert to float safely

def clean_currency_column(column):
    return (
        df[column]
        .replace(r"[\$,]", "", regex=True)
        .astype(float)
    )

if "price" in df.columns:
    df["price"] = clean_currency_column("price")

if "service_fee" in df.columns:
    df["service_fee"] = clean_currency_column("service_fee")

# Convert numeric columns safely
numeric_columns = [
    "review_rate_number",
    "number_of_reviews",
    "reviews_per_month",
    "construction_year",
    "availability_365"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# ------------------------------
# 8. FEATURE ENGINEERING
# ------------------------------

# Create days_booked (correct logic)
# availability_365 = days available
# days_booked = 365 - availability
if "availability_365" in df.columns:
    df["days_booked"] = 365 - df["availability_365"]

# Create superhost label properly
if "host_is_superhost" in df.columns:
    df["is_superhost"] = df["host_is_superhost"].apply(
        lambda x: "Superhost" if str(x).lower() == "t" else "Regular Host"
    )

# ------------------------------
# 9. BASIC EXPLORATORY ANALYSIS
# ------------------------------

# Room type distribution
if "room_type" in df.columns:
    print("\nRoom Type Distribution:")
    print(df["room_type"].value_counts())

# Most common strict cancellation room type
if "cancellation_policy" in df.columns and "room_type" in df.columns:
    strict_room = (
        df[df["cancellation_policy"].str.lower() == "strict"]["room_type"]
        .value_counts()
        .idxmax()
    )
    print("\nRoom type most associated with strict policy:", strict_room)

# Average price per neighborhood group
if "neighborhood_group" in df.columns:
    avg_price_group = df.groupby("neighborhood_group")["price"].mean()
    print("\nAverage price per neighborhood group:")
    print(avg_price_group.sort_values(ascending=False))


# ------------------------------
# 10. TOP 10 MOST & LEAST EXPENSIVE NEIGHBORHOODS
# ------------------------------
if "neighborhood" in df.columns:

    avg_price_neighborhood = (
        df.groupby("neighborhood")["price"]
        .mean()
        .reset_index()
    )

    top_10_expensive = avg_price_neighborhood.nlargest(10, "price")
    top_10_cheap = avg_price_neighborhood.nsmallest(10, "price")

    # Most expensive
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_expensive["neighborhood"], top_10_expensive["price"])
    plt.xlabel("Average Price")
    plt.ylabel("Neighborhood")
    plt.title("Top 10 Most Expensive Neighborhoods")
    plt.gca().invert_yaxis()
    plt.show()

    # Least expensive
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_cheap["neighborhood"], top_10_cheap["price"])
    plt.xlabel("Average Price")
    plt.ylabel("Neighborhood")
    plt.title("Top 10 Least Expensive Neighborhoods")
    plt.gca().invert_yaxis()
    plt.show()

    # Boxplot by Room Type
    import seaborn as sns
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8,6))
    sns.boxplot(x="room_type", y="price", data=df)
    plt.show()

    # Cleaning Fee vs Price
    sns.scatterplot(x="service_fee", y="price", data=df, alpha=0.3)
    plt.show()

# ------------------------------
# 11. LISTINGS BY CONSTRUCTION YEAR
# ------------------------------

if "construction_year" in df.columns:
    listings_per_year = df["construction_year"].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.plot(listings_per_year.index, listings_per_year.values, marker="o")
    plt.xlabel("Construction Year")
    plt.ylabel("Total Listings")
    plt.title("Listings by Construction Year")
    plt.show()


# ------------------------------
# 12. REVIEW RATE VS PRICE
# ------------------------------
import numpy as np



sns.boxplot(x="review_rate_number", y="price", data=df)
plt.show()


if "review_rate_number" in df.columns and "price" in df.columns:

    # Remove missing values
    df_scatter = df[["review_rate_number", "price"]].dropna()

    # Remove extreme price outliers (99th percentile)
    price_cap = df_scatter["price"].quantile(0.99)
    df_scatter = df_scatter[df_scatter["price"] <= price_cap]

    # Log-transform price safely
    df_scatter["log_price"] = np.log(df_scatter["price"])

    plt.figure(figsize=(10, 6))

    # Scatter plot
    sns.scatterplot(
        x="review_rate_number",
        y="log_price",
        data=df_scatter,
        alpha=0.2
    )

    # Regression line
    sns.regplot(
        x="review_rate_number",
        y="log_price",
        data=df_scatter,
        scatter=False,
        color="red"
    )

    plt.title("Review Rate vs Log(Price)")
    plt.xlabel("Review Rate Number")
    plt.ylabel("Log(Price)")
    plt.show()
# ------------------------------
# 13. SUPERHOST ANALYSIS
# ------------------------------

# Create host category 
df["is_superhost"] = df["host_identity_verified"].apply(
    lambda x: "Verified Host" if str(x).lower() == "t" else "Non-Verified Host"
)

# Compare number of reviews
plt.figure(figsize=(8,6))
sns.boxplot(x="is_superhost", y="number_of_reviews", data=df)
plt.title("Number of Reviews by Host Type")
plt.show()

# Compare reviews per month
plt.figure(figsize=(8,6))
sns.boxplot(x="is_superhost", y="reviews_per_month", data=df)
plt.title("Reviews per Month by Host Type")
plt.show()

# ------------------------------
# 14. EXPORT CLEAN DATA
# ------------------------------
df.to_csv("Airbnb_Open_Data_cleaned.csv", index=False)
df.to_excel("Airbnb_Open_Data_cleaned.xlsx", index=False)

print("\nClean dataset exported successfully.")
