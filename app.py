from flask import Flask,render_template,request
import os
from final_csd_project import *
app = Flask(__name__)

picfolder = os.path.join('static','pics')
app.config['UPLOAD_FOLDER'] = picfolder
print(app.config['UPLOAD_FOLDER'])
print(os.path.join(app.config['UPLOAD_FOLDER'],'Sentimeent_Pie.png'))

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start/', methods = ['POST'])
def getvalue() :
    hashtag = request.form['hashtag-name']
    username = request.form['username']
    fdate = request.form['from-date']
    todate = request.form['to-date']
    tnum = request.form['tweets-number']
    checki = Sentiment_Analsis(hashtag,username,fdate,todate,tnum)
    if checki == True :
        pie = os.path.join(app.config['UPLOAD_FOLDER'],'Sentimeent_Pie.png')
        bar = os.path.join(app.config['UPLOAD_FOLDER'],'Sentimeent_Bar.png')
        sca = os.path.join(app.config['UPLOAD_FOLDER'],'Sentimeent_Scatter_OverTime.png')
        wine = os.path.join(app.config['UPLOAD_FOLDER'],'wine.png')
        return render_template('pass2.html', info = "Data found",pie_chart = pie,bar_chart = bar,scatter_chart = sca,wine_cloud = wine)
    else :
        pie = os.path.join(app.config['UPLOAD_FOLDER'],'2452502.jpg')
        bar = os.path.join(app.config['UPLOAD_FOLDER'],'2452502.jpg')
        sca = os.path.join(app.config['UPLOAD_FOLDER'],'2452502.jpg')
        wine = os.path.join(app.config['UPLOAD_FOLDER'],'2452502.jpg')
        return render_template('pass.html',info = 'No information found',pie_chart = pie,bar_chart = bar,scatter_chart = sca,wine_cloud = wine)
    #return render_template('index.html',name = username)


if __name__ == '__main__':
    app.run(debug=True)