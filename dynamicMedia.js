class DynamicMedia {
  constructor(rootElementId) {
    this.root = document.getElementById(rootElementId);
  }

  mountAudio() {
    this._element = document.createElement('audio');
    // set autoplay
    this._element.setAttribute('autoplay', true);
    // display none
    this._element.style.display = 'none';
    this.root.appendChild(this._element);
  }

  unmountAudio() {
    this.root.removeChild(this._element);
  }

  setMedia(media) {
    this._element.src = media;
  }

  play() {
    this._element.play();
  }
}