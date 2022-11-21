#!/usr/bin/env bash

# AlphaRTC Docker receive command (modify config file as needed)
docker run -d --network=host --rm -v `pwd`:/app -w /app --name alphartc_pyinfer opennetlab.azurecr.io/challenge-env peerconnection_serverless receiver_pyinfer.json
