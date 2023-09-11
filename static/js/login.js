function login() {
    var form = document.getElementById("userForm");
    var formData = new FormData(form);
    var button = document.getElementById("loginbutton");
    
    //這樣的設定才會有按下按鈕的動作
    if (button){
        // 使用confirm对话框显示确认提示
    var result = confirm("確定登錄？");

    // 上面先跳確認的彈跳視窗,再確認後，才進AJAX範圍，發起請求
    if (result) {
        var xhr = new XMLHttpRequest();
        // 通过AJAX发送POST请求
        xhr.open('POST', 'http://homepi.myftp.org:8080/seflask/auth/login', true);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // 请求成功，可以执行任何成功处理的操作
                    
                    // 當回應後，不執行重定向
                   //  window.location.href = 'http://homepi.myftp.org:8080/seflask/auth/login'; // 设置重定向的URL
                     console.log("登錄成功:" +xhr.responseText);
                } else {
                    // 请求失败，可以处理错误情况
                    alert("用戶登錄失敗！");
                }
            }
        };

        xhr.send(formData); // 发送POST请求
    } else {
        // 如果用户按下取消，不执行任何操作，保持在当前页面
    }

    }

    
}
