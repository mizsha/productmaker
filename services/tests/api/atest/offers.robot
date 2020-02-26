*** Settings ***
Resource        _config.robot
Documentation   Test scenarios for products method.


*** Test Cases ***
GET non existent product offers, negative test
    GET         /products/123/offers
    Integer     response status     404

CREATE random product and verify offers with GET
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence

    &{res}=         POST    /products   { "name": "${name}", "description": "${description}" }
    Integer         response status         201

    GET             /products/${res.body['id']}/offers
    Integer         response status             200