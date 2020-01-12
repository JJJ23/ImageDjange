function updateSetting() {
    var element = document.getElementById("setting_form");
    // フォームデータを取得
    var form_data = new FormData(element);

    // POSTでアップロード
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.onload= (function() {
        var result = document.getElementById("setting_result");
        if (this.status != 200) {
            result.innerHTML = ""
            return
        }
        // IDからテーブルを取得
        result.innerHTML = "成功"
    })
    xhr.fail = (function() {
        // IDからテーブルを取得ß
        var result = document.getElementById("setting_result");
        result.innerHTML = "成功"
    })
    xhr.open("POST" , "/setting");
    xhr.send(form_data);
}


function uploadImage() {

    var element = document.getElementById("image_upload");
    // フォームデータを取得
    var form_data = new FormData(element);

    // POSTでアップロード
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.onload= (function() {
        if (this.status != 200) {
            return
        }
        // IDからテーブルを取得
        var table = document.getElementById("image_result");
        var json_response = this.response;
        for( var item in json_response) {
            // -1で末尾に追加。インデックスで指定の位置に追加も可能
            var row = table.insertRow(-1);
            var cell_image = row.insertCell(-1)
            var html = "<div class='image'><img src='data:image/png;base64," + json_response[item] + "'/> </div>"
            cell_image.innerHTML = html;
            var cell1 = row.insertCell(-1);
            cell1.innerHTML = item;
        }
    })
    xhr.open("POST" , location.href);
    xhr.send(form_data);
};
