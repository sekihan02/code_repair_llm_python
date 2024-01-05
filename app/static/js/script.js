document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("upload-form");
    const loading = document.getElementById("loading");

    form.onsubmit = function() {
        loading.style.display = 'block';  // ローディング画面を表示
    };
});
document.getElementById("upload-form").onsubmit = function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);

    xhr.onload = function() {
        // レスポンス（ログ）を表示
        document.getElementById("log").textContent = xhr.responseText;
    };

    xhr.send(formData);
};
