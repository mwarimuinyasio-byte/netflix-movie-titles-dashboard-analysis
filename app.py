import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Netflix Titles Dashboard",
    page_icon=None,
    layout="wide"
)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("netflix_titles.csv")


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Netflix Titles Analysis Dashboard")

st.markdown(
    "An interactive analysis of Netflix movies and TV shows, "
    "including content type, release year, ratings, countries, "
    "and genres."
)


# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

df["year_added"] = df["date_added"].dt.year


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Dashboard Filters")


# Content type
type_options = sorted(
    df["type"].dropna().unique()
)

selected_type = st.sidebar.multiselect(
    "Select Content Type",
    options=type_options,
    default=type_options
)


# Release year
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())

selected_year = st.sidebar.slider(
    "Release Year",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Rating
if "rating" in df.columns:

    rating_options = sorted(
        df["rating"].dropna().unique()
    )

    selected_rating = st.sidebar.multiselect(
        "Select Rating",
        options=rating_options,
        default=rating_options
    )

else:
    selected_rating = []


# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    (df["type"].isin(selected_type))
    &
    (df["release_year"].between(
        selected_year[0],
        selected_year[1]
    ))
]


if selected_rating:
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_rating)
    ]


# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("Netflix Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Titles",
        f"{len(filtered_df):,}"
    )

with col2:
    movies = (
        filtered_df["type"]
        .eq("Movie")
        .sum()
    )

    st.metric(
        "Movies",
        f"{movies:,}"
    )

with col3:
    tv_shows = (
        filtered_df["type"]
        .eq("TV Show")
        .sum()
    )

    st.metric(
        "TV Shows",
        f"{tv_shows:,}"
    )

with col4:
    st.metric(
        "Unique Release Years",
        filtered_df["release_year"].nunique()
    )


st.divider()


# ---------------------------------------------------
# CONTENT TYPE
# ---------------------------------------------------

st.subheader("Content Type")

col1, col2 = st.columns(2)

with col1:

    type_count = (
        filtered_df["type"]
        .value_counts()
        .reset_index()
    )

    type_count.columns = [
        "type",
        "count"
    ]

    fig = px.pie(
        type_count,
        names="type",
        values="count",
        title="Movies vs TV Shows",
        hole=0.4
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        type_count,
        x="type",
        y="count",
        title="Number of Titles by Content Type",
        text="count"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Content Type",
        yaxis_title="Number of Titles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------------------------------------------
# RELEASE YEAR ANALYSIS
# ---------------------------------------------------

st.subheader("Release Year Analysis")

year_count = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_count.columns = [
    "release_year",
    "count"
]

fig = px.line(
    year_count,
    x="release_year",
    y="count",
    markers=True,
    title="Netflix Titles by Release Year"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Release Year",
    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# RATINGS
# ---------------------------------------------------

st.subheader("Content Ratings")

rating_count = (
    filtered_df["rating"]
    .value_counts()
    .reset_index()
)

rating_count.columns = [
    "rating",
    "count"
]

fig = px.bar(
    rating_count,
    x="rating",
    y="count",
    title="Netflix Titles by Rating",
    text="count"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Rating",
    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# TOP COUNTRIES
# ---------------------------------------------------

st.subheader("Top Countries Producing Netflix Content")

country_df = filtered_df.dropna(
    subset=["country"]
).copy()


# Some records contain multiple countries.
country_df["country"] = country_df["country"].str.split(",")

country_df = country_df.explode("country")

country_df["country"] = (
    country_df["country"]
    .str.strip()
)

top_countries = (
    country_df["country"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_countries.columns = [
    "country",
    "count"
]

fig = px.bar(
    top_countries,
    x="count",
    y="country",
    orientation="h",
    title="Top 15 Countries by Number of Titles",
    text="count"
)

fig.update_layout(
    template="plotly_white",
    yaxis_title="Country",
    xaxis_title="Number of Titles",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# GENRES
# ---------------------------------------------------

st.subheader("Popular Genres")

genre_df = filtered_df.dropna(
    subset=["listed_in"]
).copy()

genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

genre_df = genre_df.explode(
    "listed_in"
)

genre_df["listed_in"] = (
    genre_df["listed_in"]
    .str.strip()
)

top_genres = (
    genre_df["listed_in"]
    .value_counts()
    .head(15)
    .reset_index()
)

top_genres.columns = [
    "genre",
    "count"
]

fig = px.bar(
    top_genres,
    x="count",
    y="genre",
    orientation="h",
    title="Top 15 Netflix Genres",
    text="count"
)

fig.update_layout(
    template="plotly_white",
    yaxis_title="Genre",
    xaxis_title="Number of Titles",
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# MOVIES VS TV SHOWS OVER TIME
# ---------------------------------------------------

st.subheader("Movies and TV Shows Over Time")

type_year = (
    filtered_df
    .groupby(
        ["release_year", "type"]
    )
    .size()
    .reset_index(
        name="count"
    )
)

fig = px.line(
    type_year,
    x="release_year",
    y="count",
    color="type",
    markers=True,
    title="Movies vs TV Shows by Release Year"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Release Year",
    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------------------------------------------
# SEARCH TITLES
# ---------------------------------------------------

st.subheader("Search Netflix Titles")

search_term = st.text_input(
    "Search by title"
)

if search_term:

    search_results = filtered_df[
        filtered_df["title"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]

    st.write(
        f"Found {len(search_results)} matching titles."
    )

    st.dataframe(
        search_results[
            [
                "title",
                "type",
                "release_year",
                "rating",
                "country",
                "duration",
                "listed_in",
                "description"
            ]
        ],
        use_container_width=True
    )

else:

    st.info(
        "Enter a title above to search the Netflix dataset."
    )


# ---------------------------------------------------
# FULL DATASET
# ---------------------------------------------------

st.subheader("Netflix Dataset")

with st.expander("View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ---------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------

st.subheader("Dataset Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows",
        df.shape[0]
    )

with col2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with col3:
    st.metric(
        "Missing Values",
        df.isnull().sum().sum()
    )

with col4:
    st.metric(
        "Duplicate Rows",
        df.duplicated().sum()
    )


# ---------------------------------------------------
# COLUMN INFORMATION
# ---------------------------------------------------

with st.expander("View Column Information"):

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Netflix Titles Analysis Dashboard"
)