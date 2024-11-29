let pc = new RTCPeerConnection();

async function createOffer() {
    console.log("Sending offer request");

    const offerRequest = await fetch("/offer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            sdp: "", //SDP means Session Descprtion Protocol
            type: "offer",
        }),
    });

    const offer = await offerRequest.json();
    console.log("Received offer request:", offer);

    await pc.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await pc.createAnswer();
    await pcsetLocalDescription(answer);
}

createOffer();