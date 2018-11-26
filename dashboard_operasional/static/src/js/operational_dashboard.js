var sales = [
    {
        "project": "10248",
        "vendor": "North America",
        "area": "United States of America",
        "item": "New York",
        "komponen": "ini komponen",
        "satuan": "meter",
        "sub_no": "12 No",
        "amount": 1740,
        "harga": 111,
        "qty": 3
    }, {
        "project": "10249",
        "vendor": "North America",
        "area": "United States of America 2",
        "item": "New York 2",
        "komponen": "ini komponen",
        "satuan": "meter",
        "sub_no": "12 No",
        "amount": 1741,
        "harga": 111,
        "qty": 1
    },
    {
        "project": "10250",
        "vendor": "North",
        "area": "United",
        "item": "New",
        "komponen": "ini komponen",
        "satuan": "meter",
        "sub_no": "12 No",
        "amount": 1740,
        "harga": 111,
        "qty": 31
    }, {
        "project": "10251",
        "vendor": "North",
        "area": "United 2",
        "item": "New 2",
        "komponen": "ini komponen",
        "satuan": "meter",
        "sub_no": "12 No",
        "amount": 1741,
        "harga": 111,
        "qty": 32
    }
];

flectra.define('operational.dashboard', function(require) {
    // "use strict";

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

    var OperationalDashboardRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            'change #filter_vendor': 'change_action',
            'change #filter_tahun': 'change_action',
            'change #filter_bulan': 'change_action',
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
            let year = (new Date()).getFullYear();

            self._rpc({
                route: '/operational_dashboard',
                params: {'year': year, vendor: 'active'},}).done(function
            (result) {
                self.ganganttCreate(result)
                self.pipivotCreate(result)
            });
            
            return this.fetch_data().then(function(result) {
                var operational_dashboard_view = QWeb.render('OperationalDashboard');
                super_render.call(self);
                $(operational_dashboard_view).prependTo(self.$el);
            });
        },

        ganganttCreate: function(result) {
            data    =   []

            $.each(result, (i, v) => {
                let progress_p = 0,
                    j_p        = 0

                $.each(v['series'], (q, w) => {
                    w_start =   w['start'].split(' ')
                    w_d     =   w_start[0].split('-')

                    w_end   =   w['end'].split(' ')
                    w_e     =   w_end[0].split('-')

                    data.push({
                        "id": '00' + w['id'], 
                        "text": w['name'], 
                        "start_date": `${ w_d[2] }-${ w_d[1] }-${ w_d[0] }`,
                        "end_date": `${ w_e[2] }-${ w_e[1] }-${ w_e[0] }`,
                        "bobot": w['bobot'],
                        "bobot_done": w['bobot_done'],
                        "bobot_undone": w['bobot_undone'],
                        "member": w['team'],
                        "progress": `${ w['percent'] / 100 }`,
                        "parent": '0' + w['parent_id'],
                        "open": true,
                    })

                    progress_p += (w['percent'] / 100)
                    j_p++
                })

                data.push({
                    "id": '0' + v['id'], 
                    "text": v['name'],
                    type: gantt.config.types.vendor, 
                    "open": true,
                    "bobot": '',
                    "bobot_done": '',
                    "bobot_undone": '',
                    "member": '',
                    "progress": (Number((progress_p / j_p).toFixed(2))) ? Number((progress_p / j_p).toFixed(2)) : ''
                })
            })

            gantt.config.scale_unit = "month";
            gantt.config.date_scale = "%F, %Y";
            gantt.config.scale_height = 50;
            gantt.config.subscales = [
                {unit: "day", step: 1, date: "%j, %D"}
            ];

            gantt.config.columns =  [
                {name:"text",       label:"Task name",  tree:true, width:"*" },
                {name:"start_date", label:"Start time", align:"center", width: "110" },
                {name:"end_date",   label:"End date",   align:"center", width: "110" },
                {name:"bobot",   label:"Bobot",   align:"center", width: "110" },
                {name:"bobot_done",   label:"Selesai",   align:"center", width: "110" },
                {name:"bobot_undone",   label:"Belum Selesai",   align:"center", width: "110" },
                {name:"member",   label:"Team Member",   align:"center", width: "110" },
                {name:"progress",   label:"Percent Complete",   align:"center", width: "110" },
            ];

            gantt.config.min_grid_column_width = 120;
            gantt.config.autosize = "xy";
            gantt.templates.tooltip_text = function(start,end,task){
                return "<b>Task : </b> "+task.text+"<br/><b>Start Date : </b> " + start + "<br/><b>End Date : </b>" + end + "<br/><b>Bobot : </b>" + task.bobot + "<br/><b>Selesai : </b>" + task.bobot_done + "<br/><b>Belum Selesai : </b>" + task.bobot_undone + "<br/><b>Team Member : </b>" + task.member + "<br/><b>Percent Complete : </b>" + (task.progress * 100) + '%';
            };
            gantt.config.tooltip_offset_x = 30;
            gantt.config.tooltip_offset_y = 40;
            gantt.config.readonly = true;
            gantt.config.sort = true;

            gantt.init("gantt_here");
            gantt.parse({
                data: data
            });
        },

        pipivotCreate: function(result) {
            var pivotGrid = $("#pivotgrid").dxPivotGrid({
                allowSortingBySummary: true,
                allowFiltering: true,
                showBorders: true,
                showColumnGrandTotals: false,
                showRowGrandTotals: false,
                showRowTotals: true,
                showColumnTotals: false,
                fieldChooser: {
                    enabled: true,
                    height: 400
                },
                fieldPanel: {
                    visible: true
                },
                dataSource: {
                    fields: [
                    {
                        caption: "Project",
                        width: 120,
                        dataField: "project",
                        area: "row",
                    }, {
                        caption: "Vendor",
                        width: 120,
                        dataField: "vendor",
                        area: "row",
                    }, {
                        caption: "Area",
                        width: 120,
                        dataField: "area",
                        area: "row",
                    }, {
                        caption: "Item",
                        dataField: "item",
                        width: 150,
                        area: "row"
                    }, {
                        caption: "Sub No",
                        dataField: "sub_no",
                        width: 150,
                        area: "row"
                    }, {
                        caption: "Komponen",
                        dataField: "komponen",
                        width: 150,
                        area: "row"
                    }, {
                        caption: "QTY",
                        dataField: "qty",
                        area: "row",
                        width: 150,
                    }, {
                        caption: "Satuan",
                        dataField: "satuan",
                        area: "row",
                        width: 150,
                    }, {
                        caption: "Harga",
                        dataField: "harga",
                        area: "row",
                        width: 150,
                    }, {
                        caption: "Total",
                        dataField: "amount",
                        dataType: "number",
                        summaryType: "sum",
                        format: "currency",
                        area: "data"
                    }],
                    store: sales
                }
            }).dxPivotGrid("instance");
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        change_action: function(event) {
            let vendor    =   $("#filter_vendor").val(),
                year       =   $("#filter_tahun").val(),
                month      =   $("#filter_bulan").val() || 'undefined'

            self._rpc({
                route: '/operational_dashboard',
                params: {'year': year, vendor: vendor, month: month},}).done(function
            (result) {
                gantt.clearAll(); 

                self.ganttCreate(result)
            });
        }
        
    });

    var OperationalDashboardModel = KanbanModel.extend({
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

    var OperationalDashboardController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: OperationalDashboardModel,
            Renderer: OperationalDashboardRenderer,
            Controller: OperationalDashboardController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('operational_dashboard', MyMainDashboard);

    return {
        Model: OperationalDashboardModel,
        Renderer: OperationalDashboardRenderer,
        Controller: OperationalDashboardController,
    };
});
    