"use strict";

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
    let params = { TableName: tableName };
    let scanResults = [];
    let items;

    do {
        items = await docClient.scan(params).promise();
        console.log(items);
        items.Items.forEach((item) => scanResults.push(item));
        params.ExclusiveStartKey = items.LastEvaluatedKey;
    } while (typeof items.LastEvaluatedKey != "undefined");

    const responseBody = {
        statusCode: 200,
        body: JSON.stringify(scanResults),
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    };

    return responseBody;
};
