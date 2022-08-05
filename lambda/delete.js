var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient({
    apiVersion: "2012-08-10",
    sslEnabled: false,
    paramValidation: false,
    convertResponseTypes: false,
    region: "ap-east-1",
});
const tableName = "testjoblist";

exports.handler = async (event, context, callback) => {
    let responseBody = "";
    let statusCode = 0;

    const params = {
        TableName: tableName,
        Key: { Name: JSON.parse(event["body"]).Name },
    };

    try {
        console.log("To be deleted: " + JSON.parse(event["body"]).Name);
        const data = await docClient.delete(params).promise();
        responseBody = JSON.stringify(data);
        statusCode = 204;
    } catch (err) {
        responseBody =
            `Unable to put Product: ${err}` + " ==== " + JSON.stringify(event);
        statusCode = 403;
    }

    const response = {
        statusCode: statusCode,
        body: responseBody,
    };

    //console.log("Event input: " + JSON.stringify(event))

    context.succeed(response);

    return event;
};
