// getUserMedia が使えないときは、『getUserMedia()が利用できないブラウザです！』と言ってね。
if (typeof navigator.mediaDevices.getUserMedia !== 'function') {
  const err = new Error('getUserMedia()が利用できないブラウザです！');
  alert(`${err.name} ${err.message}`);
  throw err;
}


// ---------------------------------------------------------------
//   Easy sample for showing stream from web-camera of PC
// ---------------------------------------------------------------
// 操作する画面エレメント変数定義します。
const $start = document.getElementById('start_btn');   // スタートボタン
const $video1 = document.getElementById('video_area');  // 映像表示エリア
const $take = document.getElementById('take_btn');     // 撮影ボタン
const $canvas1 = document.getElementById('streamCanvas');  // 撮影image描画先
$video1.width = 640;
$video1.height = 480;

// 「スタートボタン」を押下したら、getUserMedia を使って映像を「映像表示エリア」に表示してね。
$start.addEventListener('click', () => {
  navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(stream => $video1.srcObject = stream)
  .catch(err => alert(`${err.name} ${err.message}`));
}, false);

// 「静止画取得」ボタンが押されたら「<canvas id="streamCanvas">」に映像のコマ画像を表示します。
$take.addEventListener('click', () => {
  // canvasに『「静止画取得」ボタン』押下時点の画像を描画。
  $canvas1.width  = $video1.videoWidth;
  $canvas1.height = $video1.videoHeight;
  sendImageOfCampas($video1, $canvas1)
}, false);


// ---------------------------------------------------------------
//   Easy sample for showing stream and send picture to django
// ---------------------------------------------------------------
const $videoElem2 = document.getElementById('videoElement');
const $canvas2 = document.getElementById('canvas');
$videoElem2.width = 400;
$videoElem2.height = 300;

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({video: true})
  .then(function(stream) {
    $videoElem2.srcObject = stream;
    // $videoElem2.play();
  })
  .catch(function(_error) {});
}
let timeLeft = 20;
const timerId = setInterval(countdown, 500);

function countdown() {
  if (timeLeft == 0) {
    clearTimeout(timerId);
    return '..'
  } else {
    timeLeft--;
    sendImageOfCampas($videoElem2, $canvas2);
  }
}


function sendImageOfCampas($video, $canvas) {
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
      console.log(data)
      return data
    },
    error: function(_response) {
      console.log('Error')
    },
  });
}
