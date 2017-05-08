import psycopg2
from datetime import date,datetime
from flask import Flask,jsonify,request
app = Flask(__name__)


try:
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Bank Database Connection String >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    conn_bank = psycopg2.connect(database="mutual-erp-bank", user="odoo", password="odoo", host="localhost", port="5432")
    cur_bank = conn_bank.cursor()

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Residential Database Connection String >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    conn_residential = psycopg2.connect(database="mutual-erp-residential", user="odoo", password="odoo", host="localhost", port="5432")
    cur_residential = conn_residential.cursor()
    print "Databases Successfully Connected"

except:
    print "Unable to connect"


@app.route('/createcustomer', methods=['POST'])
def createcustomer():
    if request.form['name'] != False:
        name = request.form['name']
        cs = str(request.form['cs']).replace('False', ' ')
        bank_code = str(request.form['bank_code']).replace('False', ' ')
        branch_code = str(request.form['branch_code']).replace('False', ' ')
        street = str(request.form['street1']).replace('False', ' ')
        print(street)
        street2 = str(request.form['street2']).replace('False', ' ')
        print(type(street2))
        city = str(request.form['city']).replace('False', ' ')
        print(type(city))
        query = "INSERT INTO bank_customers (name,cs,bank_coder,branch_code,street1,street2,city,create_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        query_for_visit = "INSERT INTO new_visits (name,address,stages,cs_number,create_date) VALUES (%s,%s,%s,%s,%s)"
        data = (name,cs,bank_code,branch_code,street,street2,city,datetime.now())
        data_for_visit = (name,branch_code+"\n"+street+"\n"+street2+"\n"+city,1,cs,datetime.now())
        cur_residential.execute(query_for_visit,data_for_visit)
        cur_residential.execute(query, data)
        conn_residential.commit()
        return "Success"

if __name__ == '__main__':
    app.run(debug=True, port=2020)