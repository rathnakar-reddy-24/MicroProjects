import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = 'ACd2bb29359d1eb009a8a4dfc011f8b2b1'
auth_token = '9c679fc7cc2c10c50623d43142ed40d0'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('test_page.html')


@app.route('/user_registration_dtls', methods=['GET', 'POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to=phoneNumber,
                               from_="+18303315111",
                               body="Hello " + " " + full_name + " " + "your request to travel from " + " " + source_dt + " to " +
                                    destination_dt + " " + "has " + "been" + " " + status)
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to=phoneNumber,
                               from_="+18303315111",
                               body="Apply later")
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id)


if __name__ == "__main__":
    app.run(port=8081, debug=True)
