def format_gitlab_date(gitlab_date):
    return gitlab_date[:16].replace("T","-").replace(":","-")