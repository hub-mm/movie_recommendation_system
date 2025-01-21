# ./main.py
from scripts.top_chart.top_chart_rating import build_top_chart
from scripts.top_chart.top_chart_genre import build_genre_chart
from scripts.top_chart.top_chart_hybrid import build_chart_hybrid
from scripts.script_app.random_image import random_img


def main_func(choice, amount=10, genre='action', title='Batman', user_id=1):
    match int(choice):
        case 1:
            return build_top_chart(amount=amount)
        case 2:
            return build_genre_chart(genre=genre, amount=amount)
        case 3:
            return build_chart_hybrid(user_id, title=title, amount=amount)
        case 4:
            return random_img(amount=amount)