// app/static/js/code_correction.js

document.getElementById('start-form').onsubmit = function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process-correction", true);

    xhr.onload = function() {
        document.getElementById('logs').innerHTML = xhr.responseText;
    };

    xhr.send(formData);
};

document.getElementById('correction-form').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process-correction", true);

    // ローディング表示
    document.getElementById('overlay').style.display = 'block';

    xhr.onload = function() {
        // ローディング非表示
        document.getElementById('overlay').style.display = 'none';

        if (this.status === 200) {
            // ...
        } else {
            console.error('Error:', this.statusText);
        }
    };

    xhr.send(formData);
};

function executePythonCode(code) {
    fetch('/execute-python', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'code=' + encodeURIComponent(code)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('python-output').textContent = data.result;

        // テスト結果の表示
        var testResultText = "テストの結果: ";
        if (data.result.includes("AssertionError") || data.result.includes("Error") || data.result.includes("Exception")) {
            testResultText += "動作しなかった";
        } else {
            testResultText += "動作した";
        }
        document.getElementById('test-result').textContent = testResultText;
    });
}
