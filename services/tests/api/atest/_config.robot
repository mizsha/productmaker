*** Settings ***
Library         REST    ${SERVER}
Library         FakerLibrary
Documentation   Global config.

*** Variables ***
${SERVER}    http://localhost:5000/v1/