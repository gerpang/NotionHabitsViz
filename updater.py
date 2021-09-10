import json
from decouple import config
import requests
import datetime
import os

class Updater():
    def __init__(self):
        self.savefilepath = './data/habits.json'
        self.NOTION_URL = "https://api.notion.com/v1/databases/"
        self.integration_token =  config("INTEGRATION_TOKEN")
        self.DATABASE_ID = config("DATABASE_ID")
        self.database_url = self.NOTION_URL + self.DATABASE_ID + "/query"
        self.today = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
        self.month_ago = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(30), "%Y-%m-%d")
        self.data ={
      "filter": {
        "and": [
          {
            "property": "Date",
                    "date": {
                        "after": self.month_ago
                    }
          },
          {
                    "property": "Date",
                    "date": {
                        "on_or_before": self.today
                    }
                }
            ]
        },
      "sorts": [
        {
          "property": "Date",
          "direction": "descending"
        }
      ]
    }
    
    
    def get_response(self):
        response = requests.post(self.database_url, 
                                 headers={"Authorization": f"{self.integration_token}", 
                                          "Notion-Version":"2021-08-16"},
                                json=self.data)
        if response.status_code != 200:
            raise ApiError(f'Response Status: {response.status_code}')
        else:
            return response.json()

    def get_checks_from_day(self, day):
        # day is a dictionary
        # with the key of properties
        # for all the 'headers' in the notion table
        output_dic = {}
        for prop_name, prop_dic in day['properties'].items():
            if prop_dic['type'] == 'checkbox':
                col_name = prop_name.encode('ascii', 'ignore').decode('ascii').strip()
                col_status = prop_dic['checkbox']
                output_dic[col_name] = col_status
        return {day['properties']['Date']['date']['start']: output_dic}

    def get_data(self, savefilepath):
        if os.path.exists(savefilepath):
            with open(savefilepath, 'r') as f:
                data = json.load(f)
        else:
            os.makedirs(savefilepath)
            data = {}
        return data

    def save_data(self, new_data, savefilepath):
        data = self.get_data(savefilepath)
        data.update(new_data)
        with open(savefilepath, 'w') as f:
            json.dump(data, f)
            
    def run(self):
        results = self.get_response()
        new_data = {}
        for day in results['results']:
            day_habits_dic = self.get_checks_from_day(day)
            new_data.update(day_habits_dic)
        self.save_data(new_data, self.savefilepath)

if __name__ == "__main__":
    updater = Updater()
    updater.run()