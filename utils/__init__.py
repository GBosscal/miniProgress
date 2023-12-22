from datetime import datetime


def days_since_given_date_by_str(given_date: str):
    # 将传入的日期字符串转换为datetime对象
    given_datetime = datetime.strptime(given_date, "%Y-%m-%d")

    # 获取今天的日期
    today = datetime.today()

    # 计算天数差异
    days_difference = (today - given_datetime).days

    return days_difference


def days_since_given_date_by_datetime(given_date: datetime):
    # 将传入的日期字符串转换为datetime对象
    # given_datetime = datetime.strptime(given_date, "%Y-%m-%d")

    # 获取今天的日期
    today = datetime.today()

    # 计算天数差异
    days_difference = (today - given_date).days

    return days_difference


def format_datetime_to_string(dt, format_str="%Y-%m-%d %H:%M:%S"):
    """
    将 datetime 对象格式化为字符串

    Parameters:
    - dt (datetime): 要转换的 datetime 对象
    - format_str (str): 格式化字符串，默认为 "%Y-%m-%d %H:%M:%S"

    Returns:
    - str: 格式化后的字符串
    """
    return dt.strftime(format_str)
