'''
   This programs performs some complex analysis on twitter data and creates not only figures/plots but also stores the query results in revelant folders and files.

   Input file:/data/twitter_data.json ( the input data has to be stored in "data" folder)
   Outputs: 
      outs: is a folder which contains folders for each query performed below.
      plots: is a folder which contains  a figure/plot for each query performed below.
      
   Mehmet Acikgoz - University of Missouri-Kansas City, December 2019  


'''
import sys
import os
import conda

from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import pandas
import matplotlib.ticker as ticker


conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
os.environ["PROJ_LIB"] = proj_lib
from mpl_toolkits.basemap import Basemap


def init_folder(filename):
    folder = outs_folder + filename
    os.system("rm -rf " + folder)
    return folder

def save_to_folder(df, folder, filename ):
    plt.savefig(plots_folder+filename+".png", dpi = 1200)
    df.rdd.coalesce(1, True).saveAsTextFile(folder)
    plt.close()


# Top 10 languages used in tweets
def query1():
    filename = "langs"
    folder = init_folder(filename)

    df = spark.sql("SELECT lang, COUNT(*) AS c FROM table WHERE lang IS NOT NULL GROUP BY lang ORDER BY c DESC")
    x = df.toPandas()["lang"].values.tolist()[:10]
    y = df.toPandas()["c"].values.tolist()[:10]
    total_number_of_tweets = sum(df.toPandas()["c"].values.tolist())
    print('total_number_of_tweets', total_number_of_tweets)         # To test the result
    plt.bar(x,y, color = 'red')
    plt.title("Top 10 Languages Used In Tweets")
    plt.xlabel("Languages")
    plt.ylabel("Number of Tweets")
    save_to_folder(df, folder, filename)

# Top 10 Country codes available in Tweets
def query2():
    filename = "country"
    folder = init_folder(filename)

    number_of_tweets_from_null_country = sum(spark.sql("SELECT COUNT(*) as count FROM table WHERE place.country_code IS NULL").collect()[0])
    tweets_from_country = spark.sql("SELECT place.country_code, COUNT(*) AS count FROM table WHERE place.country_code IS NOT NULL GROUP BY place.country_code ORDER BY count DESC")

    x = tweets_from_country.toPandas()["country_code"].values.tolist()[:10]
    number_of_tweets_from_country = tweets_from_country.toPandas()["count"].values.tolist()
    y = number_of_tweets_from_country[:10]

    print('number of all tweets', sum(number_of_tweets_from_country)+number_of_tweets_from_null_country) # To test

    plt.rcParams.update({'axes.titlesize': 'small'})
    plt.barh(x,y, color = 'red')
    plt.title("Top 10 Country Codes Available In Tweets")
    plt.ylabel("Countries")
    plt.xlabel("Number of Tweets")

    save_to_folder(tweets_from_country, folder, filename)



# GPS Coordinates of the Twitter Accounts
def query3():
    filename = "GPS_locations"
    folder = init_folder(filename)



    coord = spark.sql("SELECT coordinates.coordinates FROM table WHERE coordinates IS NOT NULL")
    coordDF = coord.select(coord.coordinates[0], coord.coordinates[1])
    x = coordDF.toPandas()["coordinates[0]"].values.tolist()
    y = coordDF.toPandas()["coordinates[1]"].values.tolist()

    m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF')
    m.drawmapboundary(fill_color='#FFFFFF')

    for i in range(len(x)):
        x1, y1 = m(x[i], y[i])
        m.plot(x1, y1, 'r.')

    plt.title("GPS Coordinates of the Twitter Accounts")

    save_to_folder(coord, folder, filename)


# Tweets Distribution in USA
def query4():
    filename = "Tweets_Distribution_in_USA"
    folder = init_folder(filename)

    tweets_from_USA = spark.sql("SELECT user.location, COUNT(*) AS count FROM table WHERE user.location LIKE '%USA%' GROUP BY user.location ORDER BY count DESC")

    # # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = tweets_from_USA.toPandas()["location"].values.tolist()[:10]
    sizes = tweets_from_USA.toPandas()["count"].values.tolist()[:10]
    explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0 )  # only "explode" the 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title("Tweets Distribution in USA")

    save_to_folder(tweets_from_USA, folder, filename)


#Top 10 tweeter
def query5():
    filename = "people_tweets_most"
    folder = init_folder(filename)

    tweets_dist_person = spark.sql("Select  user.id_str, COUNT(user.id_str) AS count from table WHERE user.id_str is not null GROUP BY user.id_str ORDER BY count DESC")
    x = tweets_dist_person.toPandas()["id_str"].values.tolist()[:10]
    y = tweets_dist_person.toPandas()["count"].values.tolist()[:10]
    # total_number_of_tweets = sum(tweets_dist_person.toPandas()["count"].values.tolist())
    # print('total_number_of_tweets', total_number_of_tweets)

    figure = plt.figure()
    axes = figure.add_axes([0.35, 0.1, 0.60, 0.85])
    plt.barh(x,y, color = 'blue')
    plt.title("Top 10 Tweeters")
    plt.ylabel("User id")
    plt.xlabel("Number of Tweets")

    save_to_folder(tweets_dist_person, folder, filename)


#Top 10 People Who Have Most Friends
def query6():
    filename = "people_with_most_friends"
    folder = init_folder(filename)


    friendsCountDF = spark.sql("select user.screen_name, user.friends_count  AS friendsCount from table where (user.id_str, created_at) in (select user.id_str, max(created_at) as created_at from table group by user.id_str ) ORDER BY friendsCount DESC")
    x = friendsCountDF.toPandas()["screen_name"].values.tolist()[:10]
    y = friendsCountDF.toPandas()["friendsCount"].values.tolist()[:10]

    figure = plt.figure()
    axes = figure.add_axes([0.3, 0.1, 0.65, 0.85])
    plt.rcParams.update({'axes.titlesize': 'small'})
    plt.barh(x,y, color = 'green')
    plt.title("Top 10 People Who Have Most Friends")
    plt.ylabel("Screen Name")
    plt.xlabel("Number of Friends")

    save_to_folder(friendsCountDF, folder, filename)

#Hashtags Distribution
def query7():
    filename = "hashtags_distribution"
    folder = init_folder(filename)

    hashtagsDF = spark.sql("SELECT hashtags, COUNT(*) AS count FROM (SELECT explode(entities.hashtags.text) AS hashtags FROM table) WHERE hashtags IS NOT NULL GROUP BY hashtags ORDER BY count DESC")

    # # # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = hashtagsDF.toPandas()["hashtags"].values.tolist()[:10]
    sizes = hashtagsDF.toPandas()["count"].values.tolist()[:10]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Hashtags Distribution")

    save_to_folder(hashtagsDF, folder, filename)


# Query 8 = Tweet distribition according to time -Time series
def query8():
    filename = "tweets_distributionPerMinute"
    folder = init_folder(filename)

    tweet_distributionDF = spark.sql("SELECT SUBSTRING(created_at,12,5) as time_in_hour, COUNT(*) AS count FROM table GROUP BY time_in_hour ORDER BY time_in_hour ")
    x = pandas.to_numeric(tweet_distributionDF.toPandas()["time_in_hour"].str[:2].tolist()) + pandas.to_numeric(tweet_distributionDF.toPandas()["time_in_hour"].str[3:5].tolist())/60
    y = tweet_distributionDF.toPandas()["count"].values.tolist()

    tick_spacing = 1
    fig, ax = plt.subplots(1, 1)
    ax.plot(x, y)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.title("Tweets Distribution By Minute")
    plt.xlabel("Hours (UTC)")
    plt.ylabel("Number of Tweets")

    save_to_folder(tweet_distributionDF, folder, filename)

# Top Devices Used in the Tweets
def query9():
    filename = "devices"
    folder = init_folder(filename)

    # df = spark.sql("SELECT source, COUNT(*) AS  total_count FROM table WHERE source IS NOT NULL GROUP BY source ORDER BY total_count DESC LIMIT 10")
    df = spark.sql("SELECT source, COUNT(*) AS  total_count FROM table WHERE source IS NOT NULL GROUP BY source ORDER BY total_count DESC")
    first = df.toPandas()["source"].str.index(">")+1
    last = df.toPandas()["source"].str.index("</a>")

    text = df.toPandas()["source"].values.tolist()[:10]
    x =[]
    for i in range(len(text)):
        x.append(text[i][first[i]:last[i]])

    y = df.toPandas()["total_count"].values.tolist()[:10]


    figure = plt.figure()
    axes = figure.add_axes([0.3, 0.1, 0.65, 0.85])
    plt.barh(x,y, color = 'blue')
    # plt.title("Top ", len(x), " Devices")
    plt.ylabel("Device name")
    plt.xlabel("Number of Devices")
    plt.title("Top Devices Used in the Tweets")

    save_to_folder(df, folder, filename)




#Tweets by Verified & Unverified Users
def query10():
    filename = "verified_users"
    folder = init_folder(filename)

     # OK- verified olayan ve verified tweetlerin sayisi
    verified_usersDF = spark.sql("SELECT user.verified, COUNT(*) AS count FROM table  GROUP BY user.verified ORDER BY user.verified ASC")

    labels = verified_usersDF.toPandas()["verified"].values.tolist()
    sizes = verified_usersDF.toPandas()["count"].values.tolist()
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("Tweets by Verified & Unverified Users")
    save_to_folder(verified_usersDF, folder, filename)



if __name__ == "__main__":

#   configuration part
    plots_folder = './plots/'
    outs_folder = './outs/'

    if not os.path.exists('plots'):
       os.mkdir('plots')
       print('Directory plots created.')
    else:
       print('Directory plots already exists. Deleting the content')
       os.system('rm -f ./plots/*') 


    if not os.path.exists('outs'):
       os.mkdir('outs')
       print('Directory outs created')
    else:
       print('Directory outs already exists. Deleting the content')
       os.system('rm -rf ./outs/*') 


    print("Hello PySPark Application Started ...")
    spark = SparkSession.builder.appName("HelloWorld PySpark Application").master("local[*]").getOrCreate()
    spark.sparkContext.setLogLevel("INFO")

    tweetsDF = spark.read.json("./data/twitter_data.json", multiLine=False)
    tweetsDF.createOrReplaceTempView("table")

    query1()
    query2()
    query3()
    query4()
    query5()
    query6()
    query7()
    query8()
    query9()
    query10()

    spark.stop()
    print("PsSpark completed and cleaning up")
    os.system('rm -rf spark-warehouse')
