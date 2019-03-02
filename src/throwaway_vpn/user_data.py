#!/usr/bin/env python
# -*- coding: utf-8 -*-
user_data_core = """#!/bin/bash
apt-get update && apt-get install -y expect python3-pip apt-transport-https ca-certificates curl gnupg-agent software-properties-common && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io && pip3 install yagmail
docker volume create --name openvpn-data && docker run -v openvpn-data:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_genconfig -u udp://$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
docker run -v openvpn-data:/etc/openvpn --log-driver=none --rm -e EASYRSA_BATCH="yes" kylemanna/openvpn ovpn_initpki nopass 
docker run -v openvpn-data:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
docker run -v openvpn-data:/etc/openvpn --log-driver=none --rm kylemanna/openvpn easyrsa build-client-full vpn nopass
docker run -v openvpn-data:/etc/openvpn --log-driver=none --rm kylemanna/openvpn ovpn_getclient vpn > /root/"vpn_$(date '+%Y_%m_%d').ovpn"
/usr/bin/python3 -c \"import yagmail; yagmail.SMTP('{0}', '{1}').send(to=[{2}], subject='throwaway-vpn', contents=['New throwaway-vpn attached', '/root/vpn_$(date '+%Y_%m_%d').ovpn'])\""""
