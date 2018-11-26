flectra.define('project_scrum.dashboard', function(require) {
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

    var ScrumDashboardRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            'click .total-sprints': 'on_sprints_click',
            'click .total-tasks': 'on_tasks_click',
            'click .total-stories': 'on_stories_click',
            'click .total-projects': 'on_projects_click',
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
                route: '/project_scrum/get_sprints_data',
                params: {},}).done(function
            (result) {
                if (result) {
                    $('#total_projects').html("<h2>" + result.total_projects + "</h2>");
                    $('#total_sprints').html("<h2>" + result.total_sprints + "</h2>");
                    $('#total_stories').html("<h2>" + result.total_stories + "</h2>");
                    $('#total_tasks').html("<h2>" + result.total_tasks + "</h2>");
                }
            });
            self.render_line_chart();
            return this.fetch_data().then(function(result) {
                var scrum_dashboard_view = QWeb.render('ScrumDashboard');
                super_render.call(self);
                $(scrum_dashboard_view).prependTo(self.$el);
            });
        },

        load_sprint_burndown_chart: function(result) {
            var sprint_labels = [],
                sprint_velocities = [],
                sprint_rates = [];
            for (var key in result) {
                if (result[key]) {
                    sprint_labels.push(result[key].sprint_seq);
                    sprint_velocities.push(result[key].velocity);
                    sprint_rates.push(result[key].per);
                }
            }
            try {
                var sprint_burndown_chart = $("#scrum_chart")[0].getContext("2d");
                sprint_burndown_chart.canvas.height = 55;

                // This will get the first returned node in the jQuery collection.
                var sprint_chart = new Chart(sprint_burndown_chart);

                var sprint_chart_data = {
                    labels: sprint_labels,
                    datasets: [{
                            label: "Success (%)",
                            fillColor: "rgb(243, 156, 18)",
                            strokeColor: "rgb(243, 156, 18)",
                            pointColor: "rgb(243, 156, 18)",
                            pointStrokeColor: "#c1c7d1",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgb(243, 156, 18)",
                            data: sprint_velocities
                        },
                        {
                            label: "Estimated Velocity",
                            fillColor: "rgba(60,141,188,0.9)",
                            strokeColor: "rgba(60,141,188,0.8)",
                            pointColor: "#3b8bba",
                            pointStrokeColor: "rgba(60,141,188,1)",
                            pointHighlightFill: "#fff",
                            pointHighlightStroke: "rgba(60,141,188,1)",
                            data: sprint_rates
                        },
                    ]
                };

                var sprint_chart_options = {
                    //Boolean - If we should show the scale at all
                    showScale: true,
                    //Boolean - Whether grid lines are shown across the chart
                    scaleShowGridLines: false,
                    //String - Colour of the grid lines
                    scaleGridLineColor: "rgba(0,0,0,.05)",
                    //Number - Width of the grid lines
                    scaleGridLineWidth: 1,
                    //Boolean - Whether to show horizontal lines (except X axis)
                    scaleShowHorizontalLines: true,
                    //Boolean - Whether to show vertical lines (except Y axis)
                    scaleShowVerticalLines: true,
                    //Boolean - Whether the line is curved between points
                    bezierCurve: true,
                    //Number - Tension of the bezier curve between points
                    bezierCurveTension: 0.3,
                    //Boolean - Whether to show a dot for each point
                    pointDot: false,
                    //Number - Radius of each point dot in pixels
                    pointDotRadius: 4,
                    //Number - Pixel width of point dot stroke
                    pointDotStrokeWidth: 1,
                    //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
                    pointHitDetectionRadius: 20,
                    //Boolean - Whether to show a stroke for datasets
                    datasetStroke: true,
                    //Number - Pixel width of dataset stroke
                    datasetStrokeWidth: 2,
                    //Boolean - Whether to fill the dataset with a color
                    datasetFill: true,
                    //String - A legend template
                    legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].lineColor%>\"></span><%=datasets[i].label%></li><%}%></ul>",
                    //Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
                    maintainAspectRatio: true,
                    //Boolean - whether to make the chart responsive to window resizing
                    responsive: true
                };

                //Create the line chart
                sprint_chart.Line(sprint_chart_data, sprint_chart_options);
            } catch (e) {
                console.log("Something went wrong...", e);
            }
        },

        load_pie_chart: function(result) {
            var ctx = $("#ratio")[0].getContext("2d");

            let data = {
                labels: ["Pending", "Lost", "Win", "Opportunity"],
                datasets: [{
                    label: "Population (millions)",
                    backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                    data: [result[0].lead,result[0].lost,result[0].win,result[0].opportunity]
                }]
            }

            let options = {
                segmentShowStroke : true,
                segmentStrokeColor : "#fff",
                segmentStrokeWidth : 2,
                percentageInnerCutout : 50,
                animationSteps : 100,
                animationEasing : "easeOutBounce",
                animateRotate : true,
                animateScale : false,
                responsive: true,
                maintainAspectRatio: true,
                showScale: true,
                animateScale: true,
                legend: {
                    display: false
                }
            }

            if(window.donut != undefined)
                window.donut.destroy()

            window.donut = new Chart(ctx, {
                type: 'pie',
                data: data,
                options: options
            });
        },

        load_bar_stages: function(result) {
            var stages = $("#stages")[0].getContext("2d");

            if(window.stages_bar != undefined)
                window.stages_bar.destroy()
                
            let data = {
                labels: result[0].bulan,
                datasets: [
                    {
                        label : 'Lead',
                        backgroundColor: 'blue',
                        data: result[0].total_lead
                    },
                    {
                        label : 'Opportunity',
                        backgroundColor: '#d35400',
                        data: result[0].total_opportunity
                    }, 
                    {
                        label : 'Win',
                        backgroundColor: '#3498db',
                        data: result[0].total_win
                    }, 
                    {
                        label : 'Lost',
                        backgroundColor: '#f1c40f',
                        data: result[0].total_lost
                    },
                ]
            };

            console.log(data)
            console.log(result[0].total_lead)

            let options = {
                legend: { display: false },
                scales: {
                    xAxes: [{ stacked: true }],
                    yAxes: [
                        { 
                            stacked: true,
                            ticks: {
                                callback: function(label) {
                                    return  'Rp. ' + rupiah_scrum(label)
                                }
                            },
                        }
                    ]
                }
            }

            window.stages = new Chart(stages, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        load_bar_forecasted: function(result) {
            var forecasted = $("#forecasted")[0].getContext("2d");

            let data = {
                labels: ['Forecasted Sales'],
                datasets: [
                    {
                        label : 'Forecasted Sales',
                        backgroundColor: ['#8e44ad'],
                        data: [result[0].forecasted]
                    },
                ]
            };

            if(window.forecasted_bar != undefined)
                window.forecasted_bar.destroy()

            let options = {
                legend: { display: false },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                callback: function(label) {
                                    return  'Rp. ' + rupiah_scrum(label)
                                }
                            },
                        }
                    ]
                },
            }

            window.stages = new Chart(forecasted, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        load_bar_expected_sales: function(result) {
            var expected_sales = $("#expected_sales")[0].getContext("2d");

            let data = {
                labels: result[0].bulan,
                datasets: [
                    {
                        label : 'Expected Sales',
                        backgroundColor: '#7f8c8d',
                        data: result[0].total_expected
                    },
                ]
            };

            if(window.expected_sales_bar != undefined)
                window.expected_sales_bar.destroy()

            let options = {
                legend: { display: false },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                callback: function(label) {
                                    return  'Rp. ' + rupiah_scrum(label)
                                }
                            },
                        }
                    ]
                },
            }

            window.expected_sales =  new Chart(expected_sales, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        load_bar_person_win: function(result) {
            var person_win = $("#person_win")[0].getContext("2d");

            let data = {
                labels: result[0].team_name,
                datasets: [
                    {
                        label : 'Person Win',
                        backgroundColor: '#c0392b',
                        data: result[0].team_win
                    },
                ]
            };

            if(window.person_win_bar != undefined)
                window.person_win_bar.destroy()

            let options = {
                legend: { display: false },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                callback: function(label) {
                                    return  'Rp. ' + rupiah_scrum(label)
                                }
                            },
                        }
                    ]
                },
            }

            window.person_win = new Chart(person_win, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        load_bar_month_win: function(result) {
            var month_win = $("#month_win")[0].getContext("2d");

            let data = {
                labels: result[0].bulan,
                datasets: [
                    {
                        label : 'Month Win',
                        backgroundColor: '#05c46b',
                        data: result[0].month_win
                    },
                ]
            };

            if(window.month_win_bar != undefined)
                window.month_win_bar.destroy()

            let options = {
                legend: { display: false },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                callback: function(label) {
                                    return  'Rp. ' + rupiah_scrum(label)
                                }
                            },
                        }
                    ]
                },
            }

            window.month_win = new Chart(month_win, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        load_bar_lost_reason: function(result) {
            var lost_reason = $("#lost_reason")[0].getContext("2d");

            let data = {
                labels: result[0].team_name,
                datasets: [
                    {
                        label : 'Lost Reason',
                        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
                        data: result[0].team_win
                    },
                ]
            };

            if(window.lost_reason_bar != undefined)
                window.lost_reason_bar.destroy()

            let options = {
                legend: { display: false },
                scales: {
                    xAxes: [
                        {
                            display: false
                        }
                    ]
                },
            }

            window.lost_reason = new Chart(lost_reason, {
                type: 'bar',
                data: data,
                options: options,
            });
        },

        render_line_chart: function(tahun = null, qtr = null, bulan = null) {
            var self = this;
            self._rpc({
            route: '/project_scrum/get_line_chart_data',
            params: {},}).done(function(result) {
                if (result) {
                    self.load_sprint_burndown_chart(result); //  load sprint burndown chart
                }
            });
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        on_sprints_click: function(event) {
            var self = this,
                context = {};
            context.search_default_group_by_project = 1;
            return self._rpc({
            route: "/web/action/load",
            params: {
                action_id: "project_scrum.action_project_sprint"
            },}).done(function(result) {
                if (result) {
                    result.views = [
                        [false, 'list'],
                        [false, 'form']
                    ];
                    result.context = context;
                    return self.do_action(result);
                };
            })
        },

        on_tasks_click: function(event) {
            var self = this,
                context = {};
            context.search_default_group_by_sprint = 1;
            return self._rpc({
            route:"/web/action/load",
            params: {
                action_id: "project.action_view_task"
            },}).done(function(result) {
                if (result) {
                    result.views = [
                        [false, 'list'],
                        [false, 'form']
                    ];
                    result.context = context;
                    return self.do_action(result);
                };
            })
        },

        on_stories_click: function() {
            var self = this,
                context = {};
            context.search_default_group_by_sprint = 1;
            return self._rpc({route:"/web/action/load",
            params: {
                action_id: "project_scrum.action_project_story_sprint"
            },}).done(function(result) {
                if (result) {
                    result.views = [
                        [false, 'list'],
                        [false, 'form']
                    ];
                    result.context = context;
                    return self.do_action(result);
                };
            })
        },

        on_projects_click: function() {
            var self = this,
                context = {};
            context.search_default_Manager = 1;
            return self._rpc({
                route: "/web/action/load",
                params:{
                    action_id: "project.open_view_project_all_config"
                },
            }).done(function(result) {
                if (result) {
                    result.views = [
                        [false, 'list'],
                        [false, 'form']
                    ];
                    result.context = context;
                    return self.do_action(result);
                };
            })
        },
    });

    var ScrumDashboardModel = KanbanModel.extend({
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

    var ScrumDashboardController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: ScrumDashboardModel,
            Renderer: ScrumDashboardRenderer,
            Controller: ScrumDashboardController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('scrum_dashboard', MyMainDashboard);

    return {
        Model: ScrumDashboardModel,
        Renderer: ScrumDashboardRenderer,
        Controller: ScrumDashboardController,
    };
});
    