from .crud import create_default_schema
from .crud import create_or_update_departments
from .database import get_database_session
from .schemas import Department


def create_departments():

    _department = {
        "執行長室": "CEO",
        "技術中心": "CTO",
        "營運中心": "CFO",
        # "Group CFO": "",
        "研究開發處": "RD",
        "研究開發部": "RD",
        # "技術移轉部": "",
        # "智慧財產部": "",
        # "商業卓越處": "",
        # "系統整合部": "",
        # "產品管理部": "",
        "生物資訊暨人工智慧處": "BI",
        "生物資訊部": "BI",
        "人工智慧部": "AI",
        "數據分析部": "DA",
        "數據智能部": "DI",
        # "資料科學處": "",
        # "分子檢驗處": "",
        "次世代定序部": "NGS",
        "轉譯醫學處": "TGI",
        "癌症基因體部": "",
        # "專案管理部": "PM",
        "醫藥資訊部": "MI",
        # "臨床醫學部": "",
        "品保與環境監控部": "QA",
        "法規事務處": "RA",
        # "銷售業務處": "",
        # "銷售業務部": "",
        # "業務行政部": "",
        # "臨床衛教部": "",
        # "行政資源處": "",
        # "行政資源部": "",
        # "會計處": "",
        # "財務與出納部": "",
        "事業暨企業發展處": "BD",
        "資訊處": "IT",
        "人力資源處": "HR",
    }

    db = next(get_database_session())
    departments = [
        Department(name=key, abbreviation=value, active=True)
        for key, value in _department.items()
    ]

    created = create_or_update_departments(db, departments)
    return created


def main():
    create_default_schema()
    create_departments()


if __name__ == "__main__":

    main()
