from flask import Flask, render_template, Response, request, jsonify
from flask import redirect, url_for
from aiortc import RTCPeerConnection, RTCSessionDescription
import cv2
import json
import uuid
import asyncio
import logging
import time

app = Flask(__name__, static_url_path='/front')

def generate_frames():
 camera = cv2.VideoCapture(0) # ==============IMPORTANT============
 while True:
  start_time = time.time()
  success, frame = camera.read()
  if not success:
   break
  else:
   ret, buffer = cv2.imencode('.jpg', frame)
   frame = buffer.tobytes()
   # concat frame one by one and show result
   yield (b'--frame\r\n'
    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
   elapsed_time = time.time() - start_time
          logging.debug(f"Frame generation time: {elapsed_time} seconds")

@app.route('/')
def index():
    return render_template('index.html')

async def offer_async():
    params = await request.json
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # Create an RTCPeerConnection instance
    pc = RTCPeerConnection()

    # Generate a unique ID for the RTCPeerConnection
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pc_id = pc_id[:8]

    # Create and set the local description
    await pc.createOffer(offer)
    await pc.setLocalDescription(offer)

    # Prepare the response data with local SDP and type
    response_data = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    return jsonify(response_data)
