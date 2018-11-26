// flectra.define('operational.dashboard', function(require) {
//     // "use strict";

//     var core = require('web.core');
//     var field_utils = require('web.field_utils');
//     var KanbanView = require('web.KanbanView');
//     var KanbanModel = require('web.KanbanModel');
//     var KanbanRenderer = require('web.KanbanRenderer');
//     var KanbanController = require('web.KanbanController');
//     var data = require('web.data');
//     var view_registry = require('web.view_registry');
//     var QWeb = core.qweb;

//     var _t = core._t;
//     var _lt = core._lt;

//     var OperationalDashboardRenderer = KanbanRenderer.extend({
//         events: _.extend({}, KanbanRenderer.prototype.events, {
//             'change #filter_project': 'change_action',
//             'change #filter_tahun': 'change_action',
//             'change #filter_bulan': 'change_action',
//         }),


//         //--------------------------------------------------------------------------
//         // Private
//         //--------------------------------------------------------------------------

//         /**
//          * Notifies the controller that the target has changed.
//          *
//          * @private
//          * @param {string} target_name the name of the changed target
//          * @param {string} value the new value
//          */
//         _notifyTargetChange: function (target_name, value) {
//             this.trigger_up('dashboard_edit_target', {
//                 target_name: target_name,
//                 target_value: value,
//             });
//         },

//         fetch_data: function() {
//             // Overwrite this function with useful data
//             return $.when();
//         },
//         /**
//          * @override
//          * @private
//          * @returns {Deferred}
//          */
//         _render: function() {
//             var super_render = this._super;
//             var self = this;
//             let year = (new Date()).getFullYear();

//             self._rpc({
//                 route: '/operational_dashboard',
//                 params: {'year': year, project: 'active'},}).done(function
//             (result) {
//                 self.ganttLoad(result)
//             });
            
//             return this.fetch_data().then(function(result) {
//                 var tes_dashboard_view = QWeb.render('OperationalDashboard');
//                 super_render.call(self);
//                 $(tes_dashboard_view).prependTo(self.$el);
//             });
//         },

//         ganttLoad: function(result) {
//             data    =   []

//             $("#ganttChart").empty()

//             $.each(result, (i, v) => {
//                 series      =   []

//                 $.each(v['series'], (q, w) => {
//                     w_start =   w['start'].split(' ')
//                     w_d     =   w_start[0].split('-')

//                     w_end   =   w['end'].split(' ')
//                     w_e     =   w_end[0].split('-')

//                     series.push({ 
//                         name: w['name'], 
//                         start: new Date(parseInt(w_d[0]), parseInt(w_d[1]) - 1, parseInt(w_d[2])), 
//                         // start: new Date(2018, 7, 30), 
//                         end: new Date(parseInt(w_e[0]), parseInt(w_e[1]) - 1, parseInt(w_e[2])), 
//                         // end: new Date(2018, 7, 30), 
//                         // last_date: new Date(2010,00,02),
//                         start_date: `${ w_d[2] }/${ w_d[1] }/${ w_d[0] }`,
//                         end_date: `${ w_e[2] }/${ w_e[1] }/${ w_e[0] }`,
//                         bobot: w['bobot'],
//                         bobot_done: w['bobot_done'],
//                         bobot_undone: w['bobot_undone'],
//                         team: w['team'],
//                         percent: `${ w['percent'] }%`,
//                         color_done: '#5cbbd6',
//                         color: '#6bd9f7'
//                     })
//                 })

//                 data.push({
//                     id: v['id'], name: v['name'], series: series
//                 })
//             })

//             var ganttData = data;

//             $("#ganttChart").ganttView({ 
//                 data: ganttData,
//             });
//         },

//         //--------------------------------------------------------------------------
//         // Handlers
//         //--------------------------------------------------------------------------
//         change_action: function(event) {
//             let project    =   $("#filter_project").val(),
//                 year       =   $("#filter_tahun").val(),
//                 month      =   $("#filter_bulan").val() || 'undefined',
//                 self       =   this

//                 console.log(project)
//                 console.log(year)
//                 console.log(month)

//             self._rpc({
//                 route: '/operational_dashboard',
//                 params: {'year': year, project: project, month: month},}).done(function
//             (result) {
//                 self.ganttLoad(result)
//             });
//         }
        
//     });

//     var OperationalDashboardModel = KanbanModel.extend({
//         //--------------------------------------------------------------------------
//         // Public
//         //--------------------------------------------------------------------------

//         /**
//          * @override
//          */
//         init: function () {
//             this.dashboardValues = {};
//             this._super.apply(this, arguments);
//         },

//         /**
//          * @override
//          */
//         get: function (localID) {
//             var result = this._super.apply(this, arguments);
//             return result;
//         },


//         /**
//          * @œverride
//          * @returns {Deferred}
//          */
//         load: function () {
//             return this._super.apply(this, arguments);
//         },
//         /**
//          * @œverride
//          * @returns {Deferred}
//          */
//         reload: function () {
//             return this._super.apply(this, arguments);
//         },
//     });

//     var OperationalDashboardController = KanbanController.extend({
        
//     });

//     var MyMainDashboard = KanbanView.extend({
//         config: _.extend({}, KanbanView.prototype.config, {
//             Model: OperationalDashboardModel,
//             Renderer: OperationalDashboardRenderer,
//             Controller: OperationalDashboardController,
//         }),
//         display_name: _lt('Dashboard'),
//         icon: 'fa-dashboard',
//         searchview_hidden: true,
//     });

//     view_registry.add('operational_dashboard', MyMainDashboard);

//     return {
//         Model: OperationalDashboardModel,
//         Renderer: OperationalDashboardRenderer,
//         Controller: OperationalDashboardController,
//     };
// });
    