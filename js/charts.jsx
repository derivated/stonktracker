import Chart from "chart.js/auto"
import 'chartjs-adapter-luxon'
import { DateTime } from 'luxon'


(async function() {

    fetch("../data.json").then(response => response.json()).then(data => {


        let buyData = []
        let sellData = []
        let movingBuyData = []
        let movingSellData = []


        for (let key of Object.keys(data["data"]["buyPrice"])) {
            let time = DateTime.fromMillis(parseInt(key) * 1000)
            let value = data["data"]["buyPrice"][key].toFixed(1)

            buyData.push({x: time, y: value})

            value = data["data"]["sellPrice"][key].toFixed(1)

            sellData.push({x: time, y: value})

            value = data["data"]["buyMovingWeek"][key]/168

            movingBuyData.push({x: time, y: value})

            value = data["data"]["sellMovingWeek"][key]/168

            movingSellData.push({x: time, y: value})

        }




        new Chart(
            document.getElementById('buySellPriceChart'),
            {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Buy Price',
                        data: buyData
                    },
                    {
                        label: 'Sell Price',
                        data: sellData
                    }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'hour'
                            }
                        },
                        y: {
                            type: 'linear'
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Today's Buy/Sell Data"
                        }
                    },
                    fill: true
                }
            }
        );

        new Chart(
            document.getElementById('buySellMovingWeekChart'),
            {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Weekly Instant Buys',
                        data: movingBuyData
                    },
                        {
                            label: 'Weekly Instant Sells',
                            data: movingSellData
                        }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'week'
                            }
                        },
                        y: {
                            type: 'linear'
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Today's Estimated Instant Buys/Sells per Hour"
                        }
                    },
                    fill: true
                }
            }
        );

    });

    fetch("../historic_data.json").then(response => response.json()).then(data => {


        let buyData = []
        let sellData = []
        let movingBuyData = []
        let movingSellData = []


        for (let key of Object.keys(data["data"]["buyPrice"])) {
            let time = DateTime.fromMillis(parseInt(key) * 1000)
            let value = data["data"]["buyPrice"][key].toFixed(1)

            buyData.push({x: time, y: value})

            value = data["data"]["sellPrice"][key].toFixed(1)

            sellData.push({x: time, y: value})

            value = data["data"]["buyMovingWeek"][key]/168

            movingBuyData.push({x: time, y: value})

            value = data["data"]["sellMovingWeek"][key]/168

            movingSellData.push({x: time, y: value})

        }




        new Chart(
            document.getElementById('buySellPriceChartHistorical'),
            {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Buy Price',
                        data: buyData
                    },
                        {
                            label: 'Sell Price',
                            data: sellData
                        }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'hour'
                            }
                        },
                        y: {
                            type: 'linear'
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Historical Buy/Sell Data"
                        }
                    },
                    fill: true
                }
            }
        );

        new Chart(
            document.getElementById('buySellMovingWeekChartHistorical'),
            {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'Weekly Instant Buys',
                        data: movingBuyData
                    },
                        {
                            label: 'Weekly Instant Sells',
                            data: movingSellData
                        }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'week'
                            }
                        },
                        y: {
                            type: 'linear'
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: "Historical Estimated Instant Buys/Sells per Hour"
                        }
                    },
                    fill: true
                }
            }
        );

    });

    fetch("../summary.json").then(response => response.json()).then(data => {

        console.log(data)

        for(let i = 1; i <= 10; i++) {

            let index = i.toString()

            document.getElementById("buyOrders" + i.toString()).textContent = data["data"]["sellSummary"][index]["orders"]
            document.getElementById("buyAmount" + i.toString()).textContent = data["data"]["sellSummary"][index]["amount"]
            document.getElementById("buyPrice" + i.toString()).textContent = data["data"]["sellSummary"][index]["pricePerUnit"]

            document.getElementById("sellOrders" + i.toString()).textContent = data["data"]["buySummary"][index]["orders"]
            document.getElementById("sellAmount" + i.toString()).textContent = data["data"]["buySummary"][index]["amount"]
            document.getElementById("sellPrice" + i.toString()).textContent = data["data"]["buySummary"][index]["pricePerUnit"]
        }

    })

})();