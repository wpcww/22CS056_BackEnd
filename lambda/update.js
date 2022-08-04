var AWS = require('aws-sdk');
var docClient = new AWS.DynamoDB.DocumentClient({
    apiVersion: '2012-08-10',
    sslEnabled: false,
    paramValidation: false,
    convertResponseTypes: false,
    region: 'ap-east-1'
});
const tableName = 'testjoblist';

exports.handler = async (event, context, callback) => {
    let responseBody = "";
    let statusCode = 0;

    const params = {
        TableName: tableName,
        Item: event
    };

    try {
        const data = await docClient.put(params).promise();
        responseBody = JSON.stringify(data);
        statusCode = 201;
        console.log("POST Request Success");
    } catch (err) {
        responseBody = `Unable to put Product: ${err}` + " ==== " + JSON.stringify(event);
        statusCode = 403;
        console.log(err);
    }

    const response = {
        "statusCode": statusCode,
        "headers":{
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin":"*"
        },
        "body": responseBody
    };
    
    callback(null, response);
    context.succeed(response);

    return event;
};

