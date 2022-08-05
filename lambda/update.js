var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient({
    apiVersion: "2012-08-10",
    sslEnabled: false,
    paramValidation: false,
    convertResponseTypes: false,
    region: "ap-east-1",
});
const tableName = "testjoblist";

exports.handler = async (event, context) => {
    let responseBody = "";
    let statusCode = 0;
    let extract = JSON.parse(event["body"]);

    const params = {
        TableName: tableName,
        Item: extract,
    };

    try {
        console.log(JSON.stringify(extract));
        const data = await docClient.put(params).promise();
        responseBody = JSON.stringify(data);
        statusCode = 201;
        console.log("POST Request Success");
    } catch (err) {
        responseBody =
            `Unable to put Product: ${err}` + " ==== " + JSON.stringify(event);
        statusCode = 403;
        console.log(err);
    }

    const response = {
        statusCode: statusCode,
        headers: {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*",
        },
        body: responseBody,
    };

    context.succeed(response);

    return event;
};
