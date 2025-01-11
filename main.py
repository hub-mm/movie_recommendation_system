# ./main.py
from scripts.top_chart.top_chart_rating import build_top_chart
from scripts.top_chart.top_chart_genre import build_genre_chart
from scripts.top_chart.top_chart_similar import build_similar_chart
from scripts.top_chart.top_chart_hybrid import build_chart_hybrid


def main(choice, amount=10, genre='action', title='Batman', user_id=1):
    match int(choice):
        case 1:
            print(build_top_chart().head(amount))
        case 2:
            print(build_genre_chart(genre).head(amount))
        case 3:
            print(build_similar_chart(title, amount))
        case 4:
            print(build_chart_hybrid(user_id, title, amount))

if __name__ == '__main__':
    # main(1)
    # main(2, amount=10, genre='horror')
    # main(3, amount=10, title='happy feet')
    main(4, amount=10, title='mean girls', user_id=5000)