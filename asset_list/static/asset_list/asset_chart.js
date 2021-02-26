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
* 多次元配列による管理費収支グラフ表示 by N.Goto
* ヘッダーは含まない。
****************************************************************
*/
function assetChart(data){
    // (1) chart.jsのdataset用の配列を用意。
    var xLabels = [], assetData = [] ,debtData = [];
    for (var row in data) {
        xLabels.push(data[row][0]);
        assetData.push(data[row][1]);
//        debtData.push(data[row][2]);
    }
    // (2) データオブジェクトを用意。
    var chartData = {
        labels: xLabels,      // x軸ラベル配列。
        datasets: [
            {
                type: 'bar',
                label: '資産合計',
                backgroundColor: "red",
                data: assetData,
                stack: 1
            },
//            {
//                type: 'bar',
//                label: '負債合計',
//                backgroundColor: "blue",
//                data:debtData,
//                stack: 2
//            }
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
            text: '資産推移グラフ'
        },
        scales: {
            yAxes: [
                {
                    stacked:true,  // 積み上げ棒グラフにする設定
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
                stacked: true,              // 積み上げ棒グラフにする設定
                categoryPercentage: 0.3,    //棒グラフの太さ
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
//            mode: 'label',
            displayColors:true,             // 凡例を表示する。
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
