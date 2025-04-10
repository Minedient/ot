from datetime import datetime, timedelta
from typing import Union

class SDTime:
    """
    A class to calculate and provide various date ranges and specific dates.
    """
    strfdate = "%Y-%m-%d"
    strftime = "%H:%M"
    
    @classmethod
    def thisWeekDates(self, isStr: bool = True):
        """
        Returns a list of dates for the current week (Monday to Sunday).
        """
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        return [start_of_week + timedelta(days=i) for i in range(7)] if not isStr else [(start_of_week + timedelta(days=i)).strftime(self.strfdate) for i in range(7)]

    @classmethod
    def thisMonthDates(self, isStr: bool = True):
        """
        Returns a list of dates for the current month (1st to last day of the month).
        """
        today = datetime.today()
        start_of_month = today.replace(day=1)
        next_month = start_of_month.replace(day=28) + timedelta(days=4)  # this will never fail
        end_of_month = next_month - timedelta(days=next_month.day)
        return [start_of_month + timedelta(days=i) for i in range((end_of_month - start_of_month).days + 1)] if not isStr else [(start_of_month + timedelta(days=i)).strftime(self.strfdate) for i in range((end_of_month - start_of_month).days + 1)]

    @classmethod
    def lastWeekDates(self, isStr: bool = True):
        """
        Returns a list of dates for the last week (Monday to Sunday).
        """
        today = datetime.today()
        start_of_last_week = today - timedelta(days=today.weekday() + 7)  # Monday
        return [start_of_last_week + timedelta(days=i) for i in range(7)] if not isStr else [(start_of_last_week + timedelta(days=i)).strftime(self.strfdate) for i in range(7)]

    @classmethod
    def lastMonthDates(self, isStr: bool = True):
        """
        Returns a list of dates for the last month (1st to last day of the month).
        """
        today = datetime.today()
        first_day_of_this_month = today.replace(day=1)
        last_month = first_day_of_this_month - timedelta(days=1)
        start_of_last_month = last_month.replace(day=1)
        end_of_last_month = last_month
        return [start_of_last_month + timedelta(days=i) for i in range((end_of_last_month - start_of_last_month).days + 1)] if not isStr else [(start_of_last_month + timedelta(days=i)).strftime(self.strfdate) for i in range((end_of_last_month - start_of_last_month).days + 1)]

    @classmethod
    def thisWeekStart(self, isStr: bool = True):
        """
        Returns the start date of the current week (Monday).
        """
        return self.thisWeekDates(isStr)[0]

    @classmethod
    def thisWeekEnd(self, isStr: bool = True):
        """
        Returns the end date of the current week (Sunday).
        """
        return self.thisWeekDates(isStr)[-1]

    @classmethod
    def thisMonthStart(self, isStr: bool = True):
        """
        Returns the start date of the current month (1st).
        """
        return self.thisMonthDates(isStr)[0]

    @classmethod
    def thisMonthEnd(self, isStr: bool = True):
        """
        Returns the end date of the current month (last day).
        """
        return self.thisMonthDates(isStr)[-1]

    @classmethod
    def lastWeekStart(self, isStr: bool = True):
        """
        Returns the start date of the last week (Monday).
        """
        return self.lastWeekDates(isStr)[0]

    @classmethod
    def lastWeekEnd(self, isStr: bool = True):
        """
        Returns the end date of the last week (Sunday).
        """
        return self.lastWeekDates(isStr)[-1]

    @classmethod
    def lastMonthStart(self, isStr: bool = True):
        """
        Returns the start date of the last month (1st).
        """
        return self.lastMonthDates(isStr)[0]

    @classmethod
    def lastMonthEnd(self, isStr: bool = True):
        """
        Returns the end date of the last month (last day).
        """
        return self.lastMonthDates(isStr)[-1]

    @classmethod
    def lastNDays(self, n, isStr: bool = True):
        """
        Returns a list of dates for the last N days (including today).
        """
        today = datetime.today()
        return [today - timedelta(days=i) for i in range(n)] if not isStr else [(today - timedelta(days=i)).strftime(self.strfdate) for i in range(n)]

    @classmethod
    def lastNWeeks(self, n, isStr: bool = True):
        """
        Returns a list of dates for the last N weeks (Monday to Sunday).
        """
        today = datetime.today()
        start_of_last_week = today - timedelta(days=today.weekday() + 7 * n)  # Monday
        return [start_of_last_week + timedelta(days=i) for i in range(7 * n)] if not isStr else [(start_of_last_week + timedelta(days=i)).strftime(self.strfdate) for i in range(7 * n)]

    @classmethod
    def lastNMonths(self, n, isStr: bool = True):
        """
        Returns a list of dates for the last N months (1st to last day of the month).
        """
        today = datetime.today()
        first_day_of_this_month = today.replace(day=1)
        last_month = first_day_of_this_month - timedelta(days=1)
        start_of_last_month = last_month.replace(day=1) - timedelta(days=30 * (n - 1))
        end_of_last_month = last_month
        return [start_of_last_month + timedelta(days=i) for i in range((end_of_last_month - start_of_last_month).days + 1)] if not isStr else [(start_of_last_month + timedelta(days=i)).strftime(self.strfdate) for i in range((end_of_last_month - start_of_last_month).days + 1)]
    
    ### Time Functions ###
    @classmethod
    def diffTime(self, start: str, end: str, isStr = False) -> Union[str, int]:
        """
        Returns the difference between two times in HH:MM format.
        """
        start_time = datetime.strptime(start, self.strftime)
        end_time = datetime.strptime(end, self.strftime)
        delta = end_time - start_time
        return f"{delta.seconds // 3600}:{(delta.seconds // 60) % 60:02d}" if isStr else delta.seconds // 60


if __name__ == "__main__":
    print("This Week Dates:", SDTime.thisWeekDates())