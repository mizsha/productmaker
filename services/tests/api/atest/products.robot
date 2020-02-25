*** Settings ***
Resource        _config.robot
Documentation   Test scenarios for products method.


*** Test Cases ***
CREATE random product
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence
    POST            /products               { "name": "${name}", "description": "${description}" }
    Integer         response status         201
    Object          response body
    String          response body id
    String          response body name          ${name}
    String          response body description   ${description}

GET non existent product
    GET         /products/123
    Integer     response status     404

CREATE random product and verify with GET
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence

    &{res}=         POST    /products   { "name": "${name}", "description": "${description}" }
    Integer         response status         201

    GET             /products/${res.body['id']}
    Integer         response status             200
    String          response body name          ${name}
    String          response body description   ${description}