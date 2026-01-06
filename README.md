# ESG News Aggregation Dashboard

An internal ESG news discovery and aggregation tool built to help editorial and news teams quickly find, browse, and export ESG-related news from across the web.

The dashboard aggregates articles via Google News RSS, providing a low-maintenance, stable alternative to site-by-site scraping.

## Overview

The ESG News Aggregation Dashboard allows users to:

View the latest ESG-related news in one place

Search using keywords (e.g. climate, ESG, renewable energy)

Optionally filter results by trusted news sources

Refresh the feed to load the most recent articles

Export results as a CSV for editorial workflows

This project was designed as a lightweight internal tool, prioritizing usability, reliability, and ease of iteration.

## Key Features

Google News RSS aggregation (no direct site scraping)

Keyword-based search (single or multi-word phrases)

Optional source filtering (e.g. Reuters, ESG Today)

Automatic default view (loads ESG news on page open)

Manual refresh button to fetch the latest articles

Clean results table including:

Article title

Source

Published date (sorted newest first)

Short summary/snippet

Clickable “Link” button (no long URLs in the UI)

CSV export for offline use or reporting

## What This Tool Is / Is Not
This tool is:

A news discovery and aggregation dashboard

Intended for internal editorial use

Low-maintenance and easy to extend

Built for fast iteration based on team feedback

This tool is not:

A full web scraper

A replacement for paywalled access (e.g. Bloomberg, FT)

A content extraction or summarization engine

A production-grade crawling system

## Data Source Strategy

Primary data source: Google News RSS

Articles are returned based on keyword relevance

Source filtering is applied after retrieval

Results depend on how Google indexes and categorizes news

This approach was chosen to:

Avoid proxies and paid scraping services

Reduce maintenance overhead

Minimize risk of breaking due to site layout changes

# Getting Started

Prerequisites

Python 3.10+

pip

Install dependencies
pip install streamlit feedparser pandas

Run the app

From the project directory:

python -m streamlit run news_app_g.py

The dashboard will open automatically in your browser.

## Usage Notes

If no keyword is entered, the dashboard defaults to ESG news.

Selecting a source filters results only if articles matching the keyword exist.

Google News RSS returns articles based on search relevance, not full publisher output.

Some sources may appear less frequently depending on keyword choice.

## Project Status

Current stage: Internal pilot

Feedback cycle: Weekly iteration based on newsroom input

Ownership: Product Owner–led iteration and prioritization

Planned Enhancements

Support for multiple keywords (OR logic)

Default keyword set based on newsroom voting

Improved tagging and categorization

Basic analytics (articles per source / keyword)

Optional email or digest-style output

# License

Internal use only.
Not intended for commercial redistribution.
