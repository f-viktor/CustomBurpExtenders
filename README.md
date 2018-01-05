# CustomBurpExtenders
Some extenders for BurpSuitePro

# Add_HMAC_header.py
An extender to add custom headers, this extension should be added as a session handling rule. Headers will not show up in request history. Open up session tracer to see the actual issued request as the headers will be added just before sending the request. Extension was tested winth Jhyton 2.7.0 and BurpSuitePro 1.7.30.
