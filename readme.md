# Dashboard for Notion Habits Tracker
I use a daily Habits Tracker on Notion. Previously I used Notion's export to csv function and Google Sheets to analyze the data and make simple charts. 

In this repo, I use the Notion API to access the data directly, then analyze it using pandas and visualize it on Streamlit. 

Because the Notion API has a limit of 100 items which can be queried at any time, I maintain a local copy of the data and update it with the latest 100. This will be saved as a json file in a `/data` folder.

# Roadmap
- Use of 'habit categories' to compare how different aspects are proceeding (e.g. Producitivity, Wellness) - maybe in subplots
- Indication of when there were changes in the habits (e.g. Swapped out some habits for another) - vlines?
- Sidebar
    - Select Month to view
    - Select Date Range to view

# Set Up
You will need
* an [Integration Token](https://www.redgregory.com/notion/2021/5/13/how-to-find-the-token-to-connect-zapier-and-notion) for your Notion page.
* to share your Notion page with the integration token you just created. 
* the [database ID](https://developers.notion.com/docs/getting-started#share-a-database-with-your-integration) of the database you want to query. 

Keep these secret in an `.env` file, like this:
```
    database_id=YOUR_DATABASE_ID
    integration_token=YOUR_INTEGRATION_TOKEN
```

## References
* [Notion API](https://developers.notion.com/reference/post-database-query)
* [Productivity Tracking with the Notion API and Python](https://towardsdatascience.com/productivity-tracking-with-the-notion-api-and-python-f5f866fe11d8)