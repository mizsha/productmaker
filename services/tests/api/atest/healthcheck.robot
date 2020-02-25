*** Settings ***
Resource        _config.robot
Documentation   Test scenarios for healtcheck method.


*** Test Cases ***
GET healtcheck method
    GET             /system/healthcheck
    Integer         response status         200
    String          response body status    OK

PATCH healtcheck method, negative test
    PATCH           /system/healthcheck     {}
    Integer         response status         405