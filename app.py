from flask import Flask , redirect , url_for , render_template ,request
import csv
app = Flask(__name__)

@app.route('/<string:pagename>')
def home(pagename):
    return render_template(pagename)


@app.route('/')
def redirect_to_home():
    return render_template('index.html')



@app.route('/submit_form', methods=['POST'])
def submit():    
    data = request.form.to_dict()
    print(data)
    if data['name'] != '' and '@' in data['email'] and 'amazon.in' in data['product link'] and ',' not  in data['your price']:
        with open('database.csv','a') as csv_file:
            csv_writer= csv.writer(csv_file)
            csv_writer.writerow([data['name'],data['email'],data['your price'],data['product link']])
        return redirect('/successful.html')
    else:
        return redirect('/tryagain.html')
