*** Settings ***
Library         REST    ${SERVER}
Library         FakerLibrary
Documentation   Global config.

*** Variables ***
${SERVER}       http://localhost:5000/v1/
${API_URL}      https://applifting-python-excercise-ms.herokuapp.com/api/v1/
${API_KEY}      9414d36b-1da2-430a-b8c5-d0961dc37aa4