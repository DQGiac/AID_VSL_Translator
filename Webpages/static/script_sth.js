const resultElement = document.getElementById('result');
const startBtn = document.getElementById('recordButton');
const stopBtn = document.getElementById('stopButton');
const display = document.getElementById('display')
startBtn.addEventListener('click', startRecording);
stopBtn.addEventListener('click', stopRecording);

let recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let displaying = false, displayword = ""
unicode_to_vni = {
    'À': 'A2', 'Á': 'A1', 'Ả': 'A3', 'Ã': 'A4', 'Ạ': 'A5',
    'Â': 'A6', 'Ầ': 'A62', 'Ấ': 'A61', 'Ẩ': 'A63', 'Ẫ': 'A64', 'Ậ': 'A65',
    'Ă': 'A8', 'Ằ': 'A82', 'Ắ': 'A81', 'Ẳ': 'A83', 'Ẵ': 'A84', 'Ặ': 'A85',
    'È': 'E2', 'É': 'E1', 'Ẻ': 'E3', 'Ẽ': 'E4', 'Ẹ': 'E5',
    'Ê': 'E6', 'Ề': 'E62', 'Ế': 'E61', 'Ể': 'E63', 'Ễ': 'E64', 'Ệ': 'E65',
    'Ì': 'I2', 'Í': 'I1', 'Ỉ': 'I3', 'Ĩ': 'I4', 'Ị': 'I5',
    'Ò': 'O2', 'Ó': 'O1', 'Ỏ': 'O3', 'Õ': 'O4', 'Ọ': 'O5',
    'Ô': 'O6', 'Ồ': 'O62', 'Ố': 'O61', 'Ổ': 'O63', 'Ỗ': 'O64', 'Ộ': 'O65',
    'Ơ': 'O7', 'Ờ': 'O72', 'Ớ': 'O71', 'Ở': 'O73', 'Ỡ': 'O74', 'Ợ': 'O75',
    'Ù': 'U2', 'Ú': 'U1', 'Ủ': 'U3', 'Ũ': 'U4', 'Ụ': 'U5',
    'Ư': 'U7', 'Ừ': 'U72', 'Ứ': 'U71', 'Ử': 'U73', 'Ữ': 'U74', 'Ự': 'U75',
    'Ỳ': 'Y2', 'Ý': 'Y1', 'Ỷ': 'Y3', 'Ỹ': 'Y4', 'Ỵ': 'Y5', "Đ": "D9"
}

function displayImage(word) {
    result = ""
    for (let char in word) {
        if (word[char] in unicode_to_vni) result += (unicode_to_vni[word[char]])
        else result += (word[char])
    }
    console.log(result)
    display.src = "./images/" + result[0]
    for (let char = 1; char < result.length; char ++) {
        setTimeout(() => {
            display.src = "./images/" + result[char].toLowerCase()
        }, 700)
    }
    displaying = false
    displayword = ""
    console.log(result)
}
if (recognition) {
  recognition = new recognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = 'vi-VN';

  recognition.onstart = () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;
    // animatedSvg.classList.remove('hidden');
    console.log('Recording started');
  };

  recognition.onresult = function (event) {
    let result = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        result += event.results[i][0].transcript + ' ';
        displaying = true
        displayword = result
        console.log("hees")
      } else {
        result += event.results[i][0].transcript;
      }
    }

    resultElement.innerHTML = result;
    // setInterval()
    if (displaying) {
      console.log("yes")
      displayImage(displayword.toUpperCase())
    }

    if (result.toLowerCase().includes('stop recording')) {
      resultElement.innerHTML = result.replace(/stop recording/gi, '');
      stopRecording();
    }
  };

  recognition.onerror = function (event) {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    console.error('Speech recognition error:', event.error);
  };

  recognition.onend = function () {
    startBtn.disabled = false;
    stopBtn.disabled = true;
    // animatedSvg.classList.add('hidden');
    console.log('Speech recognition ended');
  };
} else {
  console.error('Speech recognition not supported');
}

function startRecording() {
  resultElement.innerHTML = '';
  recognition.start();
}

function stopRecording() {
  if (recognition) {
    recognition.stop();
  }
}