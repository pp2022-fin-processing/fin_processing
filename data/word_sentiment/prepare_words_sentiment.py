mf = open("Master_dictionary.csv")
header = mf.readline()

sf = open("sentiment_dictionary.csv", "a")
sf.write("WORD,SENTIMENT\n")

for line in mf:
    words = line.split(",")
    if words[7] != "0":
        sentiment_line = words[0]
        sentiment_line = sentiment_line + ",N"
        sf.write(sentiment_line + "\n")
    elif words[8] != "0":
        sentiment_line = words[0]
        sentiment_line = sentiment_line + ",P"
        sf.write(sentiment_line + "\n")
    elif words[9] != "0":
        sentiment_line = words[0]
        sentiment_line = sentiment_line + ",U"
        sf.write(sentiment_line + "\n")




