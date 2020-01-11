function uploadImage() {
    // フォームデータを取得
    var form_data = new FormData(document.getElementById("image_upload"));

    // POSTでアップロード
    var xhr = new XMLHttpRequest();

    xhr.onload= (function(){
        // IDからテーブルを取得
        var table = document.getElementById("image_result");
        // -1で末尾に追加。インデックスで指定の位置に追加も可能
        var row = table.insertRow(-1);
        var cell_image = row.insertCell(-1)
        var image_file = this.responseText.substring(1,this.responseText.length -1)
        var html = "<div class='image'><img src='data:image/png;base64," + image_file+"'/> </div>"
        cell_image.innerHTML=html;
        var cell1 = row.insertCell(-1);
        cell1.innerHTML = '抽出画像';
    })
    xhr.open("POST" , location.href);
    xhr.send(form_data);
};
