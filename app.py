import pandas as pd
import streamlit as st
import plotly.express as px


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Netflix Titles Analysis",
    layout="wide"
)


# ==========================================================
# LOAD DATASET
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df


df = load_data()


# ==========================================================
# DATA CLEANING
# ==========================================================

# Convert date_added to datetime
if "date_added" in df.columns:
    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )

    df["year_added"] = df["date_added"].dt.year


# ==========================================================
# TITLE
# ==========================================================

st.title("Netflix Titles Analysis Dashboard")

st.write(
    "An interactive dashboard for exploring Netflix movies "
    "and TV shows based on content type, release year, "
    "ratings, countries, genres, and other attributes."
)


# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")


# ----------------------------------------------------------
# Content Type Filter
# ----------------------------------------------------------

if "type" in df.columns:

    type_options = sorted(
        df["type"].dropna().unique()
    )

    selected_types = st.sidebar.multiselect(
        "Content Type",
        options=type_options,
        default=type_options
    )

else:
    selected_types = []


# ----------------------------------------------------------
# Release Year Filter
# ----------------------------------------------------------

if "release_year" in df.columns:

    min_year = int(df["release_year"].min())
    max_year = int(df["release_year"].max())

    selected_years = st.sidebar.slider(
        "Release Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

else:
    selected_years = (0, 9999)


# ----------------------------------------------------------
# Rating Filter
# ----------------------------------------------------------

if "rating" in df.columns:

    rating_options = sorted(
        df["rating"].dropna().unique()
    )

    selected_ratings = st.sidebar.multiselect(
        "Rating",
        options=rating_options,
        default=rating_options
    )

else:
    selected_ratings = []


# ==========================================================
# FILTER DATASET
# ==========================================================

filtered_df = df.copy()


if selected_types:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]


if "release_year" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["release_year"].between(
            selected_years[0],
            selected_years[1]
        )
    ]


if selected_ratings:
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_ratings)
    ]


# ==========================================================
# KEY PERFORMANCE INDICATORS
# ==========================================================

st.subheader("Netflix Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Titles",
        f"{len(filtered_df):,}"
    )


with col2:

    if "type" in filtered_df.columns:

        movie_count = (
            filtered_df["type"]
            .eq("Movie")
            .sum()
        )

        st.metric(
            "Movies",
            f"{movie_count:,}"
        )


with col3:

    if "type" in filtered_df.columns:

        tv_count = (
            filtered_df["type"]
            .eq("TV Show")
            .sum()
        )

        st.metric(
            "TV Shows",
            f"{tv_count:,}"
        )


with col4:

    if "release_year" in filtered_df.columns:

        st.metric(
            "Release Years",
            filtered_df["release_year"].nunique()
        )


st.divider()


# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.subheader("Dataset Summary")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Rows",
        f"{df.shape[0]:,}"
    )


with col2:

    st.metric(
        "Total Columns",
        df.shape[1]
    )


with col3:

    st.metric(
        "Missing Values",
        f"{df.isnull().sum().sum():,}"
    )


with col4:

    st.metric(
        "Duplicate Rows",
        f"{df.duplicated().sum():,}"
    )


# ==========================================================
# CONTENT TYPE ANALYSIS
# ==========================================================

st.subheader("Content Type Analysis")

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# Pie Chart
# ----------------------------------------------------------

with col1:

    if "type" in filtered_df.columns:

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

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ----------------------------------------------------------
# Bar Chart
# ----------------------------------------------------------

with col2:

    if "type" in filtered_df.columns:

        fig = px.bar(
            type_count,
            x="type",
            y="count",
            text="count",
            title="Number of Titles by Content Type"
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


# ==========================================================
# RELEASE YEAR ANALYSIS
# ==========================================================

st.subheader("Release Year Analysis")

if "release_year" in filtered_df.columns:

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


# ==========================================================
# CONTENT RATING ANALYSIS
# ==========================================================

st.subheader("Content Ratings")

if "rating" in filtered_df.columns:

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
        text="count",
        title="Netflix Titles by Rating"
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


# ==========================================================
# TOP COUNTRIES
# ==========================================================

st.subheader("Top Countries")

if "country" in filtered_df.columns:

    country_df = filtered_df.dropna(
        subset=["country"]
    ).copy()

    # Split multiple countries
    country_df["country"] = (
        country_df["country"]
        .str.split(",")
    )

    country_df = country_df.explode(
        "country"
    )

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
        text="count",
        title="Top 15 Countries by Number of Titles"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Number of Titles",
        yaxis_title="Country",
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# GENRE ANALYSIS
# ==========================================================

st.subheader("Popular Genres")

if "listed_in" in filtered_df.columns:

    genre_df = filtered_df.dropna(
        subset=["listed_in"]
    ).copy()

    # Split multiple genres
    genre_df["listed_in"] = (
        genre_df["listed_in"]
        .str.split(",")
    )

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
        text="count",
        title="Top 15 Netflix Genres"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Number of Titles",
        yaxis_title="Genre",
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# MOVIES VS TV SHOWS OVER TIME
# ==========================================================

st.subheader("Movies and TV Shows Over Time")

if (
    "release_year" in filtered_df.columns
    and "type" in filtered_df.columns
):

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


# ==========================================================
# TITLES ADDED TO NETFLIX OVER TIME
# ==========================================================

st.subheader("Titles Added to Netflix Over Time")

if "year_added" in filtered_df.columns:

    added_count = (
        filtered_df["year_added"]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )

    added_count.columns = [
        "year_added",
        "count"
    ]

    fig = px.bar(
        added_count,
        x="year_added",
        y="count",
        text="count",
        title="Number of Titles Added Each Year"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Year Added",
        yaxis_title="Number of Titles"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# MOVIE DURATION
# ==========================================================

st.subheader("Movie Duration Analysis")

if "duration" in filtered_df.columns:

    movie_df = filtered_df[
        filtered_df["type"] == "Movie"
    ].copy()

    movie_df["duration_minutes"] = (
        movie_df["duration"]
        .str.extract(r"(\d+)")
        [0]
    )

    movie_df["duration_minutes"] = pd.to_numeric(
        movie_df["duration_minutes"],
        errors="coerce"
    )

    movie_df = movie_df.dropna(
        subset=["duration_minutes"]
    )

    if not movie_df.empty:

        fig = px.histogram(
            movie_df,
            x="duration_minutes",
            nbins=30,
            title="Distribution of Movie Duration"
        )

        fig.update_layout(
            template="plotly_white",
            xaxis_title="Duration in Minutes",
            yaxis_title="Number of Movies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ==========================================================
# SEARCH TITLES
# ==========================================================

st.subheader("Search Netflix Titles")

search_term = st.text_input(
    "Enter a title to search"
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
        f"Search results: {len(search_results)} titles"
    )

    if not search_results.empty:

        display_columns = [
            column for column in [
                "show_id",
                "title",
                "type",
                "director",
                "cast",
                "country",
                "release_year",
                "rating",
                "duration",
                "listed_in",
                "description"
            ]
            if column in search_results.columns
        ]

        st.dataframe(
            search_results[display_columns],
            use_container_width=True
        )

    else:

        st.warning(
            "No titles were found."
        )


# ==========================================================
# FULL DATASET
# ==========================================================

st.subheader("Full Netflix Dataset")

st.write(
    f"Displaying {len(filtered_df):,} records "
    f"from the filtered dataset."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=600
)


# ==========================================================
# DOWNLOAD FULL DATASET
# ==========================================================

st.subheader("Download Dataset")

csv = df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Full Netflix Dataset",
    data=csv,
    file_name="netflix_titles.csv",
    mime="text/csv"
)


# ==========================================================
# DATASET COLUMN INFORMATION
# ==========================================================

st.subheader("Dataset Column Information")

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


# ==========================================================
# STATISTICAL SUMMARY
# ==========================================================

st.subheader("Numerical Summary")

numeric_columns = df.select_dtypes(
    include="number"
).columns


if len(numeric_columns) > 0:

    st.dataframe(
        df[numeric_columns].describe(),
        use_container_width=True
    )

else:

    st.write(
        "There are no numerical columns available "
        "for statistical analysis."
    )


# ==========================================================
# RAW DATASET PREVIEW
# ==========================================================

st.subheader("Dataset Preview")

tab1, tab2, tab3 = st.tabs([
    "First Five Rows",
    "Last Five Rows",
    "Random Sample"
])


with tab1:

    st.dataframe(
        df.head(),
        use_container_width=True
    )


with tab2:

    st.dataframe(
        df.tail(),
        use_container_width=True
    )


with tab3:

    st.dataframe(
        df.sample(
            min(10, len(df)),
            random_state=42
        ),
        use_container_width=True
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Netflix Titles Analysis Dashboard"
)