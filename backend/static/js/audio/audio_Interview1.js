document.addEventListener("DOMContentLoaded", function () {
  const startAudioBtn = document.getElementById("startAudioBtn");
  const stopAudioBtn = document.getElementById("stopAudioBtn");
  const visualizer = document.getElementById("visualizer");
  const audioPlayer = document.getElementById("audioPlayer");
  const audioSource = document.getElementById("audioSource");
  const downloadLink = document.getElementById("downloadLink");

  let mediaRecorder;
  let audioBlob;
  let audioContext;
  let analyser;
  let dataArray;

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

      // Set up audio context and visualizer
      audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContext.createMediaStreamSource(stream);
      analyser = audioContext.createAnalyser();
      source.connect(analyser);
      analyser.fftSize = 2048;
      dataArray = new Uint8Array(analyser.frequencyBinCount);

      mediaRecorder.ondataavailable = function (event) {
        if (event.data && event.data.size > 0) {
          audioBlob = new Blob([event.data], { type: "audio/webm" });
          const audioUrl = URL.createObjectURL(audioBlob);
          audioSource.src = audioUrl;
          audioPlayer.style.display = "block";
          downloadLink.href = audioUrl;
        }
      };

      mediaRecorder.start();
      startAudioBtn.style.display = "none";
      stopAudioBtn.style.display = "inline-block";
      visualize();
    } catch (error) {
      console.error("Error starting audio recording: ", error);
    }
  }

  function stopRecording() {
    if (mediaRecorder) {
      mediaRecorder.stop();
      mediaRecorder.stream.getTracks().forEach((track) => track.stop());
    }
    startAudioBtn.style.display = "inline-block";
    stopAudioBtn.style.display = "none";
    if (audioContext) {
      audioContext.close();
    }
  }

  function visualize() {
    const canvas = document.createElement("canvas");
    canvas.width = visualizer.clientWidth;
    canvas.height = visualizer.clientHeight;
    visualizer.appendChild(canvas);
    const canvasCtx = canvas.getContext("2d");

    function draw() {
      requestAnimationFrame(draw);
      analyser.getByteFrequencyData(dataArray);
      canvasCtx.fillStyle = "#000";
      canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / dataArray.length) * 2.5;
      let barHeight;
      let x = 0;

      for (let i = 0; i < dataArray.length; i++) {
        barHeight = dataArray[i];
        canvasCtx.fillStyle = 'rgb(' + (barHeight + 100) + ',50,50)';
        canvasCtx.fillRect(x, canvas.height - barHeight / 2, barWidth, barHeight / 2);
        x += barWidth + 1;
      }
    }

    draw();
  }

  startAudioBtn.addEventListener("click", startRecording);
  stopAudioBtn.addEventListener("click", stopRecording);
});
