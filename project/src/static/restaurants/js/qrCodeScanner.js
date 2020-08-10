const qr = window.qrcode;

const video = document.createElement('video');
const canvasElement = document.getElementById('qr-canvas');
const canvas = canvasElement.getContext('2d');
const btnScanQR = document.getElementById('btn-scan-qr');

let scanning = false,
    code,
    type;

// Hide any modals that are currently on screen, reset the input box
function hideModals() {
    $('#accept-modal, #notification-modal').fadeOut(600);
    $('input').val('');
}

// Show the acceptance modal and fill in the appropriate data
function showAcceptModal(info, data) {
    $('#accept-modal .text').eq(0).text(info);
    $('#accept-modal .text').eq(1).text(data);
    $('#accept-modal').fadeIn(600);
}

// Show the notification modal and show the appropriate data
function showNotificationModal(info) {
    $('#notification-modal .text').text(info);
    $('#notification-modal').fadeIn(600);
}

// Submit the last used code to the server to attempt verification
function submitCode() {
    if (type === 'goal') {
        $.ajax({
            url: '/verification/finish-goal',
            method: 'POST',
            data: { code: code },
        }).done((data) => {
            $('#accept-modal, #notification-modal').fadeOut(600, () =>
                showNotificationModal(data.message)
            );
        });
    } else if (type === 'reward') {
        $.ajax({
            url: '/verification/finish-reward',
            method: 'POST',
            data: { code: code },
        }).done((data) => {
            $('#accept-modal, #notification-modal').fadeOut(600, () =>
                showNotificationModal(data.message)
            );
        });
    }
}

// Handle data received by the server after scanning a code
function readData(data) {
    if ('goal' in data) {
        type = 'goal';
        showAcceptModal(
            `The QR code matches the goal shown below. 
            Would you like to accept the goal and mark it as complete?`,
            data.goal
        );
    } else if ('reward' in data) {
        type = 'reward';
        showAcceptModal(
            'The QR code matches the reward shown below. Would you like to accept the reward and redeem it?',
            data.reward
        );
    } else if ('message' in data) {
        type = 'message';
        showNotificationModal(data.message);
    }
}

// Send a request to the server containing the QR code
function sendData(res) {
    code = res;
    $.ajax({
        url: '/verification/verify',
        method: 'POST',
        data: { data: res },
    }).done(readData);
}

// Finish scanning QR code
qr.callback = (res) => {
    if (res) {
        sendData(res);
        scanning = false;

        video.srcObject.getTracks().forEach((track) => {
            track.stop();
        });

        canvasElement.hidden = true;
        btnScanQR.hidden = false;
    }
};

// Begin QR scanning
btnScanQR.onclick = () => {
    navigator.mediaDevices
        .getUserMedia({ video: { facingMode: 'environment' } })
        .then(function (stream) {
            scanning = true;
            btnScanQR.hidden = true;
            canvasElement.hidden = false;
            video.setAttribute('playsinline', true); // required to tell iOS safari we don't want fullscreen
            video.srcObject = stream;
            video.play();
            tick();
            scan();
        });
};

// Animate camera
function tick() {
    canvasElement.height = video.videoHeight;
    canvasElement.width = video.videoWidth;
    canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);

    scanning && requestAnimationFrame(tick);
}

// Scan for QR codes
function scan() {
    try {
        qr.decode();
    } catch (e) {
        setTimeout(scan, 300);
    }
}

// Dynamically size the modals
$(window).on('resize load', () => {
    $('#accept-modal, #notification-modal').width($('.container').width());
});

// Hide modals on launch
$('#accept-modal, #notification-modal').hide();

// Set up event listeners for buttons
$('#accept').click(submitCode);
$('#decline, #continue').click(hideModals);

// Intercept input box on submit
$('form').submit(function (e) {
    e.preventDefault();
    sendData($('input').val());
});
