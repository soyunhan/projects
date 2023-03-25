from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.40aduh7.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=191597'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


@app.route('/')
def home():
    return render_template('index.html') 

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']


    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property = "og:title"]')['content']
    ogdesc = soup.select_one('meta[property = "og:description"]')['content']
    ogimage = soup.select_one('meta[property = "og:image"]')['content']
    

    list_data = list(db.movies.find({},{'_id':False}))
    num = len(list_data) + 1 


    doc = {
        'title' : ogtitle,
        'desc' : ogdesc,
        'img' : ogimage,
        'comment' : comment_receive,
        'star' : star_receive,
        'num' : num
    }
     
    db.movies.insert_one(doc)
    return jsonify({'msg':'저장 완료!'})

# 삭제
@app.route("/movie/delete", methods=["POST"])
def movie_delete():
    delete_receive = request.form['delete_give']
    db.movies.delete_one({'num': int(delete_receive)})
    return jsonify({'msg': '삭제 완료!'})
 

@app.route("/movie", methods=["GET"])
def movie_get():
    movies_data = list(db.movies.find({},{'_id':False}))
    return jsonify({'result': movies_data})
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)