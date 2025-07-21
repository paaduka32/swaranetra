function readAloud(text) {
    if ('speechSynthesis' in window) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US';
        speech.rate = 0.8; 
        speech.pitch = 1.8;
        speech.volume = 1;

        const voices = speechSynthesis.getVoices();
        if (voices.length > 0) {
            const preferredVoice = voices.find(voice => voice.name.includes('Google')); 
            if (preferredVoice) {
                speech.voice = preferredVoice; 
            }
        }

        window.speechSynthesis.speak(speech);
    } else {
        alert("Sorry, your browser does not support text-to-speech.");
    }
}

window.onload = function() {
    const resultText = document.querySelector("#result-text");
    if (resultText) {
        readAloud(resultText.innerText); 
    }
};