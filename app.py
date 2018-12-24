from flask import Flask, render_template,request,send_file
import datetime
import pandas as pd
from geopy.geocoders import Nominatim




app=Flask(__name__)



@app.route("/")

def  index():
    return render_template("index.html")

@app.route("/success_table",methods=["POST"])

def  success_table():
    global file
    global filename
    if  request.method=="POST":
        file = request.files["file"]
        try:
            df = pd.read_csv(file)
            print(df)
            n=Nominatim()
            df["coordinates"] = df["Address"].apply(n.geocode)
            df['Latitude'] = df['coordinates'].apply(lambda x: x.latitude if x != None else None)
            df['Longitude'] = df['coordinates'].apply(lambda x: x.longitude if x != None else None)
            df = df.drop("coordinates", 1)
            filename = datetime.datetime.now().strftime("sample_files/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            df.to_csv(filename, index=None)



            #print(type(file))
            return render_template("index.html",text=df.to_html(),btn="download.html")
        except Exception as e:
            return render_template("index.html", text=str(e))

@app.route("/download-file/")

def download():
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)



if __name__=="__main__":
    app.debug=True
    app.run(port=50004)