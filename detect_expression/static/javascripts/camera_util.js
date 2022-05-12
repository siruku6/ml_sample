// getUserMedia が使えないときは、『getUserMedia()が利用できないブラウザです！』と言ってね。
if (typeof navigator.mediaDevices.getUserMedia !== 'function') {
  const err = new Error('getUserMedia()が利用できないブラウザです！');
  alert(`${err.name} ${err.message}`);
  throw err;
}


// ---------------------------------------------------------------
//   Showing stream from web-camera of PC
// ---------------------------------------------------------------
// 画面上の要素を変数に代入
const $video1 = document.getElementById('video_area');      // 映像表示エリア
const $canvas1 = document.getElementById('streamCanvas');   // 撮影image描画先
const $start = document.getElementById('start_btn');        // スタートボタン
const $take = document.getElementById('take_btn');          // 静止画撮影ボタン
const $sendStream = document.getElementById('send-stream'); // ストリーミング送信ボタン
$video1.width = 400;
$video1.height = 300;

// 1. 「映像取得開始」ボタンを押下したら、getUserMedia を使って映像を「映像表示エリア」に表示
$start.addEventListener('click', () => {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(
    stream => $video1.srcObject = stream
    // $video1.play();
  )
  .catch(err => alert(`${err.name} ${err.message}`));
}, false);

// 2. 「静止画取得」ボタンが押されたら「<canvas id="streamCanvas">」にコマ画像を表示
$take.addEventListener('click', () => {
  sendImageOfCampas($video1, $canvas1);
}, false);

// 3. 「映像解析」ボタンが押されたら「<canvas id="streamCanvas">」に映像のコマ画像を表示します。
const $progressBar = document.getElementById('left-time');    // プログレスバー
const maxTime = 50;
$sendStream.addEventListener('click', () => {
  let timeLeft = 50;
  const timerId = setInterval(sendStream20Seconds, 400);

  function sendStream20Seconds() {
    let leftPercentage = Math.ceil(timeLeft / maxTime * 100);
    $progressBar.style.width = `${leftPercentage}%`;
    $progressBar.innerHTML = `残り時間: ${leftPercentage}%`;

    if (timeLeft == 0) {
      clearTimeout(timerId);
      return '..';
    } else {
      timeLeft--;
      sendImageOfCampas($video1, $canvas1);
    }
  }
}, false);


// ---------------------------------------------------------------
//   Easy sample for showing stream and send picture to django
// ---------------------------------------------------------------
// Removed
// Reference: https://qiita.com/qiita_mona/items/e58943cf74c40678050a


// ---------------------------------------------------------------
//   Util function
// ---------------------------------------------------------------
const $resultImg = document.getElementById('result-img');
const $bestFaceImg = document.getElementById('best-face');
const $bestPercentageBoard = document.getElementById('best-percentage');  // 最も明るい表情のPercentageを表示

function sendImageOfCampas($video, $canvas) {
  // $canvas.width  = $video.videoWidth;
  // $canvas.height = $video.videoHeight;
  $canvas.width  = $video.width;
  $canvas.height = $video.height;

  const imageInCanvas = $canvas.getContext('2d');
  imageInCanvas.drawImage(
    $video, 0, 0, $video.width, $video.height
  );
  let imageData = $canvas.toDataURL('image/jpeg', 0.92);
  // imageInCanvas.clearRect(0, 0, $video.width, $video.height);
  $.ajax({
    type: 'POST',
    url: url_start_webcam,
    data: {image: imageData, csrfmiddlewaretoken: csrf_token,},
    success: function(data) {
      console.log(data);
      $resultImg.setAttribute('src', data.image);

      if (data.positive_level > parseFloat($bestPercentageBoard.innerText)) {
        $bestPercentageBoard.innerText = data.positive_level;
        $bestFaceImg.setAttribute('src', data.image);
      }
    },
    error: function(_response) {
      console.log('Error');
    },
  });
}
