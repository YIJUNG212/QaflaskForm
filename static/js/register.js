function adduser() {
    var form = document.getElementById("userForm");
    var formData = new FormData(form);
    var button = document.getElementById("add_user");
    
    //這樣的設定才會有按下按鈕的動作
    if (button){
        // 使用confirm对话框显示确认提示
    var result = confirm("確定要添加用戶嗎？");

    // 上面先跳確認的彈跳視窗,再確認後，才進AJAX範圍，發起請求
    if (result) {
        var xhr = new XMLHttpRequest();
        // 通过AJAX发送POST请求
        xhr.open('POST', 'http://homepi.myftp.org:8080/seflask/auth/register', true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // 请求成功，可以执行任何成功处理的操作
                    
                    // 执行重定向
                     window.location.href = 'http://homepi.myftp.org:8080/seflask/auth/login'; // 设置重定向的URL
                     console.log("註冊成功:" +xhr.responseText);
                } else {
                    // 请求失败，可以处理错误情况
                    alert("用戶添加失敗！");
                }
            }
        };

        xhr.send(formData); // 发送POST请求
    } else {
        // 如果用户按下取消，不执行任何操作，保持在当前页面
    }

    }

    
}






//以下是驗證碼的部份
var countdownSeconds = 60;  // 初始倒计时秒数
var countdownInterval;      // 倒计时计时器
var buttonClicked = false;  // 按钮是否被按下的标志







function getchaptch() {
    var email = document.getElementById("email").value;
    var button = document.getElementById("captcha-btn");
    
    if (button) {
        if (!buttonClicked && email) {
            // 删除之前存储在数据库中的验证码
            deleteOldCaptcha(email);
            // 生成新的验证码并存入数据库
            // generateAndStoreNewCaptcha(email);#生成驗證碼的部份,已經在sendEmailViaGET(email);裡處理了
            // 启动倒计时
            startCountdown();

            // 设置按钮为已点击状态
            buttonClicked = true;

            alert(email);
            sendEmailViaGET(email);
        } else {
            alert("信箱不得為空，無法接收驗證碼!")
        }
    } else {
        alert("按鈕未找到");
    }
}



function sendEmailViaGET(email) {
    // 创建一个新的 XMLHttpRequest 对象
    var xhr = new XMLHttpRequest();

    // 定义请求的方法、URL以及是否异步
    xhr.open("GET", "http://homepi.myftp.org:8080/seflask/auth/captcha/email?email=" + email, true);

    // 设置请求完成后的回调函数
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // 请求成功完成并且服务器返回状态码为 200
            // 可以在这里处理服务器的响应
            console.log("请求成功: " + xhr.responseText);
        }
    };

    // 发送 GET 请求
    xhr.send();
}


function startCountdown() {
    var button = document.getElementById("captcha-btn");
    if (button) {
        // 禁用按钮
        button.disabled = true;

        // 更新按钮文本为倒计时秒数
        button.innerText = countdownSeconds + " 秒";

        // 每秒更新倒计时文本
        countdownInterval = setInterval(function () {
            countdownSeconds--;
            button.innerText = countdownSeconds + " 秒";

            // 倒计时结束时清除计时器，恢复按钮状态
            if (countdownSeconds <= 0) {
                clearInterval(countdownInterval);
                button.innerText = "获取验证码";
                button.disabled = false;
                buttonClicked = false;
                countdownSeconds = 60; // 重置倒计时秒数
            }
        }, 1000);
    }
}


function deleteOldCaptcha(email) {
    fetch('http://homepi.myftp.org:8080/seflask/auth/delete_old_captcha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // 输出服务器的响应消息
    });
}

// function generateNewCaptcha(email) {
//     fetch('http://homepi.myftp.org:8080/seflask/auth/generate_new_captcha', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ email: email }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data.message); // 输出服务器的响应消息
//     });
// }
