# Vandal
C2 Framework

Vandal is a C2 Framework entirely based in Python. It is modular by design so that functionality can be easily added, removed or adjusted. 

## Introduction
At it's core the "Vandal Server Application" runs locally on a server, and all "Listeners" or "Handlers" are generated in separate Flask application. The "Agents" or "Implants" can only speak to the Listener and not the Vandal Server, so it is possible to split the infrastructure up into pieces such as a Vandal Server on Endpoint A and Listeners on Endpoint B. Currently as it stands you would need to change the code manually as I have yet built an easy way to configure this.

With Vandal, the entire C2 platform is open source. That is all the code for the server and backend functionality is there for you to use and spin up infrastructure. What is not open source is the implants or agents. These need to be developed by penetration testers. A wiki will be available that walks through building an implant in Python.

## Version 0.2 - Zephyr
As mentioned Vandal can be built upon to have features and functionality added. As of this release Vandal supports:
  + Basic C2 channel communication via HTTPS (command execution)
  + Generate listeners
  + Take screenshots of compromised hosts
  + File upload and download
  + SOCKS5 support
  + More Agent control
  + Payload Generation
      + Python
      + EXE

Some items that are a work in progress but are not completed yet:
  + AES Encryption
  + PowerShell Execution
  + Reflective Payload Loading
  + DNS Handler
  + Automated CDN generation

## Disclaimer:
This is a personal project that I created to understand at a deeper level how C2's work. From here I used it as a pivot to learn how to code implants from scratch utilzing the C2 I built. This made things a lot easier to understand for me. It is an ongoing project and currently in it's infantry stage.
