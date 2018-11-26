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

function create_chart(ctx, datasets, labels, index, chart, option = {}) {
    let stack   =   false,
        title   =   {
            display: false,
            text: 'Library Dashboard'
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
}

function color_generator(data) {
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

function process_chart(ctx, chart, data, canvas, option) {
    if(Array.isArray(data[0].labels))
        labels  =   data[0].labels
    else
        labels  =   [data[0].labels]

    let datasets    =   []
    
    data[0].value.forEach((v) => {
        $.each(v, function(key, value) {
            let color   =   color_generator([value])

            let data = {
                label: [key],
                backgroundColor: color[0],
                borderColor: color[1],
                data: [value]
            }

            datasets.push(data)
        })
    })

    Chart.plugins.register({
        id: 'paddingBelowLegends',
        beforeInit: function(chart, options) {
          chart.legend.afterFit = function() {
            this.height = this.height + 25;
          };
        }
    });

    create_chart(ctx, datasets, labels, canvas, chart, option)
}

flectra.define('library.dashboard', function(require) {
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

    var LibraryDashboardRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            'change .action-date': 'change_action_date'
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
                route: '/library_dashboard',
                params: {},}).done(function
            (result) {
                let card   = $(".card-lb")

                card.each(function(index) {
                    let t      = $(this),
                        title  = t.attr('data-title'),
                        canvas = t.attr('data-canvas'),
                        chart  = t.attr('data-chart'),
                        option  = eval(`new Array(${ t.attr('data-option') })`) || {}

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

                    $(".action-date").daterangepicker({
                        initialText : 'Last 7 Days',
                    });

                    function getLastWeek() {
                        var today = new Date();
                        var lastWeek = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 37);
                        return lastWeek;
                    }
                    
                    let lastWeek    =   $.datepicker.formatDate('yy-mm-dd', getLastWeek()),
                        today       =   $.datepicker.formatDate('yy-mm-dd', new Date())

                    /**
                     * /library_dashboard/name
                     */

                    self._rpc({
                        route: `/library_dashboard/${canvas}/${lastWeek}/${today}`,
                        params: {},}).done(function
                    (result) {
                        self.load_chart(chart, canvas, result, index, option)
                    })
                })
            });
            
            return this.fetch_data().then(function(result) {
                var tes_dashboard_view = QWeb.render('LibraryDashboard');
                super_render.call(self);
                $(tes_dashboard_view).prependTo(self.$el);
            });
        },

        load_chart: function(chart, canvas, data, index, option) {
            let ctx =   $(`#${ canvas }`)[0].getContext("2d")

            process_chart(ctx, chart, data, index, option)
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

            self._rpc({
                route: `/library_dashboard/${canvas}/${start}/${end}`,
                params: {},}).done(function
            (result) {
                self.load_chart(chart, canvas, result, index)
            })
        }
        
    });

    var LibraryDashboardModel = KanbanModel.extend({
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

    var LibraryDashboardController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: LibraryDashboardModel,
            Renderer: LibraryDashboardRenderer,
            Controller: LibraryDashboardController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('library_dashboard', MyMainDashboard);

    return {
        Model: LibraryDashboardModel,
        Renderer: LibraryDashboardRenderer,
        Controller: LibraryDashboardController,
    };
});
    