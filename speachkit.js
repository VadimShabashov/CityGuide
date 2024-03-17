class SpeechKit extends EventTarget {
    id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

    constructor({ continuous = false, interimResults = true, lang = 'ru-RU' } = {}) {
        super();
        let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = continuous;
        this.recognition.interimResults = interimResults;
        this.recognition.lang = lang;
    }

    setListener() {
        this.recognition.onresult = (event) => {
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    this.dispatchEvent(new CustomEvent('result', { detail: event.results[i][0].transcript }));
                } else {
                    this.dispatchEvent(new CustomEvent('interim', { detail: event.results[i][0].transcript }));
                }
            }
        }
        this.recognition.onend = () => {
            this.dispatchEvent(new CustomEvent('end'));
        }

        this.recognition.onerror = (event) => {
            this.dispatchEvent(new CustomEvent('error', { detail: event.error }));
        }
    }

    setLang(lang) {
        this.recognition.lang = lang;
    }

    start() {
        this.setListener();
        this.recognition.start();
    }

    stop() {
        this.recognition.stop();
    }

    get id() {
        return this.id;
    }

    isMicrophoneAvailable() {
        return navigator.mediaDevices.getUserMedia({ audio: true });
    }
}