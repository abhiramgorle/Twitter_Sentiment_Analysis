import snscrape.modules.twitter as sntwitter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import os
from PIL import Image
from wordcloud import WordCloud
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def Sentiment_Analsis(h,u,s,td,t) :
  if u == 'N/A' :
     condition = f'(#{h})until:{td} since:{s}'
     maxTweets = t
  else :
     condition  = f"(#{h}) (from:{u}) until:{td} since:{s}"
     maxTweets = int(t)
  def condn(condition,maxTweets):
      tweets_list1 = []
      for i,tweet in enumerate(sntwitter.TwitterSearchScraper(str(condition)).get_items()):
          if i>maxTweets-1:
              break
          tweets_list1.append([tweet.date,tweet.user.username,tweet.content,tweet.likeCount,tweet.retweetCount])
      tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Username','Text','like_count','retweet_count'])
      return(tweets_df1)
  # here the condition iside the function can be changed according to our needs.
  df1 = condn(condition,maxTweets)
  original_df = df1
  empty_check = df1.empty
  if empty_check == True :
     return False

  df1.insert(loc=0, column='index', value=[i for i in range(len(df1))])

  def clean_text(text):
      text = re.sub(r'http\S+', '', text)
      text = re.sub(r'@\S+', '', text)
      text = re.sub(r'[^\w\s]', '', text)
      text = text.lower()
      return text

  df1['Text'] = df1['Text'].apply(clean_text)

  df = df1.copy()
  df2 = df['Text']
  all_sentences = [] 
  for word in df2:
      x = word.strip()
      all_sentences.append(x)

  df['Text'] = pd.Series(all_sentences)


  """# **Sentiment Analysis using vaderSentiment.SentimentIntensityAnalyser** """

  sia = SentimentIntensityAnalyzer()
  res = {}
  print('\033[1m' + 'NLTK Vaders Analysis on Tweets:' + '\033[0m')
  for i, row in (df.iterrows()):
    content = row['Text']
    index = row['index']
    res[index] = sia.polarity_scores(content)
  vaders_df = pd.DataFrame(res).T
  vaders_df.insert(loc=0, column='index', value=[i for i in range(len(vaders_df))])
  df = df.merge(vaders_df, how="left")

  # Commented out IPython magic to ensure Python compatibility.

  username = h


  data_dir = r"C:/Users/asust/Downloads/csd_final_projects/static/pics/"
  # if not os.path.exists(data_dir):
  #   os.makedirs(data_dir)

  # visualizations_dir = data_dir+'//visualizations//'
  # if not os.path.exists(visualizations_dir):
  #   os.makedirs(visualizations_dir)

  plt.style.use('fivethirtyeight')
  sns.set(rc={'figure.figsize':(10,5)})
  plt.figure(figsize=(5,5), dpi=100)
  data = [df['pos'].mean(),
                  df['neu'].mean(),
                  df['neg'].mean()]
  labels = ['Positive', 'Neutral', 'Negative']
  colors = ["Green", "Orange", "Red"]
  explode = (.03, .03, .03)
  plt.title(f"Vaders Sentiment Score Distribution \nfor all {username} tweets")
  plt.pie(data,
  labels = labels,
  colors = colors,
  explode = explode,
  pctdistance=0.7,
  autopct='%.1f%%')
  plt.savefig(os.path.join(data_dir+"Sentimeent_Pie.png"))
#   plt.show()

  plt.style.use('fivethirtyeight')
  sns.set(rc={'figure.figsize':(10,5)})
  fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
  sns.barplot(data=df,  y="pos", ax=axs[0], color="green")
  sns.barplot(data=df,  y="neu", ax=axs[1], color="orange")
  sns.barplot(data=df,  y="neg", ax=axs[2], color = "red")
  axs[0].set_title('Positive')
  axs[1].set_title('Neutral')
  axs[2].set_title('Negative')
  fig.suptitle(f"Vaders Sentiment Score Distribution for all {username} Tweets", fontsize=20)
  plt.tight_layout()
  plt.savefig(data_dir+"Sentimeent_Bar.png")
#   plt.show()

  plt.style.use('fivethirtyeight')
  sns.set(rc={'figure.figsize':(10,5)})
  plt.figure(figsize=(10,5), dpi=100)
  score_polarity=df.sort_values(by=['compound'], ascending=True)['compound']
  ax = sns.scatterplot(data=df,x="Datetime",y="compound",hue=score_polarity,palette=sns.color_palette("coolwarm", as_cmap=True),legend=False)\
  .set(title=f"Vaders Compound Scores over Time for {username}")
  plt.xticks(rotation=50)
  plt.savefig(data_dir+"Sentimeent_Scatter_OverTime.png")
#   plt.show()
  
  from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
  wine_mask = np.array(Image.open("C:/Users/asust/Downloads/csd_final_projects/image.png"))
  def transform_format(val):
    if val.any() == 0:
        return 255
    else:
        return val
  transformed_wine_mask = np.ndarray((wine_mask.shape[0],wine_mask.shape[1]), np.int32)
  for i in range(len(wine_mask)):
      transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))
  text = " ".join(review for review in df1.Text)
  wc = WordCloud(background_color="white", max_words=1000, mask=transformed_wine_mask,
               stopwords=stop_words, contour_width=3, contour_color='firebrick')
  wc.generate(text)
  wc.to_file("C:/Users/asust/Downloads/csd_final_projects/static/pics/wine.png")
  plt.figure(figsize=[20,10])
  plt.imshow(wc, interpolation='bilinear')
  plt.axis("off")
#   plt.show()

  return True
# x = Sentiment_Analsis('vladirputin','N/A',"2022-02-02","2023-02-02",500)
# print(x)