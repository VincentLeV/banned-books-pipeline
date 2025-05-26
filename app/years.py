import streamlit as st
import pandas as pd
from utils import load_data
import plotly.graph_objects as go

def top_5_banned_titles(data: pd.DataFrame, year: str):
  filtered_data = data[
    ((data["Ban Status"] == "banned") | (data["Ban Status"] == "banned from libraries and classrooms")) &
    (data["Year"] == year)
  ]
  title_counts = filtered_data.groupby(["Title", "Author"]).size().reset_index(name="Ban Count")
  top_titles = title_counts.sort_values(by="Ban Count", ascending=False).head(10)
  return top_titles[["Title", "Author", "Ban Count"]]

def top_5_challenged_titles(data: pd.DataFrame, year: str):
  filtered_data = data[
    (data["Year"] == year) &
    (~data["Ban Status"].isin(["banned", "banned from libraries and classrooms"]))
  ]
  title_counts = filtered_data.groupby(["Title", "Author"]).size().reset_index(name="Challenge Count")
  top_titles = title_counts.sort_values(by="Challenge Count", ascending=False).head(10)
  return top_titles[["Title", "Author", "Challenge Count"]]

def by_year_grouped_bar_chart(data: pd.DataFrame, year: str):
  top_banned = top_5_banned_titles(data, year)
  top_challenged = top_5_challenged_titles(data, year)

  merged = pd.merge(
    top_banned,
    top_challenged,
    on=["Title", "Author"],
    how="outer"
  ).fillna(0)

  merged["Total"] = merged.get("Ban Count", 0) + merged.get("Challenge Count", 0)
  merged = merged.sort_values(by="Total", ascending=False).head(10)
  merged = merged.sort_values(by="Ban Count", ascending=False)

  labels = merged["Title"] + " (" + merged["Author"] + ")"
  banned_counts = merged["Ban Count"]
  challenged_counts = merged["Challenge Count"]

  fig = go.Figure(data=[
      go.Bar(name='Banned', y=labels, x=banned_counts, orientation='h'),
      go.Bar(name='Challenged', y=labels, x=challenged_counts, orientation='h')
  ])

  fig.update_layout(
      barmode='group',
      title=f"{year}",
      yaxis_title='Title (Author)',
      xaxis_title='Count',
      legend_title='Status',
      height=600,
      width=1000,
      xaxis=dict(
          tickmode='linear',
          tick0=0,
          dtick=100,
          range=[0, 1300]
      )
  )

  st.plotly_chart(fig, use_container_width=True)


def display_data():
  data = load_data()

  st.title("Top 10 Banned and Challenged Books by Year")

  by_year_grouped_bar_chart(data, "2024")
  by_year_grouped_bar_chart(data, "2023")
  by_year_grouped_bar_chart(data, "2022")
  by_year_grouped_bar_chart(data, "2021")

display_data()