from flask import Flask, render_template
import requests as req
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route("/")
def index():
     return render_template("index.html")

@app.route("/extra")
def extra():
     return render_template("extra.html")

@app.route("/r6track")
def r6_track():
    userid = "6a0b295b-0fe1-4f4f-a4d8-4a52c5fd76f4"
    # Making a GET request
    r = req.get('https://r6.tracker.network/profile/id/{}'.format(userid))

    # print(r.status_code)
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # print(soup.prettify())
    user_name = str(soup.find('span', class_='trn-profile-header__name').text).strip()
    right_bar = soup.find('div', class_='trn-scont__aside')
    rank_name = str(right_bar.find('div', class_='trn-text--dimmed').text)
    season_stat = right_bar.find_all('div', class_='trn-card__content pt8 pb8')
    temp = str(season_stat).split("</div>")[1].split("<span>")
    rank_MMR = temp[2].split(" ")[0]
    rank_KD = temp[1].split(" ")[0]

    data={
        'user': user_name,
        'tier': rank_name,
        'mmr': rank_MMR,
        'kd': rank_KD
    }

    return render_template("r6track.html",data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)