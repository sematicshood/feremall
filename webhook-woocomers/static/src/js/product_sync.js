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

flectra.define('product.sync', function(require) {
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

    var ProductSyncRenderer = KanbanRenderer.extend({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            "click .sync": "sync_product"
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
                route: '/webhook/product_sync/get',
                params: {},}).done(function
            (result) {
                self.render_table(result)
            });
            
            return this.fetch_data().then(function(result) {
                var tes_dashboard_view = QWeb.render('ProductSync');
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
                        <td>${ v.name }</td>
                        <td>${ v.code }</td>
                        <td>${ v.category }</td>
                        <td>Rp. ${ rupiah(v.price) }</td>
                        <td>${ (v.sync == false || v.date_sync == false || v.date_sync < v.write_date) ? '<button class="sync btn btn-primary btn-sm" id=' + v.id + '>Sync Product</button></td>' : 'Product Sync' }
                    </tr>
                `)
            })

            $("#table").DataTable()
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        sync_product: function(event) {
            var self = this

            let id  =   event.target.id

            self._rpc({
                route: `/webhook/product_sync/sync/${ id }`,
                params: {},}).done(function
            (result) {
                alert("Success Sync Product")
                $(`#${ id }`).attr('disabled', 'disabled')
            });
        }

    });

    var ProductSyncModel = KanbanModel.extend({
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

    var ProductSyncController = KanbanController.extend({
        
    });

    var MyMainDashboard = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: ProductSyncModel,
            Renderer: ProductSyncRenderer,
            Controller: ProductSyncController,
        }),
        display_name: _lt('Dashboard'),
        icon: 'fa-dashboard',
        searchview_hidden: true,
    });

    view_registry.add('product_sync', MyMainDashboard);

    return {
        Model: ProductSyncModel,
        Renderer: ProductSyncRenderer,
        Controller: ProductSyncController,
    };
});
    