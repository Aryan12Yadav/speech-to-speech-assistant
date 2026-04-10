let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Use webm format which is what browsers actually record in
    mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
    mediaRecorder.start();

    document.getElementById("status").innerText = "Recording...";
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
}

async function stopRecording() {
    mediaRecorder.stop();

    mediaRecorder.onstop = async () => {
        document.getElementById("status").innerText = "Processing...";

        // Send as webm, not wav
        const blob = new Blob(audioChunks, { type: "audio/webm" });

        const formData = new FormData();
        formData.append("file", blob, "voice.webm");

        const res = await fetch("/api/voice-chat", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("userText").innerText = data.user_text;
        document.getElementById("botText").innerText = data.bot_text;

        const audio = new Audio(data.audio);
        audio.play();

        document.getElementById("status").innerText = "Done";
    };
}