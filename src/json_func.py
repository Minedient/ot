import json
from datetime import datetime

class OTData:
    """
    A class to represent the OT data.
    """
    def __init__(self, date: str, amount: int, reason: str, by: str):
        """
        Initialize the OTData object with date, amount, reason, and by.
        """
        self.entry = {"date": date, "amount": amount}
        if reason:
            self.entry["reason"] = reason
        if by:
            self.entry["by"] = by

    def to_dict(self) -> dict:
        """
        Convert the entry to a dictionary.
        """
        return self.entry

class OTDStorage:
    """
    OTDStorage (OT Data Storage) class to manage the storage of OT data.

    This is a wrapper class for handling the loading, saving, and creating of a JSON file that stores OT data.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.data = None

    def loadJson(self):
        """
        Load the JSON file.
        """
        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = self.newJson()


    def saveJson(self):
        """
        Save the JSON file.
        """
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def newJson(self):
        """
        Create a new JSON file with the given filename.
        """
        self.data = {
            "entries": [],
            "total": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "workhour": {
                "start": "08:10",
                "end": "16:58",
                "lunch_start": "12:30",
                "lunch_end": "13:30",
            }
        }
        self.saveJson()
        return self.data

    @property
    def entries(self) -> list[dict]:
        """
        Get the entries from the JSON file.
        """
        return self.data["entries"]
    
    @entries.getter
    def entries(self) -> list[dict]:
        """
        Get the entries from the JSON file.
        """
        return self.data["entries"]
    
    @property
    def total(self) -> int:
        """
        Get the total number of entries in the JSON file.
        """
        return self.data["total"]
    
    @total.setter
    def total(self, value: int):
        """
        Set the total number of entries in the JSON file.
        """
        self.data["total"] = value
    
    @property
    def last_updated(self) -> str:
        """
        Get the last updated time of the JSON file.
        """
        return self.data["last_updated"]
    
    @last_updated.setter
    def last_updated(self, value: str):
        """
        Set the last updated time of the JSON file.
        """
        self.data["last_updated"] = value
        
    @property
    def workhour_start(self) -> str:
        """
        Get the start time of work hours.
        """
        return self.data["workhour"]["start"]
    
    @workhour_start.setter
    def workhour_start(self, value: str):
        """
        Set the start time of work hours.
        """
        self.data["workhour"]["start"] = value

    @property
    def workhour_end(self) -> str:
        """
        Get the end time of work hours.
        """
        return self.data["workhour"]["end"]
    
    @workhour_end.setter
    def workhour_end(self, value: str):
        """
        Set the end time of work hours.
        """
        self.data["workhour"]["end"] = value

    @property
    def workhour_lunch_start(self) -> str:
        """
        Get the start time of lunch break.
        """
        return self.data["workhour"]["lunch_start"]
    
    @workhour_lunch_start.setter
    def workhour_lunch_start(self, value: str):
        """
        Set the start time of lunch break.
        """
        self.data["workhour"]["lunch_start"] = value
        
    @property
    def workhour_lunch_end(self) -> str:
        """
        Get the end time of lunch break.
        """
        return self.data["workhour"]["lunch_end"]
    
    @workhour_lunch_end.setter
    def workhour_lunch_end(self, value: str):
        """
        Set the end time of lunch break.
        """
        self.data["workhour"]["lunch_end"] = value
    
    @property
    def totalLength(self) -> int:
        """
        Get the total amount from the JSON file.
        """
        return sum(entry["amount"] for entry in self.entries)
    
    @property
    def numOfDaySince(self) -> int:
        """
        Get the number of days since the first entry in the JSON file.
        """
        if not self.entries:
            return 0
        first_date = datetime.strptime(self.firstDate(), "%Y-%m-%d")
        today = datetime.now()
        return (today - first_date).days
    
    def rangedTotalLength(self, start_date: str, end_date: str) -> int:
        """
        Get the total amount in a specific date range.
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        return sum(entry["amount"] for entry in self.entries if start_date <= datetime.strptime(entry["date"], "%Y-%m-%d") <= end_date)

    def rangedTotal(self, start_date: str, end_date: str) -> int:
        """
        Get the total number of entries in a specific date range.
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        return sum(1 for entry in self.entries if start_date <= datetime.strptime(entry["date"], "%Y-%m-%d") <= end_date)

    def median(self) -> float:
        """
        Calculate the median of the amounts in the JSON file.
        """
        if not self.entries:
            return 0.0
        amounts = sorted(entry["amount"] for entry in self.entries)
        n = len(amounts)
        mid = n // 2
        if n % 2 == 0:
            return (amounts[mid - 1] + amounts[mid]) / 2.0
        else:
            return float(amounts[mid])
        
    def standardDeviation(self) -> float:
        """
        Calculate the standard deviation of the amounts in the JSON file.
        """
        if not self.entries:
            return 0.0
        mean = self.totalLength / self.total
        variance = sum((entry["amount"] - mean) ** 2 for entry in self.entries) / self.total
        return variance ** 0.5

    def newEntry(self, date: str, amount: int, reason: str = None, by: str = None):
        """
        Create a new entry in the JSON file.
        The json data will be updated after running this function.
        """
        # Perform validation on "amount" to ensure it is a positive number
        try:
            amount = int(amount)

            if amount < 0:
                raise ValueError("Amount must be a positive number.")
        except ValueError:
            raise ValueError("Amount must be a valid integer.")

        entry = OTData(date, amount, reason, by).to_dict()  # type ensured, check is skipped
        self.entries.append(entry)
        self.total += 1
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.saveJson()

    def lastDate(self) -> str:
        """
        Get the last date from the JSON file.
        """
        if not self.entries:
            return None
        # Find the latest date in the entries (as the data may not be sorted)
        latest_entry = max(self.entries, key=lambda x: x["date"])
        return latest_entry["date"]
    
    def firstDate(self) -> str:
        """
        Get the first date from the JSON file.
        """
        if not self.entries:
            return None
        # Find the earliest date in the entries (as the data may not be sorted)
        earliest_entry = min(self.entries, key=lambda x: x["date"])
        return earliest_entry["date"]