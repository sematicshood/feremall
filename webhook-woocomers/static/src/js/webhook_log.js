flectra.define('webhook.log', function(require) {
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

    var WebhookLogRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            
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
                route: '/webhook/webhook_log/get',
                params: {},}).done(function
            (result) {
                self.render_table(result)
            });
            
            return this.fetch_data().then(function(result) {
                var tes_dashboard_view = QWeb.render('WebhookLog');
                super_render.call(self);
                $(tes_dashboard_view).prependTo(self.$el);
            });
        },

        render_table: function(result) {
            console.log(result)
            $("#table-product").empty()

            $.each(result, (i, v) => {
                $("#table-product").append(`
                    <tr>
                        <td>${ i += 1 }</td>
                        <td>${ v.user }</td>
                        <td>
                            ${ (v.partner) ? v.partner : '' }
                            ${ (v.product) ? v.product : '' }
                            ${ (v.order) ? v.order : '' }
                        </td>
                        <td>
                            ${ (v.partner) ? 'Customers' : '' }
                            ${ (v.product) ? 'Product Sync' : '' }
                            ${ (v.order) ? 'Sales Order' : '' }
                        </td>
                        <td>${ v.description }</td>
                        <td>${ v.created_at }</td>
                    </tr>
                `)
            })

            $("#table").DataTable()
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        

    });

    var WebhookLogModel = KanbanModel.extend({
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

    var WebhookLogController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: WebhookLogModel,
            Renderer: WebhookLogRenderer,
            Controller: WebhookLogController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('webhook_log', MyMainDashboard);

    return {
        Model: WebhookLogModel,
        Renderer: WebhookLogRenderer,
        Controller: WebhookLogController,
    };
});
    