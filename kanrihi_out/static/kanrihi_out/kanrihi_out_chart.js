// http://mussyu1204.myhome.cx/wordpress/it/?p=322
var chart;

// 一度描画したcanvasが消せない！
function clearCanvas(){
    // canvas要素を取り出す。
    var canvas = document.getElementById("stage");
    // contextを取得。
    var ctx = canvas.getContext('2d');
    // クリアする。
    ctx.clearRect(0,0,800,500);
    if (chart){
        chart.destroy();
    }
}
/*
****************************************************************
* 多次元配列による管理費収入グラフ表示 by N.Goto
****************************************************************
*/
function expenseKanrihiChart(data){
    // (1) chart.jsのdataset用の配列を用意。
    var xLabels = [], teigakuKanrihi = [], setubihi = [], tax = [], chokusetu = [];
    var total = [];
    for (var row in data) {
        xLabels.push(data[row][0]);
        teigakuKanrihi.push(data[row][1]);
        setubihi.push(data[row][2]);
        tax.push(data[row][3]);
        chokusetu.push(data[row][4]);
        total.push(data[row][5]);
    }
    // (2) データオブジェクトを用意。
    var chartData = {
        labels: xLabels,      // x軸ラベル配列。
        datasets: [
            {
                type: 'line',
                fill: false,   // 面を非表示 trueの場合backgroundColorを指定すること。
                label: '定額管理費',
                borderWidth: 2,                 // 線の太さ
                borderColor: "red",             // 線の色
                tension:0,                      //  線は直線
                pointBorderColor: "red",        // ポイント線の色
                pointBackgroundColor: "red",    // ポイント面の色
                pointRadius: 2,                 // ポイントサイズ
                pointHoverRadius: 6,            // ホバーした時のポイントサイズ
                pointHitRadius: 8,              // カーソルのヒットエリア
                backgroundColor: "red",
                data: teigakuKanrihi,
            },
            {
                type: 'line',
                fill: false,                // 面を非表示 trueの場合backgroundColorを指定すること。
                label: '設備管理業務費',
                borderWidth: 2,                 // 線の太さ
                borderColor: "orange",          // 線の色
                tension:0,                      //  線は直線
                pointBorderColor: "orange",     // ポイント線の色
                pointBackgroundColor: "orange", // ポイント面の色
                pointRadius: 2,                 // ポイントサイズ
                pointHoverRadius: 6,            // ホバーした時のポイントサイズ
                pointHitRadius: 8,              // カーソルのヒットエリア
                backgroundColor: "orange",
                data: setubihi,
            },
            {
                type: 'line',
                fill: false,                // 面を非表示 trueの場合backgroundColorを指定すること。
                label: '消費税',
                borderWidth: 2,                 // 線の太さ
                borderColor: "green",          // 線の色
                tension:0,                      //  線は直線
                pointBorderColor: "green",     // ポイント線の色
                pointBackgroundColor: "green", // ポイント面の色
                pointRadius: 2,                 // ポイントサイズ
                pointHoverRadius: 6,            // ホバーした時のポイントサイズ
                pointHitRadius: 8,              // カーソルのヒットエリア
                backgroundColor: "green",
                data: tax,
            },
            {
                type: 'line',
                fill: false,                // 面を非表示 trueの場合backgroundColorを指定すること。
                label: '共用部分直接費',
                borderWidth: 2,                 // 線の太さ
                borderColor: "blue",            // 線の色
                tension:0,                      //  線は直線
                pointBorderColor: "blue",       // ポイント線の色
                pointBackgroundColor: "blue",   // ポイント面の色
                pointRadius: 2,                 // ポイントサイズ
                pointHoverRadius: 6,            // ホバーした時のポイントサイズ
                pointHitRadius: 8,              // カーソルのヒットエリア
                backgroundColor: "blue",
                data: chokusetu,
            },
            {
                type: 'line',
                fill: false,                // 面を非表示 trueの場合backgroundColorを指定すること。
                label: '支出合計',
                borderWidth: 3,                 // 線の太さ
                borderColor: "red",            // 線の色
                tension:0,                      //  線は直線
                pointBorderColor: "red",       // ポイント線の色
                pointBackgroundColor: "red",   // ポイント面の色
                pointRadius: 2,                 // ポイントサイズ
                pointHoverRadius: 6,            // ホバーした時のポイントサイズ
                pointHitRadius: 8,              // カーソルのヒットエリア
                backgroundColor: "red",
                data: total,
            }
        ]
    };
    // (3) チャートオプション
    // http://www.chartjs.org/docs/#chart-configuration-tooltip-configuration
    var myChartOption = {
        responsive:true,   // canvasサイズを固定する。(trueの場合windowの大きさに連動する)
        maintainAspectRatio: true,
        title: {
            display: true,
            fontSize:14,
            text: '管理費支出グラフ'
        },
        scales: {
            yAxes: [
                {
                    id: "y-axis",
                    type: "linear",
                    position: "left", // 目盛りは左側に表示。
                    scaleLabel:{
                        display:true,
                        fontSize:10,
                        fontStyle:"bold",
                        labelString:"単位 (円)",
                    },
                    ticks:{ // Y軸目盛を3桁区切りにする。
                        callback: function (value) {
                            // 正規表現による3桁区切り。
                            return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                            // ブラウザがHTML5対応していれば以下でオーケー。
                            //return value.toLocaleString();
                        }
                    }
                }
            ],
            xAxes: [{
                display: true,
                gridLines: {
                    display: true
                },
                ticks: {
                    fontColor:"black",
                    callback:function(value){
                        return value+"期";
                    }
                }
            }]
        },
        legend: {
            labels: {
                boxWidth:10,
                padding:20 //凡例の各要素間の距離
            },
            display: true
        },
        tooltips: {
            enabled: true,
            mode: 'index',
            displayColors:true,           // 凡例を表示する。
            titleFontColor: 'white',
            titleFontSize: 14,            // デファルトは12。
            bodyFontColor: 'white',
            bodyFontSize: 14,             // デファルトは12。
            backgroundColor: 'black',
            xPadding: 12,
            yPadding: 8,
            callbacks: {
                label: function(tooltipItem,data) {// https://fiddle.jshell.net/chanonroy/v2dm44gp/
                    return '  '+ data.datasets[tooltipItem.datasetIndex].label+' : '+   tooltipItem.yLabel.toLocaleString()+' 円';
                }
            }
        },
    };
    // (4) チャート描画。
    var ctx = document.getElementById('stage').getContext('2d');
    clearCanvas();
    // chartをグローバル変数とする。http://mussyu1204.myhome.cx/wordpress/it/?p=322
    chart = new Chart(ctx, {
        type: 'bar',                // datasetでグラフtypeを指定するだけではチャートが表示できない！？
        options: myChartOption,     // Optionを記述したオブジェクトを指定。
        data: chartData             // データオブジェクト。
    });
}
