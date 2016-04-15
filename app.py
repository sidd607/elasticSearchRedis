from flask import Flask, abort, request, jsonify, make_response
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch()

app = Flask(__name__)

@app.route('/')
def index():
	return "<center>Demo Redis and ElasticSearch</center>"


@app.route('/messages')
def get_messages():
	return jsonify({'tasks' : 1})


@app.route('/tasks/<int:taskId>', methods = ['GET'])
def get_message(taskId):
	task = [task for task in tasks if task['id'] == taskId]
	if len(task) == 0:
		return jsonify({"result": "False"})
	return jsonify({"task": task[0]})


@app.route('/index/message/', methods = ['POST'])
def addMessage():
	reply = addMessageToElactic(request.json)
	return jsonify(reply), 201

def addMessageToElactic(message):
	finMessage = {}
	finMessage['content'] = message['content']
	finMessage['posted-at'] = datetime.now()
	msg = es.index(index = "messages", doc_type = "text", body=finMessage)
	reply = {}
	if msg["created"] == True:
		reply["created"] = True
		reply["id"] = msg["_id"]
	else :
		reply["created"] = False
	return reply


@app.errorhandler(404)
def notFound():
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	app.run(debug=True)


