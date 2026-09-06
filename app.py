import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Netflix Titles Dashboard",
    page_icon="🎬",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🎬 Netflix Titles Analysis Dashboard")
st.write("Explore and analyze movies and TV shows available on Netflix.")


# ---------------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    # Convert date_added to datetime
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    return df


df = load_data()


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("🔎 Filters")

# Type filter
type_options = ["All"] + sorted(df["type"].dropna().unique().tolist())

selected_type = st.sidebar.selectbox(
    "Select Type",
    type_options
)


# Country filter
country_options = ["All"] + sorted(
    df["country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_options
)


# Rating filter
rating_options = ["All"] + sorted(
    df["rating"].dropna().unique().tolist()
)

selected_rating = st.sidebar.selectbox(
    "Select Rating",
    rating_options
)


# Apply filters
filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(
            selected_country,
            na=False
        )
    ]

if selected_rating != "All":
    filtered_df = filtered_df[
        filtered_df["rating"] == selected_rating
    ]


# ---------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ---------------------------------------------------------
st.subheader("📊 Netflix Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Titles",
        len(filtered_df)
    )

with col2:
    movies = (filtered_df["type"] == "Movie").sum()
    st.metric(
        "Movies",
        movies
    )

with col3:
    tv_shows = (filtered_df["type"] == "TV Show").sum()
    st.metric(
        "TV Shows",
        tv_shows
    )

with col4:
    countries = filtered_df["country"].nunique()
    st.metric(
        "Countries",
        countries
    )


st.divider()


# ---------------------------------------------------------
# FULL DATASET
# ---------------------------------------------------------
st.subheader("📋 Netflix Titles Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ---------------------------------------------------------
# FIRST FIVE ROWS
# ---------------------------------------------------------
st.subheader("🔍 First Five Rows")

st.dataframe(
    filtered_df.head(),
    use_container_width=True
)


# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------
st.subheader("ℹ️ Dataset Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.write("**Number of Rows:**", filtered_df.shape[0])
    st.write("**Number of Columns:**", filtered_df.shape[1])

with info_col2:
    st.write(
        "**Missing Values:**",
        filtered_df.isnull().sum().sum()
    )
    st.write(
        "**Duplicate Rows:**",
        filtered_df.duplicated().sum()
    )


# ---------------------------------------------------------
# TITLE TYPE DISTRIBUTION
# ---------------------------------------------------------
st.subheader("🎞️ Movies vs TV Shows")

type_count = (
    filtered_df["type"]
    .value_counts()
    .reset_index()
)

type_count.columns = ["type", "count"]

fig_type = px.bar(
    type_count,
    x="type",
    y="count",
    text="count",
    title="Number of Movies and TV Shows",
    labels={
        "type": "Title Type",
        "count": "Number of Titles"
    }
)

fig_type.update_layout(
    template="plotly_white"
)

fig_type.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_type,
    use_container_width=True
)


# ---------------------------------------------------------
# PIE CHART
# ---------------------------------------------------------
st.subheader("🥧 Netflix Content Distribution")

fig_pie = px.pie(
    filtered_df,
    names="type",
    title="Movies vs TV Shows",
    hole=0.4
)

fig_pie.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# ---------------------------------------------------------
# RELEASE YEAR DISTRIBUTION
# ---------------------------------------------------------
st.subheader("📅 Titles by Release Year")

year_count = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_count.columns = ["release_year", "count"]

fig_year = px.line(
    year_count,
    x="release_year",
    y="count",
    markers=True,
    title="Netflix Titles by Release Year",
    labels={
        "release_year": "Release Year",
        "count": "Number of Titles"
    }
)

fig_year.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP COUNTRIES
# ---------------------------------------------------------
st.subheader("🌍 Top 10 Countries")

country_data = filtered_df.copy()

country_data["country"] = country_data["country"].fillna(
    "Unknown"
)

country_data = country_data.assign(
    country=country_data["country"].str.split(", ")
).explode("country")

top_countries = (
    country_data["country"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_countries.columns = ["country", "count"]

fig_country = px.bar(
    top_countries.sort_values("count"),
    x="count",
    y="country",
    orientation="h",
    text="count",
    title="Top 10 Countries by Number of Netflix Titles",
    labels={
        "country": "Country",
        "count": "Number of Titles"
    }
)

fig_country.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP RATINGS
# ---------------------------------------------------------
st.subheader("🔞 Netflix Ratings")

rating_data = (
    filtered_df["rating"]
    .value_counts()
    .head(10)
    .reset_index()
)

rating_data.columns = ["rating", "count"]

fig_rating = px.bar(
    rating_data,
    x="rating",
    y="count",
    text="count",
    title="Top Netflix Content Ratings",
    labels={
        "rating": "Rating",
        "count": "Number of Titles"
    }
)

fig_rating.update_layout(
    template="plotly_white"
)

fig_rating.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)


# ---------------------------------------------------------
# MOVIES AND TV SHOWS BY YEAR
# ---------------------------------------------------------
st.subheader("📈 Movies and TV Shows Over Time")

year_type = (
    filtered_df
    .groupby(["release_year", "type"])
    .size()
    .reset_index(name="count")
)

fig_year_type = px.line(
    year_type,
    x="release_year",
    y="count",
    color="type",
    markers=True,
    title="Movies and TV Shows by Release Year",
    labels={
        "release_year": "Release Year",
        "count": "Number of Titles",
        "type": "Type"
    }
)

fig_year_type.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_year_type,
    use_container_width=True
)


# ---------------------------------------------------------
# TOP DIRECTORS
# ---------------------------------------------------------
st.subheader("🎥 Top 10 Directors")

director_data = filtered_df.copy()

director_data["director"] = director_data["director"].fillna(
    "Unknown"
)

director_data = director_data.assign(
    director=director_data["director"].str.split(", ")
).explode("director")

director_data = director_data[
    director_data["director"] != "Unknown"
]

top_directors = (
    director_data["director"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_directors.columns = ["director", "count"]

fig_director = px.bar(
    top_directors.sort_values("count"),
    x="count",
    y="director",
    orientation="h",
    text="count",
    title="Top 10 Directors on Netflix",
    labels={
        "director": "Director",
        "count": "Number of Titles"
    }
)

fig_director.update_layout(
    template="plotly_white"
)

st.plotly_chart(
    fig_director,
    use_container_width=True
)


# ---------------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------------
st.subheader("⬇️ Download Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="filtered_netflix_titles.csv",
    mime="text/csv"
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "Netflix Titles Analysis Dashboard | Built with Python, "
    "Pandas, Streamlit and Plotly"
)