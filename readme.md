# Dashboard for Notion Habits Tracker
I use a daily Habits Tracker on Notion. Previously I used Notion's export to csv function and Google Sheets to analyze the data and make simple charts. 

In this repo, I use the python API to access the data directly, so I can analyze the data using pandas and visualize it on Streamlit. 

# Set Up
You will need
* an [Integration Token](https://www.redgregory.com/notion/2021/5/13/how-to-find-the-token-to-connect-zapier-and-notion) for your Notion page.
* to share your Notion page with the integration token you just created. 
* the [database ID](https://developers.notion.com/docs/getting-started#share-a-database-with-your-integration) of the database you want to query. 
* The `token_v2` of a logged in Notion browser page

Keep these secret in a `tokens.json` file, like this:
```
{
    "database_id": "YOUR_DATABASE_ID",
    "integration_token": "YOUR_INTEGRATION_TOKEN"
}
```

## References
* [Productivity Tracking with the Notion API and Python](https://towardsdatascience.com/productivity-tracking-with-the-notion-api-and-python-f5f866fe11d8)