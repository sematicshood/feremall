function rupiah(bilangan = 0) {
    var	number_string = bilangan.toString(),
        sisa 	= number_string.length % 3,
        rupiah 	= number_string.substr(0, sisa),
        ribuan 	= number_string.substr(sisa).match(/\d{3}/g);
            
    if (ribuan) {
        separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }

    return rupiah
}

function create_chart_sales(ctx, datasets, labels, index, chart, option = {}) {
    let stack   =   false,
        title   =   {
            display: false,
            text: 'Sales Dashboard'
        }
    
    if(option[0] != undefined) {
        stack           =   option[0].stack || stack
        title           =   {
            display: true,
            text: option[0].title
        }
    }

    if(window[`${chart}_${index}`] != undefined)
        window[`${chart}_${index}`].destroy()

    let options     =   {
        legend: { display: true },
        title: title,
        scales: {
            yAxes: [
                {
                    ticks: {
                        callback: function(label, index, labels) {
                            if(typeof label == "string")
                                return label
                            else
                                return rupiah(Math.floor(label/1000))+'k';
                        }
                    },
                    stacked: (chart == 'bar') ? stack : false
                }
            ],
            xAxes: [
                {
                    ticks: {
                        callback: function(label, index, labels) {
                            if(typeof label == "string")
                                return label
                            else
                                return rupiah(Math.floor(label/1000))+'k';
                        },
                        beginAtZero: true,
                    },
                    stacked: true
                }
            ],
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem, data) {
                    if(typeof tooltipItem.yLabel != "string")
                        number = tooltipItem.yLabel
                    else
                        number = tooltipItem.xLabel

                    label_tool  =   data.datasets[tooltipItem.datasetIndex].label

                    if(chart == 'pie' || chart == 'doughnut') {
                        label_tool  =   data.labels[tooltipItem.index]
                        number      =   data.datasets[0].data[tooltipItem.index]
                    }

                    return label_tool + " : Rp. " + Number(number).toFixed(0).replace(/./g, function(c, i, a) {
                        return i > 0 && c !== "." && (a.length - i) % 3 === 0 ? "." + c : c;
                    });
                }
            }
        }
    }

    if(chart == 'pie' || chart == 'doughnut') {
        delete options.scales

        let label           =   [],
            data            =   [],
            backgroundColor =   []

        datasets.forEach((v) => {
            label.push(v.label.toString())
            data.push(v.data.toString())
            backgroundColor.push(v.backgroundColor[0].toString())
        })

        datasets = [
            {
                backgroundColor: backgroundColor,
                data: data
            }
        ]

        labels = label
    }

    window[`${chart}_${index}`] = new Chart(ctx, {
        type: chart,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: options
    });

    let xxx = {
        labels: labels,
        datasets: datasets
    }
}

function sales_color_generator(data) {
    var internalData = data;

    var graphColors = [];
    var graphOutlines = [];
    var hoverColor = [];

    var internalDataLength = internalData.length;
    i = 0;
    while (i <= internalDataLength) {
        var randomR = Math.floor((Math.random() * 130) + 100);
        var randomG = Math.floor((Math.random() * 130) + 100);
        var randomB = Math.floor((Math.random() * 130) + 100);
    
        var graphBackground = "rgb(" 
                + randomR + ", " 
                + randomG + ", " 
                + randomB + ")";
        graphColors.push(graphBackground);
        
        var graphOutline = "rgb(" 
                + (randomR - 80) + ", " 
                + (randomG - 80) + ", " 
                + (randomB - 80) + ")";
        graphOutlines.push(graphOutline);
        
        var hoverColors = "rgb(" 
                + (randomR + 25) + ", " 
                + (randomG + 25) + ", " 
                + (randomB + 25) + ")";
        hoverColor.push(hoverColors);
        
        i++;
    };

    return [graphColors, graphOutlines, hoverColor]
}

function sales_process_chart(ctx, chart, data, canvas, option) {
    if(Array.isArray(data[0].labels))
        labels  =   data[0].labels
    else
        labels  =   [data[0].labels]
    
    let datasets    =   []
    
    if(chart == 'bar'){        
        data[0].value.forEach((v) => {
        $.each(v, function(key, value) {
                let color   =   sales_color_generator(value)

                let data = {
                    label: [key],
                    backgroundColor: color[0],
                    borderColor: color[1],
                    data: value
                }
                datasets.push(data)
            })            
        })
    }else if(chart == 'pie' && canvas == 0){
        margin = data[0].margin
        data[0].value.forEach((v) => {
            $.each(v, function(key, value) {
                let color   =   sales_color_generator([value])
                if(key == "Total Margin"){
                    if(margin > 30){
                        var data = {
                            label: [key],
                            backgroundColor: ["rgb(51, 204, 51)"],
                            borderColor: ["rgb(0, 0, 0)"],
                            data: [value]
                        } 
                    }else if(margin > 25 && value < 30){
                        var data = {
                            label: [key],
                            backgroundColor: ["rgb(255, 255, 0)"],
                            borderColor: ["rgb(0, 0, 0)"],
                            data: [value]
                        } 
                    }else if(margin < 25){
                        var data = {
                            label: [key],
                            backgroundColor: ["rgb(255, 0, 64)"],
                            borderColor: ["rgb(0, 0, 0)"],
                            data: [value]
                        } 
                    }
                }else{
                    var data = {
                        label: [key],
                        backgroundColor: color[0],
                        borderColor: color[1],
                        data: [value]
                    } 
                }
                               
                datasets.push(data)
            })
        })
    }else{
        data[0].value.forEach((v) => {
            $.each(v, function(key, value) {
                let color   =   sales_color_generator([value])
    
                let data = {
                    label: [key],
                    backgroundColor: color[0],
                    borderColor: color[1],
                    data: [value]
                }                
                datasets.push(data)
            })
        })
    }


    if(canvas == 0){
        obj = data[0].value[0]
        nilai_total_sales = obj['Total Sales']
        if (nilai_total_sales >= 1000000000){
            nilai_total_sales = rupiah(Math.floor(nilai_total_sales/1000000000))+'B'
        }else if(nilai_total_sales >= 1000000){
            nilai_total_sales = rupiah(Math.floor(nilai_total_sales/1000000))+'M'
        }else if(nilai_total_sales >= 1000){
            nilai_total_sales = rupiah(Math.floor(nilai_total_sales/1000))+'K'
        }else{
            nilai_total_sales = rupiah(nilai_total_sales)
        }

        document.getElementById("label_total_sales").innerHTML = Object.keys(obj)[0]
        document.getElementById("nilai_total_sales").innerHTML = nilai_total_sales
        document.getElementById("label_margin").innerHTML = "Margin"
        document.getElementById("nilai_margin").innerHTML = data[0].margin+"%"
    }

    Chart.plugins.register({
        id: 'paddingBelowLegends',
        beforeInit: function(chart, options) {
          chart.legend.afterFit = function() {
            this.height = this.height + 25;
          };
        }
    });
    
    create_chart_sales(ctx, datasets, labels, canvas, chart, option)
}

flectra.define('sales.dashboard', function(require) {
    "use strict";

    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var KanbanView = require('web.KanbanView');
    var KanbanModel = require('web.KanbanModel');
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanController = require('web.KanbanController');
    var data = require('web.data');
    var view_registry = require('web.view_registry');
    var QWeb = core.qweb;

    var _t = core._t;
    var _lt = core._lt;

    var SalesDashboardRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            'change .action-date': 'change_action_date',
            'change .custom-action-date': 'change_custom_action_date',
            'change #filter_branch': 'change_button_branch',
            'change #filter_tahun': 'change_button_tahun',
            'change #filter_qtr': 'change_button_qtr',
            'change #filter_bulan': 'change_button_bulan'
        }),


        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Notifies the controller that the target has changed.
         *
         * @private
         * @param {string} target_name the name of the changed target
         * @param {string} value the new value
         */
        _notifyTargetChange: function (target_name, value) {
            this.trigger_up('dashboard_edit_target', {
                target_name: target_name,
                target_value: value,
            });
        },

        fetch_data: function() {
            // Overwrite this function with useful data
            return $.when();
        },
        /**
         * @override
         * @private
         * @returns {Deferred}
         */
        _render: function() {
            var super_render = this._super;
            var self = this;
            self._rpc({
                route: '/sales_dashboard',
                params: {},}).done(function
            (result) {
                let card   = $(".card-lb")
                let tahun   =   $("#filter_tahun").val()
                card.each(function(index) {
                    let t      = $(this),
                        title  = t.attr('data-title'),
                        canvas = t.attr('data-canvas'),
                        chart  = t.attr('data-chart'),
                        option  = eval(`new Array(${ t.attr('data-option') })`) || {}
                    let branch  =   $("#filter_branch").val() || 1

                    if (canvas == 'total_margin_sales_chart'){
                        $(this).append(`
                            <h1 class="title">${ title }</h1>	 
                            <div class="content">
                                <div class="canvas-content margin-sales">
                                    <div class="row">
                                        <div class="chart-description col-md-3 col-xs-3">
                                            <br/>
                                            <br/>
                                            <h4 id="label_total_sales"></h4>
                                            <h3 id="nilai_total_sales"></h3>
                                            <br/>
                                            <h4 id="label_margin"></h4>
                                            <h3 id="nilai_margin"></h3>
                                        </div>
                                        <div class="col-md-9 col-xs-9">
                                            <canvas id="${ canvas }"></canvas>
                                        </div>
                                    </div>
                                </div>
                                <div class="action-content">
                                    <input type="text" data-index="${ index }" class="action-date" id="datepicker-${ canvas }" data-chart="${ chart }" data-canvas="${ canvas }"/>
                                </div>
                            </div>
                        `)
                    }else{
                        $(this).append(`
                            <h1 class="title">${ title }</h1>	 
                            <div class="content">
                                <div class="canvas-content">
                                    <canvas id="${ canvas }"></canvas>
                                </div>
                                <div class="action-content">
                                    <input type="text" data-index="${ index }" class="action-date" id="datepicker-${ canvas }" data-chart="${ chart }" data-canvas="${ canvas }"/>
                                </div>
                            </div>
                        `)
                    }
                    

                    $(".action-date").daterangepicker({
                        initialText : 'This Year',
                    });

                    $(".custom-action-date").daterangepicker({
                        initialText : 'This Year',
                    });

                    function getLastWeek() {
                        var today = new Date();
                        var lastWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
                        return lastWeek;
                    }
                    
                    let lastWeek    =   $.datepicker.formatDate('yy-mm-dd', getLastWeek()),
                        today       =   $.datepicker.formatDate('yy-mm-dd', new Date())

                    /**
                     * /sales_dashboard/name
                     */

                    self._rpc({
                        route: `/sales_dashboard/${canvas}/${branch}/${tahun}-01-01/${tahun}-12-31`,
                        params: {},}).done(function
                    (result) {
                        self.load_chart(chart, canvas, result, index, option)
                    })
                })
            });
            
            self._rpc({
            route: `/sales_dashboard/branch`,
            params: {},}).done(function(result) {
                if (result) {
                    result.forEach((v, i) => {
                        if(i == 0) {
                            $("#filter_branch").append(`
                                <option selected value="${ v.id }">${ v.name }</option>
                            `)
                        } else {
                            $("#filter_branch").append(`
                                <option value="${ v.id }">${ v.name }</option>
                            `)
                        }
                    })
                }
            });
            

            return this.fetch_data().then(function(result) {
                var tes_dashboard_view = QWeb.render('SalesDashboard');
                super_render.call(self);
                $(tes_dashboard_view).prependTo(self.$el);
            });            
        },

        
        load_chart: function(chart, canvas, data, index, option) {
            let ctx =   $(`#${ canvas }`)[0].getContext("2d")

            sales_process_chart(ctx, chart, data, index, option)
        },

        load_all_chart: function(branch_name, lstWk, tdy){
            var self    = this;
            let card   = $(".card-lb");

            card.each(function(index) {
                let t      = $(this),
                    title  = t.attr('data-title'),
                    canvas = t.attr('data-canvas'),
                    chart  = t.attr('data-chart'),
                    option  = eval(`new Array(${ t.attr('data-option') })`) || {}

                $(".action-date").daterangepicker({
                    initialText : `${lstWk}~${tdy}`,
                });

                $(".custom-action-date").daterangepicker({
                    initialText : `${lstWk}~${tdy}`,
                });

                self._rpc({
                    route: `/sales_dashboard/${canvas}/${branch_name}/${lstWk}/${tdy}`,
                    params: {},}).done(function
                (result) {
                    self.load_chart(chart, canvas, result, index, option)
                })
            })
        },

        lastday: function(y,m){
            return  new Date(y, m, 0).getDate();
        },

        firstday: function(y,m){
            return  new Date(y, (m-1), 1).getDate();
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        change_action_date: function(event) {
            let id          = event.target.id,
                date        = $(`#${id}`).val(),
                date_parse  = JSON.parse(date),
                start       = date_parse.start,
                end         = date_parse.end,
                canvas      = $(`#${id}`).attr('data-canvas'),
                chart       = $(`#${id}`).attr('data-chart'),
                index       = $(`#${id}`).attr('data-index'),
                self        = this
            let branch      =   $("#filter_branch").val()

            self._rpc({
                route: `/sales_dashboard/${canvas}/${branch}/${start}/${end}`,
                params: {},}).done(function
            (result) {
                self.load_chart(chart, canvas, result, index)
            })
        },

        change_custom_action_date: function(event) {
            let id          = event.target.id,
                date        = $(`#${id}`).val(),
                date_parse  = JSON.parse(date),
                start       = date_parse.start,
                end         = date_parse.end,
                canvas1     = $(`#${id}`).attr('data-canvas1'),
                chart1      = $(`#${id}`).attr('data-chart1'),
                canvas2     = $(`#${id}`).attr('data-canvas2'),
                chart2      = $(`#${id}`).attr('data-chart2'),
                index1      = $(`#${id}`).attr('data-index1'),
                index2      = $(`#${id}`).attr('data-index2'),
                self        = this
            let branch      =   $("#filter_branch").val()

            self._rpc({
                route: `/sales_dashboard/${canvas1}/${branch}/${start}/${end}`,
                params: {},}).done(function
            (result) {
                self.load_chart(chart1, canvas1, result, index1)
            })

            self._rpc({
                route: `/sales_dashboard/${canvas2}/${branch}/${start}/${end}`,
                params: {},}).done(function
            (result) {
                self.load_chart(chart2, canvas2, result, index2)
            })
        },

        change_button_branch: function(event) {
            let tahun   =   $("#filter_tahun").val()
            let qtr     =   $("#filter_qtr").val() || null
            let bulan   =   $("#filter_bulan").val() || null
            let branch  =   $("#filter_branch").val()   
            var self = this;

            function getLastWeek() {
                var today = new Date();
                var lastWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
                return lastWeek;
            }
            
            let lastWeek    =   $.datepicker.formatDate('yy-mm-dd', getLastWeek()),
                today       =   $.datepicker.formatDate('yy-mm-dd', new Date())

            if(qtr == null && bulan == null){
                // self.load_all_chart(branch, lastWeek, today)
                self.load_all_chart(branch, `${tahun}-01-01`, `${tahun}-12-31`)
            }else if(qtr != null && bulan == null){
                if(qtr == 1){
                    self.load_all_chart(branch, `${tahun}-01-01`, `${tahun}-03-31`)
                }else if(qtr == 2){
                    self.load_all_chart(branch, `${tahun}-04-01`, `${tahun}-06-30`)
                }else if(qtr == 3){
                    self.load_all_chart(branch, `${tahun}-07-01`, `${tahun}-09-30`)
                }else if(qtr == 4){
                    self.load_all_chart(branch, `${tahun}-10-01`, `${tahun}-12-31`)
                }
            }else if(qtr == null && bulan != null){
                self.load_all_chart(branch, `${tahun}-${bulan}-${self.firstday(tahun,bulan)}`, `${tahun}-${bulan}-${self.lastday(tahun,bulan)}`)
            }   
        },

        change_button_tahun: function(event) {
            let tahun   =   $("#filter_tahun").val()
            let qtr     =   $("#filter_qtr").val() || null
            let bulan   =   $("#filter_bulan").val() || null
            let branch  =   $("#filter_branch").val() 
            var today = new Date(); 
            var self = this;

            function getLastWeek() {
                var lastWeek = new Date(tahun, today.getMonth(), today.getDate() - 7);
                return lastWeek;
            }
            
            let start_date    =   $.datepicker.formatDate('yy-mm-dd', getLastWeek()),
                end_date       =   $.datepicker.formatDate('yy-mm-dd', new Date(tahun, today.getMonth(), today.getDate()))

            if(qtr == null && bulan == null){
                // self.load_all_chart(branch, start_date, end_date)
                self.load_all_chart(branch, `${tahun}-01-01`, `${tahun}-12-31`)
            }else if(qtr != null && bulan == null){
                if(qtr == 1){
                    self.load_all_chart(branch, `${tahun}-01-01`, `${tahun}-03-31`)
                }else if(qtr == 2){
                    self.load_all_chart(branch, `${tahun}-04-01`, `${tahun}-06-30`)
                }else if(qtr == 3){
                    self.load_all_chart(branch, `${tahun}-07-01`, `${tahun}-09-30`)
                }else if(qtr == 4){
                    self.load_all_chart(branch, `${tahun}-10-01`, `${tahun}-12-31`)
                }
            }else if(qtr == null && bulan != null){
                self.load_all_chart(branch, `${tahun}-${bulan}-${self.firstday(tahun,bulan)}`, `${tahun}-${bulan}-${self.lastday(tahun,bulan)}`)
            }   
        },

        change_button_qtr: function(event) {
            let tahun   =   $("#filter_tahun").val()
            let qtr     =   $("#filter_qtr").val() || null
            let branch  =   $("#filter_branch").val() 
            var self = this;

            $("#filter_bulan").val('')

            if(qtr != null){
                if(qtr == 1){
                    self.load_all_chart(branch, `${tahun}-01-01`, `${tahun}-03-31`)
                }else if(qtr == 2){
                    self.load_all_chart(branch, `${tahun}-04-01`, `${tahun}-06-30`)
                }else if(qtr == 3){
                    self.load_all_chart(branch, `${tahun}-07-01`, `${tahun}-09-30`)
                }else if(qtr == 4){
                    self.load_all_chart(branch, `${tahun}-10-01`, `${tahun}-12-31`)
                }
            }  
        },

        change_button_bulan: function(event) {
            let tahun   =   $("#filter_tahun").val()
            let bulan   =   $("#filter_bulan").val() || null
            let branch  =   $("#filter_branch").val() 
            var self = this;
            
            $("#filter_qtr").val('')

            if(bulan != null){
                self.load_all_chart(branch, `${tahun}-${bulan}-${self.firstday(tahun,bulan)}`, `${tahun}-${bulan}-${self.lastday(tahun,bulan)}`)
            }   
        },
        
    });

    var SalesDashboardModel = KanbanModel.extend({
        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        init: function () {
            this.dashboardValues = {};
            this._super.apply(this, arguments);
        },

        /**
         * @override
         */
        get: function (localID) {
            var result = this._super.apply(this, arguments);
            return result;
        },


        /**
         * @œverride
         * @returns {Deferred}
         */
        load: function () {
            return this._super.apply(this, arguments);
        },
        /**
         * @œverride
         * @returns {Deferred}
         */
        reload: function () {
            return this._super.apply(this, arguments);
        },
    });

    var SalesDashboardController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: SalesDashboardModel,
            Renderer: SalesDashboardRenderer,
            Controller: SalesDashboardController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('sales_dashboard', MyMainDashboard);

    return {
        Model: SalesDashboardModel,
        Renderer: SalesDashboardRenderer,
        Controller: SalesDashboardController,
    };
});
    