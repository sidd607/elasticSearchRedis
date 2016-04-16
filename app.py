from flask import Flask, abort, request, jsonify, make_response
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

#Opening a redis connection

r = redis.StrictRedis()

es = Elasticsearch()

app = Flask(__name__)

@app.route('/')
def index():
	return "<center>Demo Redis and ElasticSearch</center>"

@app.route('/index/', methods = ['POST'])
def addMessage():
	replyElastic = addMessageToElactic(request.json)
	replyRedis = addMessageToRedis(request.json)
	reply = {}
	reply["createdRedis"] = replyRedis["created"]
	reply["createdElastic"] = replyElastic["created"]
	return jsonify(reply), 201

def addMessageToElactic(message):
	finMessage = {}
	finMessage['content'] = message['content']
	finMessage['posted-at'] = datetime.now()
	msg = es.index(index = "messages", doc_type = "text", body=finMessage)
	reply = {}
	if msg["created"] == True:
		reply["created"] = True
	else :
		reply["created"] = False
	return reply

def addMessageToRedis(message):
	length = r.llen("messages")
	messageKey = "message:" + str(length)
	
	x = r.hset(messageKey, "content", message['content'])
	if int(x) == 0:
		return {"created" : False}
	
	x = r.hset(messageKey, "posted-at", datetime.now())
	if int(x) == 0:
		return {"created" : False}
	
	x = r.rpush("messages", messageKey)
	if int(x) == 0:
		return {"created": False}

	return {"created" : True}


@app.route('/index/', methods = ['GET'])
def search():
	reply = {}
	noMessages = int(r.llen("messages"))
	if noMessages == 0:
		return jsonify({"messages":0}), 201
	
	reply["message"] = noMessages
	msgList = []
	messageKey = r.lrange("messages", 0, noMessages)

	for key in messageKey:
		msgList.append(r.hgetall(key))

	reply["messageList"] = msgList

	return jsonify(reply), 201

@app.route('/search/', methods = ['GET'])
def invalid():
	return jsonify({"error": "Nice Error"})


@app.route('/search/<string:searchMessage>', methods = ['GET'])
def getMessageElastic(searchMessage):
	res = es.search(index = "messages", doc_type = "text", body = {"query": {"match" : {"content" : searchMessage}}})
	results = {}
	results["found"] = res["hits"]["total"]
	if results["found"] <= 0:
		return jsonify(results)
	messages = res["hits"]["hits"]
	repMsg = []
	for hit in messages:
		tmp = {}
		tmp["content"] = hit["_source"]["content"]
		tmp["posted-at"] = hit["_source"]["posted-at"]
		repMsg.append(tmp)
	results["messages"] = repMsg
	return jsonify(results)


@app.errorhandler(404)
def notFound():
	return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
	app.run(debug=True)