from enum import Enum as EnumBase

# 日志路经
LogPath = "logs"

# Token密钥
AppSecretKey = b'painData12345678'


class DeleteOrNot(EnumBase):
    """
    用户是否被删除的常量定义
    """
    Deleted = True
    NotDeleted = False


class ErrorCode(EnumBase):
    """
    错误代码的常量定义
    """
    Success = "0"

    # 用户
    UserExists = "1001001"
    UserNotExists = "1001002"
    UserUpdateError = "1001003"
    UserAddError = "1001004"
    UserDeleteError = "1001005"

    # 反馈
    FeedbackAddError = "1002001"

    # 城市
    CityExists = "1003001"
    CityAddError = "1003002"
    CityNotExists = "1003003"
    CityUpdateError = "1003004"

    # 集邮册
    StampNotExists = "1004001"
    StampAddError = "1004002"
    StampUpdateError = "1004003"
    StampNotExistsInCity = "1004004"

    # 打卡点
    PointAddError = "1005001"
    PointNotExists = "1005002"
    PointUpdateError = "1005003"
    PointDupName = "1005004"

    # 打卡打卡点
    CheckInPointAddError = "1006001"
    CheckInPointTooFar = "1006002"


class ErrorMsg(EnumBase):
    """
    错误信息的常量定义
    """
    Success = "操作成功"
    UserExists = "用户已经存在"
    UserNotExists = "用户不存在"
    UserUpdateError = "用户信息更新失败"
    UserAddError = "用户新增失败"
    UserDeleteError = "用户删除失败"

    FeedbackAddError = "新增反馈失败"

    CityExists = "城市已经存在"
    CityAddError = "城市新增失败"
    CityNotExists = "城市不存在"
    CityUpdateError = "城市更新失败"

    StampNotExists = "集邮册不存在"
    StampAddError = "集邮册新增失败"
    StampUpdateError = "集邮册更新失败"
    StampNotExistsInCity = "当前城市不存在集邮册"

    PointAddError = "打卡点新增失败"
    PointNotExists = "打卡点不存在"
    PointUpdateError = "打卡点更新失败"
    PointDupName = "打卡点在当前集邮册中已存在"

    CheckInPointAddError = "打卡失败"
    CheckInPointTooFar = "距离打卡点太远，无法打卡!"


class RedisKey:
    AccessTokenKey = "wechat_access_token"


ChineseCities = [
    "北京", "上海", "广州", "深圳", "天津", "重庆", "成都", "杭州", "南京", "武汉",
    "西安", "郑州", "长沙", "沈阳", "青岛", "济南", "大连", "宁波", "厦门", "福州",
    "苏州", "无锡", "佛山", "东莞", "珠海", "合肥", "南昌", "南宁", "昆明", "哈尔滨",
    "长春", "太原", "呼和浩特", "西宁", "银川", "兰州", "南通", "常州", "温州", "绍兴",
    "石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊",
    "衡水", "大庆", "牡丹江", "佳木斯", "齐齐哈尔", "绥化", "黑河", "鸡西", "鹤岗", "双鸭山",
    "伊春", "七台河", "大兴安岭"
]
