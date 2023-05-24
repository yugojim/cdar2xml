import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import xmltodict
import Function

#eq	資源值等於或完全包含在參數值中	參數值的範圍完全包含資源值的範圍
#ne	資源值不等於參數值	參數值的範圍不完全包含資源值的範圍
#gt	資源值大於參數值	參數值上方的範圍與資源值的範圍相交（即重疊）
#lt	資源值小於參數值	參數值以下的範圍與資源值的範圍相交（即重疊）
#ge	資源值大於或等於參數值	參數值上方的範圍與資源值的範圍相交（即重疊），或者參數值的範圍完全包含資源值的範圍
#le	資源值小於或等於參數值	參數值以下的範圍與資源值的範圍相交（即重疊），或者參數值的範圍完全包含資源值的範圍
#sa	資源值在參數值之後開始	參數值的範圍與資源值的範圍不重疊，參數值上方的範圍包含資源值的範圍
#eb	資源值在參數值之前結束	參數值的範圍與資源值的範圍不重疊，參數值下面的範圍包含資源值的範圍
#ap	資源值與參數值大致相同。#請注意，近似值的建議值是規定值的 10%（對於日期，現在是和日期之間差距的 10%），但系統可能會在適當的情況下選擇其他值
fhir = 'http://104.208.68.39:8080/fhir/'#4600VM
#fhir = "http://61.67.8.220:8080/fhir/"#skh outside
#fhir = "http://10.2.1.17:8080/fhir/"#skh inside
#fhir = "https://sit-fhir.skh.org.tw/fhir/" #skh https
#fhir = "http://106.105.181.72:8080/fhir/"#tpech

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###serverstatus###
@app.route('/', methods=['GET'])
@cross_origin()
def serverstatus():
    return jsonify({'Server Status' : 'run'}), 200

###DischargeSummary###
@app.route('/DischargeSummary/', methods=['GET'])
@cross_origin()
def query_DischargeSummary():
    url = fhir + 'Composition?title=出院'
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['GET'])
@cross_origin()
def query_DischargeSummaryID(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['POST'])
@cross_origin()
def create_DischargeSummary(DischargeSummary_Id):
    #record = json.loads(request.data)
    #record = json.loads(request.data, strict=False)
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostDischargeSummary(record, DischargeSummary_Id)
    return jsonify(Composition), status_code

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['PUT'])
@cross_origin()
def update_DischargeSummary(DischargeSummary_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostDischargeSummary(record, DischargeSummary_Id)
    return jsonify(Composition), status_code    
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['DELETE'])
@cross_origin()
def delte_DischargeSummary(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###VisitNote###
#msh
@app.route('/VisitNote/', methods=['GET'])
@cross_origin()
def query_VisitNote():
    Search=''
    if request.args.get('Patient_Id') != None:
        Search = 'patient=' + request.args.get('Patient_Id') + '&'
    if request.args.get('mtDate') != None:
        Search = Search + 'date=ge' + request.args.get('mtDate') + '&'        
    if request.args.get('ltDate') != None:
        Search = Search + 'date=le' + request.args.get('ltDate')
    url = fhir + 'Composition/?' + Search
    #print(url)
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
'''
#skh
@app.route('/VisitNote/', methods=['GET'])
@cross_origin()
def query_VisitNote():
    url = fhir + 'Composition?title=門診'
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
'''    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['GET'])
@cross_origin()
def query_VisitNoteID(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['POST'])
@cross_origin()
def create_VisitNote(VisitNote_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostVisitNote(record, VisitNote_Id)
    return jsonify(Composition), status_code

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['PUT'])
@cross_origin()
def update_VisitNote(VisitNote_Id):
    record = xmltodict.parse(request.data)
    Composition, status_code = Function.PostVisitNote(record, VisitNote_Id)
    return jsonify(Composition), status_code    
    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['DELETE'])
@cross_origin()
def delte_VisitNote(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8100, debug=False)
	app.run(port=8100, debug=True)