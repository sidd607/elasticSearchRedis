## Example for integrating Redis and ElasticSearch in Python

This application consists of mainly 3 apis
1. POST /index - This takes in a sample message and indexes into ElasticSearch and Redis.
2. GET /index - This gets the data from Redis
3. GET /search - This searches data from ElasticSearch.

## API 1
Method: POST
URL: /index
Takes a json of the form 
'''
{
	"content" : "<Message Content>"
}

'''
It takes the message and indexes it to ElasticSearch and add this message to Redis

## API 2
Method: GET
URL: /index

retrieves all the messages added.

## API 3
Method: GET
URL: /search/<searchMessage>
Takes the <searchMessage> and searches over existing messages in ElasticSearch and return a json with the results.