*** Settings ***
Resource        _config.robot
Documentation   Test scenarios for healtcheck method.


*** Test Cases ***
GET invalid page, negative test
    GET         /404/notfound
    Integer     response status         404