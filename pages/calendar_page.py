from datetime import datetime, timedelta
import re


class Calendar:
    "Class for interracting with Home Page calendar widget"

    LEFT_ARROW = '//button[@aria-label="Previous month"]'
    RIGHT_ARROW = '//button[@aria-label="Next month"]'
    MONTH_LABEL = '//button[@data-test="DatepickerMonthButton"]'
    MONTH_CONTAINER_TEMPLATE = (
        '//button[@data-test="DatepickerMonthButton"]'
        '//div[contains(text(), "%s")]'
        '/ancestor::div'
        '/following-sibling::div[@data-test="CalendarContainer"]'
    )
    DAY_CELL_TEMPLATE = '//div[@data-test="DayDateTypography" and text()="%s"]'


    def __init__(self, page):
        self.page = page

    def _convert_time_to_days(self, time_string: str) -> int:
        """Converts time string ex. '1 week', '3 days', '2 months' to days amount.

        @param string time_string: String that presents time offset.

        @return integer: Number of days as an integer.
        """

        time_mapping = {
            'day': 1, 'days': 1,
            'week': 7, 'weeks': 7,
            'month': 30, 'months': 30
        }

        match = re.match(r'(\d+)\s*(\w+)', time_string.strip().lower())

        if not match:
            raise ValueError(f'Invalid time format: {time_string}')
        value, unit = match.groups()
        return int(value) * time_mapping[unit]

    def select_date(self, target_date: datetime):
        """Selects a specific date in the calendar, switching months if necessary.

        @param datetime target_date: Datetime object which represents target date.
        """
        target_month_year = target_date.strftime('%B %Y')
        target_day = target_date.day

        while True:
            visible_months = self.page.locator(self.MONTH_LABEL).all()
            visible_months_text = [month.text_content().strip() for month in visible_months]

            if target_month_year in visible_months_text:
                break

            self.page.click(self.RIGHT_ARROW)

        month_container_locator = self.MONTH_CONTAINER_TEMPLATE % target_date.strftime('%B')
        day_locator = f"{month_container_locator}{self.DAY_CELL_TEMPLATE % target_day}"
        self.page.locator(day_locator).click()

    def select_offset_time(self, time_offset: str):
        """Selects a date offset from the current date.

        @param string time_offset: String that specifies time offset (ex. '1 week', '3 days', '2 months').
        """
        days_offset = self._convert_time_to_days(time_offset)
        target_date = datetime.now() + timedelta(days=days_offset)
        self.select_date(target_date)