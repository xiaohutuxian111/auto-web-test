from enum import Enum



class BrowserType(str, Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"
    SAFARI = "safari"


class WaitStrategy(str, Enum):
    PRESENCE = "presence"
    VISIBILITY = "visibility"
    CLICKABLE = "clickable"
    ALL = "all"


class Keys:
    ENTER = "\ue007"
    TAB = "\ue004"
    ESCAPE = "\ue00c"
    BACKSPACE = "\ue003"
    DELETE = "\ue017"
    ARROW_UP = "\ue013"
    ARROW_DOWN = "\ue015"
    ARROW_LEFT = "\ue012"
    ARROW_RIGHT = "\ue014"
    HOME = "\ue011"
    END = "\ue010"
    PAGE_UP = "\ue00e"
    PAGE_DOWN = "\ue00f"
    F5 = "\ue035"
    CTRL = "\ue009"
    SHIFT = "\ue008"
    ALT = "\ue00a"


# 常用断言消息
class AssertMessages:
    ELEMENT_NOT_FOUND = "Element not found: {}"
    ELEMENT_NOT_VISIBLE = "Element not visible: {}"
    ELEMENT_NOT_CLICKABLE = "Element not clickable: {}"
    TEXT_NOT_MATCH = "Text not match. Expected: {}, Actual: {}"
    ATTRIBUTE_NOT_MATCH = "Attribute not match. Expected: {}, Actual: {}"
    URL_NOT_MATCH = "URL not match. Expected: {}, Actual: {}"
    TITLE_NOT_MATCH = "Title not match. Expected: {}, Actual: {}"


# 常用操作等待时间（秒）
class WaitTime:
    PAGE_LOAD = 30
    ELEMENT_LOAD = 10
    AJAX_LOAD = 10
    ANIMATION = 1
    CLICK = 1
    TYPE = 1


# 常用 HTTP 状态码
class HttpStatus:
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# 常用正则表达式
class Regex:
    EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    PHONE = r"^\+?1?\d{9,15}$"
    URL = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"
    DATE = r"^\d{4}-\d{2}-\d{2}$"
    TIME = r"^\d{2}:\d{2}:\d{2}$"
    DATETIME = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"


# 常用颜色代码
class Colors:
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    BLACK = "#000000"
    WHITE = "#FFFFFF"
    GRAY = "#808080"


# 常用日期格式
class DateFormat:
    STANDARD = "%Y-%m-%d"
    WITH_TIME = "%Y-%m-%d %H:%M:%S"
    CHINESE = "%Y年%m月%d日"
    SHORT = "%y-%m-%d"
    FILE_NAME = "%Y%m%d"
    TIMESTAMP = "%Y%m%d%H%M%S"


# 常用文件大小单位


class FileSize:
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    TB = 1024 * GB


# 常用时间单位（秒）
class TimeUnit:
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY
    YEAR = 365 * DAY


class Degree(Enum):
    """学位"""
    普通高中 = "普通高中"
    技工学校 = "技工学校"
    职业高中 = "职业高中"
    中等专科 = "中等专科"
    中等技校 = "中等技校"
    大学专科 = "大学专科"
    大学本科 = "大学本科"
    硕士研究生 = "硕士研究生"
    博士研究生 = "博士研究生"
    其他 = "其他"


class Qualifications(Enum):
    """学历"""
    初中及以下 = "初中及以下"
    高中中专 = "高中、中专"
    大专本科 = "大专、本科"
    硕士研究生 = "硕士研究生"
    博士研究生 = "博士研究生"


class Title(Enum):
    """职称"""
    初级 = "初级"
    助理工程师 = "助理工程师"
    工程师 = "工程师"
    高级工程师 = "高级工程师"
    正高级工程师 = "正高级工程师"
    讲师 = "讲师"
    副教授 = "副教授"
    教授 = "教授"
    高级技师 = "高级技师"
    技师 = "技师"
    高级经济师 = "高级经济师"
    会计师 = "会计师"
    高级会计师 = "高级会计师"
    其他 = "其他"


class InvestigateType(Enum):
    """研究类型"""
    其他 = '其他'
    临床研究 = '临床研究'
    应用开发 = '应用开发'
    应用基础研究 = '应用基础研究'
    基础研究 = '应用基础研究'


class DeliverableType(Enum):
    """成果物"""
    奖励证书 = '奖励证书'
    专著编书 = '专著编书'
    专利成果 = '专利成果'
    论文成果 = '论文成果'
    其他成果 = '其他成果'





class FileType(Enum):
    PNG = ".png"
    JPEG = ".jpeg"
    BMP = ".bmp"
    JPG = ".jpg"
    TXT = ".txt"
    XLSX = ".xlsx"
    XLS = ".xls"
    PPTX = ".pptx"
    PDF = ".pdf"
    RAR = ".rar"
    AVI = ".avi"
    RM = ".rm"
    RMV = "rmvb"
