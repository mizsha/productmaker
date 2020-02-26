*** Settings ***
Resource        _config.robot
Documentation   Test scenarios for products method.


*** Test Cases ***
GET non existent product
    GET         /products/123
    Integer     response status     404


CREATE invalid product
    ${name}=            FakerLibrary.Sentence
    ${invalidparam}=    FakerLibrary.Sentence

    &{res}=         POST    /products   { "name": "${name}", "invalidparam": "${invalidparam}" }
    Integer         response status         400

CREATE random product
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence
    POST            /products               { "name": "${name}", "description": "${description}" }
    Integer         response status         201
    Object          response body
    String          response body id
    String          response body name          ${name}
    String          response body description   ${description}

CREATE random product and verify with GET
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence

    &{res}=         POST    /products   { "name": "${name}", "description": "${description}" }
    Integer         response status         201

    GET             /products/${res.body['id']}
    Integer         response status             200
    String          response body name          ${name}
    String          response body description   ${description}

CREATE random product and REMOTE verify with GET
    ${name}=            FakerLibrary.Sentence
    ${description}=     FakerLibrary.Sentence

    &{res}=         POST    /products   { "name": "${name}", "description": "${description}" }
    Integer         response status         201

    GET             ${API_URL}/products/${res.body['id']}/offers        headers={ "Bearer": "${API_KEY}" }
    Integer         response status         200