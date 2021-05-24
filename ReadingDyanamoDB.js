'use strict'
const AWS = require('aws-sdk');

AWS.config.update({region:"us-west-1"});

exports.handler = async (event, context) => {
    const ddb = new AWS.DynamoDB({apiversion:"2012-10-08"});
    const docClient = new AWS.DynamoDB.DocumentClient({region:"us-west-1"});

    let responseBody = "";
    let statusCode = 0;


    const params = {
        TableName: "Reading",
        limit: 120
    };

    try{
        const data = await docClient.scan(params).promise();
        responseBody = JSON.stringify(data);
        statusCode = 200;
    }catch (err) {
        responseBody = 'Unreacheable Data';
        statusCode = 403;
    }

    const response = {
        statusCode : statusCode,
        body:responseBody
    }

    return response;
}
